from pprint import pprint
from collections import namedtuple, Counter
import math
import statistics
import functools


def calc_fuel_used(crabs, xc):
    return sum(abs(x - xc) for x in crabs)


def pt1():
    f = open('example.txt')
    # f = open('input.txt')

    line = f.readline()
    crabs = [int(v) for v in line.rstrip().split(',')]
    print(crabs)

    xmin = min(crabs)
    xmax = max(crabs)

    xbest = None
    fbest = None
    for x in range(xmin, xmax+1):
        f = calc_fuel_used(crabs, x)
        # print((x, f))
        if fbest is None or f < fbest:
            fbest = f
            xbest = x

    print(xbest)
    print(fbest)


def pt1cf():
    f = open('example.txt')
    # f = open('input.txt')

    line = f.readline()
    crabs = [int(v) for v in line.rstrip().split(',')]
    print(crabs)

    x = statistics.median(crabs)
    f = calc_fuel_used(crabs, x)

    print(x)
    print(f)


# @functools.cache
def calc_fuel_used_dist(dx):
    # return abs(dx)
    # return sum(range(dx + 1))
    return dx * (dx+1) / 2


def calc_total_fuel_used(crabs, xc):
    # return sum(calc_fuel_used_dist(abs(x - xc)) for x in crabs)
    return sum(
        ((dx := abs(x - xc)) * (dx + 1) / 2)
        for x in crabs)


def pt2():
    # f = open('example.txt')
    f = open('input.txt')

    line = f.readline()
    crabs = [int(v) for v in line.rstrip().split(',')]
    print(crabs)

    xmin = min(crabs)
    xmax = max(crabs)

    xbest = None
    fbest = None
    for x in range(xmin, xmax+1):
        f = calc_total_fuel_used(crabs, x)
        print((x, f))
        if fbest is None or f < fbest:
            fbest = f
            xbest = x

    print(xbest)
    print(fbest)


if __name__ == '__main__':
    # pt1()
    pt1cf()
    # pt2()
