def quicksort(lst):
    """Quicksort over a list-like sequence
    >>> a = [2,1,4,5,6]
    >>> print(quicksort(a))
    [1, 2, 4, 5, 6]
    """
    if len(lst) == 0:
        return lst
    pivot = lst[0]
    pivots = [x for x in lst if x == pivot]
    small = quicksort([x for x in lst if x < pivot])
    large = quicksort([x for x in lst if x > pivot])
    return small + pivots + large


if __name__ == '__main__':
    import doctest
    doctest.testmod()
