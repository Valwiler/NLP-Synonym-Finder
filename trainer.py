from reader import Reader as r
import processor as pr
import numpy as np


class Trainer:

    def __init__(self, researched_word, result_nb, window_size, encoding, paths):
        self.result_nb = result_nb
        self.processor = pr.Processor(window_size)
        self.processor.process_text(r.read_text(encoding, paths))
        self.word_to_index = self.processor.word_to_index
        if researched_word in self.word_to_index.keys():
            self.target_word_index = self.word_to_index.get(researched_word)
        else:
            raise ValueError('Mot absent')
        self.co_occurence_matrix = self.processor.result_array
        self.index_to_word = self.processor.index_to_word
        #self.stop_list = r.read_stoplist()
        #self.stop_list = [self.word_to_index.get(word) for word in self.stop_list if self.word_to_index.get(word)]
        #self.stop_list.append(self.target_word_index)

    def training(self, training_type):
        # On assigne le vecteur du mot recherché
        target_vector = self.co_occurence_matrix[self.target_word_index]
        training_methods = {0: self.prod_scalaire,
                           1: self.least_square,
                           2: self.city_block}
        training_method = training_methods.get(training_type)
        scores = [training_method(target_vector, row) for row in self.co_occurence_matrix]
        scores = enumerate(scores)
        scores = sorted(scores, key=lambda x: x[1], reverse=bool(training_method is self.prod_scalaire))
        top = list()
        i = 0
        # On garde seulement le nombre de synonymme recherché
        while len(top) < self.result_nb:
            if scores[i][0] not in self.stop_list:
                top.append(scores[i])
            i += 1
        results = list(zip([self.index_to_word.get(index[0]) for index in top], [scores[1] for scores in top]))
        return results

    @staticmethod
    def prod_scalaire(vect1, vect2):
        return np.dot(vect1, vect2)

    @staticmethod
    def least_square(vect1, vect2):
        return np.sum((vect1 - vect2)**2)

    @staticmethod
    def city_block(vect1, vect2):
        return np.sum(np.absolute(vect1 - vect2))
