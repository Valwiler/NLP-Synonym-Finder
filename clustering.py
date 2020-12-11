import time
import numpy

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

    def __ipow__(self, other: int):
        self.coordinates **= other
        return self

    def __truediv__(self, other : int):
        return Point(numpy.divide(self.coordinates, other))

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
        ajusted_coordinates = Point(numpy.copy(a.coordinates))
        ajusted_coordinates -= b
        ajusted_coordinates **= 2
        return numpy.sum(ajusted_coordinates.coordinates)

    def run(self, clusters_coodinates):
        start_time = time.time()
        self._init_clusters(clusters_coodinates)

        nb_iteration = 0
        # Emulating a do-while loop
        while True:
            nb_iteration += 1
            print(str(nb_iteration))
            old_clusters = []
            for cluster in self.clusters:
                old_clusters.append(Cluster(cluster.coordinates, cluster.points))

            self._clear_clusters()
            self._allocate_point_to_cluster()
            self._evaluate_clusters()

            if old_clusters == self.clusters:
                break

        self.last_nbIteration = nb_iteration
        self.last_runtime = time.time() - start_time
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

    def _evaluate_clusters(self):
        for cluster in self.clusters:
            cluster.evaluate_position()
