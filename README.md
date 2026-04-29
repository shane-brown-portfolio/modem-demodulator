# Bell 103 Modem Demodulator
This project implements a demodulator for the Bell 103 modem protocol, decoding audio signals into ASCII text. The program reads a WAV file containing Frequency Shift Keying (FSK) encoded data and reconstructs the original message.

The Bell 103 protocol transmits bits using two distinct frequencies:
- **2025 Hz** → Space (0)
- **2225 Hz** → Mark (1)

Each byte is transmitted using 8N1 framing:
- 1 start bit (0)
- 8 data bits (LSB first)
- 1 stop bit (1)

The program processes the audio signal in fixed-size blocks corresponding to each bit and determines which frequency is present using a correlator (I/Q detection).

## Build Instructions

### Requirements
- Python 3.x
- numpy

### Install Dependencies
```
pip install numpy
```
Or
```
pip install -r requirements.txt
```

### Run
Decode a WAV file:
```
python3 decoder.py <input.wav>
```
Example:
```
python3 decoder.py message.wav
```
Specify an output file:
```
python3 decoder.py message.wav -o output.txt
```

## Output
After running the program:
- The decoded message is printed to the console
- A text file is created:
  - `message.txt` (default)
  - or a custom file if specified with `-o`

## How It Works
This program decodes a Bell 103 FSK signal by processing the audio in fixed-size blocks (160 samples per bit).

1. **Load and Normalize Audio**
   - Reads a mono 16-bit WAV file and normalizes samples to [-1, 1] using Python's `wave` module.

2. **Split into Bits**
   - Divides the signal into 160-sample blocks, each representing one bit at 300 baud and 48 kHz sample rate..

3. **Detect Frequency**
   - For each block, computes correlation with 2025 Hz (0) and 2225 Hz (1).
   - Uses I/Q detection and compares power (`I² + Q²`) to decide the bit.

4. **Decode Bytes**
   - Groups bits into 10-bit frames (8N1 format):
     - 1 start bit (0)
     - 8 data bits (LSB-first)
     - 1 stop bit (1)
   - Frames with invalid start/stop bits are skipped.
   - Extracts the 8 data bits and converts them to bytes.

6. **Convert to Text**
   - Translates bytes into ASCII characters to produce the final message.


4. **Bit Stream Construction**
   - Each processed block produces a single bit.
   - All bits are collected into a continuous bit stream.

5. **Byte Decoding (8N1 Framing)**
   - Bits are grouped into frames of 10:
     - 1 start bit (0)
     - 8 data bits (LSB-first)
     - 1 stop bit (1)
   - Frames with invalid start/stop bits are skipped.
   - Valid data bits are converted into byte values.

6. **ASCII Conversion**
   - The decoded bytes are converted into characters to reconstruct the original message.

## How It Went
Overall, the project went well once the core tone detection logic was working correctly.
At first, it was not obvious how to reliably distinguish between the two frequencies, but implementing the correlator using `numpy.dot` made this much clearer.
After testing with simple tones and the provided WAV files, it became easy to confirm that the correct frequency consistently produced a much higher power value.

One of the biggest challenges was ensuring proper bit alignment. Since each bit must be exactly 160 samples, even a small offset would cause the decoded output to become unreadable.
Another challenge was remembering that the data bits are LSB-first, which initially led to incorrect characters until it was fixed. I had to ensure that each group of 10 bits had a valid start bit (0) and stop bit (1) to help filter out errors and confirm the decoding was working properly.

The provided test files were very helpful during development. Once the program correctly decoded those known messages, it worked reliably and was straightforward to apply it to the actual message file.

## Still To Be Done
While the program meets correctly decodes messages, there are several possible improvements:
- Precompute sine and cosine reference signals instead of recalculating them for every block
- Add a command-line flag to print per-bit power values for easier debugging
- Automatically detect bit alignment instead of assuming perfect alignment
- Support other modem protocols or baud rates

These improvements would make the decoder more efficient and more applicable to real-world signals beyond the clean test inputs.
