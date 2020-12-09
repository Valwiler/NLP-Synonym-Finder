import numpy as np
import random

from clustering import Mot, Clustering
from data_base import Data_Base as db


class Finder:

    def __init__(self, window_size):
        self.data_base = db.getInstance()
        self.length = self.data_base.get_vocabulary_length()
        self.index_to_word = dict(self.data_base.get_vocabulary())
        self.word_to_index = {v: k for k, v in self.index_to_word.items()}
        self.stop_list = self.data_base.get_stop_list()
        self.co_occurence_matrix = np.zeros((self.length, self.length), dtype=int)
        table_name = 'cooc_size' + str(int(window_size/2))
        self.cooc_dictionarie = self.data_base.get_coocurence_table(table_name)
        if self.cooc_dictionarie:
            for ids, coocurences in self.cooc_dictionarie.items():
                self.co_occurence_matrix[ids[0], ids[1]] = coocurences


    def find_synonym(self, researched_word, number_of_results, training_type):
        if researched_word in self.word_to_index.keys():
            target_word_index = self.word_to_index.get(researched_word)
        else:
            raise ValueError('Mot absent')
        self.stop_list.append(researched_word)
        target_vector = self.co_occurence_matrix[target_word_index]
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
        while len(top) < number_of_results and i < self.length - 1:
            if self.index_to_word.get(scores[i][0]) not in self.stop_list:
                top.append(scores[i])
            i += 1
        results = list(zip([self.index_to_word.get(index[0]) for index in top], [scores[1] for scores in top]))

        return results

    def generate_clusters(self, clusters_coordinates, results_per_cluster):
        mots = [Mot(r, self.co_occurence_matrix[r])for r in range(len(self.co_occurence_matrix))]
        algorithm = Clustering(mots)
        clusters = algorithm.run(clusters_coordinates)
        for cluster in clusters:
            # Sort points from their distance with the cluster's coordinate
            sorted(cluster.points, key=lambda x: x[1])
            # Keep only the n best results (n = results_per_cluster)
            cluster.points = cluster.points.slice(results_per_cluster)
            for mot in cluster.points:
                # Convert the id to the string value of the word
                mot.identity = self.index_to_word.get(mot.identity)
            
        return algorithm
        
    def generate_random_clusters(self, number_of_cluster, results_per_cluster):
        clusters_coordinates = []
        for i in range(0, number_of_cluster):
            coordinates_cluster = [random.randint(0, len(self.co_occurence_matrix)) for c in range(len(self.co_occurence_matrix))]
            clusters_coordinates.append(np.array(coordinates_cluster))

        return self.generate_clusters(clusters_coordinates, results_per_cluster)
            
        

    @staticmethod
    def prod_scalaire(vect1, vect2):
        return np.dot(vect1, vect2)

    @staticmethod
    def least_square(vect1, vect2):
        return np.sum((vect1 - vect2) ** 2)

    @staticmethod
    def city_block(vect1, vect2):
        return np.sum(np.absolute(vect1 - vect2))
