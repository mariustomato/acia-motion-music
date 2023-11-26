import numpy as np
import pyaudio

from listeners.abstract_listener import Listener


class MicrophoneListener(Listener):
    # Constants
    FORMAT = pyaudio.paInt16  # Audio format (16-bit PCM)
    CHANNELS = 1              # Single channel for microphone
    RATE = 44100              # Sampling rate
    CHUNK = 1024              # Number of frames per buffer
    MAX_AMPLITUDE = 2**(16 - 1)  # Maximum amplitude for 16-bit audio

    def __init__(self):
        self.audio = pyaudio.PyAudio()

    def read(self):
        self.stream = self.audio.open(format=self.FORMAT,
                                      channels=self.CHANNELS,
                                      rate=self.RATE,
                                      input=True,
                                      frames_per_buffer=self.CHUNK)

        data=self.stream.read(self.CHUNK)
        _data=np.frombuffer(b''.join([data]), dtype=np.int16)
        _data= 20 * np.log10(np.abs(_data) / self.MAX_AMPLITUDE)
        return _data

    def __del__(self):
        # Stop and close the stream
        self.stream.stop_stream()
        self.stream.close()
        self.audio.terminate()
