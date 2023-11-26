import time

from listeners.microphone_listener import MicrophoneListener
from utils.peak_detection import real_time_peak_detection

THREASHOLD=5 #the amount for a trigger (away from curr average
LAG=10
INFLUENCE=0.8#value between [0,1]->no to full influence

def main():
    #Listener die benutzt werden sollen
    listeners=[MicrophoneListener()]

    #fill in lag
    lag_data=[[]]
    for i in range(LAG):
        for listener in listeners:
            lag_data[i].append(int(listener.read()))

    print("lagdata "+str(lag_data))

    #muss noch auf mehrere listener angepasst werden
    peak_detector = real_time_peak_detection(array=lag_data[0], lag=LAG, threshold=THREASHOLD, influence=2)

    while True:
        #just print some detections
        for listener in listeners:
            val=int(listener.read())
            print(f"${val} converts to ${peak_detector.thresholding_algo(val)}")
        time.sleep(.01)
main()
