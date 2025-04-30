import sounddevice as sd
import numpy as np

def play_audio(audio_array, sample_rate=24000):
    """Play a numpy array audio using sounddevice."""
    if isinstance(audio_array, np.ndarray):
        sd.play(audio_array, samplerate=sample_rate)
        sd.wait()  # Wait until playback is finished
    else:
        raise ValueError("Audio must be a numpy array")
