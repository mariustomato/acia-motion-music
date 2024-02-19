import time
from datetime import datetime

import numpy as np
from keras.models import load_model

from listeners.com_listener import ComListener
from listeners.simulated_listener import SimulatedListener
from utils.client import Client
from utils.plain_bpm_detector import advanced_detect_bpm_capped

THRESHOLD = 5  # the amount for a trigger (away from curr average)
LAG = 10
INFLUENCE = 0.1  # value between [0,1]->no to full influence
PEAK_VAL = 1  # TODO: adjust peak value on hardware implementation
MODEL_PATH = './model.h5'
SAMPLING_RATE = 160
PEAK_VAL = 1
SAMPLING_SIZE = 480
MAX_BPM = 200
USE_STATIC_BPM = False


def calc_avg_bpm(arr: []):
    sum_bpm = 0
    for curr_bpm in arr:
        if curr_bpm != 0:
            sum_bpm += curr_bpm
    return sum_bpm / len(arr)


if __name__ == '__main__':
    listeners = [
        # ComListener(com_port='COM6', sampling_size=SAMPLING_SIZE, max_bpm=MAX_BPM, sampling_rate=SAMPLING_RATE),
        SimulatedListener(sampling_size=SAMPLING_SIZE, sampling_rate=SAMPLING_RATE, max_bpm=MAX_BPM)
    ]

    PROGRAM_START = time.time()

    osc_client = Client()
    model = load_model(MODEL_PATH)
        
    predicted_bpms = [0]  # Smoothing of the predicted bpm

    CURR_TIME = datetime.now()
    window_size = 4
    sampling_time_diff = 1 / SAMPLING_RATE
    bpm = 0

    while True:
        bpm = 0  # will be set to current highest bpm of all listeners
        for listener in listeners:
            # stop "overclocking"
            if listener.last_update + sampling_time_diff > time.time():
                continue
            else:
                listener.handleLostSignals()

            # stop double values
            if listener.inThreashold():
                listener.updateSequence(0)
                continue
            # get new value
            val = int(listener.read())
            val = listener.peak_detector.thresholding_algo(val)

            listener.updateSequence(val)

            adjusted_sequence = np.array([listener.sequence])

            if USE_STATIC_BPM:
                bpm = advanced_detect_bpm_capped(listener.sequence, SAMPLING_RATE, PEAK_VAL, SAMPLING_RATE * 10)
            else:
                bpm = model.predict(adjusted_sequence, verbose=0)[0][0]

            predicted_bpms.append(bpm)
            smoothed_bpm = round(calc_avg_bpm(predicted_bpms))

            if val > 0:  # print new value if peak was detected
                print(f"{PROGRAM_START - time.time()}s- Detected BPM: {bpm} and val {val}")
                print(f"Detected BPM: {smoothed_bpm}")

            if bpm > bpm: bpm = bpm  # choose biggest bpm of all listeners

            osc_client.tempoChange(bpm / 60, 4)
