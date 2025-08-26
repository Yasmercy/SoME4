import numpy as np
import pseudocode
import sample
from assets import *
from manim import *


def generate_stream(n):
    rng = np.random.default_rng(1337)
    for _ in range(n):
        yield int(rng.integers(n * n))


def main():
    stream = generate_stream(10)
    func = sample.sample_permute
    trace = func(stream, 5, np.random.default_rng(1234))

    for lines, action, state in trace:
        print(action, state)
