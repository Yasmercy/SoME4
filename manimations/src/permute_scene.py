import numpy as np
import pseudocode
import sample


class PermuteScene(pseudocode.Pseudocode):
    def __init__(self):
        def generate_stream(n):
            rng = np.random.default_rng(1337)
            for _ in range(n):
                yield int(rng.integers(n * n))

        super().__init__(
            sample.sample_permute,
            sample.program_permute,
            generate_stream(10),
            5,
            np.random.default_rng(1234),
        )
