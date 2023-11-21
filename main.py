import time

from utils.com_listener import read_com
from utils.peak_detection import real_time_peak_detection

THREASHOLD=5 #the amount for a trigger (away from curr average
LAG=10
INFLUENCE=0.1#value between [0,1]->no to full influence

def main():
    #provides {-1,0;1} for determining a peak
    peak_detector=real_time_peak_detection(array=[],lag=LAG,threshold=THREASHOLD,influence=2)

    #fill in lag
    for i in range(10):
        peak_detector.thresholding_algo(read_com())

    while True:
        #just print some detections
        print(peak_detector.thresholding_algo(read_com()))
        time.sleep(0.1)
