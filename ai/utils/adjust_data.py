from keras.preprocessing.sequence import pad_sequences
import ai.utils.dummy_data_creator2 as data
import numpy as np
import json


def adjust(amount=50_000, use_old_data=False):
    if use_old_data:
        return
    # Create training data
    data.create_training_data(dataAmount=amount)

    # Load the data back from the file
    with open('./data/plain_data.json', 'r') as file:
        loaded_data = json.load(file)

    data_items = [entry['data'] for entry in loaded_data]


    # Extracting prevBPM and nextBPM
    next_bpm = [entry['nextBPM'] for entry in loaded_data]

    # Split the padded data
    x_size = int(len(data_items) * .8)
    y_size = int(len(next_bpm) * .8)
    x_train = data_items[:x_size]
    x_test = data_items[x_size:]
    y_train = next_bpm[:y_size]
    y_test = next_bpm[y_size:]

    print("NaNs in x_train:", np.isnan(x_train).any())
    print("NaNs in y_train:", np.isnan(y_train).any())
    print("NaNs in x_test:", np.isnan(x_test).any())
    print("NaNs in y_test:", np.isnan(y_test).any())

    with open('./data/train_data_x.json', 'w') as file:
        json.dump(x_train, file)
    with open('./data/train_data_y.json', 'w') as file:
        json.dump(y_train, file)
    with open('./data/test_data_x.json', 'w') as file:
        json.dump(x_test, file)
    with open('./data/test_data_y.json', 'w') as file:
        json.dump(y_test, file)

