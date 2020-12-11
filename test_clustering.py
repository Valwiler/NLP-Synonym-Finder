import random
import time
import numpy

from clustering_v2 import Clustering, Point


def main():
    total_time = 0
    nb_algo = 1
    nb_elements = 30000
    nb_dimension = 3000
    nb_cluster = 5

    for algo in range(nb_algo):
        points = []
        for i in range(0, nb_elements):
            points.append(Point(numpy.array([random.randint(0, nb_dimension) for c in range(nb_dimension)])))

        clusters_coordinates = []
        for i in range(0, nb_cluster):
            clusters_coordinates.append([random.randint(0, nb_dimension) for c in range(nb_dimension)])

        algorithm = Clustering(points)
        start_time = time.time()
        clusters = algorithm.run(clusters_coordinates)
        end_time = time.time() - start_time
        print("--- %s seconds ---" % (end_time))
        total_time += end_time

    #verify_clusters(clusters)

    print("--- Copy time: {} | {}%  ---".format(Clustering.time_distance_deepcopy,
                                                Clustering.time_distance_deepcopy * 100 / total_time))
    print("--- Substract time: {} | {}% ---".format(Clustering.time_distance_substract,
                                                    Clustering.time_distance_substract * 100 / total_time))
    print("--- Power time: {} | {}% ---".format(Clustering.time_distance_power,
                                                Clustering.time_distance_power * 100 / total_time))
    print("--- Sum time: {} | {}% ---".format(Clustering.time_distance_sum,
                                              Clustering.time_distance_sum * 100 / total_time))
    print("--- Evaluate time: {} | {}% ---".format(Clustering.time_evaluating,
                                                   Clustering.time_evaluating * 100 / total_time))
    other_time = Clustering.runtime - Clustering.time_distance_deepcopy - Clustering.time_evaluating - Clustering.time_distance_power - Clustering.time_distance_sum - Clustering.time_distance_substract
    print("--- Totals seconds | Other: {} | {}% ---".format(Clustering.runtime, other_time * 100 / Clustering.runtime))


def verify_clusters(clusters):
    for cluster in clusters:
        print(cluster)

    for cluster in clusters:
        for point in cluster.points:
            distances_from_cluster = {}
            for c in clusters:
                distances_from_cluster[None] = c

            min_distance_from_cluster = min(distances_from_cluster.keys())
            if distances_from_cluster[min_distance_from_cluster] is cluster:
                string = "Good(" + point.__str__() + "): "
                for d in distances_from_cluster:
                    string += "[" + d.__str__() + ": [" + distances_from_cluster[d].x.__str__() + ", " + \
                              distances_from_cluster[d].y.__str__() + "] "
                print(string)
            else:
                print("Bad")


if __name__ == '__main__':
    main()
