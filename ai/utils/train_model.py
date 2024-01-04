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

    lstm_layers = 200
    activation = 'sigmoid'
    optimizer = 'adam'
    loss = 'mse'
    epochs = 5

    # l=25, a=tanh, 1785
    # l=50, a=tanh
    # l=100, a=tanh
    # l=200, a=tanh
    # l=25, a=sigmoid
    # l=50, a=sigmoid
    # l=100, a=sigmoid
    # l=200, a=sigmoid


    # Build the LSTM model
    model = Sequential()
    model.add(LSTM(lstm_layers, activation=activation, input_shape=(len(x_train[0]), 2)))  # Adjusted for 2 features
    model.add(Dense(1))
    model.compile(optimizer=optimizer, loss=loss)

    # Train the model using nextBPM as labels
    model.fit(x_train, y_train, epochs=epochs, verbose=1)

    # Save model
    model_name = 'lstm_' + str(lstm_layers) + '_activation_' + activation + '_optimizer_' + optimizer + '_loss_' + loss + '_epochs_' + str(epochs) + '.keras'
    model.save('../models/' + model_name)

