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
        # WARNING: ΑΥΤΟ ΤΟ ΠΕΤΑΞΕ PROMPT, ΕΧΩ ΧΑΜΗΛΕΣ ΕΩΣ ΚΑΘΟΛΟΥ ΕΛΠΙΔΕΣ
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
