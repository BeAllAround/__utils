from time import time

from collections.abc import Iterable


def is_iter(v):
    try:
        for x in v: break
    except TypeError: return False
    return True

def isiter(v):
    return isinstance(v, Iterable)


def _is_iter(v):
    try: iter(v)
    except TypeError: return False
    return True

def __is_iter(v):
    try: v.__iter__
    except AttributeError: return False
    return True

def benchmark(func, *args):
    SIZE = 100

    for arg in args:
        avg = 0
        for i in range(0, SIZE):
            start = time()
            for i in range(0, 10000):
                func(arg)
            avg += time() - start

        print(str(type(arg)) + ' avg: ', avg / SIZE )

if __name__ == '__main__':

    benchmark(is_iter, [1] * 100000, 1, 'aaa', (1, 3) )

