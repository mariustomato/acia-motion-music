import time
import numpy as np

from datetime import datetime
from listeners.simulated_listener import SimulatedListener
from utils.peak_detection import real_time_peak_detection
from utils.client import Client
from keras.models import load_model

THRESHOLD = 5  # the amount for a trigger (away from curr average)
LAG = 10
INFLUENCE = 0.1  # value between [0,1]->no to full influence
PEAK_VAL = 1  # TODO: adjust peak value on hardware implementation
MODEL_PATH = './model.keras'
SAMPLING_RATE = 160


def calc_avg_bpm(arr: []):
    sum_bpm = 0
    for curr_bpm in arr:
        if curr_bpm != 0:
            sum_bpm += curr_bpm
    return sum_bpm / len(arr)


if __name__ == '__main__':
    # TODO: change to hardware listener
    listeners = [SimulatedListener()]

    # fill in lag
    lag_data = []
    for _ in range(LAG):
        lag_data.append(int(listeners[0].read()))

    peak_detector = real_time_peak_detection(array=lag_data, lag=LAG, threshold=THRESHOLD, influence=2)

    sequence_length = 480
    sequence = [0] * sequence_length  # Array containing the data for the model to predict on

    osc_client = Client()
    model = load_model(MODEL_PATH)
    predicted_bpms = [0]  # Smoothing of the predicted bpm

    CURR_TIME = datetime.now()

    while True:
        for listener in listeners:
            val = peak_detector.thresholding_algo(int(listener.read()))
            if len(sequence) >= sequence_length:
                sequence = sequence[1:]
            sequence.append(val)
            adjusted_sequence = np.array([sequence])
            bpm = model.predict(adjusted_sequence, verbose=0)[0][0]

            if len(predicted_bpms) >= 320:  # Window for the bpm smoothing is set to 2 second (160 data points * 2 seconds)
                predicted_bpms = predicted_bpms[1:]
            predicted_bpms.append(bpm)
            smoothed_bpm = calc_avg_bpm(predicted_bpms)

            # print(f"Detected BPM: {round(smoothed_bpm)}")

            clock = datetime.now()
            osc_client.tempo_change(clock, round(smoothed_bpm / 60), 8)

            time.sleep(1 / SAMPLING_RATE)
