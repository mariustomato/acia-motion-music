from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
import numpy as np


def sliding_window(sequence, window_size):
    return [sequence[i:i+window_size] for i in range(len(sequence) - window_size + 1)]


def analyze_sequence(sequence, window_size, n_clusters):
    if len(sequence) < window_size:
        return None

    windows = sliding_window(sequence, window_size)

    if len(windows) < n_clusters:
        return None

    scaler = StandardScaler()
    windows_scaled = scaler.fit_transform(windows)

    kmeans = KMeans(n_clusters=n_clusters, random_state=0, n_init='auto').fit(windows_scaled)
    return kmeans.labels_


def calculate_bpm(labels, window_size, sampling_rate):
    # Find the most common cluster
    most_common_cluster = np.bincount(labels).argmax()
    print(f"Most common cluster {most_common_cluster}")

    # Calculate the timestamps for each occurrence of the most common cluster
    timestamps = [i * (window_size / sampling_rate) for i, label in enumerate(labels) if label == most_common_cluster]
    print(f"Timestamps {timestamps}")

    # Calculate the average time interval between these timestamps
    if len(timestamps) > 1:
        average_interval = np.mean(np.diff(timestamps))
        print(f"Average interval {average_interval}")

        # Convert to BPM
        bpm = 60 / average_interval
        return bpm
    else:
        return None



# sequence = []
# new_data = [0, 1, 1, 0, 0, 1, 1, 1, 0, 0, 1, 0, 1, 0, 1, 0]
#
# for data_point in new_data:
#    sequence.append(data_point)
#    labels = analyze_sequence(sequence, window_size=4, n_clusters=2)
#    if labels is not None:
#        print(labels)
