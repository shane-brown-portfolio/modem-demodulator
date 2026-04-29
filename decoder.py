import wave
import numpy as np
import argparse

FS = 48000                  # Expected sample rate (Hz)
BIT_RATE = 300              # Bits per second
SAMPLES_PER_BIT = 160       # Number of samples per bit at 48 kHz and 300 bps
FREQ_SPACE = 2025           # Space frequency (Hz), 0 bit
FREQ_MARK = 2225            # Mark frequency (Hz), 1 bit

def load_wav(path: str):
    '''
    Load a mono 16-bit WAV file and normalize the samples.

    Returns:
        fs: Sample rate (Hz)
        samples: Normalized audio samples as a numpy array
    '''
    with wave.open(path, 'rb') as wf:
        if wf.getnchannels() != 1:
            raise ValueError("Only mono audio supported")
        
        fs = wf.getframerate()
        frames = wf.readframes(wf.getnframes())

        samples = np.frombuffer(frames, dtype=np.int16)
        samples = samples.astype(np.float32) / 32768.0

    return fs, samples

def tone_power(samples, f, fs):
    '''
    Calculate the power of a specific tone (frequency f) in the given block of samples.
    Uses a correlator (I/Q detection) to measure power at the target frequency.

    Returns:
        The power of the tone at frequency f in the block of samples.
    '''
    N = len(samples)
    n = np.arange(N)
    cos_ref = np.cos(2 * np.pi * f * n / fs)
    sin_ref = np.sin(2 * np.pi * f * n / fs)

    I = np.dot(samples, cos_ref)
    Q = np.dot(samples, sin_ref)

    return I**2 + Q**2

def detect_bit(block):
    '''
    Determine if the given block of samples corresponds to a mark (1) or space (0) tone.
    Compares the power at the mark and space frequencies and returns the bit value.
    '''
    p_mark = tone_power(block, FREQ_MARK, FS)
    p_space = tone_power(block, FREQ_SPACE, FS)

    return 1 if p_mark > p_space else 0

def extract_bits(samples):
    '''
    Process the audio samples in blocks corresponding to each bit and use tone detection to extract the bit values.
    
    Returns:
        A list of bits (0s and 1s) extracted from the audio samples.
    '''
    bits = []
    for i in range(0, len(samples), SAMPLES_PER_BIT):
        block = samples[i:i+SAMPLES_PER_BIT]

        # Ignore incomplete blocks at the end of the sample stream
        if len(block) < SAMPLES_PER_BIT:
            break

        bits.append(detect_bit(block))

    return bits

def bits_to_bytes(bits):
    '''
    Convert a stream of bits to a list of bytes using 8N1 framing.

    Framing format:
        - Start bit: 0
        - Data bits: 8 bits (LSB first)
        - Stop bit: 1

    The function processes the bits in chunks of 10 (1 start + 8 data + 1 stop) and extracts the byte values.
    '''
    bytes_out = []
    for i in range(0, len(bits), 10):
        frame = bits[i:i+10]

        if len(frame) < 10:
            break

        start_bit = frame[0]
        data_bits = frame[1:9]
        stop_bit = frame[9]

        # Validate framing: start bit must be 0 and stop bit must be 1
        if start_bit != 0 or stop_bit != 1:
            continue

        value = sum(bit << j for j, bit in enumerate(data_bits))

        bytes_out.append(value)

    return bytes_out

def bytes_to_string(byte_list):
    '''
    Convert a list of byte values to a string by interpreting each byte as an ASCII character.
    '''
    return ''.join(chr(b) for b in byte_list)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Bell 103 Modem Demodulator - Decode Bell 103 modem signals from a WAV file")
    parser.add_argument("input", help="Input WAV file")
    parser.add_argument("-o", "--output", help="Output text file (default: message.txt)")
    args = parser.parse_args()

    # Determine output file path
    output_path = args.output if args.output else "message.txt"

    print("Loading WAV file...")
    fs, samples = load_wav(args.input)

    if fs != FS:
        print(f"Warning: expected {FS} Hz, got {fs} Hz")
    
    print(f"Sample rate: {fs} Hz")
    print(f"Total samples: {len(samples)}")

    print("\nDecoding bits...")
    bits = extract_bits(samples)
    
    print("Decoding bytes...")
    data = bits_to_bytes(bits)

    print("Converting to ASCII...")
    text = bytes_to_string(data)

    print("\nDecoded Message:", end=" ")
    print(text)

    # Save output
    with open(output_path, "w") as f:
        f.write(text)

    print(f"\nMessage saved to {output_path}")