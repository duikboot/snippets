import functools


def outer(outer_arg):
    def inner(inner_arg):
        return outer_arg + inner_arg
    return inner


def func(a, b, c):
    return a, b, c


p_func = functools.partial(func, 10)
print(p_func(3, 4))

l = ["a", "bb", "f", "sdf"]
print(sorted(l, key=len))
print(sorted(l, key=functools.partial(len)))
