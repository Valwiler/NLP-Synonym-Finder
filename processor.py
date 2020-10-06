from collections import Counter
import numpy as np


class Processor:
    def __init__(self, widow_size, full_text):
        self.full_text = full_text
        self.window_size = int(widow_size / 2)
        self.word_to_index = dict()
        self.index_to_word = dict()
        self.indexed_text = list()

    def process_text(self):
        self.index()
        self.result_array = self.build_array()

    def index(self):
        self.index_to_word = dict(enumerate(x for x in Counter(self.full_text).keys()))
        self.word_to_index = {v: k for k, v in self.index_to_word.items()}
        self.indexed_text = [*map(self.get_word_index, self.full_text)]

    def pos_generator(self, sliced_list):
        current_word = 0
        for set in sliced_list:
            current_word_index = self.indexed_text[current_word]
            for element in set:
                yield current_word_index, element
            current_word += 1

    def build_array(self):
        wordcount = len(self.word_to_index.keys())
        co_occurence_word_list = [self.indexed_text[i + 1: i + self.window_size + 1] for i, word in
                                  enumerate(self.indexed_text)]
        co_occurence_matrix = np.zeros((wordcount * wordcount), dtype=int)
        # # generator = (((i, element) for element in words) for i, words in enumerate(co_occurence_word_list))
        # generator = self.pos_generator(co_occurence_word_list)
        # # generator = self.pos_generator(co_occurence_word_list)
        # for elements in generator:
        #     co_occurence_matrix[elements[0] + (elements[1] * wordcount)] += 1
        #     co_occurence_matrix[elements[1] + (elements[0] * wordcount)] += 1

        for i, word in enumerate(self.indexed_text):
            for adjacent_word in co_occurence_word_list[i]:
                co_occurence_matrix[adjacent_word + (word*wordcount)] += 1
                co_occurence_matrix[word + (adjacent_word*wordcount)] += 1
        co_occurence_matrix = co_occurence_matrix.reshape((wordcount, wordcount))
        print(co_occurence_matrix)
        return co_occurence_matrix

    def initialise_co_occurence_matrix(self):
        wordcount = len(self.word_to_index.keys())
        return np.zeros((wordcount*wordcount), dtype=int)

    def get_word_index(self, word):
        return self.word_to_index[word]
