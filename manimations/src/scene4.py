import numpy as np
import population_reservoir
from sample import Action
import heapq as q

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

            out = [key for key, value in reservoir]
            out.sort()
            yield (4, Action.UPDATE, out)

class PopulationReservoirScene(population_reservoir.PopulationReservoir):
    def __init__(self):
        def generate_stream(n):
            rng = np.random.default_rng(1337)
            for _ in range(n):
                yield int(rng.integers(n * n))

        super().__init__(
            sample_bottomk,
            generate_stream(20),
            3,
            np.random.default_rng(841),
        )
