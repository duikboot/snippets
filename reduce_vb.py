from functools import reduce

f = lambda x, y: x if (len(x) > len(y)) else y
print(reduce(f, ['a', 'bb', 'cc', 'd']))
# OUT: 'cc'

f = lambda x, y: x if (len(x) >= len(y)) else y
print(reduce(f, ['a', 'bb', 'cc', 'd']))
# OUT: 'bb'
