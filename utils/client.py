import time

from pythonosc import udp_client


class Client:
    last_update = time.time() - 4

    def __init__(self):
        self.ip = "127.0.0.1"
        self.port = 57120
        self.client = udp_client.SimpleUDPClient(self.ip, self.port)

    def tempoChange(self, bpm, duration=4):
        if self.last_update + duration > time.time(): return
        self.last_update = time.time()
        if bpm < 0: bpm = 0
        self.client.send_message("/tempoChange", [bpm, duration])

    def stopAll(self):
        self.client.send_message("/pdef_control", ["stop"])

    def startAll(self):
        self.client.send_message("/pdef_control", ["start"])
