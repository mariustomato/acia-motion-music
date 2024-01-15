import time
import numpy as np
from listeners.com_listener import ComListener
#import tensorflow.python.keras as keras ##does not load
import keras ##loads
from utils.peak_detection import real_time_peak_detection
from utils.client import Client

THRESHOLD = 5  # the amount for a trigger (away from curr average
LAG = 10
INFLUENCE = 0.8  # value between [0,1]->no to full influence
PEAK_VAL = 1  # TODO: adjust peak value on hardware implementation

if __name__ == '__main__':
    # TODO: change to hardware listener
    listeners = [ComListener()]

    # fill in lag
    lag_data = []
    for _ in range(LAG):
        lag_data.append(int(listeners[0].read()))

    sampling_size = 1000
    sequence = np.full((sampling_size, 2), 0)
    peak_detector = real_time_peak_detection(array=lag_data, lag=LAG, threshold=THRESHOLD, influence=2)

    # TODO: adjust window size on hardware implementation
    window_size = 4
    # TODO: adjust sampling rate on hardware implementation
    sampling_rate = 160
    osc_client = Client()
    last_update = time.time()
    model = keras.models.load_model("./model.h5")
    bpm=0

    while True:
        for listener in listeners:

            val = int(listener.read())
            val = peak_detector.thresholding_algo(val)

            sequence[:-1] = sequence[1:]
            sequence[-1]=np.array([val, bpm])
            print(sequence[-1])
            bpm = model.predict(sequence)

            #bpm = model. # advanced_detect_bpm_capped(sequence, sampling_rate, PEAK_VAL, sampling_rate * 10)

            if val > 0:
                print(f"Detected BPM: {bpm} and val {val}")

            osc_client.tempoChange(bpm / 60, 4)

    osc_client.stopAll()
