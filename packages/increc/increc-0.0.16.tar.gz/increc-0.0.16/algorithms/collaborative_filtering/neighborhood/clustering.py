from random import sample
from algorithms.collaborative_filtering.neighborhood import NeighborhoodCF
from data_structures import DynamicArray
from utils import knn


class Clustering(NeighborhoodCF):
    """
    Description
        Clustering algorithm which extends NeighborhoodCF.
    """
    def __init__(
        self, neighbors=[], n_neighbors=5, treshold=0.5, clusters=[],
            centroids=[], cluster_map=[]):
        """
        Description
            Clustering's constructor.

        Arguments
            :param neighbors: The neighborhood model.
            :type neighbors: list
            :param treshold: A minimum similarity which pairs need to have for
                clusters.
            :type treshold: float
            :param clusters: The cluster model.
            :type clusters: list
            :param centroids: The centroids model.
            :type centroids: list
            :param cluster_map: The inverted index of elements to their cluster
            :type cluster_map: dictionary
        """
        self.th = treshold
        self.centroids = self._init_model(centroids, self._init_centroids)
        self.clusters = self._init_model(clusters, self._init_clusters)
        self.cluster_map = self._init_model(
            cluster_map, self._init_cluster_map)
        super().__init__(neighbors, n_neighbors)

    def _init_centroids(self, elements):
        """
        Description
            A function which computes and returns an initial centroid.

        Arguments
            :param elements: The candidates to centroids.
            :type elements: set
        """
        if len(elements) == 0:
            return []
        return sample(elements, 1)

    def _init_clusters(self, elements):
        """
        Description
            A function which computes and returns the initial cluster.

        Arguments
            :param elements: The set to form clusters by.
            :type elements: set
        """
        clusters = [set() for centroid in self.centroids]
        for element in elements:
            sims = [self.similarity_between(
                element, centroid) for centroid in self.centroids]
            max_sim = max(sims)
            if max_sim < self.th:
                self.centroids.append(element)
                clusters.append({element})
            else:
                centroid_index = sims.index(max_sim)
                clusters[centroid_index].add(element)
        return clusters

    def _init_cluster_map(self, elements):
        """
        Description
            A function which computes and returns an inverted index
            which maps elements to their clusters.

        Arguments
            :param elements: The set to form the inverted index by.
            :type elements: set
        """
        cluster_map = dict()
        for element in elements:
            for index, cluster in enumerate(self.clusters):
                if element in cluster:
                    cluster_map[element] = index
                    break
        return cluster_map

    def _init_neighborhood(self):
        """
        Description
            A function which computes and returns the neighborhood
            model which is a DynamicArray object.
        """
        neighbors = DynamicArray(
            default_value=lambda: DynamicArray(default_value=lambda: list()))
        for cluster in self.clusters:
            cluster_neighborhood = self._init_neighborhood_cluster(cluster)
            neighbors.append(cluster_neighborhood)
        return neighbors

    def _init_neighborhood_cluster(self, candidate_set):
        """
        Description
            A function which computes and returns the neighborhood
            for a cluster which is a DynamicArray object.

        Argument
            :param candidate_set: The cluster.
            :type candidate_set: DynamicArray
        """
        neighbors = DynamicArray(
            [self._neighborhood(
                ide, candidate_set
                ) for ide in candidate_set], default_value=lambda: list())
        return neighbors

    def _neighborhood(self, ident, candidate_set):
        """
        Description
            A function which computes and returns the neighborhood
            of an element inside a cluster which is a DynamicArray object.

        Argument
            :param ident: The element to calculate the neighborhood for.
            :type ident: int
            :param candidate_set: The cluster.
            :type candidate_set: DynamicArray
        """
        candidates = candidate_set.difference({ident})
        return knn(ident, candidates, self.n_neighbors,
                   self.similarity_between)

    def neighborhood_of(self, identifier):
        """
        Description
            A function which returns the neighborhood of an
            element.

        Argument
            :param ident: Element of which we want to return the neighborbood.
            :type ident: int
        """
        try:
            cluster_index = self.cluster_map[identifier]
            position = list(self.clusters[cluster_index]).index(identifier)
            return self.neighbors[cluster_index][position]
        except KeyError:
            return []

    def increment(self, identifier):
        """
        Description
            A function which increments the current cluster model
            for a new entry.

        Arguments
            :param identifier: An element of a rating.
            :type identifier: int
        """
        sims = [self.similarity_between(
            identifier, centroid) for centroid in self.centroids]
        try:
            max_sim = max(sims)
        except ValueError:
            max_sim = 0
        if max_sim < self.th:
            self.centroids.append(identifier)
            self.clusters.append({identifier})
            self.cluster_map[identifier] = len(self.clusters) - 1
        else:
            centroid_index = sims.index(max_sim)
            self.clusters[centroid_index].add(identifier)
            self.cluster_map[identifier] = centroid_index
            cluster = self.clusters[centroid_index]
            self.neighbors[centroid_index] = self._init_neighborhood_cluster(
                cluster)
