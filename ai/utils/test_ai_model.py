from keras.models import load_model
import matplotlib.pyplot as plt
from sklearn.metrics import mean_squared_error
from math import sqrt
import numpy as np
import json


def test_model(model_path):
    # Load the data back from the file
    with open('./data/test_data_x.json', 'r') as file:
        x_train = np.array(json.load(file))
    with open('./data/test_data_y.json', 'r') as file:
        y_train = np.array(json.load(file))

    model = load_model(model_path + 'model.keras')

    if model is None:
        print('No model')
        exit(1)

    # Predict BPM
    predicted_bpm = model.predict(x_train)
    mse = mean_squared_error(y_train, predicted_bpm.flatten())
    print('MSE: ' + str(mse))
    print('Average off-value: ' + str(sqrt(mse)))

    conclusion = []
    for i in range(len(predicted_bpm)):
        prediction = predicted_bpm[i].item()
        wanted = y_train[i]
        difference = abs(prediction - wanted)
        conclusion.append([prediction, wanted, difference])

    # Unzipping the data
    predicted, actual, abs_diff = zip(*conclusion)

    # Convert to numpy arrays for easier manipulation
    predicted = np.array(predicted)
    actual = np.array(actual)
    abs_diff = np.array(abs_diff)

    # Creating subplots
    fig, axs = plt.subplots(3, 1, figsize=(9, 14))

    # Plotting Predicted vs Actual values with just points
    axs[0].plot(predicted, 'r.', label='Predicted')  # Red points
    axs[0].plot(actual, 'b.', label='Actual')  # Blue points
    axs[0].set_title('Predicted vs Actual Values')
    axs[0].legend()

    # Plotting Absolute Differences with just points
    axs[1].plot(range(len(abs_diff)), abs_diff, 'g.', label='Abs Diff')  # Green points
    axs[1].set_title('Absolute Differences')

    # Plotting the percentage for points with 5-100+ points difference in 5 steps
    bins = [5, 10, 15, 20, 25, 30, 35, 40, 45, 50, 55, 60, 65, 70, 75, 80, 85, 90, 95, 100]
    bin_counts = np.histogram(abs_diff, bins=bins)[0]
    percentages = (bin_counts / len(abs_diff)) * 100  # Convert counts to percentages
    axs[2].bar(bins[:-1], percentages, width=4, align='edge', color='purple')
    axs[2].set_xticks(bins)
    axs[2].set_title('Percentage of Points by Difference Range')
    axs[2].set_xlabel('Difference Range')
    axs[2].set_ylabel('Percentage')

    # Display the plots
    plt.tight_layout()

    # Save the figure
    plt.savefig(model_path + '/stats.png', dpi=300)  # Saves the figure to a file named 'plot.png' with 300 dpi

    plt.show()  # This will display the plot
