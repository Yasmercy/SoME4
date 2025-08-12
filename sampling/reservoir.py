import heapq as q

import numpy as np


def sample_botk(stream, k, rng):
    """simple resevoir algorithm"""

    reservoir = []
    for value in stream:
        key = rng.random()
        item = (-key, value)
        if len(reservoir) < k:
            q.heappush(reservoir, item)
        elif key < -reservoir[0][0]:
            q.heappushpop(reservoir, item)

    return np.array([v for _, v in reservoir])


def sample_jumps(stream, k, rng):
    """same as sample_botk, but with geometric jumps"""

    reservoir = []
    jump = 1
    for value in stream:
        if len(reservoir) < k:
            key = rng.random()
            item = (-key, value)
            q.heappush(reservoir, item)
        elif jump > 1:
            jump = jump - 1
        else:
            # key ~ U(0, max_key)
            max_key = -reservoir[0][0]
            key = max_key * rng.random()
            item = (-key, value)
            q.heappushpop(reservoir, item)

            max_key = -reservoir[0][0]
            jump = int(np.ceil(np.log(rng.random()) / np.log(1 - max_key)))

    return np.array([v for _, v in reservoir])
