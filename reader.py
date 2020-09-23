import numpy as np
import re


class Reader:
    def __init__(self, widow_size, encoding, paths):
        self.widow_size = widow_size
        self.encoding = encoding
        self.paths = paths
        self.word_index = dict()
        self.text_list = list()
        self.read()
        self.index()


    def read(self):
        for path in self.paths:
            f = open(path, 'r', encoding=self.encoding)
            self.text_list.append(f.read())

    def index(self):
        current_index = 0
        for text in self.text_list:
            text_split = re.split("[.!?,\-';:()\n\" «»]+", text)
            text_split = filter(None, text_split)
            print(text_split)
            for word in text_split:
                if word not in self.word_index.keys():
                    self.word_index[word] = current_index
                    current_index += 1
            print(self.word_index)


    def match(self):
        pass


if __name__ == '__main__':
    Reader(5, 'utf-8', ['test.txt', 'LesTroisMousquetairesUTF8.txt'])
