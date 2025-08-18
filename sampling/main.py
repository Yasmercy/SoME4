import time

import numpy as np
from matplotlib import pyplot as plt
from permute import sample_permute
from reservoir import sample_botk, sample_jumps


def plot_histogram(seed, collect, n, k, rep=100):
    def generate_stream(n):
        rng = np.random.default_rng(seed)
        index = 0
        while index < n:
            yield (index, rng.integers(n * n))
            index += 1

    counts = np.zeros(n)
    runtime = []
    rng = np.random.default_rng(seed)
    for _ in range(rep):
        start = time.perf_counter_ns()
        sample = collect(generate_stream(n), k, rng)
        end = time.perf_counter_ns()

        runtime.append(end - start)
        for index, _ in sample:
            counts[index] += 1

    _, (ax1, ax2) = plt.subplots(1, 2, tight_layout=True, width_ratios=[1, 3])
    ax1.boxplot(runtime)
    ax2.hist(list(range(n)), weights=counts)
    plt.show()


def main():
    plot_histogram(1234, sample_permute, 10_000, 50)
    plot_histogram(1234, sample_botk, 10_000, 50)
    plot_histogram(1234, sample_jumps, 10_000, 50)


if __name__ == "__main__":
    main()
