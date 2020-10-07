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
        if self.target_word in self.index_to_word.values():
            if training_type == 1:
                score = zip([self.prod_scalaire(target_vector, row) for row in self.co_occurence_matrix],
                            self.word_to_index.keys())
                sort_reverse = True
            elif training_type == 2:
                score = zip([self.least_square(target_vector, row) for row in self.co_occurence_matrix],
                            self.word_to_index.keys())
                sort_reverse = False
            elif training_type == 3:
                score = zip([self.city_block(target_vector, row) for row in self.co_occurence_matrix],

                            +                        self.word_to_index.keys())
                sort_reverse = False
            score = list(score)
            score.sort(reverse=sort_reverse)
            score = list(score)
            return score
        else:
            print("ce mot n'existe pas dans le copus")

    def prod_scalaire(self,vect1, vect2):
        return np.sum(np.dot(vect1, vect2))

    def least_square(self,vect1, vect2):
        return np.square(vect1 - vect2).sum()

    def city_block(self, vect1, vect2):
        return np.sum(np.absolute(vect1 - vect2))
