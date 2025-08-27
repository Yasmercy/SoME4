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
    "resevoir = init_resevoir()",
    "for item in stream:",
    "    add(resevoir, item)",
    "permute(resevoir)",
    "truncate(resevoir, k)",
]


def sample_permute(stream, k, rng):
    # 1. Initialize reservoir
    reservoir = []
    yield (0, Action.INIT, reservoir)

    for value in stream:
        # 2. Read item from stream
        yield (1, Action.READ, value)

        # 3. Add to reservoir
        reservoir.append(value)
        yield (2, Action.UPDATE, [(0, x) for x in reservoir])

    # 4. Permute reservoir
    reservoir = rng.permutation(reservoir)
    for _ in range(len(reservoir)):
        yield (3, Action.RAND, rng.random())
    yield (3, Action.UPDATE, [(0, x) for x in reservoir])

    # 5. Truncate reservoir
    reservoir = reservoir[:k]
    yield (4, Action.UPDATE, [(0, x) for x in reservoir])


program_bottomk = [
    "resevoir = init_resevoir()",
    "for item in stream:",
    "    key = generate_key()",
    "    if key in lowest_k_keys(resevoir):",
    "        add_to_resevoir(item, key)",
]


def sample_bottomk(stream, k, rng):
    # 1. Initialize reservoir
    reservoir = []
    yield (0, Action.INIT, reservoir)

    for value in stream:
        # 2. Read item from stream
        yield (1, Action.READ, value)

        # 3. Generate a random key
        key = rng.random()
        yield (2, Action.RAND, key)

        # 4. Check if key is in bottom k
        yield (3, Action.BRANCH, None)
        if len(reservoir) < k or key < -reservoir[0][0]:
            item = (-key, value)

            # 5. Add to resevoir
            q.heappush(reservoir, item)
            if len(reservoir) > k:
                q.heappop(reservoir)

            out = [x for x in reservoir]
            out.sort()
            yield (4, Action.UPDATE, out)


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
