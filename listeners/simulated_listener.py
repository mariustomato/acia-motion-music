import numpy as np
import time
import random

from listeners.abstract_listener import Listener


class SimulatedListener(Listener):
    def __init__(self):
        self.triggered_counter = 0
        self.triggered = False

    def read(self):
        """
        Generiert bei Aufruf der Funktion in bestimmten Zeitintervallen peakartige Werte,
        ansonsten den Wert 0.

        Returns:
            int: Der generierte Wert
        """
        # Konfiguration der Peaks
        peak_interval = 190  # Zeitintervall in ms
        peak_width = 10  # Breite der Peaks in ms
        peak_height = 100  # Höhe der Peaks


        if((time.time()*100)%peak_interval<=peak_width):
            return peak_height

        return 0
