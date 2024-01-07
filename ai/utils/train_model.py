from keras.models import Sequential
from keras.layers import LSTM, Dense
import numpy as np
import json
import datetime
import os
import matplotlib.pyplot as plt


def train_model(lstm_units=15, activation="tanh", optimizer="adam", loss="mse", epochs=10, lstm_layers=3, batch_size=64):
    data_dir = './data'

    if not os.path.exists(data_dir):
        print("Data directory not found!")
        exit(1)

    print("Loading data...")
    # Load the data back from the file
    with open('data/train_data_x.json', 'r') as file:
        x_train = np.array(json.load(file))
    with open('data/train_data_y.json', 'r') as file:
        y_train = np.array(json.load(file))

    print("Loading model finished!")
    print("Starting to train model...")

    # Build the LSTM model
    model = Sequential()
    for i in range(lstm_layers):
        if i < lstm_layers - 1:
            # All layers except the last one return full sequences
            model.add(LSTM(lstm_units, activation=activation, return_sequences=True, input_shape=(len(x_train[0]), 2)))
        else:
            # Last layer only returns the last output
            model.add(LSTM(lstm_units, activation=activation, input_shape=(len(x_train[0]), 2)))

    model.add(Dense(1))
    model.compile(optimizer=optimizer, loss=loss)

    # Train the model using nextBPM as labels
    history = model.fit(x_train, y_train, epochs=epochs, batch_size=batch_size, verbose=1)

    time_stamp = str(datetime.datetime.now().timestamp())
    base_path = './models/' + time_stamp + '/'

    os.makedirs(base_path, exist_ok=True)

    model_configs = {
        'units': lstm_units,
        'layers': lstm_layers,
        'activation': activation,
        'optimizer': optimizer,
        'epochs': epochs,
        'batch_size': batch_size,
        'loss': loss
    }

    with open(base_path + 'config.json', 'w') as file:
        json.dump(model_configs, file)

    with open(base_path + 'history.json', 'w') as file:
        json.dump(history.history, file)

    # Save model
    model.save(base_path + 'model.keras')

    plt.figure(figsize=(10, 6))
    plt.plot(history.history['loss'], label='Training Loss')
    plt.title('Training Loss over Epochs')
    plt.xlabel('Epochs')
    plt.ylabel('Loss')
    plt.legend()
    plt.show()

    return base_path

