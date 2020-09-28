import time

import numpy as np
import re


class Reader:
    def __init__(self, widow_size, encoding, paths):
        self.window_size = int(widow_size / 2)
        self.encoding = encoding
        self.paths = paths
        self.word_to_index = dict()
        self.index_to_word = dict()
        self.full_text = str()
        self.read()
        self.index()
        t0 = time.time()
        self.result_array = self.build_array()
        print(time.time() - t0)

    def read(self):
        for path in self.paths:
            f = open(path, 'r', encoding=self.encoding)
            self.full_text += f.read()
        self.full_text = re.findall('(\w+|[!?])', self.full_text)

    def index(self):
        current_index = 0
        for word in self.full_text:
            if word not in self.word_to_index.keys():
                self.word_to_index[word] = current_index
                self.index_to_word[current_index] = word
                current_index += 1

    def build_array(self):
        word_count = len(self.word_to_index.keys())
        maximum = len(self.full_text)
        current_word = 0
        cooc_array = np.zeros((word_count, word_count), dtype=int)
        for word in self.full_text:
            for ind in range(self.window_size, 0, -1):
                if self.word_in_range_left(current_word, ind):
                    self.add_word_to_coo_ar(cooc_array, word, current_word - ind)
                if self.word_in_range_right(current_word, ind, maximum):
                    self.add_word_to_coo_ar(cooc_array, word, current_word + ind)
            current_word += 1
        return cooc_array

    def word_in_range_left(self, current_word, n):
        return current_word - n >= 0

    def word_in_range_right(self, current_word, n, maximum):
        return current_word + n < maximum

    def add_word_to_coo_ar(self, coo_arr, current_word, ind):
        coo_arr[self.word_to_index.get(current_word)][self.word_to_index.get(self.full_text[ind])] += 1


if __name__ == '__main__':
    Reader(5, 'utf-8', ['LesTroisMousquetairesUTF8.txt', 'LeVentreDeParisUTF8.txt', 'GerminalUTF8.txt'])
