import heapq as q

import numpy as np


def sample_botk(stream, k):
    """simple resevoir algorithm"""

    # stores (-key, value) as an item
    resevoir = []
    for value in stream:
        key = np.random.random()
        item = (-key, value)
        if len(resevoir) < k:
            q.heappush(resevoir, item)
        else:
            if key < -resevoir[0]:
                q.heappushpop(resevoir, item)


def sample_jumps(stream, k):
    """same as sample_botk, but with geometric jumps"""

    resevoir = []
    jump = 0

    for value in stream:
        key = np.random.random()
        item = (-key, value)
        if len(resevoir) < k:
            q.heappush(resevoir, item)
        elif jump > 0:
            jump = jump - 1
        else:
            # key ~ U(0, max_key)
            max_key = -resevoir[0][0]
            key = max_key * np.random.random()
            q.heappushpop(resevoir, item)

            jump = int(np.ceil(np.log(np.random.random()) / np.log(1 - max_key)))
