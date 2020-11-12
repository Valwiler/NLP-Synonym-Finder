from collections import Counter
import numpy as np
import data_base as db
from timeit import default_timer as t
import reader as r


class Processor:
    def __init__(self, widow_size):
        self.full_text = []
        self.window_size = int(widow_size / 2)
        self.word_to_index = dict()
        self.index_to_word = dict()
        self.indexed_text = list()
        self.data_base = db.Data_Base.getInstance()

    def process_text(self, encoding, paths):
        self.full_text = r.Reader.read_text(encoding, paths)
        self.index()
        # self.result_array = self.build_array()

    def index(self):
        debut = t()
        for w in self.full_text:
            self.data_base.add_word(w)
        fin = t()
        self.data_base.commit()
        print(fin - debut)
        # self.index_to_word = self.data_base.get_index_word(self.data_base)
        # self.word_to_index = self.data_base.get_word_index(self.data_base)
        # self.indexed_text = [*map(self.get_word_index, self.full_text)]

    def get_word_index(self, word):
        return self.word_to_index[word]
