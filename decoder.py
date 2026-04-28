import wave
import numpy as np

FS = 48000
BIT_RATE = 300
SAMPLES_PER_BIT = 160
FREQ_SPACE = 2025
FREQ_MARK = 2225

def load_wav(path: str):
    with wave.open(path, 'rb') as wf:
        if wf.getnchannels() != 1:
            raise ValueError("Only mono audio supported")
        
        fs = wf.getframerate()
        frames = wf.readframes(wf.getnframes())

        samples = np.frombuffer(frames, dtype=np.int16)
        samples = samples.astype(np.float32) / 32768.0

    return fs, samples

if __name__ == "__main__":
    print("Loading WAV file...")
    fs, samples = load_wav("message.wav")
    
    if fs != FS:
        raise ValueError(f"Expected {FS} Hz, got {fs} Hz")
    
    print(f"Sample rate: {fs} Hz, Total samples: {len(samples)}")