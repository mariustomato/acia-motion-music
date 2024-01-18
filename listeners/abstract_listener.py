import time
from abc import ABC

import numpy as np


class Listener(ABC):
    last_update = time.time()
    sequence=np.array()

    def red(self,sampling_size=1000, max_bpm=200, sampling_rate=100):
        self.sequence= np.full(sampling_size, 0)
        self.max_bpm=max_bpm
        self.sampling_rate=sampling_rate

    def updateSequence(self,val):
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
        if 1 in self.sequence[-int(self.sampling_rate / (2 * (self.MAX_BPM / 60))):]:
                self.sequence[:-1] = self.sequence[1:]
                self.sequence[-1] = 0
                self.last_update = time.time()
                return False
        return True
    