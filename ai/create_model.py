import ai.utils.train_model as model
import ai.utils.split_data as data
import ai.utils.test_ai_model as test


if __name__ == '__main__':
    units = 15
    epochs = 50
    layers = 1
    activation = 'tanh'

    print(activation)
    print('Epochs:', epochs)

    # Generate and adjust data
    data.adjust_data(300, False)

    # Train model
    ai_model_path = model.train_model(lstm_units=units, epochs=epochs, lstm_layers=layers, activation=activation)

    # Test model
    test.test_model(model_path=ai_model_path)
