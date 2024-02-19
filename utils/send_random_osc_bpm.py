import time
from client import Client
import numpy as np

while(True):
    osc_client = Client()
    time.sleep(2.0)
    noise = np.random.normal(0,0.2,1)
    bps = 100.0/60.0 + noise[0]
    duration = 8.0
    osc_client.tempoChange(bps, duration)
    print(f'bpm: {bps}, duration: {duration}')
    osc_client.stopAll()
