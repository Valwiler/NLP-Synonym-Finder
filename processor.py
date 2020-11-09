from collections import Counter
import numpy as np


class Processor:
    def __init__(self, widow_size):
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
        # initialisation du Dictionnaire permettant la conversion d'un index en mot
        self.index_to_word = dict(enumerate(x for x in Counter(self.full_text).keys()))

        # initialisation du Dictionnaire à partir de index_to_word permettant la conversion d'un mot en index
        self.word_to_index = {v: k for k, v in self.index_to_word.items()}

        # convertis chacun des mots du text en sa valeur indexée pour accélérer le traitement des données
        self.indexed_text = [*map(self.get_word_index, self.full_text)]

    # def build_array(self):
    #     wordcount = len(self.word_to_index)
    #
    #     # génération de la matrice Numpy en fonction du nombre de mots unique dans le corpus
    #     co_occurence_matrix = np.zeros((wordcount * wordcount), dtype=int)
    #
    #     for i, word in enumerate(self.indexed_text):
    #         # on va chercher les mots dans la fenêtre de contexte de chaques mots
    #         adjacent_word_list = self.indexed_text[i + 1: i + self.window_size + 1]
    #         # On incrémente le poid de mots à travers le vecteur sélectionné en fonction de sa fréquence
    #         # dans le contexte
    #         for adjacent_word in adjacent_word_list:
    #             co_occurence_matrix[adjacent_word + (word * wordcount)] += 1
    #             co_occurence_matrix[word + (adjacent_word * wordcount)] += 1
    #
    #     co_occurence_matrix = co_occurence_matrix.reshape((wordcount, wordcount))
    #
    #     return co_occurence_matrix

    def build_array(self):
        wordcount = len(self.word_to_index)

        co_occurence_matrix = np.zeros((wordcount * wordcount), dtype=int)

        coocurence_dictionarie = {}

        for word in self.indexed_text:
            for i in range(self.window_size):
                pass
                 #coocurence_dictionarie.

        return co_occurence_matrix


    def get_word_index(self, word):
        return self.word_to_index[word]
