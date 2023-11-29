import pyaudio
import numpy as np
import matplotlib.pyplot as plt

# Constants
FORMAT = pyaudio.paInt16  # Audio format (16-bit PCM)
CHANNELS = 1              # Single channel for microphone
RATE = 44100              # Sampling rate
CHUNK = 1024              # Number of frames per buffer
RECORD_SECONDS = 3        # Duration of recording
MAX_AMPLITUDE = 2**(16 - 1)  # Maximum amplitude for 16-bit audio

# Initialize PyAudio
audio = pyaudio.PyAudio()

# Open stream
stream = audio.open(format=FORMAT, channels=CHANNELS,
                    rate=RATE, input=True,
                    frames_per_buffer=CHUNK)

print("Recording...")

# Record for a few seconds
frames = []
for _ in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
    data = stream.read(CHUNK)
    frames.append(data)

print("Finished recording.")

# Stop and close the stream
stream.stop_stream()
stream.close()
audio.terminate()

# Concatenate all the frames and convert to byte array
byte_array = np.frombuffer(b''.join(frames), dtype=np.int16)

# Convert to dBm
dbm_values = 20 * np.log10(np.abs(byte_array) / MAX_AMPLITUDE)

# Time values for x-axis
time_values = np.linspace(0, RECORD_SECONDS, len(dbm_values))

# Plotting
plt.figure(figsize=(10, 4))
plt.plot(time_values, dbm_values)
plt.title("dBm Values Over Time")
plt.xlabel("Time (seconds)")
plt.ylabel("dBm")
plt.grid(True)
plt.show()