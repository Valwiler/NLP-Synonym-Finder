from collections import Counter
from data_base import Data_Base as db
from timeit import default_timer as t
import reader as r


class Processor:
    def __init__(self, widow_size):
        self.full_text = []
        self.window_size = int(widow_size / 2)
        self.word_to_index = dict()
        self.index_to_word = dict()
        self.indexed_text = list()
        self.data_base = db.getInstance()

    def process_text(self, encoding, paths):
        self.full_text = r.Reader.read_text(encoding, paths)
        self.index()
        self.data_base.add_stop_word(r.Reader.read_stoplist())
        # self.result_array = self.build_array()

    def index(self):
        self.index_to_word = dict(enumerate(x for x in Counter(self.full_text).keys()))
        debut = t()
        index_iter = self.word_generator()
        self.data_base.add_words(index_iter)
        self.data_base.commit()
        self.index_to_word = dict(self.data_base.get_vocabulary())
        # initialisation du Dictionnaire à partir de index_to_word permettant la conversion d'un mot en index
        self.word_to_index = {v: k for k, v in self.index_to_word.items()}
        # convertis chacun des mots du text en sa valeur indexée pour accélérer le traitement des données
        self.indexed_text = [*map(self.get_word_index, self.full_text)]
        fin = t()
        print(fin - debut)

    def word_generator(self):
        for w in self.index_to_word.values():
            yield (w,)

    def search_cooccurence(self):
        pass

    def get_word_index(self, word):
        return self.word_to_index[word]
