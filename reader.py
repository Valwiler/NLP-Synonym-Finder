import chrono
import numpy as np
import re


class Reader:
    def __init__(self, widow_size, encoding, paths):
        self.chrono = chrono.Chrono()
        self.window_size = int(widow_size / 2)
        self.encoding = encoding
        self.paths = paths
        self.word_to_index = dict()
        self.index_to_word = dict()
        self.full_text = str()
        self.read()
        self.index()
        self.result_array = self.build_array()
        print(self.result_array)

    def read(self):
        self.chrono.start()
        for path in self.paths:
            f = open(path, 'r', encoding=self.encoding)
            self.full_text += f.read()
        self.full_text = re.findall('(\w+|[!?])', self.full_text)
        self.chrono.end()
        self.chrono.log("read time : ")

    def index(self):
        self.chrono.start()
        current_index = 0
        for word in self.full_text:
            if word not in self.word_to_index.keys():
                self.word_to_index[word] = current_index
                self.index_to_word[current_index] = word
                current_index += 1
        self.chrono.end()
        self.chrono.log("Indexing time : ")

    # def build_array(self):
    #     self.chrono.start()
    #     word_count = len(self.word_to_index.keys())
    #     maximum = len(self.full_text)
    #     occurrence_array = np.zeros((word_count, word_count), dtype=int)
    #     for word_ind in range(self.window_size):
    #         self.add_adjacent_words_to_coocurence_array(occurrence_array, self.full_text[word_ind],
    #                                                     self.slice_coocurent_words(0, word_ind,
    #                                                                                word_ind + self.window_size))
    #     for word_ind in range(self.window_size, maximum - self.window_size):
    #         self.add_adjacent_words_to_coocurence_array(occurrence_array, self.full_text[word_ind],
    #                                                     self.slice_coocurent_words(word_ind-self.window_size, word_ind,
    #                                                                                word_ind + self.window_size))
    #     for word_ind in range(maximum - self.window_size, maximum):
    #         self.add_adjacent_words_to_coocurence_array(occurrence_array, self.full_text[word_ind],
    #
    #                                                     self.slice_coocurent_words(word_ind - self.window_size,
    #                                                                                word_ind,
    #                                                                                maximum))
    #     self.chrono.end()
    #     self.chrono.log("occurence array making time : ")
    #     return occurrence_array
    #
    # def slice_coocurent_words(self, begining, middle,  end):
    #     return self.full_text[begining:middle] + self.full_text[middle+1:end+1]
    #
    # def add_adjacent_words_to_coocurence_array(self, occurrence_array, current_word, coocurent_words):
    #     for word in coocurent_words:
    #         occurrence_array[self.word_to_index.get(current_word)][self.word_to_index.get(word)] += 1

    # def build_array(self):
    #     self.chrono.start()
    #     maximum = len(self.full_text)
    #     co_occurence_matrix = self.initialise_co_occurence_matrix()
    #     current_word_ind = 0;
    #     for word in self.full_text:
    #         self.add_adjacent_words_to_co_ocurence_array(co_occurence_matrix, word,
    #                                                      self.slice_adjacent_words(current_word_ind,
    #                                                                                current_word_ind + self.window_size
    #                                                                                if current_word_ind + self.window_size < maximum
    #                                                                                else maximum))
    #         current_word_ind += 1
    #     self.chrono.end()
    #     self.chrono.log("co_occurence time : ")
    #     return co_occurence_matrix
    #
    # def slice_adjacent_words(self, begining, end):
    #     return self.full_text[begining + 1:end + 1]
    #
    # def initialise_co_occurence_matrix(self):
    #     wordcount = len(self.word_to_index.keys())
    #     return np.zeros((wordcount, wordcount), dtype=int)
    #
    # def add_adjacent_words_to_co_ocurence_array(self, co_occurence_matrix, current_word, coocurent_words):
    #     for adjacent_word in coocurent_words:
    #         co_occurence_matrix[self.word_to_index.get(current_word)][self.word_to_index.get(adjacent_word)] += 1
    #         co_occurence_matrix[self.word_to_index.get(adjacent_word)][self.word_to_index.get(current_word)] += 1

    def build_array(self):
        self.chrono.start()
        co_occurence_word_list = [self.full_text[i + 1: i + self.window_size + 1] for i, word in
                                  enumerate(self.full_text)]
        self.chrono.end()
        self.chrono.log("Adjacent words defenition time : ")
        co_occurence_matrix = self.initialise_co_occurence_matrix()
        self.chrono.start()
        current_word = 0
        for words in co_occurence_word_list:
            for adjacent_word in words:
                current_word_ind = self.word_to_index.get(self.full_text[current_word])
                current_adjacent_word_ind = self.word_to_index.get(adjacent_word)
                co_occurence_matrix[current_word_ind][current_adjacent_word_ind] += 1
                co_occurence_matrix[current_adjacent_word_ind][current_word_ind] += 1
            current_word += 1
        self.chrono.end()
        self.chrono.log("co_occurence time : ")
        return co_occurence_matrix

    def initialise_co_occurence_matrix(self):
        wordcount = len(self.word_to_index.keys())
        return np.zeros((wordcount, wordcount), dtype=int)


if __name__ == '__main__':
    Reader(4, 'utf-8', ['LesTroisMousquetairesUTF8.txt', 'LeVentreDeParisUTF8.txt', 'GerminalUTF8.txt'])
    # Reader(4, 'utf-8', ['coucou.txt'])
