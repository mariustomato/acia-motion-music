from keras.models import load_model
import numpy as np
import json

if __name__ == '__main__':
    # Load the data back from the file
    with open('../data/train_data_x.json', 'r') as file:
        x_train = np.array(json.load(file))
    with open('../data/train_data_y.json', 'r') as file:
        y_train = np.array(json.load(file))

    model_name = '../models/old/somewhat-ok/lstm_15_activation_tanh_optimizer_adam_loss_mse_epochs_20'
    model = load_model(model_name + '.keras')
    epochs = 500

    # Train the model using nextBPM as labels
    #history = model.fit(x_train, y_train, epochs=epochs, verbose=1)

    #with open('../stats/histories/history_model_15.json', 'w') as file:
    #    json.dump(history.history, file)

    # Save model
    #model_name_new = model_name + '_updated_500_epochs.keras'
    #model.save('../models/' + model_name_new)

