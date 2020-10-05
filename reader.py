from numpy.core.defchararray import lower

import chrono
import numpy as np
import re


class Reader:
    def __init__(self, widow_size, encoding, paths):
        self.chrono = chrono.Chrono()
        self.chrono.start()
        self.window_size = int(widow_size / 2)
        self.encoding = encoding
        self.paths = paths
        self.word_to_index = dict()
        self.index_to_word = dict()
        self.full_text = str()
        self.indexed_text = list()
        self.read()
        self.index()
        self.result_array = self.build_array()
        self.chrono.end()
        self.chrono.log(" all process : ")

    def read(self):
        for path in self.paths:
            f = open(path, 'r', encoding=self.encoding)
            self.full_text += f.read()
        self.full_text = lower(re.findall('(\w+|[!?])', self.full_text))

    def index(self):
        current_index = 0
        for word in self.full_text:
            if word not in self.word_to_index.keys():
                self.word_to_index[word] = current_index
                self.index_to_word[current_index] = word
                current_index += 1
            self.indexed_text.append(self.word_to_index.get(word))

    def build_array(self):
        co_occurence_word_list = [self.indexed_text[i + 1: i + self.window_size + 1] for i, word in
                                  enumerate(self.indexed_text)]

        co_occurence_matrix = self.initialise_co_occurence_matrix()
        current_word = 0
        for words in co_occurence_word_list:
            for adjacent_word in words:
                current_word_ind = self.word_to_index.get(self.full_text[current_word])
                #               current_adjacent_word_ind = self.word_to_index.get(adjacent_word)
                co_occurence_matrix[current_word_ind][adjacent_word] += 1
                co_occurence_matrix[adjacent_word][current_word_ind] += 1
            current_word += 1
        return co_occurence_matrix

    def initialise_co_occurence_matrix(self):
        wordcount = len(self.word_to_index.keys())
        return np.zeros((wordcount, wordcount), dtype=int)

    def find_index(self, word):
        return self.word_to_index(word)


if __name__ == '__main__':
    Reader(5, 'utf-8', ['LesTroisMousquetairesUTF8.txt', 'LeVentreDeParisUTF8.txt', 'GerminalUTF8.txt'])
