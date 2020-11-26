class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __sub__(self, other):
        return Point(self.x - other.x, self.y - other.y)

    def __add__(self, other):
        return Point(self.x + other.x, self.y + other.y)

    def __truediv__(self, other):
        if isinstance(other, int):
            return Point(self.x / other, self.y / other)
        else:
            return Point(self.x / other.x, self.y / other.y)

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def __hash__(self):
        return (self.x, self.y).__hash__()

    def __str__(self):
        return "[" + self.x.__str__() + ", " + self.y.__str__() + "]"

class Cluster(Point):
    """
    position: Object contains x and y with position[0] and position[1]
    points: Iterable object containing all points with their distance from position
            Type: dictionnary with point's position as key and distance as value
    """
    def __init__(self, x, y, points):
        super().__init__(x, y)
        self.points = points

    def evaluate_position(self):
        total_point = Point(0, 0)
        for point in list(self.points.keys()):
            total_point = total_point + point
        mean_point = total_point
        mean_point = mean_point / len(self.points)
        self.x = mean_point.x
        self.y = mean_point.y
        

    def __eq__(self, other):
        return super().__eq__(other) and self.points == other.points

    def __str__(self):
        string = super().__str__()
        for point in self.points:
            string += '\n' + point.__str__() + ": " + self.points[point].__str__()
        return string

class Clustering:
    """
    points: Iterable object containing all the points recommended type Point
    """
    def __init__(self, points):
        self.points = points
        self.clusters = []

    @staticmethod
    def distance(a, b):
        ajusted_position = a - b
        return (ajusted_position.x ** 2) + (ajusted_position.y ** 2)

    def run(self, clusters_position):
        self._init_clusters(clusters_position)

        # Emulating a do-while loop
        nb_it = 0
        while True:
            nb_it += 1
            print("Iteration" + str(nb_it))
            old_clusters = []
            for cluster in self.clusters:
                old_clusters.append(Cluster(cluster.x, cluster.y, cluster.points))

            self._clear_clusters()
            self._allocate_point_to_cluster()
            self._evaluate_clusters()

            if old_clusters == self.clusters:
                break
        
        return self.clusters

    def _init_clusters(self, clusters_position):
        self.clusters.clear()
        for position in clusters_position:
            self.clusters.append(Cluster(position[0], position[1], {}))

    def _clear_clusters(self):
        for cluster in self.clusters:
            cluster.points.clear()

    def _allocate_point_to_cluster(self):
        for point in self.points:
            distances_from_cluster = {}
            for cluster in self.clusters:
                distances_from_cluster[Clustering.distance(cluster, point)] = cluster

            min_distance_from_cluster = min(distances_from_cluster.keys()) 
            distances_from_cluster[min_distance_from_cluster].points[point] = min_distance_from_cluster

    def _evaluate_clusters(self):
        for cluster in self.clusters:
            cluster.evaluate_position()
