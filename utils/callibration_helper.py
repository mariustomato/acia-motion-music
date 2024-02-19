from listeners.abstract_listener import Listener
from listeners.com_listener import ComListener
from listeners.simulated_listener import SimulatedListener
from utils.peak_detection import real_time_peak_detection
import matplotlib.pyplot as plt
from IPython.display import display, clear_output
import time
import numpy as np




class CallibrationHelper:
    listener:Listener=None
    THREASHOLD = 1  # the amount for a trigger (away from curr average
    LAG = 100
    INFLUENCE = 0.8  # value between [0,1]->no to full influence
    peak_detector=None



    def __init__(self,listener:Listener):
        self.listener=listener
        self.initializePeakDetector()

    def initializePeakDetector(self):
        lag_data=[]
        for i in range(self.LAG):
            lag_data.append(int(self.listener.read()))
            print(lag_data[-1])
        self.peak_detector = real_time_peak_detection(array=lag_data, lag=self.LAG, threshold=self.THREASHOLD, influence=2)

    def get_current_data(self):
        val = int(self.listener.read())
        return [val,self.peak_detector.thresholding_algo(val)]


    def startGraph(self):
        values1 = []
        values2 = []

        DELTA=0.0001 #in seconds
        DISPLAYSEONDS=5 # in seconds


        # Set up the plot
        plt.ion()  # Turn on interactive mode
        fig, ax1 = plt.subplots()

        ax2 = ax1.twinx()  # Create a second y-axis that shares the same x-axis

        line1, = ax1.plot(values1, 'g-', label='Value 1')  # Initial empty plot for Value 1 (green line)
        line2, = ax2.plot(values2, 'b-', label='Value 2')  # Initial empty plot for Value 2 (blue line)

        # Set the y-axis scale for value2
        ax2.set_ylim(-1.1, 1.1)  # This sets the y-axis to be slightly larger than the 0-1 range

        # Set titles and labels
        ax1.set_title('Real-time graph with Dual Axes')
        ax1.set_xlabel('Sample Number')
        ax1.set_ylabel('Value 1', color='g')
        ax2.set_ylabel('Value 2', color='b')

        # Create legends for both lines
        ax1.legend(loc='upper left')
        ax2.legend(loc='upper right')

        start=time.time()

        while True:  # Or replace '50' with 'True' for an infinite loop
            # Fetch new data
            val1, val2 = self.get_current_data()

            # Append data to lists
            values1.append(val1)
            values2.append(val2)

            if (start+DISPLAYSEONDS<time.time()):
               values1.pop(0)
               values2.pop(0)

            # Update data of both lines
            line1.set_data(range(len(values1)), values1)
            line2.set_data(range(len(values2)), values2)

            # Adjust x-axis limits dynamically to accommodate more data points
            ax1.set_xlim(0, len(values1))

            # Automatically adjust Value 1's y-axis
            ax1.relim()
            ax1.autoscale_view()

            # Since Value 2 has fixed y-axis limits, we skip the relim and autoscale

            # Refresh the plot
            fig.canvas.draw()
            fig.canvas.flush_events()
            time.sleep(DELTA)  # Adjust the sleep time as per your need for updates

        # Disable interactive mode to prevent further updates
        plt.ioff()
        plt.show()

calli=CallibrationHelper(ComListener())
calli.startGraph()

