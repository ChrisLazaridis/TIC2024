import numpy as np


class HammingCodeEncode:
    def __init__(self, message_):
        """
        :param message_: the message to encode
        """
        self.message = np.array([int(bit) for bit in message_])
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
        identity_matrix = np.eye(11, dtype=int)
        # Create the parity matrix
        parity_matrix = np.zeros((m, 11), dtype=int)

        for i in range(m):
            for j in range(11):
                parity_matrix[i, j] = (j + 1) & (1 << i) != 0

        generator_matrix = np.hstack((identity_matrix, parity_matrix.T))
        return generator_matrix

    def encode_message(self):
        """
        Encode the message using the Hamming code
        :return: the encoded message
        """
        final_message = []
        for i in range(0, len(self.message), 8):
            chunk = self.message[i:i + 8]
            actual_length = len(chunk)
            padding_length = 8 - actual_length if actual_length < 8 else 0
            if padding_length > 0:
                chunk = np.append(chunk, [0] * padding_length)
            header = [int(bit) for bit in bin(padding_length)[2:].zfill(3)]
            padded_message = header + chunk.tolist() + [0] * (11 - 3 - len(chunk))
            message_vector = np.array(padded_message, dtype=int)
            encoded_chunk = np.dot(message_vector, self.generator_matrix) % 2
            final_message.extend(encoded_chunk)
        return final_message


class HammingCodeDecode:
    def __init__(self, encoded_message):
        """
        :param encoded_message: the message to decode
        """
        self.encoded_message = np.array(encoded_message)
        self.H_matrix = self.create_h_matrix()
        self.decoded_message, self.errors_found, self.errors_corrected = self.decode_message()

    @staticmethod
    def create_h_matrix():
        """
        Create the parity check matrix for the Hamming code
        :return: matrix, the parity check matrix
        """
        m = 4
        parity_matrix = np.zeros((m, 11), dtype=int)

        for i in range(m):
            for j in range(11):
                parity_matrix[i, j] = (j + 1) & (1 << i) != 0

        identity_matrix = np.eye(m, dtype=int)
        h_matrix = np.hstack((parity_matrix, identity_matrix))
        return h_matrix

    def calculate_syndrome(self, message):
        """
        Calculate the syndrome of the encoded message
        :param message: the message vector
        :return: vector, the syndrome of the encoded message
        """
        encoded_message_vector = np.array(message, dtype=int)
        syndrome = np.dot(self.H_matrix, encoded_message_vector) % 2
        return syndrome

    @staticmethod
    def correct_errors(message, syndrome):
        """
        Correct the errors in the encoded message based on the syndrome
        :param message: the message vector
        :param syndrome: the syndrome vector
        :return: corrected message
        """
        syndrome_as_ints = syndrome.tolist()
        error_index = sum(2 ** i * bit for i, bit in enumerate(syndrome_as_ints))
        if 0 < error_index <= 15:
            message[error_index - 1] = int(message[error_index - 1]) ^ 1
        return message

    def decode_message(self):
        """
        Decode the message by removing the header and padding
        :return: str, the decoded message
        """
        decoded_message = []
        errors_found = 0
        errors_corrected = 0
        for i in range(0, len(self.encoded_message), 15):
            error_detected = False
            chunk = self.encoded_message[i:i + 15]
            while True:
                syndrome = self.calculate_syndrome(chunk)
                if np.sum(syndrome) != 0:
                    error_detected = True
                    errors_found += 1
                    chunk = self.correct_errors(chunk, syndrome)
                else:
                    if error_detected:
                        errors_corrected += 1
                    corrected_chunk = chunk
                    break

            header = corrected_chunk[:3]
            padding_length = int(''.join(str(bit) for bit in header), 2)
            original_message = corrected_chunk[3:11 - padding_length]
            decoded_message.extend(original_message)
        # Remove any trailing zeros introduced by padding
        return decoded_message, errors_found, errors_corrected
