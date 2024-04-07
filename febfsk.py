import threading
import pyaudio
import numpy as np
from scipy.signal import find_peaks

'''The following deals with dictionaries for translation and compression, to be used in the
"translation and "detranslation" functions.'''
letter_to_bits = {
    '␑': '01',  # <<CAP>> using DC1, does not correspond with Unicode! Will actually toggle caps.
    '␒': '10',  # DC2 for any use someone desires (in this project, to switch to Japanese.).
    '␓': '11',  # DC3 for any use someone desires (in this project, to switch to pure binary).
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
    '␒': '10',  # DC2 for any use someone desires (in this project, to switch to Japanese.).
    '␓': '11',  # DC3 for any use someone desires (in this project, to switch to pure binary).
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
japanese_LTB = {
    '␑': '01',  # <<CAP>> using DC1, does not correspond with Unicode! Will actually toggle caps.
    '␒': '10',  # DC2 for any use someone desires (in this project, to switch to Japanese.).
    '␓': '11',  # DC3 for any use someone desires (in this project, to switch to pure binary).
    ' ': '00',

    '␂': '000',  # <<STX>>
    '␃': '001',  # <<ETX>>
    '␄': '010',  # <<EOT>>: Will actually end transmission on receiving end.
    '␅': '011',  # <<ENQ>>
    '␆': '100',  # <<ACK>>
    '␤': '101',  # <<NWL>>: Will actually print a newline.
    '␛': '110',  # <<ESC>>
    '␀': '111',  # <<NUL>>: Will actually print nothing. Good for buffers.

    '♥': '0000',
    'ぁ': '0001',
    'ァ': '0010',
    'あ': '0011',
    'ア': '0100',
    'ぃ': '0101',
    'ィ': '0110',
    'い': '0111',
    'イ': '1000',
    'ぅ': '1001',
    'ゥ': '1010',
    'う': '1011',
    'ウ': '1100',
    'ぇ': '1101',
    'ェ': '1110',
    'え': '1111',

    'エ': '00000',
    'ぉ': '00001',
    'ォ': '00010',
    'お': '00011',
    'オ': '00100',
    'か': '00101',
    'カ': '00110',
    'が': '00111',
    'ガ': '01000',
    'き': '01001',
    'キ': '01010',
    'ぎ': '01011',
    'ギ': '01100',
    'く': '01101',
    'ク': '01110',
    'ぐ': '01111',
    'グ': '10000',
    'け': '10001',
    'ケ': '10010',
    'げ': '10011',
    'ゲ': '10100',
    'こ': '10101',
    'コ': '10110',
    'ご': '10111',
    'ゴ': '11000',
    'さ': '11001',
    'サ': '11010',
    'ざ': '11011',
    'ザ': '11100',
    'し': '11101',
    'シ': '11110',
    'じ': '11111',

    'ジ': '000000',
    'す': '000001',
    'ス': '000010',
    'ず': '000011',
    'ズ': '000100',
    'せ': '000101',
    'セ': '000110',
    'ぜ': '000111',
    'ゼ': '001000',
    'そ': '001001',
    'ソ': '001010',
    'ぞ': '001011',
    'ゾ': '001100',
    'た': '001101',
    'タ': '001110',
    'だ': '001111',
    'ダ': '010000',
    'ち': '010001',
    'チ': '010010',
    'ぢ': '010011',
    'ヂ': '010100',
    'っ': '010101',
    'ッ': '010110',
    'つ': '010111',
    'ツ': '011000',
    'づ': '011001',
    'ヅ': '011010',
    'て': '011011',
    'テ': '011100',
    'で': '011101',
    'デ': '011110',
    'と': '011111',
    'ト': '100000',
    'ど': '100001',
    'ド': '100010',
    'な': '100011',
    'ナ': '100100',
    'に': '100101',
    'ニ': '100110',
    'ぬ': '100111',
    'ヌ': '101000',
    'ね': '101001',
    'ネ': '101010',
    'の': '101011',
    'ノ': '101100',
    'は': '101101',
    'ハ': '101110',
    'ば': '101111',
    'バ': '110000',
    'ぱ': '110001',
    'パ': '110010',
    'ひ': '110011',
    'ヒ': '110100',
    'び': '110101',
    'ビ': '110110',
    'ぴ': '110111',
    'ピ': '111000',
    'ふ': '111001',
    'フ': '111010',
    'ぶ': '111011',
    'ブ': '111100',
    'ぷ': '111101',
    'プ': '111110',
    'へ': '111111',

    'ヘ': '0000000',
    'べ': '0000001',
    'ベ': '0000010',
    'ぺ': '0000011',
    'ペ': '0000100',
    'ほ': '0000101',
    'ホ': '0000110',
    'ぼ': '0000111',
    'ボ': '0001000',
    'ぽ': '0001001',
    'ポ': '0001010',
    'ま': '0001011',
    'マ': '0001100',
    'み': '0001101',
    'ミ': '0001110',
    'む': '0001111',
    'ム': '0010000',
    'め': '0010001',
    'メ': '0010010',
    'も': '0010011',
    'モ': '0010100',
    'ゃ': '0010101',
    'ャ': '0010110',
    'や': '0010111',
    'ヤ': '0011000',
    'ゅ': '0011001',
    'ュ': '0011010',
    'ゆ': '0011011',
    'ユ': '0011100',
    'ょ': '0011101',
    'ョ': '0011110',
    'よ': '0011111',
    'ヨ': '0100000',
    'ら': '0100001',
    'ラ': '0100010',
    'り': '0100011',
    'リ': '0100100',
    'る': '0100101',
    'ル': '0100110',
    'れ': '0100111',
    'レ': '0101000',
    'ろ': '0101001',
    'ロ': '0101010',
    'ゎ': '0101011',
    'ヮ': '0101100',
    'わ': '0101101',
    'ワ': '0101110',
    'ゐ': '0101111',
    'ヰ': '0110000',
    'ゑ': '0110001',
    'ヱ': '0110010',
    'を': '0110011',
    'ヲ': '0110100',
    'ん': '0110101',
    'ン': '0110110',
    'ゔ': '0110111',
    'ヴ': '0111000',
    'ゕ': '0111001',
    'ヵ': '0111010',
    'ゖ': '0111011',
    'ヶ': '0111100',
    'ヷ': '0111101',
    'ヸ': '0111110',
    '゙': '0111111',
    'ヹ': '1000000',
    '゚': '1000001',
    'ヺ': '1000010',
    '゛': '1000011',
    '・': '1000100',
    '゜': '1000101',
    'ー': '1000110',
    'ゝ': '1000111',
    'ヽ': '1001000',
    'ゞ': '1001001',
    'ヾ': '1001010',
    'ゟ': '1001011',
    'ヿ': '1001100',
    '々': '1001101',
    '仝': '1001110',
    '「': '1001111',
    '」': '1010000',
    '『': '1010001',
    '』': '1010010',
    '（': '1010011',
    '）': '1010100',
    '〔': '1010101',
    '〕': '1010110',
    '［': '1010111',
    '］': '1011000',
    '｛': '1011001',
    '｝': '1011010',
    '｟': '1011011',
    '｠': '1011100',
    '〈': '1011101',
    '〉': '1011110',
    '《': '1011111',
    '》': '1100000',
    '【': '1100001',
    '】': '1100010',
    '〖': '1100011',
    '〗': '1100100',
    '〘': '1100101',
    '〙': '1100110',
    '〚': '1100111',
    '〛': '1101000',
    '。': '1101001',
    '、': '1101010',
    '゠': '1101011',
    '〆': '1101100',
    '〜': '1101101',
    '…': '1101110',
    '※': '1101111',
    '＊': '1110000',
    '♪': '1110001',
    '〇': '1110010',
    '：': '1110011',
    '！': '1110100',
    '？': '1110101',
    '〒': '1110110',
    '〄': '1110111',
    'Ⓧ ': '1111000',
    'Ⓛ': '1111001',
    'Ⓨ': '1111010',
    '♫': '1111011',
    '♬': '1111100',
    '♩': '1111101',
    '〽': '1111110',
    '￥': '1111111',
}  # Experimental Japanese dictionary for switching languages. No research on how common characters are.
japanese_BTL = {v: k for k, v in japanese_LTB.items()}
purebinary_LTB = {
    '␑': '01',  # <<CAP>> using DC1, does not correspond with Unicode! Will actually toggle caps.
    '␒': '10',  # DC2 for any use someone desires (in this project, to switch to Japanese.).
    '␓': '11',  # DC3 for any use someone desires (in this project, to switch to pure binary).
    ' ': '00',

    '␂': '000',  # <<STX>>
    '␃': '001',  # <<ETX>>
    '␄': '010',  # <<EOT>>: Will actually end transmission on receiving end.
    '␅': '011',  # <<ENQ>>
    '␆': '100',  # <<ACK>>
    '␤': '101',  # <<NWL>>: Will actually print a newline.
    '␛': '110',  # <<ESC>>
    '␀': '111',  # <<NUL>>: Will actually print nothing. Good for buffers.

    '0': '0',  # 0
    '1': '1',  # 1

}
purebinary_BTL = {v: k for k, v in purebinary_LTB.items()}
'''The following are variables used for the FSK signal generation.'''
baud_rate = 100  # Baud rate (bits per second).
bit_duration = 1 / baud_rate  # Duration of each bit in seconds.
frequency_0 = 1600  # Frequency for '0' compressed bit.
frequency_1 = 2000  # Frequency for '1' compressed bit.
frequency_STOP = 2400  # Frequency for ' ' "stop-gap" marker.
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


def translation_JP(input_str):
    encoded_bits = []
    for char in input_str.upper():
        if char in japanese_LTB:
            encoded_bits.append(japanese_LTB[char])
        else:
            encoded_bits.append(' ')
    return ' '.join(encoded_bits)

def translation_binary(input_str):
    encoded_bits = []
    for char in input_str.upper():
        if char in purebinary_LTB:
            encoded_bits.append(purebinary_LTB[char])
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
                            elif decoded_byte == '␒':
                                # Switch dictionaries
                                active_dict = japanese_BTL
                            elif decoded_byte == '␓':
                                # Switch dictionaries
                                active_dict = purebinary_BTL
                            elif decoded_byte == '␄':
                                demodulate_end()  # Kill it
                            else:
                                print(decoded_byte, end="")
                    decoded_line = ""  # Clear the decoded_line after processing complete bytes
    stream.stop_stream()
    stream.close()
    p.terminate()


def demodulate_end():
    global thread2_stop
    thread2_stop = True
