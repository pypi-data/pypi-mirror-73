import os
import numpy as np
from colorama import Fore, Style
import pandas as pd
import torch
from keras_preprocessing import sequence
from sklearn.model_selection import train_test_split
from tensorflow.python.keras.callbacks import EarlyStopping
from tensorflow.python.keras.saving.saved_model.json_utils import Encoder
from torch.utils.data import DataLoader
from transformers import T5Tokenizer, T5ForConditionalGeneration
import tensorflow as tf

from verve.data_generation.dataset_labelmatcher import get_similar_column
from verve.data_generation.grammartree import get_value_instruction
from verve.modeling.prediction_model_creation import get_keras_text_class
from verve.plotting.generate_plots import generate_classification_plots
from verve.preprocessing.NLP_preprocessing import get_target_values, text_clean_up, lemmatize_text, encode_text
from verve.preprocessing.huggingface_model_finetune_helper import CustomDataset, train, inference
from verve.preprocessing.image_caption_helpers import load_image, map_func, CNN_Encoder, RNN_Decoder, get_path_column, \
    generate_caption_helper

# Sentiment analysis predict wrapper
from verve.query.supplementaries import save, get_standard_training_output_keras, get_standard_training_output_generic
from verve.plotting.generate_plots import plot_loss

counter = 0
currLog = 0


def clearLog():
    global currLog
    global counter

    currLog = ""
    counter = 0


def logger(instruction, found=""):
    '''
    logging function that creates hierarchial display of the processes of
    different functions. Copied into different python files to maintain
    global variables.

    :param instruction: what you want to be displayed
    :param found: if you want to display something found like target column

    '''
    global counter
    if counter == 0:
        print((" " * 2 * counter) + str(instruction) + str(found))
    elif instruction == "->":
        counter = counter - 1
        print(Fore.BLUE + (" " * 2 * counter) +
              str(instruction) + str(found) + (Style.RESET_ALL))
    else:
        print((" " * 2 * counter) + "|- " + str(instruction) + str(found))
        if instruction == "done...":
            print("\n" + "\n")

    counter += 1


def classify_text(self, text):
    sentimentInfo = self.models.get("Text Classification")
    vocab = sentimentInfo["vocabulary"]
    # Clean up text
    text = lemmatize_text(text_clean_up([text]))
    # Encode text
    text = encode_text(vocab, text)
    text = sequence.pad_sequences(text, sentimentInfo["maxTextLength"])
    model = sentimentInfo["model"]
    prediction = tf.keras.backend.argmax(model.predict(text))
    return sentimentInfo["classes"][tf.keras.backend.get_value(prediction)[0]]


# Sentiment analysis query
def text_classification_query(self, instruction, drop=None,
                              preprocess=True,
                              test_size=0.2,
                              val_size=0.1,
                              random_state=49,
                              learning_rate=1e-2,
                              epochs=20,
                              maximizer="val_loss",
                              batch_size=32,
                              maxTextLength=200,
                              generate_plots=True,
                              save_model=False,
                              save_path=os.getcwd()):
    data = pd.read_csv(self.dataset)
    if preprocess:
        data.fillna(0, inplace=True)
    if drop is None:
        drop = []
    data = data.drop(drop)
    X, Y, target = get_target_values(data, instruction, "label")
    Y = np.array(Y)
    classes = np.unique(Y)

    logger("->", "Target Column Found: {}".format(target))

    vocab = {}
    if preprocess:
        logger("Preprocessing data")
        X = lemmatize_text(text_clean_up(X.array))
        vocab = X
        X = encode_text(X, X)

    X = np.array(X)

    model = get_keras_text_class(maxTextLength, len(classes), learning_rate)
    logger("Building Keras LSTM model dynamically")
    X_train, X_test, y_train, y_test = train_test_split(
        X, Y, test_size=test_size, random_state=random_state)
    X_train = sequence.pad_sequences(X_train, maxlen=maxTextLength)
    X_test = sequence.pad_sequences(X_test, maxlen=maxTextLength)

    y_vals = np.unique(np.append(y_train, y_test))
    label_mappings = {}
    for i in range(len(y_vals)):
        label_mappings[y_vals[i]] = i
    map_func = np.vectorize(lambda x: label_mappings[x])
    y_train = map_func(y_train)
    y_test = map_func(y_test)

    logger("Training initial model")

    # early stopping callback
    es = EarlyStopping(
        monitor=maximizer,
        mode='min',
        verbose=0,
        patience=5)

    history = model.fit(X_train, y_train, validation_data=(X_test, y_test),
                        batch_size=batch_size,
                        epochs=epochs, callbacks=[es], verbose=0)
    # Print Epoch-History Table
    get_standard_training_output_keras(epochs, history)
    logger("->", "Final training loss: {}".format(history.history["loss"][len(history.history["loss"]) - 1]))
    logger("->", "Final validation loss: {}".format(history.history["val_loss"][len(history.history["val_loss"]) - 1]))
    logger("->", "Final validation accuracy: {}".format(
        history.history["val_accuracy"][len(history.history["val_accuracy"]) - 1]))

    plots = {}
    if generate_plots:
        # generates appropriate classification plots by feeding all
        # information
        logger("Generating plots")
        plots = generate_classification_plots(
            history, X, Y, model, X_test, y_test)

    if save_model:
        save(model, save_model, save_path=save_path)

    logger("Storing information in client object under key 'Text Classification'")
    # storing values the model dictionary

    self.models["Text Classification"] = {"model": model,
                                          "classes": classes,
                                          "plots": plots,
                                          "target": Y,
                                          "vocabulary": vocab,
                                          "interpreter": label_mappings,
                                          "maxTextLength": maxTextLength,
                                          'test_data': {'X': X_test, 'y': y_test},
                                          'losses': {
                                              'training_loss': history.history['loss'],
                                              'val_loss': history.history['val_loss']},
                                          'accuracy': {
                                              'training_accuracy': history.history['accuracy'],
                                              'validation_accuracy': history.history['val_accuracy']}}
    clearLog()
    return self.models["Text Classification"]


# Document summarization predict wrapper
def get_summary(self, text):
    modelInfo = self.models.get("Document Summarization")
    model = modelInfo['model']
    model.eval()
    tokenizer = T5Tokenizer.from_pretrained("t5-small")
    df = pd.DataFrame({'text': [""], 'ctext': [text]})
    params = {
        'batch_size': 1,
        'shuffle': True,
        'num_workers': 0
    }
    loader = DataLoader(
        CustomDataset(
            df,
            tokenizer,
            modelInfo["maxTextLength"],
            modelInfo["maxSumLength"]),
        **params)
    predictions, truth = inference(tokenizer, model, "cpu", loader)
    return predictions


# Text summarization query
def summarization_query(self, instruction, preprocess=True,
                        drop=None,
                        epochs=10,
                        batch_size=64,
                        learning_rate=1e-4,
                        max_text_length=512,
                        max_summary_length=150,
                        test_size=0.2,
                        random_state=49,
                        generate_plots=True,
                        save_model=False,
                        save_path=os.getcwd()):
    if drop is None:
        drop = []
    data = pd.read_csv(self.dataset)
    if preprocess:
        data.fillna(0, inplace=True)
    data = data.drop(drop)

    logger("Preprocessing data...")

    X, Y, target = get_target_values(data, instruction, "summary")
    df = pd.DataFrame({'text': Y, 'ctext': X})
    logger("->", "Target Column Found: {}".format(target))

    device = 'cpu'

    torch.manual_seed(random_state)
    np.random.seed(random_state)

    tokenizer = T5Tokenizer.from_pretrained("t5-small")

    train_size = 1 - test_size
    train_dataset = df.sample(
        frac=train_size,
        random_state=random_state).reset_index(
        drop=True)
    val_dataset = df.drop(train_dataset.index).reset_index(drop=True)
    logger("Establishing dataset walkers")
    training_set = CustomDataset(
        train_dataset, tokenizer, max_text_length, max_summary_length)
    val_set = CustomDataset(
        val_dataset,
        tokenizer,
        max_text_length,
        max_summary_length)
    train_params = {
        'batch_size': batch_size,
        'shuffle': True,
        'num_workers': 0
    }

    val_params = {
        'batch_size': batch_size,
        'shuffle': False,
        'num_workers': 0
    }

    training_loader = DataLoader(training_set, **train_params)
    val_loader = DataLoader(val_set, **val_params)
    # used small model
    model = T5ForConditionalGeneration.from_pretrained("t5-small")
    model = model.to(device)

    optimizer = torch.optim.Adam(
        params=model.parameters(), lr=learning_rate)

    logger('Fine-Tuning the model on your dataset...')
    total_loss_train = []
    total_loss_val = []
    for epoch in range(epochs):
        loss_train, loss_val = train(
            epoch, tokenizer, model, device, training_loader, val_loader, optimizer)
        total_loss_train.append(loss_train)
        total_loss_val.append(loss_val)
    # Print Epoch-Loss Table
    get_standard_training_output_generic(
        epochs, total_loss_train, total_loss_val)
    logger("Final Training Loss: ", loss_train)
    logger("Final Validation Loss: ", loss_val)

    plots = {}
    if generate_plots:
        plots.update({"loss": plot_loss(total_loss_train, total_loss_val)})

    if save_model:
        logger("Saving model")
        path = save_path + "DocSummarization.pth"
        torch.save(model, path)
        logger("->", "Saved model to disk as DocSummarization.pth")

    logger("Storing information in client object under key 'Document Summarization'")

    self.models["Document Summarization"] = {
        "model": model,
        "maxTextLength": max_text_length,
        "maxSumLength": max_summary_length,
        "plots": plots,
        'losses': {'training_loss': loss_train,
                   'val_loss': loss_val}
    }
    clearLog()
    return self.models["Document Summarization"]


# Image Caption Generation Prediction
def generate_caption(self, image):
    modelInfo = self.models.get("Image Caption")
    decoder = modelInfo['decoder']
    encoder = modelInfo['encoder']
    tokenizer = modelInfo['tokenizer']
    image_features_extract_model = modelInfo['feature_extraction']
    return generate_caption_helper(
        image,
        decoder,
        encoder,
        tokenizer,
        image_features_extract_model)


# Image Caption Generation query
def image_caption_query(self, instruction,
                        drop=None,
                        epochs=10,
                        preprocess=True,
                        random_state=49,
                        top_k=5000,
                        batch_size=1,
                        buffer_size=1000,
                        embedding_dim=256,
                        units=512,
                        generate_plots=True,
                        save_model_decoder=False,
                        save_path_decoder=os.getcwd(),
                        save_model_encoder=False,
                        save_path_encoder=os.getcwd()):
    np.random.seed(random_state)
    tf.random.set_seed(random_state)

    df = pd.read_csv(self.dataset)
    if preprocess:
        df.fillna(0, inplace=True)
    if drop is not None:
        df = df.drop(drop)

    logger("Preprocessing data")

    train_captions = []
    img_name_vector = []
    x = get_path_column(df)
    y = get_similar_column(get_value_instruction(instruction), df)
    logger("->", "Target Column Found: {}".format(y))

    for row in df.iterrows():
        if preprocess:
            caption = '<start> ' + row[1][y] + ' <end>'
        image_id = row[1][x]
        image_path = image_id

        img_name_vector.append(image_path)
        train_captions.append(caption)

    image_model = tf.keras.applications.InceptionV3(include_top=False,
                                                    weights='imagenet')
    new_input = image_model.input
    hidden_layer = image_model.layers[-1].output
    logger("Extracting features from model")
    image_features_extract_model = tf.keras.Model(new_input, hidden_layer)

    image_dataset = tf.data.Dataset.from_tensor_slices(
        sorted(set(img_name_vector)))
    image_dataset = image_dataset.map(
        load_image, num_parallel_calls=tf.data.experimental.AUTOTUNE).batch(16)

    for img, path in image_dataset:
        batch_features = image_features_extract_model(img)
        batch_features = tf.reshape(
            batch_features, (batch_features.shape[0], -1, batch_features.shape[3]))

        for bf, p in zip(batch_features, path):
            path_of_feature = p.numpy().decode("utf-8")
            np.save(path_of_feature, bf.numpy())
    logger("->", "Tokenizing top {} words".format(top_k))
    tokenizer = tf.keras.preprocessing.text.Tokenizer(
        num_words=top_k, oov_token="<unk>", filters='!"#$%&()*+.,-/:;=?@[\]^_`{|}~ ')
    tokenizer.fit_on_texts(train_captions)
    tokenizer.word_index['<pad>'] = 0
    tokenizer.index_word[0] = '<pad>'
    train_seqs = tokenizer.texts_to_sequences(train_captions)
    cap_vector = tf.keras.preprocessing.sequence.pad_sequences(
        train_seqs, padding='post')

    vocab_size = top_k + 1
    num_steps = len(img_name_vector) // batch_size

    img_name_train, img_name_val, cap_train, cap_val = train_test_split(
        img_name_vector, cap_vector, test_size=0.2, random_state=0)

    dataset = tf.data.Dataset.from_tensor_slices((img_name_train, cap_train))

    dataset = dataset.map(lambda item1, item2: tf.numpy_function(
        map_func, [item1, item2], [tf.float32, tf.int32]),
                          num_parallel_calls=tf.data.experimental.AUTOTUNE)

    # Shuffle and batch
    logger("Shuffling dataset")
    dataset = dataset.shuffle(buffer_size).batch(batch_size)
    dataset = dataset.prefetch(buffer_size=tf.data.experimental.AUTOTUNE)

    dataset_val = tf.data.Dataset.from_tensor_slices((img_name_val, cap_val))

    dataset_val = dataset_val.map(lambda item1, item2: tf.numpy_function(
        map_func, [item1, item2], [tf.float32, tf.int32]),
                                  num_parallel_calls=tf.data.experimental.AUTOTUNE)

    # Shuffle and batch
    dataset_val = dataset_val.shuffle(buffer_size).batch(batch_size)
    dataset_val = dataset_val.prefetch(
        buffer_size=tf.data.experimental.AUTOTUNE)

    logger("Establishing encoder decoder framework")
    encoder = CNN_Encoder(embedding_dim)
    decoder = RNN_Decoder(embedding_dim, units, vocab_size)

    optimizer = tf.keras.optimizers.Adam()
    loss_object = tf.keras.losses.SparseCategoricalCrossentropy(
        from_logits=True, reduction='none')

    def loss_function(real, pred):
        mask = tf.math.logical_not(tf.math.equal(real, 0))
        loss_ = loss_object(real, pred)

        mask = tf.cast(mask, dtype=loss_.dtype)
        loss_ *= mask

        return tf.reduce_mean(loss_)

    @tf.function
    def train_step(img_tensor, target):
        loss = 0

        # initializing the hidden state for each batch
        # because the captions are not related from image to image
        hidden = decoder.reset_state(batch_size=target.shape[0])

        dec_input = tf.expand_dims(
            [tokenizer.word_index['<start>']] * target.shape[0], 1)

        with tf.GradientTape() as tape:
            features = encoder(img_tensor)

            for i in range(1, target.shape[1]):
                # passing the features through the decoder
                predictions, hidden, _ = decoder(dec_input, features, hidden)

                loss += loss_function(target[:, i], predictions)

                # using teacher forcing
                dec_input = tf.expand_dims(target[:, i], 1)

        total_loss = (loss / int(target.shape[1]))

        trainable_variables = encoder.trainable_variables + decoder.trainable_variables

        gradients = tape.gradient(loss, trainable_variables)

        optimizer.apply_gradients(zip(gradients, trainable_variables))

        return loss, total_loss

    @tf.function
    def val_step(img_tensor, target):
        loss = 0

        # initializing the hidden state for each batch
        # because the captions are not related from image to image
        hidden = decoder.reset_state(batch_size=target.shape[0])

        dec_input = tf.expand_dims(
            [tokenizer.word_index['<start>']] * target.shape[0], 1)

        with tf.GradientTape() as tape:
            features = encoder(img_tensor)

            for i in range(1, target.shape[1]):
                # passing the features through the decoder
                predictions, hidden, _ = decoder(dec_input, features, hidden)

                loss += loss_function(target[:, i], predictions)

                # using teacher forcing
                dec_input = tf.expand_dims(target[:, i], 1)

        total_loss = (loss / int(target.shape[1]))
        return total_loss

    logger("Training model...")

    loss_plot_train = []
    loss_plot_val = []
    for epoch in range(epochs):
        total_loss = 0
        total_loss_val = 0

        for (batch, (img_tensor, target)) in enumerate(dataset):
            batch_loss, t_loss = train_step(img_tensor, target)
            total_loss += t_loss

        loss_plot_train.append(total_loss.numpy() / num_steps)

        for (batch, (img_tensor, target)) in enumerate(dataset_val):
            batch_loss, t_loss = train_step(img_tensor, target)
            total_loss_val += t_loss

        loss_plot_val.append(total_loss_val.numpy() / num_steps)
    # Print Epoch-Loss Table
    get_standard_training_output_generic(
        epochs, loss_plot_train, loss_plot_val)

    logger("Storing information in client object under key 'Image Caption' ...")

    dir_name = os.path.dirname(img_name_vector[0])
    files = os.listdir(dir_name)

    for item in files:
        if item.endswith(".npy"):
            os.remove(os.path.join(dir_name, item))

    plots = {}
    if generate_plots:
        plots.update({"loss": plot_loss(loss_plot_train, loss_plot_val)})

    logger("Final Training Loss: ", str(total_loss.numpy() / num_steps))
    logger("Final Validation Loss: ", str(total_loss_val.numpy() / num_steps))

    if save_model_decoder:
        logger("Saving decoder...")
        encoder.save_weights(save_path_decoder + "decoderImgCap.ckpt")

    if save_model_encoder:
        logger("Saving encoder...")
        encoder.save_weights(save_path_encoder + "encoderImgCap.ckpt")

    logger("Storing information in client object under key 'Image Caption'")

    self.models["Image Caption"] = {
        "decoder": decoder,
        "encoder": encoder,
        "tokenizer": tokenizer,
        "feature_extraction": image_features_extract_model,
        "plots": plots,
        'losses': {
            'training_loss': total_loss.numpy(),
            'validation_loss': total_loss_val.numpy()
        }
    }
    clearLog()
    return self.models["Image Caption"]
