# Python script to trigger SuperCollider Synth

from pythonosc import udp_client
from time import sleep

# Set the SuperCollider server address and port
sc_address = "127.0.0.1"
sc_port = 57120

# Create an OSC client
client = udp_client.SimpleUDPClient(sc_address, sc_port)

# Function to trigger the SuperCollider Synth
def trigger_synth(freq, amp):
    # Send an OSC message to start the Synth
    client.send_message("/s_new", ["sineSynth", 1000, 1, 0, "freq", freq, "amp", amp])

    # Wait for a moment (you can adjust the duration as needed)
    sleep(2.0)

    # Send an OSC message to free the Synth (stop it)
    client.send_message("/n_free", [1000])

# Example usage
trigger_synth(freq=523.25, amp=0.7)