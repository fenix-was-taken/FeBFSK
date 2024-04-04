import threading
import pyaudio
import numpy as np
from scipy.signal import find_peaks

'''The following deals with dictionaries for translation and compression, to be used in the
"translation and "detranslation" functions.'''
letter_to_bits = {
    '␑': '01',  # <<CAP>> using DC1, does not correspond with Unicode! Will actually toggle caps.
    '␒': '10',  # <<STP>> using DC2, does not correspond with Unicode! Unused...
    ' ': '00',

    '␂': '000',  # <<STX>>
    '␃': '001',  # <<ETX>>
    '␄': '010',  # <<EOT>>: Will actually end transmission on receiving end.
    '␅': '011',  # <<ENQ>>
    '␆': '100',  # <<ACK>>
    '␤': '101',  # <<NWL>>: Will actually print a newline.
    '␛': '110',  # <<ESC>>
    '␀': '111',  # <<NUL>>: Will actually print nothing. Good for buffers.

    'E': '0000',
    'A': '0001',
    'T': '0010',
    'O': '0011',
    'N': '0100',
    'I': '0101',
    'R': '0110',
    'S': '0111',
    'L': '1000',
    'C': '1001',
    'H': '1010',
    'D': '1011',
    'M': '1100',
    'U': '1101',
    'P': '1110',
    'G': '1111',

    'F': '00000',
    'Y': '00001',
    '-': '00010',
    'W': '00011',
    'B': '00100',
    '.': '00101',
    '0': '00110',
    ',': '00111',
    'V': '01000',
    'K': '01001',
    '/': '01010',
    '1': '01011',
    '2': '01100',
    '=': '01101',
    ':': '01110',
    '*': '01111',
    '_': '10000',
    '3': '10001',
    'J': '10010',
    '>': '10011',
    '@': '10100',
    '5': '10101',
    '4': '10110',
    '	': '10111',
    '9': '11000',
    'X': '11001',
    '8': '11010',
    '7': '11011',
    'Q': '11100',
    ')': '11101',
    '6': '11110',
    '(': '11111',

    '\"': '000000',
    '\'': '000001',
    '?': '000010',
    '<': '000011',
    'Z': '000100',
    ';': '000101',
    '&': '000110',
    '$': '000111',
    '!': '001000',
    '+': '001001',
    '[': '001010',
    ']': '001011',
    '%': '001100',
    '#': '001101',
    '~': '001110',
    '\\': '001111',
    '|': '010000',
    '`': '010001',
    '}': '010010',
    '{': '010011',
}  # Dictionary that translates the standardized character set into binary bits.
bits_to_letter = {v: k for k, v in letter_to_bits.items()}  # "letter_to_bits" but reversed.
letter_to_bits_lowercase = {
    '␑': '01',  # <<CAP>> using DC1, does not correspond with Unicode! Will actually toggle caps.
    '␒': '10',  # <<STP>> using DC2, does not correspond with Unicode! Unused...
    ' ': '00',

    '␂': '000',  # <<STX>>
    '␃': '001',  # <<ETX>>
    '␄': '010',  # <<EOT>>: Will actually end transmission on receiving end.
    '␅': '011',  # <<ENQ>>
    '␆': '100',  # <<ACK>>
    '␤': '101',  # <<NWL>>: Will actually print a newline.
    '␛': '110',  # <<ESC>>
    '␀': '111',  # <<NUL>>: Will actually print nothing. Good for buffers.

    'e': '0000',
    'a': '0001',
    't': '0010',
    'o': '0011',
    'n': '0100',
    'i': '0101',
    'r': '0110',
    's': '0111',
    'l': '1000',
    'c': '1001',
    'h': '1010',
    'd': '1011',
    'm': '1100',
    'u': '1101',
    'p': '1110',
    'g': '1111',

    'f': '00000',
    'y': '00001',
    '-': '00010',
    'w': '00011',
    'b': '00100',
    '.': '00101',
    '0': '00110',
    ',': '00111',
    'v': '01000',
    'k': '01001',
    '/': '01010',
    '1': '01011',
    '2': '01100',
    '=': '01101',
    ':': '01110',
    '*': '01111',
    '_': '10000',
    '3': '10001',
    'j': '10010',
    '>': '10011',
    '@': '10100',
    '5': '10101',
    '4': '10110',
    '	': '10111',
    '9': '11000',
    'x': '11001',
    '8': '11010',
    '7': '11011',
    'q': '11100',
    ')': '11101',
    '6': '11110',
    '(': '11111',

    '\"': '000000',
    '\'': '000001',
    '?': '000010',
    '<': '000011',
    'z': '000100',
    ';': '000101',
    '&': '000110',
    '$': '000111',
    '!': '001000',
    '+': '001001',
    '[': '001010',
    ']': '001011',
    '%': '001100',
    '#': '001101',
    '~': '001110',
    '\\': '001111',
    '|': '010000',
    '`': '010001',
    '}': '010010',
    '{': '010011',
}  # Dictionary that translates the standardized character set into binary bits.
bits_to_letter_lowercase = {v: k for k, v in letter_to_bits_lowercase.items()}  # "letter_to_bits" but reversed.
'''The following are variables used for the FSK signal generation.'''
baud_rate = 100  # Baud rate (bits per second).
bit_duration = 1 / baud_rate  # Duration of each bit in seconds.
frequency_0 = 1600  # Frequency for 'A' compressed bit.
frequency_1 = 2000  # Frequency for 'B' compressed bit.
frequency_STOP = 2400  # Frequency for 'E' "stop-gap" marker.
rest_frequency = 1200  # Rest frequency when nothing is being transmitted.
sample_rate = 44100  # Sample rate (samples per second).
'''The following is used for demodulation - frequency detection parameters.'''
peak_threshold = 0.9  # Threshold for peak detection
rest_frequency_range = 100  # Range around rest frequency to consider
noise_threshold = 0.10  # Adjust this threshold according to your noise level
'''The following is used for threading and function control.'''
user_input = ''  # Global variable to watch
thread_stop = False  # Flag to tell the modulation threads when to stop
thread2_stop = False  # Flag to tell the demodulation threads when to stop
active_dict = bits_to_letter  # Initially active dictionary is bits_to_letter


def translation(input_str):
    encoded_bits = []
    for char in input_str.upper():
        if char in letter_to_bits:
            encoded_bits.append(letter_to_bits[char])
        else:
            encoded_bits.append(' ')
    return ' '.join(encoded_bits)


def detranslation(input_str):
    decoded_bits = ''
    bits_list = input_str.split()
    for bit in bits_list:
        if bit in bits_to_letter:
            decoded_bits += bits_to_letter[bit]
        else:
            decoded_bits += ' '
    return decoded_bits


def watch_variable():
    global user_input
    p = pyaudio.PyAudio()
    stream = p.open(format=pyaudio.paFloat32,
                    channels=1,
                    rate=sample_rate,
                    output=True)
    while not thread_stop:
        if user_input:
            bits = user_input
            user_input = ''  # Clear user input after processing
        else:
            bits = ' '  # Empty space indicates rest frequency
        for bit in bits:
            if bit == '1':
                frequency = frequency_0
            elif bit == '0':
                frequency = frequency_1
            elif bit == ' ':
                frequency = frequency_STOP
            else:
                frequency = rest_frequency  # Play rest frequency if character is not recognized

            # Generate sine wave for the current bit
            t = np.linspace(0, bit_duration, int(bit_duration * sample_rate), endpoint=False)
            signal = np.sin(2 * np.pi * frequency * t)

            # Play the filtered signal
            stream.write(signal.astype(np.float32).tobytes())
    stream.stop_stream()
    stream.close()
    p.terminate()


def send(new_value):
    global user_input
    user_input = new_value


def modulate_start():
    global thread_stop
    thread_stop = False
    watcher_thread = threading.Thread(target=watch_variable)
    watcher_thread.daemon = False
    watcher_thread.start()


def modulate_end():
    global thread_stop
    thread_stop = True


def demodulate_start():
    global thread2_stop
    thread2_stop = False
    watcher2_thread = threading.Thread(target=demodulate_process)
    watcher2_thread.daemon = False
    watcher2_thread.start()


def demodulate_process():
    global active_dict
    p = pyaudio.PyAudio()
    stream = p.open(format=pyaudio.paFloat32,
                    channels=1,
                    rate=sample_rate,
                    input=True,
                    frames_per_buffer=int(sample_rate / baud_rate))  # Set frame buffer to match bit duration

    bits_buffer = []  # Buffer to store detected bits
    decoded_line = ""  # Variable to store the decoded characters in the same line

    while not thread2_stop:
        data = stream.read(int(sample_rate / baud_rate))
        signal = np.frombuffer(data, dtype=np.float32)

        # Apply noise thresholding
        signal_copy = signal.copy()
        signal_copy[np.abs(signal_copy) < noise_threshold] = 0

        # Perform Fourier Transform to get frequency spectrum
        spectrum = np.abs(np.fft.fft(signal_copy))
        frequencies = np.fft.fftfreq(len(spectrum), d=1 / sample_rate)

        # Find peaks in the spectrum
        peaks, _ = find_peaks(spectrum, height=peak_threshold * np.max(spectrum))

        # Decode the detected frequencies
        detected_bits = set()  # Set to store detected bits in this duration
        for peak in peaks:
            freq = frequencies[peak]
            if np.isclose(freq, frequency_0, atol=50):
                detected_bits.add('1')
            elif np.isclose(freq, frequency_1, atol=50):
                detected_bits.add('0')
            elif np.isclose(freq, frequency_STOP, atol=50):
                detected_bits.add(' ')
            elif np.isclose(freq, rest_frequency, atol=50):
                detected_bits.add('R')  # 'R' for rest state
                pass
            else:
                pass

        if detected_bits:
            bits_buffer.extend(detected_bits)

        # Check if enough bits have been accumulated to form a complete character
        if bits_buffer:
            character_length = min(1, len(bits_buffer))  # Maximum character length
            if len(bits_buffer) >= character_length:
                character_bits = bits_buffer[:character_length]
                bits_buffer = bits_buffer[character_length:]
                decoded_character = ''.join(character_bits)
                decoded_line += decoded_character  # Append the decoded character to the line

                # Check if the received bits contain complete bytes delimited by spaces
                if " " in decoded_line:
                    bytes_list = decoded_line.split(" ")  # Split by spaces to get bytes
                    for byte in bytes_list:
                        if byte in active_dict:  # Check if the byte is in the active dictionary
                            decoded_byte = active_dict[byte]
                            if decoded_byte == '␤':  # Check if the translated character is newline
                                print()  # Print a newline
                            elif decoded_byte == '␀':
                                pass  # Do nothing
                            elif decoded_byte == '␑':
                                # Switch dictionaries
                                if active_dict == bits_to_letter:
                                    active_dict = bits_to_letter_lowercase
                                else:
                                    active_dict = bits_to_letter
                            elif decoded_byte == '␄':
                                demodulate_end() # Kill it
                            else:
                                print(decoded_byte, end="")
                    decoded_line = ""  # Clear the decoded_line after processing complete bytes
    stream.stop_stream()
    stream.close()
    p.terminate()


def demodulate_end():
    global thread2_stop
    thread2_stop = True
