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
python decoder.py <input.wav>
```
Example:
```
python decoder.py message.wav
```
Specify an output file:
```
python decoder.py message.wav -o output.txt
```

## Output
After running the program:
- The decoded message is printed to the console
- A text file is created:
  - `message.txt` (default)
  - or a custom file if specified with `-o`

## How It Works

## How It Went

## Still To Be Done
