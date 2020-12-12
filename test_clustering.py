import random
import time
import numpy

#from clustering import Clustering, Point
from clustering_build import Clustering, Point


def main():
    total_time = 0
    nb_algo = 1
    nb_elements = 30000
    nb_dimension = 3000
    nb_cluster = 5
    avg_sec_per_it = 0
    avg_runtime = 0

    points = []
    for i in range(0, nb_elements):
        points.append(Point(numpy.array([random.randint(0, nb_elements) for c in range(nb_dimension)])))
        if (i/nb_elements) * 100 % 5 == 0:
            print("Generation: {}%".format((i/nb_elements) * 100))
    
    #points = numpy.array(points)

    print("Points generated")

    for algo in range(0, nb_algo):
        clusters_coordinates = []
        for i in range(0, nb_cluster):
            clusters_coordinates.append([random.randint(0, nb_elements) for c in range(nb_dimension)])


        algorithm = Clustering()
        start_time = time.time()
        clusters = algorithm.run(points, clusters_coordinates)
        end_time = time.time() - start_time
        print("--- {} Algorithm | {} Iterations ---".format(algo + 1, algorithm.last_nbIteration))
        sec_per_it = algorithm.last_runtime / algorithm.last_nbIteration
        avg_sec_per_it += sec_per_it
        avg_runtime += algorithm.last_runtime
        print(algorithm.iterations_stats)
        print("--- %s seconds per iterations ---" % sec_per_it)
        print("--- %s seconds ---" % (end_time))
        total_time += end_time

    #verify_clusters(clusters)

    print("--- Copy time: {} | {}%  ---".format(Clustering.time_distance_deepcopy, Clustering.time_distance_deepcopy * 100 / total_time))
    print("--- Substract time: {} | {}% ---".format(Clustering.time_distance_substract, Clustering.time_distance_substract * 100 / total_time))
    print("--- Power time: {} | {}% ---".format(Clustering.time_distance_power, Clustering.time_distance_power * 100 / total_time))
    print("--- Sum time: {} | {}% ---".format(Clustering.time_distance_sum, Clustering.time_distance_sum * 100 / total_time))
    print("--- Evaluate time: {} | {}% ---".format(Clustering.time_evaluating, Clustering.time_evaluating * 100 / total_time))
    other_time = Clustering.runtime - Clustering.time_distance_deepcopy - Clustering.time_evaluating - Clustering.time_distance_power - Clustering.time_distance_sum - Clustering.time_distance_substract
    print("--- Average seconds/iteration: {} ---".format(avg_sec_per_it / nb_algo))
    print("--- Average runtime: {} ---".format(avg_runtime / nb_algo))
    print("--- Totals seconds | Other: {} | {}% ---".format(Clustering.runtime,  other_time * 100 / Clustering.runtime))



def verify_clusters(clusters):
    for cluster in clusters:
        for point in cluster.points:
            distances_from_cluster = {}
            for c in clusters:
                distances_from_cluster[Clustering.distance(c, point)] = c

            min_distance_from_cluster = min(distances_from_cluster.keys())
            if distances_from_cluster[min_distance_from_cluster] is cluster:
                pass
            else:
                print("Bad")
                print(distances_from_cluster.items())


if __name__ == '__main__':
    main()
