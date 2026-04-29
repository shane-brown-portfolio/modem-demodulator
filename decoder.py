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

def tone_power(samples, f, fs):
    N = len(samples)
    n = np.arange(N)
    cos_ref = np.cos(2 * np.pi * f * n / fs)
    sin_ref = np.sin(2 * np.pi * f * n / fs)

    I = np.dot(samples, cos_ref)
    Q = np.dot(samples, sin_ref)

    return I**2 + Q**2

def detect_bit(block):
    p_mark = tone_power(block, FREQ_MARK, FS)
    p_space = tone_power(block, FREQ_SPACE, FS)

    return 1 if p_mark > p_space else 0

def extract_bits(samples):
    bits = []
    for i in range(0, len(samples), SAMPLES_PER_BIT):
        block = samples[i:i+SAMPLES_PER_BIT]
        if len(block) < SAMPLES_PER_BIT:
            break
        bits.append(detect_bit(block))
    return bits

def bits_to_bytes(bits):
    bytes_out = []
    for i in range(0, len(bits), 10):
        frame = bits[i:i+10]
        if len(frame) < 10:
            break

        start = frame[0]
        data = frame[1:9]
        stop = frame[9]

        if start != 0 or stop != 1:
            continue

        value = 0
        for i, bit in enumerate(data):
            value |= (bit << i)

        bytes_out.append(value)

    return bytes_out

def bytes_to_string(byte_list):
    return ''.join(chr(b) for b in byte_list)

if __name__ == "__main__":
    print("Loading WAV file...")
    fs, samples = load_wav("test2.wav")
    
    if fs != FS:
        raise ValueError(f"Expected {FS} Hz, got {fs} Hz")
    
    print(f"Sample rate: {fs} Hz, Total samples: {len(samples)}")

    bits = extract_bits(samples)
    
    # Then convert bits to bytes and then to string for full message decoding
    data = bits_to_bytes(bits)
    text = bytes_to_string(data)
    print(text)