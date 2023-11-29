import time
from utils.com_listener import read_com
from utils.peak_detection import real_time_peak_detection
from pattern_detection import analyze_sequence

THREASHOLD = 5 # the amount for a trigger (away from curr average
LAG = 10
INFLUENCE = 0.1 # value between [0,1]->no to full influence

def main():
    # provides {-1,0;1} for determining a peak

    # fill in lag
    lag_data = []
    for i in range(LAG):
        lag_data.append(int(read_com()))

    print("lagdata "+str(lag_data))

    peak_detector = real_time_peak_detection(array=lag_data, lag=LAG, threshold=THREASHOLD, influence=2)
    sequence = []

    while True:
        # just print some detections
        val=int(read_com())
        # print(f"${val} converts to ${peak_detector.thresholding_algo(val)}")
        sequence.append(val)
        labels = analyze_sequence(sequence, window_size=4, n_clusters=2)
        if labels is not None:
            print(labels)
        time.sleep(.5)
        # print(read_com())
main()