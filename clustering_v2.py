import numpy
import time
import threading


class DistanceCalculationThread(threading.Thread):
    def __init__(self, points, clusters):
        threading.Thread.__init__(self)
        self.points = points
        self.clusters = clusters

    def run(self):
        # print(self.name + " has started with %s points" % len(self.points))
        for point in self.points:
            distances_from_cluster = {}
            for cluster in self.clusters:
                d = Clustering.distance(cluster, point)
                distances_from_cluster[d] = cluster

            min_distance_from_cluster = min(distances_from_cluster.keys())
            distances_from_cluster[min_distance_from_cluster].points.append((point, min_distance_from_cluster))
        # print(self.name + " has ended")


class Point:

    def __init__(self, coordinates):
        self.coordinates = coordinates

    def __sub__(self, other):
        return Point(numpy.subtract(self.coordinates, other.coordinates))

    def __isub__(self, other):
        self.coordinates -= other.coordinates
        return self

    def __add__(self, other):
        return Point(numpy.add(self.coordinates, other.coordinates))

    def __iadd__(self, other):
        self.coordinates += other.coordinates
        return self

    def __pow__(self, other):
        if isinstance(other, int):
            return Point(numpy.power(self.coordinates, other))
        else:
            return Point(numpy.power(self.coordinates, other.coordinates))

    def __ipow__(self, other):
        if isinstance(other, int):
            self.coordinates **= other
        else:
            self.coordinates **= other.coordinates

        return self

    def __truediv__(self, other):
        if isinstance(other, int):
            return Point(numpy.divide(self.coordinates, other))
        else:
            return Point(numpy.divide(self.coordinates, other.coordinates))

    def __itruediv__(self, other):
        if isinstance(other, int):
            self.coordinates /= other
        else:
            self.coordinates /= other.coordinates

        return self

    def __eq__(self, other):
        return numpy.equal(self.coordinates, other.coordinates).all()

    def __hash__(self):
        return tuple(self.coordinates).__hash__()

    def __str__(self):
        return str(self.coordinates)


class Mot(Point):
    def __init__(self, identity, coordinates):
        super().__init__(coordinates)
        self.identity = identity


class Cluster(Point):
    """
    position: Object contains x and y with position[0] and position[1]
    points: Iterable object containing all points with their distance from position
            Type: list of tuple with the following format: (point, distance)
    """

    def __init__(self, coordinates, points):
        super().__init__(coordinates)
        self.points = points

    def evaluate_position(self):
        total_point = Point(numpy.zeros(len(self.coordinates)))
        for point in self.points:
            total_point = total_point + point[0]
        mean_point = total_point
        mean_point = mean_point / len(self.points)
        self.coordinates = mean_point.coordinates

    def __eq__(self, other):
        return super().__eq__(other) and self.points == other.points

    def __str__(self):
        string = super().__str__()
        for point in self.points:
            string += '\n' + point[0].__str__() + ": " + point[1].__str__()
        return string


class Clustering:
    time_distance_deepcopy = 0
    time_distance_substract = 0
    time_distance_power = 0
    time_distance_sum = 0
    time_evaluating = 0
    runtime = 0
    """
    points: Iterable object containing all the points recommended type Point
    """

    def __init__(self, points):
        self.points = points
        self.clusters = []
        self.last_runtime = 0
        self.last_nbIteration = 0

    @staticmethod
    def distance(a, b):
        d_start_time = time.time()
        ajusted_coordinates = Point(numpy.copy(a.coordinates))
        Clustering.time_distance_deepcopy += time.time() - d_start_time

        d_start_time = time.time()
        ajusted_coordinates -= b
        Clustering.time_distance_substract += time.time() - d_start_time

        d_start_time = time.time()
        ajusted_coordinates **= 2
        Clustering.time_distance_power += time.time() - d_start_time

        d_start_time = time.time()
        d = numpy.sum(ajusted_coordinates.coordinates)
        Clustering.time_distance_sum += time.time() - d_start_time

        return d

    @staticmethod
    def distance2(a, b):
        return numpy.sum((a[:, None, :] - b[None, :, :]) ** 2)

    def run(self, clusters_coodinates):
        start_time = time.time()
        self._init_clusters(clusters_coodinates)

        nb_iteration = 0
        # Emulating a do-while loop
        while True:
            nb_iteration += 1
            print("Iteration %s" % nb_iteration)
            old_clusters = []
            for cluster in self.clusters:
                old_clusters.append(Cluster(cluster.coordinates, cluster.points))

            self._clear_clusters()
            self._allocate_point_to_cluster2()
            self._evaluate_clusters()

            if old_clusters == self.clusters:
                break

        self.last_nbIteration = nb_iteration
        self.last_runtime = time.time() - start_time
        Clustering.runtime += self.last_runtime
        return self.clusters

    def _init_clusters(self, clusters_coodinates):
        self.clusters.clear()
        for coordinates in clusters_coodinates:
            self.clusters.append(Cluster(coordinates, []))

    def _clear_clusters(self):
        for cluster in self.clusters:
            cluster.points.clear()

    def _allocate_point_to_cluster(self):
        for point in self.points:
            distances_from_cluster = {}
            for cluster in self.clusters:
                d = Clustering.distance(cluster, point)
                distances_from_cluster[d] = cluster

            min_distance_from_cluster = min(distances_from_cluster.keys())
            distances_from_cluster[min_distance_from_cluster].points.append((point, min_distance_from_cluster))

    def _allocate_point_to_cluster2(self):
        threads = []
        nb_threads = 10
        nb_points_sublist = min((int)(len(self.points) / nb_threads), 250)
        sub_lists = [self.points[x:x + nb_points_sublist] for x in range(0, len(self.points), nb_points_sublist)]

        for points in sub_lists:
            threads.append(DistanceCalculationThread(points, self.clusters))

        for thread in threads:
            thread.run()

        for thread in threads:
            if thread.is_alive():
                thread.join()

    def _evaluate_clusters(self):
        start_time = time.time()
        for cluster in self.clusters:
            cluster.evaluate_position()
        Clustering.time_evaluating += time.time() - start_time
