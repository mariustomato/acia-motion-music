import time

from pythonosc import udp_client


class Client:
    last_update = time.time()

    def __init__(self):
        self.ip = "127.0.0.1"
        self.port = 57120
        self.client = udp_client.SimpleUDPClient(self.ip, self.port)

    def tempoChange(self, bpm, number_beats=8):
        if self.last_update + 3 > time.time(): return
        self.last_update = time.time()
        if bpm < 0: bpm = 0
        self.client.send_message("/tempoChange", [bpm, number_beats])

    def stopAll(self):
        self.client.send_message("/stopAll", [])

    def startAll(self):
        self.client.send_message("/")
