import glob
from itertools import chain


def from_logs(fnames):
    yield from (open(file) for file in fnames)

if __name__ == '__main__':
    lines = chain.from_iterable(from_logs(glob.glob("*py")))
    [print(i, end=" ") for i in lines]
