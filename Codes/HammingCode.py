from sage.all import *
import random as rnd
import math

class HammingCodeEncode:
    def __init__(self, message_):
        self.message = message_
        self.original_k = len(self.message)
        if self.original_k == 0:
            raise ValueError("Message cannot be empty.")
        self.header_length = 32
        self.header = [int(bit) for bit in bin(self.original_k)[2:].zfill(self.header_length)]
        self.k = self.original_k + self.header_length  # k includes the original message length and the header
        self.padding = (8 - (self.k % 8)) % 8  # Padding to make k a multiple of 8
        self.k += self.padding  # Update k to include the padding
        self.n = self.calculate_n()
        self.generator_matrix = self.create_generator_matrix()
        self.parity_matrix = self.generator_matrix[:, self.k:]
        self.encoded_message = self.encode_message()

    def calculate_n(self):
        return self.k + math.ceil(math.log2(self.k + math.ceil(math.log2(self.k + 1))))

    def create_generator_matrix(self):
        m = math.ceil(math.log2(self.k + 1))  # Number of parity bits
        n = self.k + m  # Total number of bits
        identity_matrix = matrix.identity(GF(2), self.k)
        parity_matrix = matrix(GF(2), m, self.k)

        for i in range(m):
            for j in range(self.k):
                parity_matrix[i, j] = (j + 1) & (1 << i) != 0

        generator_matrix = identity_matrix.augment(parity_matrix.transpose())
        return generator_matrix

    def encode_message(self):
        random_bits = ''.join(str(rnd.randint(0, 1)) for _ in range(self.padding))
        header_str = ''.join(str(bit) for bit in self.header)
        m = header_str + ''.join(map(str, self.message)) + random_bits
        message_vector = vector(GF(2), [int(bit) for bit in m])
        encoded_message = message_vector * self.generator_matrix
        return encoded_message

class HammingCodeDecode:
    def __init__(self, encoded_message, parity_matrix):
        self.encoded_message = encoded_message
        self.parity_matrix = parity_matrix
        self.H_matrix = self.create_h_matrix()
        self.syndrome = self.calculate_syndrome()
        self.error_count = self.check_errors()
        self.decoded_message = self.decode_message()

    def create_h_matrix(self):
        p_transposed = self.parity_matrix.transpose()
        num_parity_bits = p_transposed.nrows()
        identity_matrix = matrix.identity(GF(2), num_parity_bits)
        h_matrix = p_transposed.augment(identity_matrix)
        return h_matrix

    def calculate_syndrome(self):
        encoded_message_vector = vector(GF(2), self.encoded_message)
        syndrome = self.H_matrix * encoded_message_vector.column()
        return syndrome

    def check_errors(self):
        return sum(1 for bit in self.syndrome if bit != 0)

    def correct_errors(self):
        # Convert the syndrome to a list of integers
        syndrome_as_ints = [int(bit) for bit in self.syndrome.list()]
        # Calculate the error index
        error_index = sum(2 ** i * bit for i, bit in enumerate(syndrome_as_ints))
        if error_index > 0:
            if error_index <= len(self.encoded_message):
                # Convert the encoded message to a list for modification
                corrected_message = list(map(int, self.encoded_message))
                # Flip the bit at the error index (adjust for 0-based index)
                corrected_message[error_index - 1] = 1 if corrected_message[error_index - 1] == 0 else 0
                # Convert back to a vector
                self.encoded_message = vector(GF(2), corrected_message)
            else:
                print("Uncorrectable error detected at position:", error_index)

    def decode_message(self):
        if self.error_count > 0:
            self.correct_errors()
        header = self.encoded_message[:32]
        k = int(''.join(str(bit) for bit in header), 2)
        original_message = self.encoded_message[32:32 + k]
        return original_message
