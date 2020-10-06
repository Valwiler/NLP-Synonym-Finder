import numpy as np


class Trainer:
    def __init__(self, researched_word, co_occurence_matrix, index_to_word, word_to_index):
        self.co_occurence_matrix = co_occurence_matrix
        self.index_to_word = index_to_word
        self.word_to_index = word_to_index
        self.target_word = researched_word
        self.researched_word_ind = word_to_index.get(researched_word)
        self.result_matrix = ()

    def training(self, training_type=2):
        if training_type == 1:
            self.prod_scalaire()
        elif training_type == 2:
            self.least_square()
        elif training_type == 3:
            self.city_block()

    def prod_scalaire(self):
        array = self.co_occurence_matrix
        target_word_index = self.word_to_index.get(self.target_word)
        target_vector = array[target_word_index]
        prod = [np.sum(np.dot(target_vector, rows)) for rows in array]
        index_list = [x for x in range(0, len(prod))]
        results = zip(prod, index_list)
        results = sorted(results, reverse=True, key=lambda i: i[0])
        return results

    def least_square(self):
        target_word_index = self.word_to_index.get(self.target_word)
        target_vector = self.co_occurence_matrix[target_word_index]
        prod = [np.linalg.norm(target_vector - row) for row in self.co_occurence_matrix]
        index_list = [x for x in range(0, len(prod))]
        results = zip(prod, index_list)
        results = sorted(results, key=lambda i: i[0])
        return results


def city_block(self):
        # tym
        pass
