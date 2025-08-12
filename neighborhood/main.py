import heapq

import igraph

import numpy as np


def exp(theta=1):
    """
    Samples a value X ~ Exp(theta)
    @param theta = EV[ Exp(theta) ]
    """

    return -theta * np.log(np.random.random())


def sample_k_hop(g: igraph.Graph, n: int, k: int = 2) -> list[list[int]]:
    """
    For each vertex, samples n nodes uniformly from the k-hop.
    This runs in O(k(nlogn + m)) time.

    @param g, an undirected unweighted graph where the node ids are continuous
    @param n, the sample size for each node
    @param k, the neighborhood depth to sample from
    @returns a list of samples S(v) subset N_k(v), where |S(v)| =  min(n, N_k(v))
    """

    N = g.vcount()
    samples = [list() for _ in range(N)]

    def _sample_k_hop():
        """One iteration of the algorithm (i.e. n = 1)"""
        h = g.copy()

        # trackers for what is already done
        sampled = [False] * N
        removed = [False] * N
        # the heap with the random exponentially distributed weights
        heap = [(exp(), v) for v in range(N)]
        heapq.heapify(heap)

        while heap:
            # finding the smallest element
            v = heapq.heappop(heap)
            if removed[v]:
                continue

            # add v as the sample for u in S = N_k(v)
            S = h.neighborhood(v, order=k, mindist=1)
            for u in S:
                if sampled[u] or v in samples[u]:
                    continue
                samples[u].append(v)

                # remove S + v from the heap
                sampled[u] = True
                removed[u] = True

            # remove S + v from the edgelist
            h.es.select(_to=S).delete()
            h.es.select(_source=v).delete()

    for _ in range(n):
        _sample_k_hop()

    return samples


def main():
    # TODO: do some sort of test
    pass


if __name__ == "__main__":
    main()
