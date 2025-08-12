from permute import sample_permute
from resevoir import sample_botk, sample_jumps


def test_sample(seed, k):
    pass


def main():
    stream = []
    sample_permute(stream, 0)
    sample_botk(stream, 0)
    sample_jumps(stream, 0)


if __name__ == "__main__":
    main()
