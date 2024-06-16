from fannon_shannon import Compress
from HammingCode import HammingCodeEncode, HammingCodeDecode
from sage.all import *

# Example usage
message = "Bill Gamas Re Pousti Mou"
compressor = Compress(message_=message)
frequencies = compressor.frequencies
code_table = compressor.code_table
compressed_message = compressor.compress
print(f"Compressed message: {compressed_message}")
HammingCodeEncode_ = HammingCodeEncode(compressed_message)
encoded_message = HammingCodeEncode_.encoded_message
print(f"Encoded message: {encoded_message}")
# introduce a single bit error
encoded_message[0] = 1 - encoded_message[0]
HammingCodeDecode_ = HammingCodeDecode(encoded_message)
print(f"Error count: {HammingCodeDecode_.error_count}")
decoded_message = HammingCodeDecode_.decoded_message
# turn the decoded message into a string
print(f"Decoded message: {decoded_message}")
decompressor = Compress(message_=decoded_message, code_table_=code_table, mode='decode')
decompressed_message = decompressor.decompress()
print(f"Decompressed message: {decompressed_message}")
