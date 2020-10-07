from collections import Counter
import numpy as np
import chrono as ch


class Processor:
    def __init__(self, widow_size):
        self.chrono = ch.Chrono()
        self.full_text = []
        self.window_size = int(widow_size / 2)
        self.word_to_index = dict()
        self.index_to_word = dict()
        self.indexed_text = list()

    def process_text(self, full_text):
        self.full_text = full_text
        self.index()
        self.result_array = self.build_array()

    def index(self):
        self.index_to_word = dict(enumerate(x for x in Counter(self.full_text).keys()))
        self.word_to_index = {v: k for k, v in self.index_to_word.items()}
        self.indexed_text = [*map(self.get_word_index, self.full_text)]

    def build_array(self):
        wordcount = len(self.word_to_index.keys())
        co_occurence_matrix = np.zeros((wordcount * wordcount), dtype=int)
        for i, word in enumerate(self.indexed_text):
            adjacent_word_list = self.indexed_text[i + 1: i + self.window_size + 1]
            for adjacent_word in adjacent_word_list:
                co_occurence_matrix[adjacent_word + (word * wordcount)] += 1
                co_occurence_matrix[word + (adjacent_word * wordcount)] += 1
        co_occurence_matrix = co_occurence_matrix.reshape((wordcount, wordcount))
        return co_occurence_matrix

    def initialise_co_occurence_matrix(self):
        wordcount = len(self.index_to_word.keys())
        return np.zeros((wordcount*wordcount), dtype=int)

    def get_word_index(self, word):
        return self.word_to_index[word]
