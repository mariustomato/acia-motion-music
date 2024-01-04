from pythonosc import udp_client


class Client:
    def __init__(self):
        self.ip = "127.0.0.1"
        self.port = 57120
        self.client = udp_client.SimpleUDPClient(self.ip, self.port)

    def tempoChange(self, clock, bpm, number):
        self.client.send_message("/tempoChange", [clock, bpm, number])
