import numpy as np
import re


class Reader:
    def __init__(self, widow_size, encoding, paths):
        self.widow_size = int(widow_size / 2)
        self.encoding = encoding
        self.paths = paths
        self.word_index = dict()
        self.index_to_word = dict()
        self.full_text = str()
        self.read()
        self.index()
        self.result_array = self.build_array()
        print('fini')


    def read(self):
        for path in self.paths:
            f = open(path, 'r', encoding=self.encoding)
            self.full_text += f.read()
        self.full_text = list(filter(None, re.split('[\-.,\'\";:«»!?\s]', self.full_text)))

    def index(self):
        current_index = 0
        for word in self.full_text:
            if word not in self.word_index.keys():
                self.word_to_index[word] = current_index
                self.index_to_word[current_index] = word
                current_index += 1

    def build_array(self):
        pass


if __name__ == '__main__':
    Reader(5, 'utf-8', ['LesTroisMousquetairesUTF8.txt'])
