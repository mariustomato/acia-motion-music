from keras.models import Sequential, load_model
from keras.layers import LSTM, Dense
from sklearn.model_selection import train_test_split
import numpy as np
import json

if __name__ == '__main__':
    # Load the data back from the file
    with open('../data/test_data_x.json', 'r') as file:
        x_train = np.array(json.load(file))
    with open('../data/test_data_y.json', 'r') as file:
        y_train = np.array(json.load(file))

    model = load_model('../predict_bpm_dense_3_activation_sigmoid_epochs_200.keras')

    # Predict BPM
    predicted_bpm = model.predict(x_data)

    print(predicted_bpm)
