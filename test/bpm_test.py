import numpy as np
from utils.plain_bpm_detector import basic_detect_bpm

def generate_test_sequence(peak_height, sampling_rate, duration, peak_every_x_points):
    sequence = []
    for i in range(duration * sampling_rate):
        if i % peak_every_x_points == 0:
            sequence.append(peak_height)
        else:
            sequence.append(0)
    return sequence

def main():
    sampling_rate = 100  # 50 data points per second
    peak_every_x_points = 5
    peak_height = 1
    duration = 10  # seconds
    window_size = 4

    test_sequence = generate_test_sequence(peak_height, sampling_rate, duration, peak_every_x_points)
    bpm = basic_detect_bpm(test_sequence, sampling_rate)
    print(f"Detected BPM: {bpm}")


main()
