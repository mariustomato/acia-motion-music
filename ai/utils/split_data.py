from keras.preprocessing.sequence import pad_sequences
from sklearn.model_selection import train_test_split
import ai.utils.dummy_data_creator as data
import numpy as np
import json


def adjust_data(amount=50_000, useOldData=False):
    if useOldData:
        return
    # Create training data
    data.create_training_data(dataAmount=amount)

    # Load the data back from the file
    with open('./data/plain_data.json', 'r') as file:
        loaded_data = json.load(file)

    data_items = [np.array(entry['data']) for entry in loaded_data]

    # Determine the maximum sequence length
    max_sequence_length = max(len(sequence) for sequence in data_items)

    # Pad the sequences with -1
    data_items_padded = [pad_sequences([sequence], maxlen=max_sequence_length, padding='post', value=-1)[0] for sequence in data_items]
    data_items_padded = np.stack(data_items_padded)

    # Extracting prevBPM and nextBPM
    prev_bpm = np.array([entry['prevBPM'] for entry in loaded_data])
    next_bpm = np.array([entry['nextBPM'] for entry in loaded_data])

    prev_bpm_expanded = np.repeat(prev_bpm.reshape(len(loaded_data), 1), max_sequence_length, axis=1)  # reshape and repeat to match data_items
    prev_bpm_expanded_padded = pad_sequences(prev_bpm_expanded, maxlen=max_sequence_length, padding='post', value=-1)

    # Combine the padded data
    x_data_padded = np.concatenate((data_items_padded[..., np.newaxis], prev_bpm_expanded_padded[..., np.newaxis]), axis=2)

    # Split the padded data
    x_train, x_test = train_test_split(x_data_padded, test_size=0.2, random_state=42)
    y_train, y_test = train_test_split(next_bpm, test_size=0.2, random_state=42)

    print("NaNs in x_train:", np.isnan(x_train).any())
    print("NaNs in y_train:", np.isnan(y_train).any())
    print("NaNs in x_test:", np.isnan(x_test).any())
    print("NaNs in y_test:", np.isnan(y_test).any())

    with open('./data/train_data_x.json', 'w') as file:
        json.dump(x_train.tolist(), file)
    with open('./data/train_data_y.json', 'w') as file:
        json.dump(y_train.tolist(), file)
    with open('./data/test_data_x.json', 'w') as file:
        json.dump(x_test.tolist(), file)
    with open('./data/test_data_y.json', 'w') as file:
        json.dump(y_test.tolist(), file)

