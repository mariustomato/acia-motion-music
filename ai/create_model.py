import ai.utils.train_model as model
import ai.utils.adjust_data as data
import ai.utils.test_model as test


if __name__ == '__main__':
    units = 64
    epochs = 100
    layers = 1
    activation = 'tanh'

    print(activation)
    print('Epochs:', epochs)

    # Generate and adjust data
    data.adjust(300, False)

    # Train model
    ai_model_path = model.train(lstm_units=units, epochs=epochs, lstm_layers=layers, activation=activation)

    # Test model
    test.test(model_path=ai_model_path)
