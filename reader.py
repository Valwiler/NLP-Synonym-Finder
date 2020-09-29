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
        print(self.result_array)

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

    # def build_array(self):
    #     word_count = len(self.word_to_index.keys())
    #     maximum = len(self.full_text)
    #     current_word = 0
    #     cooc_array = np.zeros((word_count, word_count), dtype=int)
    #     for word in self.full_text:
    #         for ind in range(self.window_size, 0, -1):
    #             if self.word_in_range_left(current_word, ind):
    #                 self.add_word_to_coo_ar(cooc_array, word, current_word - ind)
    #             if self.word_in_range_right(current_word, ind, maximum):
    #                 self.add_word_to_coo_ar(cooc_array, word, current_word + ind)
    #         current_word += 1
    #     return cooc_array
    #
    # def word_in_range_left(self, current_word, n):
    #     return current_word - n >= 0
    #
    # def word_in_range_right(self, current_word, n, maximum):
    #     return current_word + n < maximum
    #
    # def add_word_to_coo_ar(self, coo_arr, current_word, ind):
    #     coo_arr[self.word_to_index.get(current_word)][self.word_to_index.get(self.full_text[ind])] += 1
    #
    # def build_array(self):
    #     word_count = len(self.word_to_index.keys())
    #     maximum = len(self.full_text)
    #     current_word = 0
    #     coocurence_array = np.zeros((word_count, word_count), dtype=int)
    #     for word in self.full_text:
    #         if not self.in_range_left(current_word):
    #             range_left = 0
    #         if not self.in_range_right(current_word, maximum):
    #             range_right = maximum
    #         coocurent_words = self.full_text[range_left:current_word]+self.full_text[current_word+1:range_right+1]
    #         self.add_word_occurence_to_coocurence_array(coocurence_array, word, coocurent_words)
    #         current_word += 1
    #     return coocurence_array
    #
    # def in_range_left(self, current_word):
    #     return current_word - self.window_size >= 0
    #
    # def in_range_right(self, current_word, maximum):
    #     return current_word + self.window_size < maximum
    #
    # def add_word_occurence_to_coocurence_array(self, coocurence_array, current_word, coocurent_words):
    #     for word in coocurent_words :
    #         coocurence_array[self.word_to_index.get(current_word)][self.word_to_index.get(word)] += 1
    #
    #
    # def build_array(self):
    #     word_count = len(self.word_to_index.keys())
    #     maximum = len(self.full_text)
    #     current_word = 0
    #     range_left = current_word - self.window_size
    #     range_right = current_word + self.window_size
    #     occurrence_array = np.zeros((word_count, word_count), dtype=int)
    #     for word in self.full_text:
    #        co_ocurent_words = self.slice_coocurent_words(range_left, current_word) \
    #            if self.in_range_left(range_left) \
    #            else self.slice_coocurent_words( 0, current_word)
    #        co_ocurent_words += self.slice_coocurent_words(current_word + 1, range_right + 1) \
    #             if self.in_range_right(range_right, maximum) \
    #             else self.slice_coocurent_words(current_word + 1, maximum)
    #        self.add_word_occurence_to_coocurence_array(occurrence_array, word, co_ocurent_words)
    #        current_word += 1
    #        range_left += 1
    #        range_right += 1
    #     return occurrence_array

    def build_array(self):
        word_count = len(self.word_to_index.keys())
        maximum = len(self.full_text)
        occurrence_array = np.zeros((word_count, word_count), dtype=int)
        for word_ind in range(self.window_size):
            self.add_word_occurence_to_coocurence_array(occurrence_array, self.full_text[word_ind],
                                                        self.slice_coocurent_words(0, word_ind,
                                                                                   word_ind + self.window_size))
        for word_ind in range(self.window_size, maximum - self.window_size):
            self.add_word_occurence_to_coocurence_array(occurrence_array, self.full_text[word_ind],
                                                        self.slice_coocurent_words(word_ind-self.window_size, word_ind,
                                                                                   word_ind + self.window_size))
        for word_ind in range(maximum - self.window_size, maximum):
            self.add_word_occurence_to_coocurence_array(occurrence_array, self.full_text[word_ind],
                                                        self.slice_coocurent_words(word_ind - self.window_size,
                                                                                   word_ind,
                                                                                   maximum))
        return occurrence_array

    def slice_coocurent_words(self, begining, middle,  end):
        return self.full_text[begining:middle] + self.full_text[middle+1:end+1]

    def add_word_occurence_to_coocurence_array(self, occurrence_array, current_word, coocurent_words):
        for word in coocurent_words:
            occurrence_array[self.word_to_index.get(current_word)][self.word_to_index.get(word)] += 1



if __name__ == '__main__':

    Reader(4, 'utf-8', ['LesTroisMousquetairesUTF8.txt', 'LeVentreDeParisUTF8.txt', 'GerminalUTF8.txt'])
    #Reader(4, 'utf-8', ['coucou.txt'])
