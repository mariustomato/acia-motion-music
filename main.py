import time

from listeners.com_listener import ComListener
# from listeners.simulated_listener import SimulatedListener
from utils.client import Client
from utils.plain_bpm_detector import advanced_detect_bpm_capped

# import tensorflow.python.keras as keras ##does not load

PEAK_VAL = 1
SAMPLING_SIZE = 1000
MAX_BPM = 200
SAMPLING_RATE = 100

if __name__ == '__main__':
    # TODO: change to hardware listener
    listeners = [ComListener(sampling_size=SAMPLING_SIZE, max_bpm=MAX_BPM, sampling_rate=SAMPLING_RATE)]
    PROGRAM_START = time.time()

    window_size = 4
    sampling_time_diff = 1 / SAMPLING_RATE
    osc_client = Client()
    # model = keras.models.load_model("./model.h5")
    bpm = 0

    while True:
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

            bpm = advanced_detect_bpm_capped(listener.sequence, SAMPLING_RATE, PEAK_VAL, SAMPLING_RATE * 10)

            if val > 0:
                print(f"{PROGRAM_START - time.time()}s- Detected BPM: {bpm} and val {val}")

            osc_client.tempoChange(bpm / 60, 4)

    osc_client.stopAll()
