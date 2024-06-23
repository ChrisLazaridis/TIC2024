from flask import Flask, request, jsonify
from Codes.linear import LinearCode
from Codes.fano_shannon import Compress
import base64
import numpy as np

app = Flask(__name__)


def calculate_entropy(message):
    freq = {}
    message_length = len(message)
    for char in message:
        if char in freq:
            freq[char] += 1
        else:
            freq[char] = 1
    for char in freq:
        freq[char] /= message_length
    freq = dict(sorted(freq.items(), key=lambda x: x[1], reverse=True))
    en = 0
    for f in freq.values():
        en += f * np.log2(1 / f)
    return round(en, 2)


def bytes_to_bits_with_header(byte_array):
    # Get the header
    header = byte_array[0]

    # Get the bits from the byte array
    bits = []
    for i in range(1, len(byte_array)):
        byte = byte_array[i]
        for j in range(7, -1, -1):
            bits.append((byte >> j) & 1)

    # Remove the padding bits
    if header < 8:
        bits = bits[:-8 + header]

    return bits


@app.route('/', methods=['GET', 'POST'])
def hello_world():
    return "TIC 2024, P22083, P22126, P22252"


@app.route('/receive', methods=['POST'])
def decode_and_send_back():
    data = request.json
    if not data:
        return jsonify({'error': 'Invalid JSON data'}), 400

    message = data.get('message')
    code_table = data.get('code_table')
    n = data.get('n')
    errors = data.get('errors')
    original_entropy = data.get('entropy')
    compression = data.get('compression_algorithm')
    encoding = data.get('encoding')

    try:
        # Decode the base64 message
        byte_array = base64.b64decode(message)
        encoded_message_ = bytes_to_bits_with_header(byte_array)
        encoded_message_ = [int(bit) for bit in encoded_message_]
        llinear_code = LinearCode(encoded_message_, n=n, mode='decode')
        decoded_message_ = llinear_code.decoded_message
        errors_found = llinear_code.error_count
        errors_corrected = llinear_code.errors_corrected

        # Decompress the message
        decompressor = Compress(decoded_message_, code_table_=code_table, mode='decode')
        decompressed_message = decompressor.decompress()
        entropy = calculate_entropy(decompressed_message)

        return jsonify(
            {'message': decompressed_message,
             'compression_algorithm': compression,
             'encoding': encoding,
             'original errors': errors,
             'corrected errors': errors_corrected,
             'original entropy': original_entropy,
             'new entropy': entropy})
    except Exception as e:
        return jsonify({'error': str(e)}), 500


if __name__ == '__main__':
    app.run(debug=True)
