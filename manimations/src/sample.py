import heapq as q
from enum import Enum, auto

import numpy as np


class Action(Enum):
    # initializing the reservoir
    INIT = auto()
    # reading an element from the stream
    READ = auto()
    # updating the reservoir in some way
    UPDATE = auto()
    # generating a random number
    RAND = auto()
    # control flow
    BRANCH = auto()


program_permute = [
    r"\State Initialize reservoir",
    r"\State \textbf{while} read item from stream",
    r"    \State Add item to reservoir",
    r"\State Permute reservoir",
    r"\State Truncate reservoir",
]


def sample_permute(stream, k, rng):
    # 1. Initialize reservoir
    reservoir = []
    yield ([0], Action.INIT, reservoir)

    for value in stream:
        # 2. Read item from stream
        yield ([1], Action.READ, value)

        # 3. Add to reservoir
        reservoir.append(value)
        yield ([2], Action.UPDATE, reservoir)

    # 4. Permute reservoir
    reservoir = rng.permutation(reservoir)
    for _ in range(len(reservoir)):
        yield ([3], Action.RAND, None)
    yield ([3], Action.UPDATE, reservoir)

    # 5. Truncate reservoir
    reservoir = reservoir[:k]
    yield ([4], Action.UPDATE, reservoir)


def sample_botk(stream, k, rng):
    # 1. Initialize reservoir
    reservoir = []
    yield (1, Action.INIT, reservoir)

    for value in stream:
        # 2. Read item from stream
        yield (2, Action.READ, value)

        # 3. Check if reservoir has space
        yield (3, Action.BRANCH, None)
        if len(reservoir) < k:
            # 4. Generate item
            key = rng.random()
            yield (4, Action.RAND, key)

            # 5. Add to the reservoir
            item = (-key, value)
            q.heappush(reservoir, item)
            yield (5, Action.UPDATE, reservoir)
            continue

        # 6. Generate item
        key = rng.random()
        item = (-key, value)
        yield (6, Action.RAND, key)

        # 7. Check if less than maximum
        yield (7, Action.BRANCH, None)
        if key < -reservoir[0][0]:
            # 8. Add to reservoir
            q.heappushpop(reservoir, item)
            yield (8, Action.UPDATE, reservoir)


def sample_jumps(stream, k, rng):
    # 1. Initialize reservoir
    reservoir = []
    yield (1, Action.INIT, reservoir)

    jump = 1
    for value in stream:
        # 2. Read item from stream
        yield (2, Action.READ, value)

        # 3. Check if reservoir has space
        yield (3, Action.BRANCH, None)
        if len(reservoir) < k:
            # 4. Generate item
            key = rng.random()
            yield (4, Action.RAND, key)

            # 5. Add to the reservoir
            item = (-key, value)
            q.heappush(reservoir, item)
            yield (5, Action.UPDATE, reservoir)
            continue

        # 6. Check if we need to keep skipping
        yield (6, Action.BRANCH, None)
        if jump > 1:
            continue

        # 7. Generate item
        max_key = -reservoir[0][0]
        key = max_key * rng.random()
        item = (-key, value)
        yield (7, Action.RAND, key)

        # 8. Add to heap
        q.heappushpop(reservoir, item)
        yield (8, Action.UPDATE, reservoir)

        # 9. Generate new random number
        max_key = -reservoir[0][0]
        jump = int(np.ceil(np.log(rng.random()) / np.log(1 - max_key)))
        yield (9, Action.UPDATE, reservoir)
