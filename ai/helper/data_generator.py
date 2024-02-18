import os

import ai.helper.dummy_data_creator4 as data
import numpy as np
import json


def generate(amount=50_000, base_path=None, use_old_data=False):
    if use_old_data:
        return

    if base_path is None:
        raise ValueError("base_path must not be None")

    os.makedirs(base_path + '/data/', exist_ok=True)

    # Create training data
    generated_data = data.create_training_data(amount, base_path)

    data_items = [entry['data'] for entry in generated_data]

    # Extracting nextBPM value
    next_bpm = [entry['nextBPM'] for entry in generated_data]

    # Split the padded data into 80% training and 20% testing
    x_size = int(len(data_items) * .8)
    y_size = int(len(next_bpm) * .8)
    x_train = data_items[:x_size]
    x_test = data_items[x_size:]
    y_train = next_bpm[:y_size]
    y_test = next_bpm[y_size:]

    if np.isnan(x_train).any() or np.isnan(y_train).any() or np.isnan(x_test).any() or np.isnan(y_test).any():
        raise ValueError("NaNs in the data")

    with open(base_path + '/data/train_data_x.json', 'w') as file:
        json.dump(x_train, file)
    with open(base_path + '/data/train_data_y.json', 'w') as file:
        json.dump(y_train, file)
    with open(base_path + '/data/test_data_x.json', 'w') as file:
        json.dump(x_test, file)
    with open(base_path + '/data/test_data_y.json', 'w') as file:
        json.dump(y_test, file)

    return x_train, y_train, x_test, y_test

