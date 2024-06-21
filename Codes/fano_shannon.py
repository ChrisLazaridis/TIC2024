class Compress:
    def __init__(self, message_, code_table_=None, mode='encode'):
        self.message = message_
        self.code_table = code_table_ if code_table_ else {}
        self.frequencies = {}

        if mode == 'encode':
            self.frequencies = self.calculate_frequencies(self.message)
            self.code_table = self.build_code_table(self.frequencies)
        elif mode == 'decode':
            self.message = ''.join(map(str, self.message))
            if not self.code_table:
                raise ValueError("Code table must be provided for decoding")

    @staticmethod
    def calculate_frequencies(message_):
        freq = {}
        message_length = len(message_)
        for char in message_:
            if char in freq:
                freq[char] += 1
            else:
                freq[char] = 1
        for char in freq:
            freq[char] /= message_length
        freq = dict(sorted(freq.items(), key=lambda x: x[1], reverse=True))
        return freq

    def build_code_table(self, frequencies_):
        ct = {symbol: '' for symbol in frequencies_}
        self.build_code_table_rec(frequencies_, ct)
        return ct

    def build_code_table_rec(self, frequencies_rec, code_table_rec):
        if len(frequencies_rec) <= 1:
            return
        frequency_high, frequency_low = self.split_frequency(frequencies_rec)
        for char in frequency_high:
            code_table_rec[char] += '0'
        for char in frequency_low:
            code_table_rec[char] += '1'
        self.build_code_table_rec(frequency_high, code_table_rec)
        self.build_code_table_rec(frequency_low, code_table_rec)

    @staticmethod
    def split_frequency(frequencies_):
        total = sum(frequencies_.values())
        frequency_high = {}
        frequency_low = {}
        running_total = 0
        sorted_items = list(frequencies_.items())
        for i, (char, freq) in enumerate(sorted_items):
            if running_total + freq <= total / 2 or i == 0:
                frequency_high[char] = freq
                running_total += freq
            else:
                frequency_low[char] = freq
        return frequency_high, frequency_low

    @property
    def compress(self):
        enc_mes = ''.join(self.code_table[char] for char in self.message)
        return list(enc_mes)

    def decompress(self):
        reverse_code_table = {v: k for k, v in self.code_table.items()}
        decode_message = ''
        current_code = ''
        for bit in self.message:
            current_code += bit
            if current_code in reverse_code_table:
                decode_message += reverse_code_table[current_code]
                current_code = ''
        return decode_message
