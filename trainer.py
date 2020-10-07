from reader import Reader as r
import processor as pr
import numpy as np


class Trainer:
    def __init__(self, researched_word, window_size, encoding, paths):
        self.processor = pr.Processor(window_size)
        self.processor.process_text(r.read(encoding, paths))
        self.co_occurence_matrix = self.processor.result_array
        self.index_to_word = self.processor.index_to_word
        self.word_to_index = self.processor.word_to_index
        self.target_word = researched_word

    def training(self, training_type):
        target_word_index = self.word_to_index.get(self.target_word)
        target_vector = self.co_occurence_matrix[target_word_index]
        sort_reverse = False
        if self.target_word in self.index_to_word.values():
            if training_type == 1:
                scores = [self.prod_scalaire(row, target_vector) for row in self.co_occurence_matrix]
                sort_reverse = True
            elif training_type == 2:
                scores = [self.least_square(target_vector, row) for row in self.co_occurence_matrix]
            elif training_type == 3:
                scores = [self.city_block(target_vector, row) for row in self.co_occurence_matrix]
            scores = enumerate(scores)
            scores = sorted(scores, key=lambda x: x[1], reverse=sort_reverse)
            results = [self.index_to_word.get(score[0]) for score in scores[:9]]
            return results
        else:
            print("ce mot n'existe pas dans le copus")

    def prod_scalaire(self,vect1, vect2):
        return np.sum(np.subtract(vect1, vect2))

    def least_square(self,vect1, vect2):
        return np.square(vect1 - vect2).sum()

    def city_block(self, vect1, vect2):
        return np.sum(np.absolute(vect1 - vect2))
