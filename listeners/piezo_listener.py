# piezo using nono every


# Importing Libraries
import serial

from listeners.abstract_listener import Listener


class PiezoListener(Listener):
    def __init__(self):
        self.com = serial.Serial(port='COM6', baudrate=9600, timeout=.1, write_timeout=0)

    def read(self):
        data = ""
        while data == "" or data==b'':
            self.com.flush()
            self.com.write(bytes("TRIG:IMM", 'utf-8'))

            data = self.com.readline()

        return data.decode().replace("\r\n", "")
