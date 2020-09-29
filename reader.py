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
