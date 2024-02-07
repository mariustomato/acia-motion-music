# Importing Libraries
import serial

from listeners.abstract_listener import Listener


class ComListener(Listener):
    def __init__(self, com_port='COM6', sampling_size=1000, max_bpm=200, sampling_rate=100):
        self.com = serial.Serial(port=com_port, baudrate=9600, timeout=.1, write_timeout=0)
        super().__init__(sampling_size, max_bpm, sampling_rate)

    def read(self):
        self.com.flush()
        # self.com.write(bytes("TRIG:IMM", 'utf-8'))
        data = ""
        while (data == ""):
            data = self.com.readline()
        return data.decode().replace("\r\n", "")
