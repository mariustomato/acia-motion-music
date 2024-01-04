def basic_detect_bpm(sequence, sampling_rate):
    timespan = len(sequence) / sampling_rate
    return sum(1 for elem in sequence if elem == 1) / timespan * 60


def advanced_detect_bpm(sequence, sampling_rate, peak_val):
    if len(sequence) == 0:
        return 0
    # bps
    timespan = len(sequence) / sampling_rate
    # bps prediction to bpm
    return sum(1 for elem in sequence if elem >= peak_val) / timespan * 60


def advanced_detect_bpm_capped(sequence, sampling_rate, peak_val, cap):
    if len(sequence) == 0:
        return 0
    # bps
    if len(sequence) > 1.5 * cap:
        cut_sequence = sequence[len(sequence) - cap:]
    else:
        cut_sequence = sequence
    # print(cut_sequence)
    timespan = len(cut_sequence) / sampling_rate
    # bps prediction to bpm
    return sum(1 for elem in cut_sequence if elem >= peak_val) / timespan * 60
