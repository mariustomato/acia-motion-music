from pythonosc import udp_client


class Client:
    def __init__(self):
        self.ip = "129.187.5.1"
        # self.ip = "10.156.33.53"
        self.port = 57120
        self.client = udp_client.SimpleUDPClient(self.ip, self.port)

    def tempo_change(self, clock, bpm, number):
        self.client.send_message("/tempoChange", [clock, bpm, number])
