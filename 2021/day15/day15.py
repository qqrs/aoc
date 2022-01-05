from pprint import pprint
from collections import namedtuple, Counter
import math
import statistics
import functools
from queue import PriorityQueue


def pt1():
    # f = open('example.txt')
    f = open('input.txt')

    hmap = [[int(ch) for ch in line.rstrip()] for line in f]
    # pprint(hmap)

    max_x = len(hmap[0]) - 1
    max_y = len(hmap) - 1

    def is_in_bounds(y, x):
        return not (y < 0 or y > max_y or x < 0 or x > max_x)

    def calc_adjacent_points(y, x):
        neighbors = [
            (y-1, x),
            (y+1, x),
            (y, x-1),
            (y, x+1)
        ]
        return [(y, x) for (y, x) in neighbors if is_in_bounds(y, x)]

    pq = PriorityQueue()
    D = [[math.inf for i in range(max_x + 1)] for j in range(max_y + 1)]
    visited = []

    D[0][0] = 0
    pq.put((0, (0,0)))

    while not pq.empty():
        d, pt = pq.get()
        visited.append(pt)

        neighbors = calc_adjacent_points(*pt)
        for neighbor in neighbors:
            y, x = neighbor
            old_cost = D[y][x]
            new_cost = d + hmap[y][x]
            if new_cost < old_cost:
                pq.put((new_cost, (y, x)))
                D[y][x] = new_cost

    # pprint(D)
    print(D[max_y][max_x])


def pt2():
    # f = open('example.txt')
    f = open('input.txt')

    hmap = [[int(ch) for ch in line.rstrip()] for line in f]

    hbig = [[v+rx+ry for rx in range(5) for v in row]
            for ry in range(5) for row in hmap]
    for i in range(len(hbig)):
        for j in range(len(hbig)):
            if hbig[i][j] > 9:
                hbig[i][j] -= 9

    hmap = hbig

    max_x = len(hmap[0]) - 1
    max_y = len(hmap) - 1

    def is_in_bounds(y, x):
        return not (y < 0 or y > max_y or x < 0 or x > max_x)

    def calc_adjacent_points(y, x):
        neighbors = [
            (y-1, x),
            (y+1, x),
            (y, x-1),
            (y, x+1)
        ]
        return [(y, x) for (y, x) in neighbors if is_in_bounds(y, x)]

    pq = PriorityQueue()
    D = [[math.inf for i in range(max_x + 1)] for j in range(max_y + 1)]
    visited = []

    D[0][0] = 0
    pq.put((0, (0,0)))

    while not pq.empty():
        d, pt = pq.get()
        visited.append(pt)

        neighbors = calc_adjacent_points(*pt)
        for neighbor in neighbors:
            y, x = neighbor
            old_cost = D[y][x]
            new_cost = d + hmap[y][x]
            if new_cost < old_cost:
                pq.put((new_cost, (y, x)))
                D[y][x] = new_cost

    # pprint(D)
    print(D[max_y][max_x])


if __name__ == '__main__':
    # pt1()
    pt2()
