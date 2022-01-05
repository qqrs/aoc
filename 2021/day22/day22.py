from pprint import pprint
from collections import namedtuple, Counter
import re
import math
import statistics
import functools
import itertools

import numpy as np


Step = namedtuple('Step', ['sgn', 'box'])
Box = namedtuple('Box', ['x1', 'x2', 'y1', 'y2', 'z1', 'z2'])


def parse_line(line):
    sgn = 1 if line.split(' ')[0] == 'on' else -1
    coords = [int(v) for v in re.findall('-?[0-9]+', line)]
    return Step(sgn, Box(*coords))


def pt1():
    f = open('example.txt')
    # f = open('input.txt')

    steps = [parse_line(line) for line in f]
    steps = [s for s in steps if not any(abs(v) > 50 for v in s.box)]
    steps = [Step(sgn, Box(*[v+50 for v in box])) for sgn, box in steps]

    pprint(steps)

    R = np.zeros((101, 101, 101), dtype=np.bool_)
    for sgn, v in steps:
        R[v.x1:v.x2+1, v.y1:v.y2+1, v.z1:v.z2+1] = (sgn == 1)

    print(np.count_nonzero(R))


def vol(b: Box):
    lengths = (b.x2 - b.x1 + 1), (b.y2 - b.y1 + 1), (b.z2 - b.z1 + 1)
    if any(v <= 0 for v in lengths):
        return 0
    return math.prod(lengths)


def pt2():
    # f = open('example.txt')
    f = open('example2.txt')
    # f = open('input.txt')

    steps = [parse_line(line) for line in f]
    # steps = [s for s in steps if not any(abs(v) > 50 for v in s.box)]

    cubes = Counter()

    for bsgn, b in steps:
        update = Counter()
        for c, csgn in cubes.items():
            d = Box(
                max(b.x1, c.x1), min(b.x2, c.x2),
                max(b.y1, c.y1), min(b.y2, c.y2),
                max(b.z1, c.z1), min(b.z2, c.z2))

            if vol(d) <= 0:
                continue

            update[d] -= csgn

        cubes.update(update)
        if bsgn > 0:
            cubes[b] += bsgn

    z = sum(sgn * vol(b) for b, sgn in cubes.items())
    print(z)
    import ipdb; ipdb.set_trace()


if __name__ == '__main__':
    # pt1()
    pt2()
