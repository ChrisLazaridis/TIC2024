# Implement a linear code with a generator matrix to check for errors. The length of the codeword should be rounded to the nearest multiple of 8.
# padding will be used to fill the remaining bits. Along with the message, a number of log(k) bits will be encoded in the start of the message, which will indicate
# the amount of data bits in the message. The message will be encoded using the generator matrix, and then sent to the server. The server will decode the message using the
# parity check matrix, and then check for errors. If an error is detected, the server will send a message to the client to resend the message. If no error is detected, the server
# two classes will be made, one for the encoding, and one for the decoding. The encoding class is responsible for:
# - creating the generator matrix based on the message length + the amount of bits needed to indicate the length of the message
# - the parity matrix should be made for an n = k + log(k) so it should have k rows and  k+log(k) columns.
# - the generator matrix should be an augmented matrix with the identity matrix of size k as the left part, and the parity matrix as the right part
# - padding the message to match the length of the codeword exactly, for that reason random bits should be added at the end of the message
# - encoding the message using the generator matrix, basically multiplying message vector by the generator matrix
# The decoding class is responsible for:
# - decoding the message using the parity matrix
# - checking for errors in the message
# - show how many errors there are in the message
# - create the H matrix used for error checking and decoding. H = [P^T I] where P is the parity matrix (transposed) and I is the identity matrix of size log(k)
# - the decoding should be done by multiplying the encoded message vector by the H matrix transposed
# - the error checking should be done by checking if the result of the multiplication between H and the encoded message vector transposed is a zero vector


from sage.all import *
import random as rnd
import math


class LinearCodeEncode:
    def __init__(self, message_):
        self.message = message_
        self.original_k = len(self.message)
        if self.original_k == 0:
            raise ValueError("Message cannot be empty.")
        # Correctly calculate the header length.
        self.header_length = 32
        self.header = [int(bit) for bit in bin(self.original_k)[2:].zfill(self.header_length)]
        self.k = self.original_k + self.header_length  # k includes the original message length and the header
        self.padding = (8 - (self.k % 8)) % 8  # Padding to make k a multiple of 8
        self.k += self.padding  # Update k to include the padding
        self.n = self.k + math.ceil(math.log2(self.k))  # n includes k and the parity bits
        self.generator_matrix = self.create_generator_matrix()
        self.parity_matrix = self.create_parity_matrix()
        self.encoded_message = self.encode_message()

    def create_generator_matrix(self):
        identity_matrix = matrix.identity(GF(2), self.k)
        parity_matrix = matrix.random(GF(2), self.k, self.n - self.k)
        generator_matrix = identity_matrix.augment(parity_matrix)
        return generator_matrix

    def calculate_n(self):
        return self.k + math.ceil(math.log2(self.k))

    def create_parity_matrix(self):
        return self.generator_matrix[:, self.k:]

    def encode_message(self):
        random_bits = ''.join(str(rnd.randint(0, 1)) for _ in range(self.padding))
        header_str = ''.join(str(bit) for bit in self.header)  # Convert header bits to string correctly
        m = header_str + ''.join(map(str, self.message)) + random_bits
        print("Message string m:", m)  # This should now print a correct binary string
        message_vector = vector(GF(2), [int(bit) for bit in m])
        print("Generator matrix columns:", self.generator_matrix.ncols())
        encoded_message = message_vector * self.generator_matrix
        return encoded_message


class LinearCodeDecode:
    def __init__(self, encoded_message, parity_matrix):
        self.encoded_message = encoded_message
        x = rnd.randint(33, len(self.encoded_message) - 1)
        self.encoded_message[x] = 1 if self.encoded_message[x] == 0 else 0
        self.parity_matrix = parity_matrix
        self.H_matrix = self.create_h_matrix()
        self.syndrome = self.calculate_syndrome()
        self.error_count = self.check_errors()
        self.decoded_message = self.decode_message()

    def create_h_matrix(self):
        # Transpose the parity matrix P to get P^T
        p_transposed = self.parity_matrix.transpose()
        # get the rows of the parity matrix
        num_parity_bits = p_transposed.nrows()
        # Create an identity matrix I with the same number of rows as the number of parity bits
        identity_matrix = matrix.identity(GF(2), num_parity_bits)
        # Augment P^T with I to form the H matrix
        h_matrix = p_transposed.augment(identity_matrix)
        return h_matrix

    def calculate_syndrome(self):
        # Convert the encoded message to a vector
        encoded_message_vector = vector(GF(2), self.encoded_message)
        # Transpose the encoded message vector
        encoded_message_vector_transposed = encoded_message_vector.column()
        # Multiply by the H matrix to get the syndrome vector
        syndrome = self.H_matrix * encoded_message_vector_transposed
        return syndrome

    def check_errors(self):
        # Check if the syndrome is a zero vector (no errors)
        error_count = sum(1 for bit in self.syndrome if bit != 0)
        return error_count

    @staticmethod
    def correct_errors(encoded_message, syndrome):
        # Remove parentheses from the syndrome
        syndrome_str = ''.join(str(bit) for bit in syndrome).replace('(', '').replace(')', '')

        # Convert the syndrome to an integer index
        error_index = int(syndrome_str, 2)

        # If the syndrome is all zeros, there is no error
        if error_index == 0:
            return encoded_message

        # If the error index is greater than the length of the message, it's an uncorrectable error
        if error_index > len(encoded_message):
            raise ValueError("Uncorrectable error detected.")

        # Flip the bit at the error index (subtract 1 because syndrome indexing starts at 1)
        corrected_message = list(encoded_message)
        corrected_message[error_index - 1] = 1 - corrected_message[error_index - 1]

        return corrected_message

    def decode_message(self):
        # If no errors, extract the original message from the encoded message
        if self.error_count == 0:
            # Extract the header (first 32 bits) from the encoded message
            header = self.encoded_message[:32]
            # turn it to an int from the binary form
            k = int(''.join(str(bit) for bit in header), 2)
            # Extract the original message from the encoded message
            original_message = self.encoded_message[32:32 + k]
            return original_message
        else:
            # If errors are detected, try to correct them
            corrected_message = self.correct_errors(self.encoded_message, self.syndrome)
            # Extract the header (first 32 bits) from the corrected message
            header = corrected_message[:32]
            # turn it to an int from the binary form
            k = int(''.join(str(bit) for bit in header), 2)
            # Extract the original message from the corrected message
            original_message = corrected_message[32:32 + k]
            return original_message


# Example usage
message = [1, 0, 1, 0, 0, 1, 0, 1]
encoder = LinearCodeEncode(message)
print(f"Encoded message: {encoder.encoded_message}")
decoder = LinearCodeDecode(encoder.encoded_message, encoder.parity_matrix)
print(f"Decoded message: {decoder.decoded_message}")
print(f"Error count: {decoder.error_count}")
