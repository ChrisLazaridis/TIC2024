import random

import numpy as np
from itertools import product


class LinearCode:
    def __init__(self, message_, n=7, mode='encode'):
        m = np.array([int(bit) for bit in message_])
        self.n = n if n >= 7 else exit('n must be greater than or equal to 7')
        self.k = 4
        self.parity_matrix = self.create_parity_matrix()
        self.generator_matrix = self.create_generator_matrix()
        if mode == 'encode':
            self.padding_length = (self.k - ((len(m) + 2) % self.k)) % self.k
            self.header = [int(bit) for bit in bin(self.padding_length)[2:].zfill(2)]
            self.header = np.array(self.header)
            padded_message = np.append(m, [random.randint(0, 1)] * self.padding_length)
            self.message = np.concatenate((self.header, padded_message))
            self.encoded_message = self.encode_message()
            self.encoded_message = [int(bit) for bit in self.encoded_message]
        elif mode == 'decode':
            self.h_matrix = self.create_h_matrix()
            self.words = self.calculate_words()
            self.checker_matrix = self.create_checker_matrix()
            self.encoded_message = m
            self.decoded_message, self.error_count, self.errors_corrected = self.decode_message()
            self.decoded_message = [int(bit) for bit in self.decoded_message]

    def create_generator_matrix(self):
        identity_matrix = np.eye(self.k, dtype=int)
        generator_matrix = np.hstack((identity_matrix, self.parity_matrix))
        return generator_matrix

    def create_parity_matrix(self):
        parity_matrix = np.zeros((self.k, self.n - self.k), dtype=int)
        for i in range(self.k):
            for j in range(self.n - self.k):
                parity_matrix[i, j] = ((j + 1) >> i) & 1
        return parity_matrix

    def encode_message(self):
        final_message = []
        for i in range(0, len(self.message), self.k):
            chunk = self.message[i:i + self.k]
            message_vector = np.array(chunk, dtype=int)
            encoded_chunk = np.dot(message_vector, self.generator_matrix) % 2
            final_message.extend(encoded_chunk)
        return final_message

    def create_h_matrix(self):
        return np.hstack((self.parity_matrix.T, np.eye(self.n - self.k, dtype=int)))

    def calculate_syndrome(self, message__):
        encoded_message_vector = np.array(message__, dtype=int)
        syndrome = np.dot(self.h_matrix, encoded_message_vector) % 2
        return syndrome

    def calculate_words(self):
        words = []
        for word in product([0, 1], repeat=self.k):
            word = np.array(word)
            encoded_word = np.dot(word, self.generator_matrix) % 2
            words.append(encoded_word)
        return words

    def create_checker_matrix(self):
        num_codewords = 2 ** self.k
        num_syndromes = 2 ** (self.n - self.k)
        checker_matrix = np.zeros((num_syndromes, num_codewords), dtype=object)

        for idx, word in enumerate(self.words):
            for error_pos in range(self.n):
                distorted_word = word.copy()
                distorted_word[error_pos] = 1 if distorted_word[error_pos] == 0 else 0  # flip the bit
                syndrome = self.calculate_syndrome(distorted_word)
                syndrome_int = int(''.join(map(str, syndrome)), 2)
                checker_matrix[syndrome_int, idx] = distorted_word.copy()

        return checker_matrix

    def decode_message(self):
        error_count = 0
        errors_corrected = 0
        dm = []

        for i in range(0, len(self.encoded_message), self.n):
            chunk = self.encoded_message[i:i + self.n]
            syndrome = self.calculate_syndrome(chunk)
            syndrome_int = int(''.join(map(str, syndrome)), 2)

            if syndrome_int != 0:
                error_count += 1
                for idx, codeword in enumerate(self.checker_matrix[syndrome_int, :]):
                    if np.array_equal(chunk, codeword):
                        chunk = self.words[idx].copy()
                        errors_corrected += 1
                        break

            dm.extend(chunk[:self.k])

        header = dm[:2]
        padding_length = int(''.join(str(bit) for bit in header), 2)
        if padding_length > 0:
            dm = dm[:-padding_length]
        decoded_message = dm[2:]
        return decoded_message, error_count, errors_corrected
