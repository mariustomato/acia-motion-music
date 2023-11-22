from pythonosc import udp_client

ip = "127.0.0.1"
port = 57120  # Default SuperCollider OSC port
client = udp_client.SimpleUDPClient(ip, port)


# Function to change frequency
def change_frequency(new_freq):
    client.send_message("/changeFreq", [new_freq])


# Example usage
change_frequency(440)  # Change frequency to 440 Hz
