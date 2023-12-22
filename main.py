from datetime import datetime
import time
from listeners.simulated_listener import SimulatedListener
from utils.peak_detection import real_time_peak_detection
from utils.plain_bpm_detector import advanced_detect_bpm
from utils.plain_bpm_detector import advanced_detect_bpm_capped
from utils.client import Client

THRESHOLD = 5  # the amount for a trigger (away from curr average
LAG = 10
INFLUENCE = 0.1  # value between [0,1]->no to full influence
PEAK_VAL = 80  # TODO: adjust peak value on hardware implementation

if __name__ == '__main__':
    # TODO: change to hardware listener
    listeners = [SimulatedListener()]

    # fill in lag
    lag_data = []
    for _ in range(LAG):
        lag_data.append(int(listeners[0].read()))

    peak_detector = real_time_peak_detection(array=lag_data, lag=LAG, threshold=THRESHOLD, influence=2)

    sequence = []
    # TODO: adjust window size on hardware implementation
    window_size = 4
    # TODO: adjust sampling rate on hardware implementation
    sampling_rate = 100
    osc_client = Client()

    while True:
        for listener in listeners:
            # TODO: add peak detection
            val = int(listener.read())
            # currently capping sequence length at 60 seconds
            if len(sequence) == sampling_rate * 60:
                sequence = sequence[1:]
            sequence.append(val)
            bpm = advanced_detect_bpm_capped(sequence, sampling_rate, PEAK_VAL, sampling_rate * 10)

            print(f"Detected BPM: {bpm}")

            clock = datetime.now()
            # osc_client.tempoChange(clock, bpm, 8)

            time.sleep(1 / sampling_rate)
