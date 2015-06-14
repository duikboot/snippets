from itertools import izip


def find_(seq, target):
    for i, value in enumerate(seq):
        if value == target:
            break
    else:
        return -1
    return i


if __name__ == "__main__":
    keys = ["a", "b", "c"]
    values = [1, 2, 3, 4]

    seq = xrange(2, 30)

    print(find_(seq, 28))
    print(find_(seq, 38))

    d = izip(keys, values)

    for i in d:
        print(i)

    print(dict(izip(keys, values)))

