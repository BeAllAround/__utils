from time import time


def is_iter(v):
    try:
        for x in v: break
    except TypeError: return False
    return True


def _is_iter(v):
    try: iter(v)
    except TypeError: return False
    return True

def benchmark():
    l = [1] * 1000000

    SIZE = 100
    avg = 0

    for i in range(0, SIZE):
        start = time()
        for i in range(0, 10000):
            is_iter(l)
        avg += time() - start

    print('avg: ', avg / SIZE )

if __name__ == '__main__':

    benchmark()

