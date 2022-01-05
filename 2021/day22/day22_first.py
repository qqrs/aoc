from pprint import pprint
from collections import namedtuple, Counter
import math
import statistics
import functools
import itertools

import numpy as np

np.set_printoptions(linewidth=240)
np.set_printoptions(edgeitems=20)
np.set_printoptions(formatter={'bool': lambda x: '█' if x else '_'})


Point = namedtuple('Point', ['x', 'y', 'z'])
Step = namedtuple('Step', ['o', 'p', 'q'])


def parse_line(line):
    ontxt, cuboid = line.rstrip().split(' ')
    onoff = 1 if ontxt == 'on' else 0

    pts = [sorted(int(v) for v in dim.split('=')[-1].split('..'))
           for dim in cuboid.split(',')]
    return Step(onoff,
                Point(pts[0][0] + 50, pts[1][0] + 50, pts[2][0] + 50),
                Point(pts[0][1] + 50, pts[1][1] + 50, pts[2][1] + 50))


def pt1():
    # txt = open('example.txt').read()
    txt = open('input.txt').read()

    steps = [parse_line(line) for line in txt.splitlines()]
    steps = [step for step in steps
             if step.p.x >= 0 and step.p.y >= 0 and step.p.z >= 0
             and step.q.x <= 100 and step.q.y <= 100 and step.q.z <= 100]
    pprint(steps)

    R = np.zeros((101, 101, 101), dtype=np.bool_)

    for step in steps:
        R[step.p.x:step.q.x+1, step.p.y:step.q.y+1, step.p.z:step.q.z+1] = step.o

    print(np.count_nonzero(R))
    return


def pt2():
    txt = open('example2.txt').read()
    # txt = open('input.txt').read()





if __name__ == '__main__':
    pt1()
    # pt2()
