import inspect
import time
from abc import ABC

import numpy as np

from utils.peak_detection import real_time_peak_detection

THRESHOLD = 5  # the amount for a trigger (away from curr average)
LAG = 10
INFLUENCE = 0.8  # value between [0,1]->no to full influence


class Listener(ABC):
    last_update = time.time()

    def __init__(self, sampling_size=1000, max_bpm=200, sampling_rate=100):
        self.sequence = np.full(sampling_size, 0)
        self.max_bpm = max_bpm
        self.sampling_rate = sampling_rate
        self.sampling_time_diff = 1 / sampling_rate
        self._initalizePeakDetector()

    def read(self):
        NotImplementedError()

    def updateSequence(self, val):
        self.handleLostSignals()
        self.sequence[:-1] = self.sequence[1:]
        self.sequence[-1] = val

    def handleLostSignals(self):
        lost_signals = int((time.time() - self.last_update) / self.sampling_time_diff) - 1
        if lost_signals > 0:
            # Shift the existing data to the end of the array, only if there are more than zero lost signals
            self.sequence[lost_signals:] = self.sequence[:-lost_signals]
            # Fill the start of the array with zeros
            self.sequence[:lost_signals] = 0
            self.last_update = time.time()

    def inThreashold(self):
        if 1 in self.sequence[-int(self.sampling_rate / (1 * (self.max_bpm / 60))):]:
            x = self.sequence[-int(self.sampling_rate / (1 * (self.max_bpm / 60))):]
            self.sequence[:-1] = self.sequence[1:]
            self.sequence[-1] = 0
            self.last_update = time.time()
            print("in threash")
            return True
        return False

    def _initalizePeakDetector(self):
        if inspect.isabstract(self):
            NotImplementedError("Cannot use abstract class")

        lag_data = []
        for _ in range(LAG):
            lag_data.append(int(self.read()))

        self.peak_detector = real_time_peak_detection(array=lag_data, lag=LAG, threshold=THRESHOLD, influence=2)
