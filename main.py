import time

# import tensorflow.python.keras as keras ##does not load
import numpy as np

from listeners.com_listener import ComListener
# from listeners.simulated_listener import SimulatedListener
from utils.client import Client
from utils.peak_detection import real_time_peak_detection
from utils.plain_bpm_detector import advanced_detect_bpm_capped

THRESHOLD = 5  # the amount for a trigger (away from curr average)
LAG = 10
INFLUENCE = 0.8  # value between [0,1]->no to full influence
PEAK_VAL = 1  # TODO: adjust peak value on hardware implementation
SAMPLING_SIZE = 1000
MAX_BPM= 200
SAMPLING_RATE = 100 

if __name__ == '__main__':
    # TODO: change to hardware listener
    listeners = [ComListener(sampling_size=SAMPLING_SIZE, max_bpm=MAX_BPM, sampling_rate=SAMPLING_RATE)]
    PROGRAM_START = time.time()

    # fill in lag
    lag_data = []
    for _ in range(LAG):
        lag_data.append(int(listeners[0].read()))

    
    
    peak_detector = real_time_peak_detection(array=lag_data, lag=LAG, threshold=THRESHOLD, influence=2)


    window_size = 4
    sampling_time_diff = 1 / sampling_rate
    osc_client = Client()
    # model = keras.models.load_model("./model.h5")
    bpm = 0

    while True:
        for listener in listeners:
            # stop "overclocking"
            if listener.last_update + sampling_time_diff > time.time():
                continue
            else:
                listener.handleLostSignals

            # stop double values
            if listener.inThreashold():
                listener.updateSequence(0)
                continue
            
            # get new value
            val = int(listener.read())
            val = peak_detector.thresholding_algo(val)

            listener.updateSequence(val)

            bpm = advanced_detect_bpm_capped(listener.sequence, sampling_rate, PEAK_VAL, sampling_rate * 10)

            if val > 0:
                print(f"{PROGRAM_START - time.time()}s- Detected BPM: {bpm} and val {val}")

            osc_client.tempoChange(bpm / 60, 4)

    osc_client.stopAll()
