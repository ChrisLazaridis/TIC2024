from numpy import double
import numpy as np
import base64
import requests

from Codes.fano_shannon import Compress
from Codes.linear import LinearCode
import random


def create_noise(mes, percentage):
    if percentage < 0 or percentage > 1:
        percentage = 0.01
    noise_count = int(len(mes) * percentage)
    indexes = set()
    for _ in range(noise_count):
        index = random.randint(0, len(mes) - 1)
        if index not in indexes:
            indexes.add(index)
            mes[index] ^= 1
    return mes, len(indexes)


def bits_to_bytes_with_header(bits):
    # Calculate the number of bits in the last byte
    last_byte_bits = len(bits) % 8

    # Header is the first 4 bits indicating the number of bits in the last byte
    header = last_byte_bits if last_byte_bits else 8

    # Initialize byte array with header as the first byte
    b_a = bytearray()
    b_a.append(header)

    # Iterate over the bits in chunks of 8 to convert to bytes
    for i in range(0, len(bits), 8):
        byte = 0
        for j in range(8):
            if i + j < len(bits):
                byte = (byte << 1) | bits[i + j]
            else:
                break
        b_a.append(byte)

    return b_a


def calculate_entropy(frequencies_):
    en = 0
    for freq in frequencies_.values():
        en += freq * np.log2(1 / freq)
    return en


message = input("Enter the message: ")
noise_percentage = double(input("Enter the noise percentage (0.001 to 1): "))
n = int(input("Enter the value of n (must be greater than 7, we observed the code functions best at 21 : "))
if n < 7:
    print("n must be greater than or equal to 7, setting n to 7")
    n = 7
compressor = Compress(message_=message)
entropy = calculate_entropy(compressor.frequencies)
# make entropy a float with 2 decimal places
entropy = float(f"{entropy:.2f}")
code_table = compressor.code_table
liner_code = LinearCode(compressor.compress, n=n)
encoded_message = liner_code.encoded_message
encoded_message_with_noise, total_errors = create_noise(list(encoded_message), noise_percentage)
# print(f"encoded_message_with_noise: {encoded_message_with_noise}")
# byte_array = np.packbits(encoded_message_with_noise).tobytes()
byte_array = bits_to_bytes_with_header(encoded_message_with_noise)
base64_encoded_message = base64.b64encode(byte_array).decode('utf-8')
# print(f"base64_encoded_message: {base64_encoded_message}")
# create a json object
data = {'message': base64_encoded_message, 'code_table': code_table, 'n': n, 'errors': total_errors, 'entropy': entropy}
# send the json object to the server
del code_table
del n
response = requests.post('http://127.0.0.1:5000/', json=data)
if response.status_code == 200:
    # Get the JSON data from the response
    json_data = response.json()

    # Print each key-value pair line by line
    for key, value in json_data.items():
        print(f"{key}: {value}")
