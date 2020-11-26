import random
import time

from clustering import Clustering, Point

def main():
    total_time = 0
    nb_algo = 100

    for algo in range(0, nb_algo):
        points = []
        for i in range(0, 30000):
            points.append(Point(random.randint(0, 30000), random.randint(0, 30000)))

        clusters_position = []
        for i in range(0, 5):
            clusters_position.append((random.randint(0, 30000), random.randint(0, 30000)))

        algorithm = Clustering(points)
        start_time = time.time()
        clusters = algorithm.run(clusters_position)
        end_time = time.time() - start_time
        print("--- %s seconds ---" % (end_time))
        total_time += end_time

    print("--- Totals seconds: %s ---" % (total_time / nb_algo))




    #verify_clusters(clusters)
    

def verify_clusters(clusters):
    for cluster in clusters:
        print(cluster)

    for cluster in clusters:
        for point in cluster.points:
            distances_from_cluster = {}
            for c in clusters:
                distances_from_cluster[Clustering.distance(c, point)] = c

            min_distance_from_cluster = min(distances_from_cluster.keys()) 
            if distances_from_cluster[min_distance_from_cluster] is cluster:
                string = "Good(" + point.__str__() + "): "
                for d in distances_from_cluster:
                    string += "[" + d.__str__() + ": [" + distances_from_cluster[d].x.__str__() + ", " + distances_from_cluster[d].y.__str__() + "] "
                print(string)
            else:
                print("Bad")

if __name__ == '__main__':
    main()