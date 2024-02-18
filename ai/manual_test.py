import json
from keras.models import load_model
import ai.helper.test_model as model_tester


def load_data(base_path):
    with open(base_path + 'test_data_x.json', 'r') as file:
        x_test = json.load(file)
    with open(base_path + 'test_data_y.json', 'r') as file:
        y_test = json.load(file)
    return x_test, y_test

if __name__ == '__main__':
    model = load_model('./models/1707505069.758845/models/model.keras')
    x_test, y_test = load_data('./models/1707505069.758845/data/')
    model_tester.test(model, x_test, y_test, './models/1707505069.758845/')