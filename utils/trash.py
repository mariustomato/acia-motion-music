import random
from time import sleep

import client


if __name__ == '__main__':
    bpm = 0
    while True:
        bpm = random.randint(60, 180)
        client.Client().tempo_change(0, bpm, 4)
        sleep(5)
        print('BPM:', bpm)