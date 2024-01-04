from keras.models import Sequential, load_model
from keras.layers import LSTM, Dense
from sklearn.model_selection import train_test_split
import numpy as np
import json

if __name__ == '__main__':
    # Load the data back from the file
    with open('../data/plain_data.json', 'r') as file:
        loaded_data = json.load(file)

    data_items = np.array([entry['data'] for entry in loaded_data])  # Extracting all data arrays
    data_items = data_items.reshape((len(loaded_data), len(loaded_data[0]['data']), 1))  # Reshaping to be 3D

    # Extracting prevBPM and nextBPM
    prev_bpm = np.array([entry['prevBPM'] for entry in loaded_data])
    next_bpm = np.array([entry['nextBPM'] for entry in loaded_data])

    prev_bpm_expanded = np.repeat(prev_bpm.reshape(len(loaded_data), 1, 1), len(loaded_data[0]['data']), axis=1) # reshape and repeat to match data_items
    x_data = np.concatenate((data_items, prev_bpm_expanded), axis=2)  # Now each time step has 2 features

    x_train, x_test = train_test_split(x_data, test_size=0.2, random_state=42)
    y_train, y_test = train_test_split(next_bpm, test_size=0.2, random_state=42)

    print("NaNs in x_train:", np.isnan(x_train).any())
    print("NaNs in y_train:", np.isnan(y_train).any())
    print("NaNs in x_test:", np.isnan(x_test).any())
    print("NaNs in y_test:", np.isnan(y_test).any())

    with open('../data/train_data_x.json', 'w') as file:
        json.dump(x_train.tolist(), file)
    with open('../data/train_data_y.json', 'w') as file:
        json.dump(y_train.tolist(), file)
    with open('../data/test_data_x.json', 'w') as file:
        json.dump(x_test.tolist(), file)
    with open('../data/test_data_y.json', 'w') as file:
        json.dump(y_test.tolist(), file)

