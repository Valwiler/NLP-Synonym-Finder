import numpy as np


class Trainer:
    def __init__(self, researched_word, co_occurence_matrix, index_to_word, word_to_index):
        self.co_occurence_matrix = co_occurence_matrix
        self.index_to_word = index_to_word
        self.word_to_index = word_to_index
        self.target_word = researched_word
        self.researched_word_ind = word_to_index.get(researched_word)
        print(self.researched_word_ind)
        print(self.target_word)

        self.result_matrix = ()
        self.stop_words = ["le", "la", "les", "de", "du", "des", "l'", "d'", "ma", "me", "mon", "pour", "sur", "j'", "je", "et", "qui","au","aux","the", "et"]

    def training(self, training_type=2):
        target_word_index = self.word_to_index.get(self.target_word)
        target_vector = self.co_occurence_matrix[target_word_index]
        if training_type == 1:
            score = zip([self.prod_scalaire(target_vector, row) for row in self.co_occurence_matrix],
                        self.word_to_index.keys())
        elif training_type == 2:
            score = zip([self.least_square(target_vector, row) for row in self.co_occurence_matrix],
                        self.word_to_index.keys())
        elif training_type == 3:
            score = zip([self.city_block(target_vector, row) for row in self.co_occurence_matrix],
                        self.word_to_index.keys())
        score = sorted(score, reverse=False, key = lambda  i: i[0])

        self.print_synonyme(score,10)
        return score

    def prod_scalaire(self, vect1, vect2):
        return np.sum(np.dot(vect1, vect2))

    def least_square(self, vect1 ,vect2):
        return np.linalg.norm(vect1 - vect2)


    def city_block(self,vect1 , vect2):
        return np.sum(np.absolute(vect1 - vect2))

    def print_synonyme(self, score = (), nb_synonyme = int):
        synonyme = []
        i = 0
        while len(synonyme) != nb_synonyme :
            if score[i][1] not in self.stop_words and score[i][1] != self.target_word:
                synonyme.append(score[i])
            i += 1
        print(synonyme)


