def fibonacci():
    a, b = 1, 1
    while True:
        yield a
        a, b = b, a + b

if __name__ == '__main__':
    # for a, b in zip(range(20), fibonacci()):
    #     print(a, b)
    from itertools import tee, accumulate
    s, t = tee(fibonacci())
    pairs = zip(t, accumulate(s))
    for _, (fib, total) in zip(range(20), pairs):
        print(fib, total)
