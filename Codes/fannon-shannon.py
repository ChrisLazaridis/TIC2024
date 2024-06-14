class Compress:
    def __init__(self, message, code_table=None, mode='linear_code'):
        """
        Initialize the Compress class based on the mode.

        :param message: str or list, the message to linear_code or decode.
        :param code_table: dict, the code table for decoding.
        :param mode: str, 'linear_code' or 'decode'.
        """
        self.message = message
        self.code_table = code_table if code_table else {}
        self.frequencies = {}

        if mode == 'linear_code':
            self.frequencies = self.calculate_frequencies(self.message)
            self.code_table = self.build_code_table(self.frequencies)
        elif mode == 'decode':
            if not self.code_table:
                raise ValueError("Code table must be provided for decoding")

    def calculate_frequencies(self, message):
        """
        Calculate the frequency of each character in the message.

        :param message: list, the message as a list of characters.
        :return: dict, the frequencies of each character.
        """
        frequencies = {}
        message_length = len(message)
        for char in message:
            if char in frequencies:
                frequencies[char] += 1
            else:
                frequencies[char] = 1
        for char in frequencies:
            frequencies[char] /= message_length
        frequencies = dict(sorted(frequencies.items(), key=lambda x: x[1], reverse=True))
        return frequencies

    def build_code_table(self, frequencies):
        """
        Build the code table based on frequencies.

        :param frequencies: dict, the frequencies of each character.
        :return: dict, the code table.
        """
        code_table = {symbol: '' for symbol in frequencies}
        self.build_code_table_rec(frequencies, code_table)
        return code_table

    def build_code_table_rec(self, frequencies_rec, code_table_rec):
        """
        Recursively build the code table.

        :param frequencies_rec: dict, the frequencies of the remaining characters.
        :param code_table_rec: dict, the code table being built.
        """
        if len(frequencies_rec) <= 1:
            return
        frequency_high, frequency_low = self.split_frequency(frequencies_rec)
        for char in frequency_high:
            code_table_rec[char] += '0'
        for char in frequency_low:
            code_table_rec[char] += '1'
        self.build_code_table_rec(frequency_high, code_table_rec)
        self.build_code_table_rec(frequency_low, code_table_rec)

    def split_frequency(self, frequencies):
        """
        Split the frequencies into two groups.

        :param frequencies: dict, the frequencies of each character.
        :return: tuple of two dicts, the split frequencies.
        """
        total = sum(frequencies.values())
        frequency_high = {}
        frequency_low = {}
        running_total = 0
        sorted_items = list(frequencies.items())
        for i, (char, freq) in enumerate(sorted_items):
            if running_total + freq <= total / 2 or i == 0:
                frequency_high[char] = freq
                running_total += freq
            else:
                frequency_low[char] = freq
        return frequency_high, frequency_low

    def compress(self):
        """
        Encode the message using the code table.

        :return: str, the encoded message.
        """
        encoded_message = ''.join(self.code_table[char] for char in self.message)
        return encoded_message

    def decompress(self):
        """
        Decode the message using the code table.

        :return: str, the decoded message.
        """
        reverse_code_table = {v: k for k, v in self.code_table.items()}
        decode_message = ''
        current_code = ''
        for bit in self.message:
            current_code += bit
            if current_code in reverse_code_table:
                decode_message += reverse_code_table[current_code]
                current_code = ''
        return decode_message


# Example usage
message = "hello world"
compressor = Compress(message=list(message))
frequencies = compressor.frequencies
code_table = compressor.code_table
encoded_message = compressor.compress()

print("\n Frequencies:", frequencies)
print("\n Code Table:", code_table)
print("\n Encoded Message:", encoded_message)

# For decoding
decoder = Compress(encoded_message, code_table=code_table, mode='decode')
decoded_message: str = decoder.decompress()
print("\n Decoded Message:", decoded_message)
decoded_bytes = bytes(decoded_message, 'utf-8')

result = ""

for char_ in decoded_message:
    result+=format(ord(char_), '08b')
print("\n Decoded Bytes:", result)

#binary_representation = ''.join(format(ord(char), '08b')) input_string = for char in decoded_message)
