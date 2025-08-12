import numpy as np


def sample_permute(stream, k):
    arr = list(stream)
    arr = np.random.permutation(arr)
    return arr[:k]
