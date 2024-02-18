import datetime
import os

import ai.helper.train_model as model_wrapper
import ai.helper.data_generator as data_creator
import ai.helper.test_model as model_tester


if __name__ == '__main__':
    units = 80
    epochs = 100
    layers = 1
    activation = 'tanh'

    # Create folder for the model, data, history etc.
    base_path = './models/' + str(datetime.datetime.now().timestamp()) + '/'
    os.makedirs(base_path, exist_ok=True)

    # Print the model configuration
    print('Model configuration:')
    print('Units:', units)
    print('Layers:', layers)
    print('Activation:', activation)
    print('Epochs:', epochs)

    print('#############################################')

    # Create training data
    print('Creating training data...')
    x_train, y_train, x_test, y_test = data_creator.generate(50_000, base_path, False)
    print('Training data created!')

    print('#############################################')

    # Create and train model
    print('Creating and training model...')
    model = model_wrapper.train(lstm_units=units, epochs=epochs, lstm_layers=layers, activation=activation,
                                base_path=base_path, verbose=2, x_train=x_train, y_train=y_train)
    print('Model created and trained!')

    print('#############################################')

    # Test model
    print('Testing model...')
    model_tester.test(model, x_test, y_test, base_path)
    print('Model tested!')