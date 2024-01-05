import random
import json


def create_training_data(dataPointsPerSecond, dataAmount):
    data = []
    counter = 0
    while counter < dataAmount:
        test_data = create_test_data(dataPointsPerSecond)
        if test_data is not None:
            data.append(test_data)
            counter += 1
    return data


def create_test_data(dataPointsPerSecond):
    dataLengthInSeconds = 3
    sizePrevBPM = random.randint(40, 60)
    sizeNextBPM = 100 - sizePrevBPM
    prevBPMArray = create_data_array(sizePrevBPM / 100 * dataLengthInSeconds, dataPointsPerSecond)
    nextBPMArray = create_data_array(sizeNextBPM / 100 * dataLengthInSeconds, dataPointsPerSecond)
    prevBPM = get_bpm(prevBPMArray, dataPointsPerSecond)
    nextBPM = get_bpm(nextBPMArray, dataPointsPerSecond)
    if nextBPM == prevBPM == 0:
        return None
    data = prevBPMArray + nextBPMArray
    return {'data': data, 'prevBPM': prevBPM, 'nextBPM': nextBPM}


def create_data_array(size, dataPointsPerSecond):
    arraySize = round(size * dataPointsPerSecond)
    array = []
    for _ in range(0, arraySize):
        array.append(random_zero_or_one())
    return array


def get_bpm(data, dataPointsPerSecond):
    spikes = 0
    for i in range(0, len(data)):
        if data[i] == 1:
            spikes += 1
    timespan = len(data) / dataPointsPerSecond
    return spikes / timespan * 60


def random_zero_or_one():
    perc = random.randint(0, 1)
    return 1 if random.randint(1, 100) <= perc else 0


if __name__ == '__main__':
    data = create_training_data(160, 50000)
    # Convert data to JSON and write to a file
    with open('../data/plain_data.json', 'w') as file:
        json.dump(data, file)

