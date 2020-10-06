import numpy as np


class Trainer:
    def __init__(self, researched_word, co_occurence_matrix, index_to_word, word_to_index):
        self.co_occurence_matrix = co_occurence_matrix
        self.index_to_word = index_to_word
        self.word_to_index = word_to_index
        self.researched_word = researched_word
        self.researched_word_ind = word_to_index.get(researched_word)
        print(self.researched_word_ind)
        self.result_matrix = ()

    def training(self, training_type=2):

        if training_type == 1:
            self.prod_scalaire()
        elif training_type == 2:
            self.least_square()
        elif training_type == 3:
            self.city_block()

    def prod_scalaire(self):
        # oli
        pass

    def least_square(self):
        reference_matrix = np.square(np.diff(self.co_occurence_matrix[self.researched_word_ind]))
        print(reference_matrix)
        return [[np.sum(np.square(np.diff(self.co_occurence_matrix[self.researched_word_ind])), np.square(np.diff(row)))]for row in self.co_occurence_matrix]



    def city_block(self):
        # tym
        pass
