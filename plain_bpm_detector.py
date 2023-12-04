def basic_detect_bpm(sequence, sampling_rate):
    timespan = len(sequence) / sampling_rate
    return sum(1 for elem in sequence if elem == 1) / timespan * 60


def advanced_detect_bpm(sequence, sampling_rate, peak_val):
    if len(sequence) == 0:
        return 0
    timespan = len(sequence) / sampling_rate
    return sum(1 for elem in sequence if elem >= peak_val) / timespan * 60
