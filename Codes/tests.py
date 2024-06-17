from fannon_shannon import Compress
from HammingCodeNumPy import HammingCodeEncode, HammingCodeDecode
from sage.all import *
import random


def create_noise(mes, percentage):
    """
    Create noise in the message
    :param mes: list, the message to add noise to
    :param percentage: float, the percentage of noise to add
    :return: list, the message with noise
    """
    noise = [0, 1]
    if percentage < 0 or percentage > 1:
        raise ValueError("Percentage must be between 0 and 1")
    noise_count = int(len(mes) * percentage)
    for _ in range(noise_count):
        index = random.randint(0, len(mes) - 1)
        mes[index] = random.choice(noise)
    return mes


# Example usage
message = (
    "Ex-Fiorentina icon Jovetic, introduced from the Olympiakos bench, "
    "forced a good save from Terracciano with a curling 20-yard strike one minute later as the match seemed to spark back to life. "
    "However, the game then tightened up again as neither team appeared to want to take a risk that might cost them the tie. "
    "Penalties seemed certain until the 116th minute when El Kaabi stooped to head home Santiago Hezze’s cross for his 16th goal in European competition this season. "
    "The roar that greeted the validation of El Kaabi’s goal, following a lengthy VAR check, in the 120th minute from the majority Greek fans in Athens showed what the occasion meant to the club.")
compressor = Compress(message_=message)
frequencies = compressor.frequencies
code_table = compressor.code_table
compressed_message = compressor.compress
HammingCodeEncode_ = HammingCodeEncode(compressed_message)
encoded_message = HammingCodeEncode_.encoded_message
encoded_message = create_noise(encoded_message, 0.01)
HammingCodeDecode_ = HammingCodeDecode(encoded_message)
print(f"Error count: {HammingCodeDecode_.errors_found}")
print(f"Errors Corrected: {HammingCodeDecode_.errors_corrected}")
decoded_message = HammingCodeDecode_.decoded_message
# turn the decoded message into a an array of ints, from the np
decoded_message = [int(bit) for bit in decoded_message]
# turn the decoded message into a string
decompressor = Compress(message_=decoded_message, code_table_=code_table, mode='decode')
decompressed_message = decompressor.decompress()
print(f"Decompressed message: {decompressed_message}")
if message == decompressed_message:
    print("Success")
else:
    print("Failure")

# class CompressEncodeDecodeDecomress:
#
#     def __init__(self, message):
#         self.message = self.compressEncodeDecodeDecomress_(message)
#
#     def compressEncodeDecodeDecomress_(message):
#         message = "Bill Gamas Re Pousti Mou"
#         compressor = Compress(message_=message)
#         frequencies = compressor.frequencies
#         code_table = compressor.code_table
#         compressed_message = compressor.compress
#         print(f"Compressed message: {compressed_message}")
#         HammingCodeEncode_ = HammingCodeEncode(compressed_message)
#         encoded_message = HammingCodeEncode_.encoded_message
#         print(f"Encoded message: {encoded_message}")
#         # introduce a single bit error
#         encoded_message[0] = 1 - encoded_message[0]
#         HammingCodeDecode_ = HammingCodeDecode(encoded_message)
#         print(f"Error count: {HammingCodeDecode_.error_count}")
#         decoded_message = HammingCodeDecode_.decoded_message
#         # turn the decoded message into a string
#         print(f"Decoded message: {decoded_message}")
#         decompressor = Compress(message_=decoded_message, code_table_=code_table, mode='decode')
#         decompressed_message = decompressor.decompress()
#         print(f"Decompressed message: {decompressed_message}")
