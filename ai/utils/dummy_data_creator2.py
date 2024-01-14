import random
import json
import os


def create_training_data(dataAmount):
    data = []
    counter = 0
    while counter < dataAmount:
        test_data = create_test_data(160)
        if test_data is not None:
            data.append(test_data)
            counter += 1

    data_dir = './data'

    if not os.path.exists(data_dir):
        os.makedirs(data_dir)

    with open(data_dir + '/plain_data.json', 'w') as file:
        json.dump(data, file)


def create_test_data(dataPointsPerSecond):
    dataEntryLength = 1000
    sizePrevBPM = random.randint(20, 80)
    sizeNextBPM = 100 - sizePrevBPM
    prevBPMArray = create_data_array(sizePrevBPM / 100 * dataEntryLength, dataPointsPerSecond)
    nextBPMArray = create_data_array(sizeNextBPM / 100 * dataEntryLength, dataPointsPerSecond)
    prevBPM = get_bpm(prevBPMArray, dataPointsPerSecond)
    nextBPM = get_bpm(nextBPMArray, dataPointsPerSecond)
    if nextBPM == prevBPM == 0:
        return None
    data = prevBPMArray + nextBPMArray
    return {'data': data, 'prevBPM': prevBPM, 'nextBPM': nextBPM}


def create_data_array(size, dataPointsPerSecond):
    randBPMGoal = random.randint(39, 180)
    randBPSGoal = (randBPMGoal / 60.0)
    maxVariance = round(dataPointsPerSecond / 10)  # max. 100ms variance per "beat"
    currVariance = random.randint(0, maxVariance)  # random variance between 0 and 100ms
    nextOne = round(dataPointsPerSecond / randBPSGoal)
    arraySize = round(size)
    randStart = random.randint(1, 200)
    array = []
    slidingNextOne = nextOne
    for i in range(randStart, arraySize + randStart):
        if (i % (slidingNextOne + currVariance)) == 0:
            array.append(1)
            currVariance = random.randint(0, maxVariance)  # generate new variance
            slidingNextOne = nextOne + i
        else:
            array.append(0)
    return array


def get_bpm(dataSeq, dataPointsPerSecond):
    spikes = 0
    for i in range(0, len(dataSeq)):
        if dataSeq[i] == 1:
            spikes += 1
    timespan = len(dataSeq) / dataPointsPerSecond
    return spikes / timespan * 60
