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

def tone_power(samples, N, f, fs):
    I = 0.0
    Q = 0.0
    
    for n in range(N):
        angle = 2 * np.pi * f * n / fs
        I += samples[n] * np.cos(angle)
        Q += samples[n] * np.sin(angle)
    
    return I**2 + Q**2

def detect_bit(block):
    p_mark = tone_power(block, FREQ_MARK, FS)
    p_space = tone_power(block, FREQ_SPACE, FS)

    return 1 if p_mark > p_space else 0

if __name__ == "__main__":
    print("Loading WAV file...")
    fs, samples = load_wav("message.wav")
    
    if fs != FS:
        raise ValueError(f"Expected {FS} Hz, got {fs} Hz")
    
    print(f"Sample rate: {fs} Hz, Total samples: {len(samples)}")