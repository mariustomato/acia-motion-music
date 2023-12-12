import time

from listeners.simulated_listener import SimulatedListener
from utils.peak_detection import real_time_peak_detection
from plain_bpm_detector import advanced_detect_bpm
from plain_bpm_detector import advanced_detect_bpm_capped
# from pattern_detection import analyze_sequence, calculate_bpm


THREASHOLD = 5  # the amount for a trigger (away from curr average
LAG = 10
INFLUENCE = 0.1  # value between [0,1]->no to full influence

def main():
    # Listener die benutzt werden sollen
    listeners = [SimulatedListener()]

    # fill in lag
    lag_data = []
    for i in range(LAG):
        lag_data.append(int(listeners[0].read()))

    # print("lagdata "+str(lag_data))

    peak_detector = real_time_peak_detection(array=lag_data, lag=LAG, threshold=THREASHOLD, influence=2)
    sequence = []
    window_size = 4
    # aka how many datapoint per second
    sampling_rate = 100
    iteration = 0
    # get current time
    start_time = time.time()

    while True:
        for listener in listeners:
            if time.time() - start_time > 60:
                val = int(listener.read_2())
            else:
                val = int(listener.read())
            if len(sequence) == sampling_rate * 60:
                sequence = sequence[1:]
            sequence.append(val)
            # bpm = advanced_detect_bpm(sequence, sampling_rate, 80)
            bpm = advanced_detect_bpm_capped(sequence, sampling_rate, 80, sampling_rate * 10)
            # print(f"Sequence: {sequence}")
            print(f"Detected BPM: {bpm}")
            time.sleep(1/sampling_rate)
        # just print some detections
        #iteration += 1
        #for listener in listeners:
        #    val = int(listener.read())
        #    # print(f"${val} converts to ${peak_detector.thresholding_algo(val)}")
        #    sequence.append(val)
        #    labels = analyze_sequence(sequence, window_size, n_clusters=1)
        #    if labels is not None:
        #        print(labels)
        #        bpm = calculate_bpm(labels, window_size, sampling_rate)
        #        if bpm is not None:
        #           print(f"(I{iteration}) Estimated BPM: {bpm}")
        #        else:
        #           print("Not enough data to estimate BPM.")
        #time.sleep(1/sampling_rate)
        #print(read_com())


main()
