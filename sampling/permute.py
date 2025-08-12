def sample_permute(stream, k, rng):
    arr = list(stream)
    arr = rng.permutation(arr)
    return arr[:k]
