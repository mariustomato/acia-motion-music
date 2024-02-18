from keras.models import Sequential
from keras.layers import LSTM, Dense, MaxPooling1D
import numpy as np
import json
import os
import matplotlib.pyplot as plt


def train(lstm_units=15, activation="tanh", optimizer="adam", loss="mse", epochs=10, lstm_layers=3,
          base_path=None, verbose=0, x_train=None, y_train=None):
    data_dir = './data'

    if not os.path.exists(base_path + data_dir):
        raise ValueError("Data directory does not exist")

    ############################### MODEL ###############################

    # Build the LSTM model
    model = Sequential()
    # model.add(MaxPooling1D(pool_size=40))
    model.add(MaxPooling1D(pool_size=20, input_shape=(len(x_train[0]), 1)))
    # model.add(Flatten())
    for i in range(lstm_layers - 1):
        # All layers except the last one return full sequences
        model.add(LSTM(lstm_units, activation=activation, return_sequences=True, input_shape=(len(x_train[0]), 1)))
    model.add(LSTM(lstm_units, activation=activation, input_shape=(len(x_train[0]), 1)))
    model.add(Dense(1))
    model.compile(optimizer=optimizer, loss=loss, metrics=['accuracy'])

    x_train = np.array(x_train)
    y_train = np.array(y_train)

    # Train the model using nextBPM as labels
    history = model.fit(x_train.reshape(-1, len(x_train[0]), 1), y_train, epochs=epochs, verbose=verbose,
                        validation_split=0.2)

    #####################################################################

    model_path = base_path + './models/'

    os.makedirs(model_path, exist_ok=True)

    model_configs = {
        'units': lstm_units,
        'layers': lstm_layers,
        'activation': activation,
        'optimizer': optimizer,
        'epochs': epochs,
        'loss': loss
    }

    with open(model_path + 'config.json', 'w') as file:
        json.dump(model_configs, file)

    with open(model_path + 'history.json', 'w') as file:
        json.dump(history.history, file)

    # Save model
    model.save(model_path + 'model.keras')
    model.save(model_path + 'model.h5')

    plt.figure(figsize=(10, 6))
    plt.plot(history.history['loss'], label='Loss')
    plt.plot(history.history['val_loss'], label='Validation Loss')
    plt.title('Loss over Epochs')
    plt.xlabel('Epochs')
    plt.ylabel('Loss')
    plt.legend()

    plt.savefig(base_path + 'loss.png')

    plt.show()

    return model

