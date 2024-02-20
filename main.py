import time
from datetime import datetime

import numpy as np
from keras.models import load_model
from utils.peak_detection import real_time_peak_detection
from listeners.com_listener import ComListener
from listeners.simulated_listener import SimulatedListener
from utils.client import Client

THRESHOLD = 5  # the amount for a trigger (away from curr average)
LAG = 10
INFLUENCE = 0.1  # value between [0,1]->no to full influence
PEAK_VAL = 1  # TODO: adjust peak value on hardware implementation
MODEL_PATH = './model.keras'
SAMPLING_RATE = 160
PEAK_VAL = 1
SAMPLING_SIZE = 480
MAX_BPM = 200
USE_STATIC_BPM = False


def calc_avg_bpm(arr: []):
    sum_bpm = 0
    for curr_bpm in arr:
        sum_bpm += curr_bpm
    return sum_bpm / len(arr)


if __name__ == '__main__':
    listeners = [
        # ComListener(com_port='COM6', sampling_size=SAMPLING_SIZE, max_bpm=MAX_BPM, sampling_rate=SAMPLING_RATE),
        SimulatedListener()
    ]



    PROGRAM_START = time.time()
    time_stamp = time.time()

    osc_client = Client()
    model = load_model(MODEL_PATH)

    predicted_bpms = [0]  # Smoothing of the predicted bpm

    CURR_TIME = datetime.now()
    window_size = 4
    sampling_time_diff = 1 / SAMPLING_RATE
    bpm = 0
    sequence = [0] * SAMPLING_SIZE

    peak_detector = real_time_peak_detection(array=sequence, lag=LAG, threshold=THRESHOLD, influence=2)

    while True:
        bpm = 0  # will be set to current highest bpm of all listeners
        for listener in listeners:
            # stop "overclocking"
            if listener.last_update + sampling_time_diff > time.time():
                continue
            else:
                listener.handleLostSignals()

            # get new value
            val = int(listener.read())
            val = listener.peak_detector.thresholding_algo(val)

            if len(sequence) >= SAMPLING_SIZE:
                sequence = sequence[1:]
            sequence.append(val)

            adjusted_sequence = np.array([sequence])

            bpm = model.predict(adjusted_sequence, verbose=0)[0][0]

            predicted_bpms.append(bpm)
            smoothed_bpm = calc_avg_bpm(predicted_bpms)

            if val > 0:  # print new value if peak was detected
                ones = sum(1 for element in sequence if element == 1)
                print(f"Num. of 1's detected: {ones}")
                print(f"{abs(time_stamp - time.time())}s since last peak -->  BPM: {smoothed_bpm}; Val: {val}")
                time_stamp = time.time()
                print(f"Detected BPM: {smoothed_bpm}; Unsmoothed BPM: {bpm}; Difference: {abs(smoothed_bpm - bpm)}")

            if bpm > bpm: bpm = bpm  # choose biggest bpm of all listeners

            # osc_client.tempoChange(bpm / 60, 4)
