import numpy as np


class Trainer:
    def __init__(self, researched_word, co_occurence_matrix, index_to_word, word_to_index):

        self.co_occurence_matrix = co_occurence_matrix
        self.index_to_word = index_to_word
        self.word_to_index = word_to_index
        self.target_word = researched_word
        self.target_word_index = word_to_index.get(self.target_word)
        self.target_vector = self.co_occurence_matrix[self.target_word_index]
        self.result_matrix = ()

    def training(self, training_type=2):

        if self.target_word in self.index_to_word.values():
            if training_type == 1:
                score = zip([self.prod_scalaire(row) for row in self.co_occurence_matrix],
                            self.word_to_index.keys())
                sort_reverse = True
            elif training_type == 2:
                score = zip([self.least_square(row) for row in self.co_occurence_matrix],
                            self.word_to_index.keys())
                sort_reverse = False
            elif training_type == 3:
                score = zip([self.city_block(row) for row in self.co_occurence_matrix],
                            self.word_to_index.keys())
                sort_reverse = False
            score = list(score)
            score.sort(reverse=sort_reverse)
            score = list(score)
            return score
        else:
            print("ce mot n'existe pas dans le copus")

    def prod_scalaire(self, row):
        return np.sum(np.dot(self.target_vector, row))

    def least_square(self, row):
        return np.square(self.target_vector - row).sum()


def city_block(self):
    # tym
    pass
