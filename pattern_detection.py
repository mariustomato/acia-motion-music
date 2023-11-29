from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler


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

    kmeans = KMeans(n_clusters=n_clusters, random_state=0).fit(windows_scaled)
    return kmeans.labels_



# sequence = []
# new_data = [0, 1, 1, 0, 0, 1, 1, 1, 0, 0, 1, 0, 1, 0, 1, 0]
#
# for data_point in new_data:
#    sequence.append(data_point)
#    labels = analyze_sequence(sequence, window_size=4, n_clusters=2)
#    if labels is not None:
#        print(labels)
