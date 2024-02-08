import json
import os
import random

import numpy as np
import scipy.signal as signal


def create_training_data(dataAmount):
    data = []
    counter = 0
    while counter < dataAmount:
        test_data = create_test_data(160, counter)
        if test_data is not None:
            data.append(test_data)
            counter += 1

    random.shuffle(data)
    data_dir = './data'

    if not os.path.exists(data_dir):
        os.makedirs(data_dir)

    with open(data_dir + '/plain_data.json', 'w') as file:
        json.dump(data, file)


def create_test_data(dataPointsPerSecond, iteration):
    dataEntryLength = 500
    frequency = iteration * 0.01 + 0.01
    sample_rate = dataPointsPerSecond
    sine_array = create_randomized_sine_array(dataEntryLength, frequency, sample_rate)
    return {'data': sine_array.tolist(), 'nextBPM': frequency}


def create_randomized_sine_array(length, frequency, sample_rate):
    t = np.linspace(0, length / sample_rate, length, endpoint=False)
    sine_wave = np.sin(2 * np.pi * frequency * t)
    return np.clip(sine_wave, -1, 1)


def calculate_frequency(array, sample_rate):
    frequencies, times, spectrogram = signal.spectrogram(array, sample_rate)
    dominant_frequency_index = np.argmax(np.mean(spectrogram, axis=1))
    return frequencies[dominant_frequency_index]
