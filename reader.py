import numpy as np
import re
import time


class Reader:
    def __init__(self, window_size, encoding, paths):
        self.window_size = int(window_size / 2)
        self.encoding = encoding
        self.paths = paths
        self.word_to_index = dict()
        self.index_to_word = dict()
        self.full_text = str()
        self.read()
        self.index()
        t0 = time.time()
        self.result_array = self.build_array()
        print('fini en ' + str(time.time() - t0))

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

    def get_context(self, wordIndex, size_of_corpus):
        contexte = [self.full_text[x] for x in range(max(0, wordIndex - self.window_size),
                                                     max(wordIndex + 1,
                                                     min(wordIndex + self.window_size + 1, size_of_corpus )))
                    if wordIndex != x]
        return contexte

    def build_array(self):
        size_of_corpus = len(self.index_to_word)
        length_fulltext = len(self.full_text)
        M = np.zeros((size_of_corpus, size_of_corpus), dtype=int)
        for i, word in enumerate(self.full_text):
            mot_contexte = self.get_context(i, length_fulltext)
            for words in mot_contexte:
                j = self.word_to_index[words]
                M[self.word_to_index[word]][j] += 1



        print(M)

        return M


if __name__ == '__main__':
    Reader(5, 'utf-8', ['LesTroisMousquetairesUTF8.txt'])
