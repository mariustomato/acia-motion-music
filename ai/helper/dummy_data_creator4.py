import random
import json
import os


def create_training_data(data_amount: int, base_path: str) -> []:
    data = []
    curr_base_bpm = 7
    total_bpms = 200 - curr_base_bpm  # max possible bpm (200) - min possible bpm (7)
    sequence_size = 1600  # 10 seconds * 160 entries per second
    if data_amount < total_bpms:
        print(f"Raised data amount to {total_bpms} as this is the minimum amount of data needed to cover all possible BPMs")
        data_amount = total_bpms
    loops = round(data_amount / total_bpms)  # loops on same bpm
    counter = 0
    while counter < data_amount:
        for i in range(loops):
            data_entry = random_bpm_sequence(curr_base_bpm, sequence_size)
            calculated_bpm = get_bpm(data_entry)
            cutted_entry = data_entry[:1600]
            random_slice = random.randint(0, len(cutted_entry) - 1)
            new_start = cutted_entry[random_slice:]
            new_end = cutted_entry[:random_slice]
            data.append({'data': new_start + new_end, 'nextBPM': calculated_bpm})
            if len(data) == data_amount:
                break
        counter += loops
        curr_base_bpm += 1
    random.shuffle(data)
    save_data(data, base_path)
    return data


def save_data(data: [], base_path: str) -> None:
    if base_path is None:
        return
    data_dir = base_path + '/data'

    if not os.path.exists(data_dir):
        os.makedirs(data_dir)

    with open(data_dir + '/plain_data.json', 'w') as file:
        json.dump(data, file)

    return data


def random_bpm_sequence(curr_bpm: int, sequence_size: int) -> []:
    bpm_sequence = []
    base_sec = 160  # 160 entries per second
    max_var = 16  # max 100ms variance per "beat"
    peak_indices = get_peak_indices(sequence_size, base_sec, max_var, curr_bpm)
    if len(peak_indices) > curr_bpm:
        x = 1
    for i in range(sequence_size):
        if i in peak_indices:
            bpm_sequence.append(1)
        else:
            bpm_sequence.append(0)
    return bpm_sequence


def get_peak_indices(sequence_size: int, base_sec: int, max_var: int, curr_bpm: int) -> []:
    peaks = []
    entries_between_beats = base_sec / (curr_bpm / 60)
    for i in range(sequence_size):
        index = round(i * entries_between_beats)
        if index >= sequence_size:
            return peaks
        variance = random.randint(0, max_var*2) - max_var  # +/- 100ms
        peaks.append(abs(index + variance))
    return peaks


def get_bpm(sequence):
    spikes = sum(1 for point in sequence if point == 1)
    timespan = len(sequence) / 160
    return spikes / timespan * 60