import matplotlib.pyplot as plt
from sklearn.metrics import mean_squared_error
import numpy as np


def test(model, x_test, y_test, base_path):
    if model is None:
        raise ValueError("model must not be None")

    x_test = np.array(x_test)
    y_test = np.array(y_test)

    # Predict BPM
    predicted_bpm = model.predict(x_test.reshape(-1, len(x_test[0]), 1))
    # mse = mean_squared_error(y_test, predicted_bpm.flatten())

    conclusion = []
    for i in range(len(predicted_bpm)):
        prediction = predicted_bpm[i].item()
        wanted = y_test[i]
        difference = abs(prediction - wanted)
        conclusion.append([prediction, wanted, difference])

    # Unzipping the data
    predicted, actual, abs_diff = zip(*conclusion)

    t_predicted = list(predicted)
    t_actual = list(actual)

    indexed_actual = list(enumerate(actual))
    sorted_pairs = sorted(indexed_actual, key=lambda x: x[1])
    actual_sorted = [value for index, value in sorted_pairs]
    actual_indices = [index for index, value in sorted_pairs]
    sub_sorted_predicted = [predicted[actual_indices[i]] for i in range(len(actual_sorted))]
    sub_sorted_abs_diff = [abs_diff[actual_indices[i]] for i in range(len(actual_sorted))]

    # Convert to numpy arrays for easier manipulation
    predicted = np.array(sub_sorted_predicted)
    actual = np.array(actual_sorted)
    abs_diff = np.array(sub_sorted_abs_diff)
    sortedasdas = sorted(sub_sorted_abs_diff)
    abs_diff_sorted = np.array(sortedasdas)

    # Creating subplots
    fig, axs = plt.subplots(3, 1, figsize=(9, 14))

    # Plotting Predicted vs Actual values with just points
    axs[0].plot(predicted, 'r.', label='Predicted')  # Red points
    axs[0].plot(actual, 'b.', label='Actual')  # Blue points
    axs[0].set_title('Predicted vs Actual Values')
    axs[0].legend()

    # Plotting Absolute Differences with just points
    axs[1].plot(range(len(abs_diff_sorted)), abs_diff_sorted, 'g.')  # Green points
    axs[1].set_title('Absolute Differences (Sorted)')

    # Plotting the percentage for points with 0-100+ points difference in 5 steps
    bins = [0.0001, 0.001, 0.01, 0.1, 1, 2, 5, 10, 100]
    bin_counts = np.histogram(abs_diff, bins=bins)[0]
    percentages = (bin_counts / len(abs_diff)) * 100  # Convert counts to percentages
    axs[2].bar(bins[:-1], percentages, width=4, align='edge', color='orange')
    axs[2].set_xticks(bins)
    axs[2].set_title('Percentage of Points by Difference Range')
    axs[2].set_xlabel('Difference Range')
    axs[2].set_ylabel('Percentage')
    axs[2].set_xscale('log')

    # Display the plots
    plt.tight_layout()

    # Save the figure
    plt.savefig(base_path + '/train_stats.png', dpi=300)

    plt.show()
