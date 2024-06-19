import random
from fannon_shannon import Compress  # Assuming this is your compression module
from linear import LinearCode  # Assuming this is your linear code module


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
    # nc = 0
    # for _ in range(0, len(mes) - 1, 7):
    #     mes[_ + random.randint(0, 6)] ^= 1
    #     nc += 1
    #     if nc >= noise_count:
    #         break
    # if nc < noise_count:
    #     while nc < noise_count:
    #         mes[random.randint(2, len(mes) - 1)] ^= 1
    #         nc += 1
    # return mes
    for _ in range(noise_count):
        mes[random.randint(0, len(mes) - 1)] ^= 1
    return mes


# Example usage
message2 = "Hello World This Is My first Message!?!?!?!?!??!??!"
message = (
    "Ex-Fiorentina icon Jovetic, introduced from the Olympiakos bench, "
    "forced a good save from Terracciano with a curling 20-yard strike one minute later as the match seemed to spark back to life. "
    "However, the game then tightened up again as neither team appeared to want to take a risk that might cost them the tie. "
    "Penalties seemed certain until the 116th minute when El Kaabi stooped to head home Santiago Hezze’s cross for his 16th goal in European competition this season. "
    "The roar that greeted the validation of El Kaabi’s goal, following a lengthy VAR check, in the 120th minute from the majority Greek fans in Athens showed what the occasion meant to the club."
)

# Compression
compressor = Compress(message_=message)
frequencies = compressor.frequencies
code_table = compressor.code_table
compressed_message = compressor.compress
compressed_message = [int(bit) for bit in compressed_message]

# Encoding
linear_code = LinearCode(compressed_message, n=15)
encoded_message = linear_code.encoded_message

# Adding noise
encoded_message_with_noise = create_noise(list(encoded_message), 0.01)

if len(encoded_message) != len(encoded_message_with_noise):
    print("Error: Encoded message and encoded message with noise are not the same length")
    exit()

# Count the differences between the encoded message and the encoded message with noise
differences = sum(1 for bit1, bit2 in zip(encoded_message, encoded_message_with_noise) if bit1 != bit2)
print(f"Differences: {differences / len(encoded_message) * 100:.2f}%")

# Decoding
linear_code_decode = LinearCode(encoded_message_with_noise, n=15, mode='decode')
decoded_message = linear_code_decode.decoded_message
decoded_message = [int(bit) for bit in decoded_message]

# Count the differences between the compressed and decoded messages
differences = sum(1 for bit1, bit2 in zip(compressed_message, decoded_message) if bit1 != bit2)
print(f"Compressed message length: {len(compressed_message)}")
print(f"Decoded message length: {len(decoded_message)}")
print(f"Error count: {linear_code_decode.error_count}")
print(f"Errors Corrected: {linear_code_decode.errors_corrected}")

if len(decoded_message) != 0:
    print(f"Differences: {differences / len(decoded_message) * 100:.2f}%")
else:
    print("Differences: 100.00%")

# Decompression
decompressor = Compress(message_=decoded_message, code_table_=code_table, mode='decode')
decompressed_message = decompressor.decompress()
print(f"Decompressed message: {decompressed_message}")

# Final check
if message == decompressed_message:
    print("Success")
else:
    print("Failure")
