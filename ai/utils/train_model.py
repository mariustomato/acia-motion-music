from keras.models import Sequential, load_model
from keras.layers import LSTM, Dense
from sklearn.model_selection import train_test_split
import numpy as np
import json

if __name__ == '__main__':
    # Load the data back from the file
    with open('../data/train_data_x.json', 'r') as file:
        x_train = np.array(json.load(file))
    with open('../data/train_data_y.json', 'r') as file:
        y_train = np.array(json.load(file))

    lstm_units = 5
    activation = 'tanh'
    optimizer = 'adam'
    loss = 'mse'
    epochs = 20
    lstm_layers = 1

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
    history = model.fit(x_train, y_train, epochs=epochs, verbose=1)

    with open('../data/history_1_layer_5_units.json', 'w') as file:
        json.dump(history.history, file)

    # Save model
    model_name = 'lstm_units_' + str(lstm_units) + '_lstm_layers_' + str(lstm_layers) + '_activation_' + activation + '_optimizer_' + optimizer + '_loss_' + loss + '_epochs_' + str(epochs) + '.keras'
    model.save('../models/' + model_name)

