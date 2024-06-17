from sage.all import *
import random as rnd

class HammingCodeEncode:
    def __init__(self, message_):
        """
        :param message_: the message to encode
        """
        self.message = [int(bit) for bit in message_]
        self.generator_matrix = self.create_generator_matrix()
        self.encoded_message = self.encode_message()

    @staticmethod
    def create_generator_matrix():
        """
        Create the generator matrix for the Hamming code
        :return: matrix, the generator matrix
        """
        # Number of parity bits
        m = 4
        # Identity matrix of size k
        identity_matrix = matrix.identity(GF(2), 11)
        # Create the parity matrix
        parity_matrix = matrix(GF(2), m, 15)

        for i in range(m):
            for j in range(11):
                parity_matrix[i, j] = (j + 1) & (1 << i) != 0

        generator_matrix = identity_matrix.augment(parity_matrix.transpose())
        return generator_matrix

    def encode_message(self):
        """
        Encode the message using the Hamming code
        :return: the encoded message
        """
        final_message = []
        for i in range(0, len(self.message), 7):
            chunk = self.message[i:i+7]
            actual_length = len(chunk)
            if actual_length < 7:
                chunk += [0] * (7 - actual_length)
            header = [int(bit) for bit in bin(actual_length)[2:].zfill(4)]
            padded_message = header + chunk + [0] * (11 - 4 - len(chunk))
            message_vector = vector(GF(2), padded_message)
            encoded_chunk = message_vector * self.generator_matrix
            final_message.extend(encoded_chunk)
        return final_message


class HammingCodeDecode:
    def __init__(self, encoded_message):
        """
        :param encoded_message: the message to decode
        """
        self.encoded_message = encoded_message
        self.H_matrix = self.create_h_matrix()
        self.decoded_message, self.error_count = self.decode_message()

    @staticmethod
    def create_h_matrix():
        """
        Create the parity check matrix for the Hamming code
        :return: matrix, the parity check matrix
        """
        m = 4
        parity_matrix = matrix(GF(2), m, 15)
        for i in range(m):
            for j in range(11):
                parity_matrix[i, j] = (j + 1) & (1 << i) != 0
        identity_matrix = matrix.identity(GF(2), m)
        h_matrix = parity_matrix.augment(identity_matrix)
        return h_matrix

    def calculate_syndrome(self, message):
        """
        Calculate the syndrome of the encoded message
        :param message: the message vector
        :return: vector, the syndrome of the encoded message
        """
        encoded_message_vector = vector(GF(2), message)
        syndrome = self.H_matrix * encoded_message_vector.column()
        return syndrome

    def correct_errors(self, message, syndrome):
        """
        Correct the errors in the encoded message based on the syndrome
        :param message: the message vector
        :param syndrome: the syndrome vector
        :return: corrected message
        """
        syndrome_as_ints = [int(bit) for bit in syndrome.list()]
        error_index = sum(2 ** i * bit for i, bit in enumerate(syndrome_as_ints))
        if error_index > 0 and error_index <= 15:
            message[error_index - 1] = 1 if message[error_index - 1] == 0 else 0
        return message

    def decode_message(self):
        """
        Decode the message by removing the header and padding
        :return: str, the decoded message
        """
        decoded_message = []
        error_count = 0
        for i in range(0, len(self.encoded_message), 15):
            chunk = self.encoded_message[i:i+15]
            syndrome = self.calculate_syndrome(chunk)
            error_count += sum(1 for bit in syndrome if bit != 0)
            corrected_chunk = self.correct_errors(chunk, syndrome)
            header = corrected_chunk[:4]
            k = int(''.join(str(bit) for bit in header), 2)
            original_message = corrected_chunk[4:4 + k]
            decoded_message.extend(original_message)
        # Remove any trailing zeros introduced by padding
        decoded_message = decoded_message[:len(self.encoded_message)//20*12]
        return decoded_message, error_count
