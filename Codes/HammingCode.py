from sage.all import *
import random as rnd
import math


class HammingCodeEncode:
    def __init__(self, message_):
        """

        :param message_: the message to encode
        """
        self.message = message_
        # Correctly calculate the final length of the precoded message (k)
        self.original_k = len(self.message)
        if self.original_k == 0:
            raise ValueError("Message cannot be empty.")
        # Header is always 32 bit, which means we can facilitate messages up to 2^32 bits
        self.header_length = 32
        # Convert the original message length to binary and pad it to the header length
        self.header = [int(bit) for bit in bin(self.original_k)[2:].zfill(self.header_length)]
        # k includes the original message length and the header
        self.k = self.original_k + self.header_length
        # Padding to make k a multiple of 8
        self.padding = (8 - (self.k % 8)) % 8
        # Update k to include the padding
        self.k += self.padding
        # n includes k and the parity bits, it is the final length of the encoded message
        self.n = self.calculate_n()
        # Create the generator matrix
        self.generator_matrix = self.create_generator_matrix()
        # Separate the parity matrix from the generator matrix
        self.parity_matrix = self.generator_matrix[:, self.k:]
        # Encode the message
        self.encoded_message = self.encode_message()

    def calculate_n(self):
        """
        calculate the total number of bits in the final encoded message
        :return: int, the total number of bits in the final encoded message
        """
        # n = k + ceil(log2(k)), which means I take the ceiling of log2(k) as the parity bits
        return self.k + math.ceil(math.log2(self.k + math.ceil(math.log2(self.k + 1))))

    def create_generator_matrix(self):
        """
        Create the generator matrix for the Hamming code
        :return: matrix, the generator matrix
        """
        # Number of parity bits
        m = math.ceil(math.log2(self.k + 1))
        # Identity matrix of size k
        identity_matrix = matrix.identity(GF(2), self.k)
        # Create the parity matrix
        # The parity matrix is a matrix of size m x k, where each row represents a parity bit
        # Instantiate the parity matrix
        parity_matrix = matrix(GF(2), m, self.k)

        for i in range(m):
            for j in range(self.k):
                # For each row i and column j, set the value to be the j-th bit of i+1 (1-based index)
                # The way this is done is by checking if the j-th bit of i+1 is set
                # If it is set, then the value is 1, otherwise it is 0
                # the << operator is a bitwise shift operator, which shifts the bits of the number to the left
                # we do this to get the i-th bit of the number j+1
                # effectively for each row the second part of the expression (j+1) & (1 << i) != 0 will always be
                # the same power of 2, which is the i-th bit of the number j+1
                # we perform a bitwise AND operation between the number j+1 and the power of 2 to get the i-th bit

                parity_matrix[i, j] = (j + 1) & (1 << i) != 0

        generator_matrix = identity_matrix.augment(parity_matrix.transpose())
        return generator_matrix

    def encode_message(self):
        """
        Encode the message using the Hamming code
        :return: the encoded message
        """
        random_bits = ''.join(str(rnd.randint(0, 1)) for _ in range(self.padding))
        header_str = ''.join(str(bit) for bit in self.header)
        m = header_str + ''.join(map(str, self.message)) + random_bits
        message_vector = vector(GF(2), [int(bit) for bit in m])
        encoded_message = message_vector * self.generator_matrix
        return encoded_message


class HammingCodeDecode:
    def __init__(self, encoded_message, parity_matrix):
        """
        :param encoded_message: the message to decode
        :param parity_matrix: the parity matrix used to encode the message
        """
        self.encoded_message = encoded_message
        self.parity_matrix = parity_matrix
        self.H_matrix = self.create_h_matrix()
        self.syndrome = self.calculate_syndrome()
        self.error_count = self.check_errors()
        self.decoded_message = self.decode_message()

    def create_h_matrix(self):
        """
        Create the parity check matrix for the Hamming code
        :return: matrix, the parity check matrix
        """
        p_transposed = self.parity_matrix.transpose()
        num_parity_bits = p_transposed.nrows()
        identity_matrix = matrix.identity(GF(2), num_parity_bits)
        h_matrix = p_transposed.augment(identity_matrix)
        return h_matrix

    def calculate_syndrome(self):
        """
        Calculate the syndrome of the encoded message, which is the result of multiplying the encoded message by the
        parity check matrix
        :return: vector, the syndrome of the encoded message
        """
        encoded_message_vector = vector(GF(2), self.encoded_message)
        syndrome = self.H_matrix * encoded_message_vector.column()
        return syndrome

    def check_errors(self):
        """
        Check the syndrome for errors
        :return: int, the number of errors detected
        """
        return sum(1 for bit in self.syndrome if bit != 0)

    def correct_errors(self):
        """
        Correct the errors in the encoded message based on the syndrome
        """
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
        """
        Decode the message by removing the header and padding
        :return: str, the decoded message
        """
        if self.error_count > 0:
            self.correct_errors()
        header = self.encoded_message[:32]
        k = int(''.join(str(bit) for bit in header), 2)
        original_message = self.encoded_message[32:32 + k]
        return original_message
