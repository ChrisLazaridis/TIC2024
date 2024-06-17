import random
from fannon_shannon import Compress
from HammingCodeNumPy import HammingCodeEncode, HammingCodeDecode


def create_noise(mes, percentage):
    """
    Create noise in the message
    :param mes: list, the message to add noise to
    :param percentage: float, the percentage of noise to add
    :return: list, the message with noise
    """
    if percentage < 0 or percentage > 1:
        raise ValueError("Percentage must be between 0 and 1")
    noise_count = int(len(mes) * percentage)
    for _ in range(noise_count):
        mes[len(mes) - (len(mes)//2) - _] ^= 1
    return mes


# Example usage
message = "Hello World This Is My first Message"
message2 = (
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
compressed_message = [int(bit) for bit in compressed_message]
encoded_message = HammingCodeEncode_.encoded_message
encoded_message_with_noise = create_noise(list(encoded_message), 0.01)
if len(encoded_message) != len(encoded_message_with_noise):
    print("Error: Encoded message and encoded message with noise are not the same length")
    exit()
# count the differences between the encoded message and the encoded message with noise
differences = sum(1 for bit1, bit2 in zip(encoded_message, encoded_message_with_noise) if bit1 != bit2)
print(f"Differences: {differences / len(encoded_message) * 100:.2f}%")
HammingCodeDecode_ = HammingCodeDecode(encoded_message_with_noise)
decoded_message = HammingCodeDecode_.decoded_message
# count the differences between the encoded and decoded messages
decoded_message = [int(bit) for bit in decoded_message]
differences = sum(1 for bit1, bit2 in zip(compressed_message, decoded_message) if bit1 != bit2)
print(f"Compressed message length: {len(compressed_message)}")
print(f"Decoded message length: {len(decoded_message)}")
print(f"Differences: {differences / len(decoded_message) * 100:.2f}%")
# turn the decoded message into an array of ints
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
