from keras.models import Sequential
from keras.layers import LSTM, Dense
import numpy as np
import json
import datetime
import os
import matplotlib.pyplot as plt


def train(lstm_units=15, activation="tanh", optimizer="adam", loss="mse", epochs=10, lstm_layers=3):
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

    print("Loading data finished!")
    print("Starting to train model...")

    ############################### MODEL ###############################

    # Build the LSTM model
    model = Sequential()
    #for i in range(lstm_layers - 1):
        # All layers except the last one return full sequences
        #model.add(LSTM(lstm_units, activation=activation, return_sequences=True, input_shape=(len(x_train[0]), 1)))
    model.add(LSTM(lstm_units, activation=activation, input_shape=(len(x_train[0]), 1)))
    model.add(Dense(1))
    model.compile(optimizer=optimizer, loss=loss, metrics=['accuracy'])

    # Train the model using nextBPM as labels
    history = model.fit(x_train.reshape(-1, len(x_train[0]), 1), y_train, epochs=epochs, verbose=2, validation_split=0.2)

    #####################################################################

    time_stamp = str(datetime.datetime.now().timestamp())
    base_path = './models/' + time_stamp + '/'

    os.makedirs(base_path, exist_ok=True)

    model_configs = {
        'units': lstm_units,
        'layers': lstm_layers,
        'activation': activation,
        'optimizer': optimizer,
        'epochs': epochs,
        'loss': loss
    }

    with open(base_path + 'config.json', 'w') as file:
        json.dump(model_configs, file)

    with open(base_path + 'history.json', 'w') as file:
        json.dump(history.history, file)

    # Save model
    model.save(base_path + 'model.keras')
    model.save(base_path + 'model.h5')

    plt.figure(figsize=(10, 6))
    plt.plot(history.history['loss'], label='Training Loss')
    plt.title('Training Loss over Epochs')
    plt.xlabel('Epochs')
    plt.ylabel('Loss')
    plt.legend()

    plt.savefig(base_path + 'loss.png')

    plt.show()

    return base_path

