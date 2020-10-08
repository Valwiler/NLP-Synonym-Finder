from reader import Reader as r
import processor as pr
import numpy as np


class Trainer:
    def __init__(self, researched_word, result_nb, window_size, encoding, paths):
        self.result_nb = result_nb
        self.processor = pr.Processor(window_size)
        self.processor.process_text(r.read(encoding, paths))
        self.co_occurence_matrix = self.processor.result_array
        self.index_to_word = self.processor.index_to_word
        self.word_to_index = self.processor.word_to_index
        if researched_word in self.word_to_index.keys():
            self.target_word_index = self.word_to_index.get(researched_word)
        else:
            raise Exception('Mot absent')
        self.stop_list = r.read('utf-8', ['stopword.txt'], stoplist=True)
        self.stop_list = [self.word_to_index.get(word) for word in self.stop_list if self.word_to_index.get(word)]
        self.stop_list.append(self.target_word_index)

    def training(self, training_type):
        # On assigne le vecteur du mot recherché
        target_vector = self.co_occurence_matrix[self.target_word_index]
        # On crée une variable pour savoir si l'orde de tri doit être inversé
        sort_reverse = False
        # Produit Scalaire
        if training_type == 1:
            scores = [self.prod_scalaire(target_vector, row) for row in self.co_occurence_matrix]
            sort_reverse = True
        # Moindre-carré
        elif training_type == 2:
            scores = [self.least_square(target_vector, row) for row in self.co_occurence_matrix]
        # Manhattan distance
        else:
            scores = [self.city_block(target_vector, row) for row in self.co_occurence_matrix]
        # Tri du score
        scores = enumerate(scores)
        scores = sorted(scores, key=lambda x: x[1], reverse=sort_reverse)
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
        return np.sum(np.dot(vect1, vect2))

    @staticmethod
    def least_square(vect1, vect2):
        return np.square(vect1 - vect2).sum()

    @staticmethod
    def city_block(vect1, vect2):
        return np.sum(np.absolute(vect1 - vect2))
