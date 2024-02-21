import time
from datetime import datetime

import numpy as np
from keras.models import load_model
from serial import SerialException

from listeners.com_listener import ComListener
from utils.client import Client
from utils.plain_bpm_detector import advanced_detect_bpm_capped

PEAK_VAL = 1  # TODO: adjust peak value on hardware implementation
MODEL_PATH = './model.h5'
SAMPLING_RATE = 160
PEAK_VAL = 1
MAX_BPM = 200
USE_STATIC_BPM = True
SAMPLING_SIZE = 480 if not USE_STATIC_BPM else 800


def calc_avg_bpm(arr: []):
    sum_bpm = 0

    for curr_bpm in arr:
        if curr_bpm != 0:
            sum_bpm += curr_bpm
    return sum_bpm / len(arr)


if __name__ == '__main__':
    listeners = [
        ComListener(com_port='COM6', sampling_size=SAMPLING_SIZE, max_bpm=MAX_BPM, sampling_rate=SAMPLING_RATE),
        # SimulatedListener(sampling_size=SAMPLING_SIZE, sampling_rate=SAMPLING_RATE, max_bpm=MAX_BPM)
    ]

    PROGRAM_START = time.time()

    osc_client = Client()
    if not USE_STATIC_BPM:
        model = load_model(MODEL_PATH)

    predicted_bpms = [0] * int(SAMPLING_SIZE / 2)  # Smoothing of the predicted bpm

    CURR_TIME = datetime.now()
    window_size = 4
    sampling_time_diff = 1 / SAMPLING_RATE
    bpm = 0

    while True:
        for listener in listeners:
            # stop "overclocking"
            if listener.last_update + sampling_time_diff > time.time():
                continue
            else:
                listener.handleLostSignals()

            # stop double values
            if listener.inThreashold(bpm):
                listener.updateSequence(0)
                continue
            # get new value
            try:
                val = int(listener.read())
            except (ValueError, SerialException) as e:
                print(f"Notice: {e}")
                continue

            val = listener.peak_detector.thresholding_algo(val)

            listener.updateSequence(val)

            if USE_STATIC_BPM:
                bpm = advanced_detect_bpm_capped(listener.sequence, SAMPLING_RATE, PEAK_VAL, SAMPLING_SIZE)
            else:
                bpm = model.predict(np.array([listener.sequence]), verbose=0)[0][0]

            predicted_bpms.append(bpm)
            predicted_bpms.pop(0)
            smoothed_bpm = round(calc_avg_bpm(predicted_bpms))

            if val > 0:  # print new value if peak was detected
                print(f"{time.time() - PROGRAM_START :3.5f}s\tDetected BPM: {smoothed_bpm:3.1f}\t(raw: {bpm:3.1f})")

            if bpm > bpm: bpm = bpm  # choose biggest bpm of all listeners

            osc_client.tempoChange(smoothed_bpm / 60, 4)
