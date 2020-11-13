import numpy as np
from data_base import Data_Base as db


class Synonym_Finder:

    def __init__(self, window_size):
        self.data_base = db.getInstance()
        self.length = self.data_base.get_vocabulary_legnth()
        self.coocurence_matrix = np.zeros(self.length * self.length, dtype=int)
        table_name = 'cooc_size' + str(window_size)
        self.cooc_dictionarie = self.data_base.get_coocurence_table(table_name)
        if self.cooc_dictionarie:
            for ids, coocurences in self.cooc_dictionarie.items():
                self.coocurence_matrix[ids[0], ids[1]] = coocurences

    def find_synonym(self, reseacherd_word, number_of_results, training_type):
        pass
        # On assigne le vecteur du mot recherché
        # # if researched_word in self.word_to_index.keys():
        # #     self.target_word_index = self.word_to_index.get(researched_word)
        # # else:
        #     raise ValueError('Mot absent')
        #
        # target_vector = self.co_occurence_matrix[self.target_word_index]
        # training_methods = {0: self.prod_scalaire,
        #                    1: self.least_square,
        #                    2: self.city_block}
        # training_method = training_methods.get(training_type)
        # scores = [training_method(target_vector, row) for row in self.co_occurence_matrix]
        # scores = enumerate(scores)
        # scores = sorted(scores, key=lambda x: x[1], reverse=bool(training_method is self.prod_scalaire))
        # top = list()
        # i = 0
        # # On garde seulement le nombre de synonymme recherché
        # while len(top) < self.result_nb:
        #     if scores[i][0] not in self.stop_list:
        #         top.append(scores[i])
        #     i += 1
        # results = list(zip([self.index_to_word.get(index[0]) for index in top], [scores[1] for scores in top]))
        # return results

    @staticmethod
    def prod_scalaire(vect1, vect2):
        return np.dot(vect1, vect2)

    @staticmethod
    def least_square(vect1, vect2):
        return np.sum((vect1 - vect2) ** 2)

    @staticmethod
    def city_block(vect1, vect2):
        return np.sum(np.absolute(vect1 - vect2))
