import random

import numpy as np
from keras.models import load_model
import matplotlib.pyplot as plt


def gen_test_input():
    data = []
    rand_bpm = random.randint(10, 200)
    peak = int(9600 / rand_bpm)
    for i in range(9600):
        data.append(1) if i % peak == 0 else data.append(0)
    peaks = sum(1 for point in data if point == 1)
    return [data], peaks


if __name__ == '__main__':
    model = load_model('./model.keras')
    stats = []
    for i in range(10_000):
        test_input, curr_bpm = gen_test_input()
        kappa = np.array(test_input)
        pred_bpm = model.predict(np.array(test_input), verbose=0)[0][0]
        stats.append([curr_bpm, pred_bpm, abs(curr_bpm - pred_bpm)])
        progress_perc = int((i + 1) / 1000 * 100)
        print(f"Progress: {progress_perc}%", end='\r')

    actual, predicted, abs_diff = zip(*stats)

    indecies = list(enumerate(actual))
    sorted_pairs = sorted(indecies, key=lambda x: x[1])
    actual = [value for index, value in sorted_pairs]
    actual_indices = [index for index, value in sorted_pairs]
    predicted = [predicted[actual_indices[i]] for i in range(len(actual))]

    # Creating subplots
    fig, axs = plt.subplots(2, 1, figsize=(9, 14))

    # Plotting Predicted vs Actual values with just points
    axs[0].plot(np.array(predicted), 'r.', label='Predicted')  # Red points
    axs[0].plot(np.array(actual), 'b.', label='Actual')  # Blue points
    axs[0].set_title('Predicted vs Actual Values')
    axs[0].legend()

    # Plotting Absolute Differences with just points
    axs[1].plot(range(len(abs_diff)), np.array(sorted(abs_diff)), 'g.')  # Green points
    axs[1].set_title('Absolute Differences (Sorted)')

    plt.show()