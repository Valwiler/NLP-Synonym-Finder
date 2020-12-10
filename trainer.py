from collections import Counter
from data_base import Data_Base as db
import reader as r

class Trainer:
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
        self.search_cooccurence()

    def index(self):
        vocab_start = self.data_base.get_vocabulary()
        vocab_start.extend(self.full_text)
        self.index_to_word = dict(enumerate(x for x in Counter(vocab_start).keys()))
        self.index_to_word = {k:v for (k,v) in enumerate(Counter(vocab_start))}
        index_iter = self.word_generator()
        self.data_base.add_words(index_iter)
        self.data_base.commit()
        # initialisation du Dictionnaire à partir de index_to_word permettant la conversion d'un mot en index
        self.word_to_index = {v: k for k, v in self.index_to_word.items()}
        # convertis chacun des mots du text en sa valeur indexée pour accélérer le traitement des données
        self.indexed_text = [*map(self.get_word_index, self.full_text)]

    def word_generator(self):
        for i, w in self.index_to_word.items():
            yield (i, w)

    def search_cooccurence(self):
        word_count = len(self.indexed_text)
        table_name = 'cooc_size' + str(self.window_size)
        self.data_base.create_coocurence_table(table_name)
        cooc_dictionarie = self.data_base.get_coocurence_table(table_name)
        for i, word in enumerate(self.indexed_text):
            limit = min(i + self.window_size, word_count - 1)
            for j in range(limit, i, -1):
                key_value = (word, self.indexed_text[j])
                reversed_key_value = (self.indexed_text[j], word)
                cooc_dictionarie[key_value] = cooc_dictionarie.get(key_value, 0) + 1
                cooc_dictionarie[reversed_key_value] = cooc_dictionarie.get(reversed_key_value, 0) + 1
        self.data_base.update_coocurence(table_name, self.cooccurence_generator(cooc_dictionarie))
        self.data_base.commit()

    def cooccurence_generator(self, cooc_dictionnarie):
        for ids, occurences in cooc_dictionnarie.items():
            yield ids[0], ids[1], occurences

    def get_word_index(self, word):
        return self.word_to_index[word]
