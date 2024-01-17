import time

# import tensorflow.python.keras as keras ##does not load
import numpy as np

from listeners.simulated_listener import SimulatedListener
from utils.client import Client
from utils.peak_detection import real_time_peak_detection
from utils.plain_bpm_detector import advanced_detect_bpm_capped

THRESHOLD = 5  # the amount for a trigger (away from curr average
LAG = 10
INFLUENCE = 0.8  # value between [0,1]->no to full influence
PEAK_VAL = 1  # TODO: adjust peak value on hardware implementation

if __name__ == '__main__':
    # TODO: change to hardware listener
    listeners = [SimulatedListener()]

    # fill in lag
    lag_data = []
    for _ in range(LAG):
        lag_data.append(int(listeners[0].read()))

    sampling_size = 1000
    sequence = np.full(sampling_size, 0)
    peak_detector = real_time_peak_detection(array=lag_data, lag=LAG, threshold=THRESHOLD, influence=2)

    # TODO: adjust window size on hardware implementation
    window_size = 4
    # TODO: adjust sampling rate on hardware implementation
    sampling_rate = 100  # per second
    sampling_time_diff = 1 / sampling_rate
    osc_client = Client()
    last_update = time.time()
    # model = keras.models.load_model("./model.h5")
    bpm = 0

    while True:
        for listener in listeners:
            # check if its time for an update
            if listener.last_update + sampling_time_diff > time.time():
                print("skip")
                continue

            # filling up the lost datapoints
            lost_signals = int((time.time() - listener.last_update) / sampling_time_diff) - 1
            if lost_signals > 0:
                # Shift the existing data to the end of the array, only if there are more than zero lost signals
                sequence[lost_signals:] = sequence[:-lost_signals]
                # Fill the start of the array with zeros
                sequence[:lost_signals] = 0
                listener.last_update = time.time()

            # get new value
            val = int(listener.read())
            val = peak_detector.thresholding_algo(val)

            print(f"Lost singlas {lost_signals} with len of {len(sequence)}")

            sequence[:-1] = sequence[1:]
            sequence[-1] = val
            print(sequence[-1])
            # bpm = model.predict(sequence)

            bpm = advanced_detect_bpm_capped(sequence, sampling_rate, PEAK_VAL, sampling_rate * 10)

            if val > 0:
                print(f"Detected BPM: {bpm} and val {val}")

            osc_client.tempoChange(bpm / 60, 4)

    osc_client.stopAll()
