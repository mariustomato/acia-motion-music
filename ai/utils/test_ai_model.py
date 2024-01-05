from keras.models import load_model
import matplotlib.pyplot as plt
from sklearn.metrics import mean_squared_error
from math import sqrt
import numpy as np
import json

if __name__ == '__main__':
    # Load the data back from the file
    with open('../data/test_data_x.json', 'r') as file:
        x_train = np.array(json.load(file))
    with open('../data/test_data_y.json', 'r') as file:
        y_train = np.array(json.load(file))

    model = load_model('../models/lstm_20_activation_tanh_optimizer_adam_loss_mse_epochs_500.keras')

    # Predict BPM
    predicted_bpm = model.predict(x_train)
    mse = mean_squared_error(y_train, predicted_bpm.flatten())
    print(mse)
    print(sqrt(mse))
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

    # Plotting Differences as a point plot for a more detailed view
    axs[2].plot(abs_diff, 'g.')
    axs[2].set_title('Absolute Differences (Point Plot)')

    # Display the plots
    plt.tight_layout()

    # Save the figure
    plt.savefig('plot2.png', dpi=300)  # Saves the figure to a file named 'plot.png' with 300 dpi

    plt.show()  # This will display the plot
