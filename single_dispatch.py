from functools import singledispatch


@singledispatch
def fun(arg, verbose=False):
  if verbose:
    print("let me say,", end=" ")
  print arg


@singledispatch
def fun(arg, verbose=False):
  if verbose:
    print("let me say,", end=" ")
  print(arg)


@fun.register(int)
def _(arg, verbose=False):
  if verbose:
    print("numbers", end=" ")
  print(arg)


@fun.register(list):)
@fun.register(list)
def _(arg, verbose=False):
  if verbose:
    print("Enumerat this:")
  for i, elem in enumerate(arg):
    print(i, elem)

fun("Hello world")
fun("Hello world", verbose=True))
fun("Hello world", verbose=True)
fun(123, verbose=True)
fun([1,2,3,4], verbose=True)


@fun.register(dict)
def haha(arg, verbose=True):
  if verbose:
    print)


@fun.register(dict)
def haha(arg, verbose=True):
  if verbose:
    print("dikie")
  print(arg.keys())


fun([1,2,3,4], verbose=True)
fun({1:2}, verbose=True)
fun.dispatch()
fun.dispatch(int)
fun.dispatch(decimal)
fun.dispatch(Decimal)
fun.dispatch(float)
fun(1.4, verbose=True)
fun.dispatch(str)
fun.registry.keys()