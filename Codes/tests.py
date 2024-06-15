from fannon_shannon import Compress
from linear import LinearCodeEncode, LinearCodeDecode
from sage.all import *

# Example usage
message = "hello world"
compressor = Compress(message_=list(message))
frequencies = compressor.frequencies
code_table = compressor.code_table
compressed_message = compressor.compress
print(f"Compressed message: {compressed_message}")
linearCodeEncode = LinearCodeEncode(compressed_message)
parity_matrix = linearCodeEncode.parity_matrix
encoded_message = linearCodeEncode.encoded_message
print(f"Encoded message: {encoded_message}")
linearCodeDecode = LinearCodeDecode(encoded_message, parity_matrix)
decoded_message = linearCodeDecode.decoded_message
# turn the decoded message into a string
decoded_message = ''.join(map(str, decoded_message))
print(f"Decoded message: {decoded_message}")
decompressor = Compress(message_=list(decoded_message), code_table_=code_table, mode='decode')
decompressed_message = decompressor.decompress()
print(f"Decompressed message: {decompressed_message}")
