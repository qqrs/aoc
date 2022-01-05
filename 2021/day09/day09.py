from pprint import pprint
from collections import namedtuple, Counter
import math
import statistics
import functools


def pt1():
    f = open('example.txt')
    # f = open('input.txt')

    hmap = [[int(ch) for ch in line.rstrip()] for line in f]
    pprint(hmap)

    max_x = len(hmap[0]) - 1
    max_y = len(hmap) - 1

    low_points = []

    for i in range(max_y + 1):
        for j in range(max_x + 1):
            v = hmap[i][j]
            is_low = (
                (i-1 < 0 or hmap[i-1][j] > v)
                and (i+1 > max_y or hmap[i+1][j] > v)
                and (j-1 < 0 or hmap[i][j-1] > v)
                and (j+1 > max_x or hmap[i][j+1] > v))
            if is_low:
                low_points.append((i, j, v))

    print(low_points)

    risk = sum((v+1) for _, _, v in low_points)
    print(risk)


def pt2():
    # f = open('example.txt')
    f = open('input.txt')

    hmap = [[int(ch) for ch in line.rstrip()] for line in f]
    pprint(hmap)

    max_x = len(hmap[0]) - 1
    max_y = len(hmap) - 1

    def is_in_bounds(i, j):
        return not (i < 0 or i > max_y or j < 0 or j > max_x)

    def calc_adjacent_points(i, j):
        neighbors = [
            (i-1, j),
            (i+1, j),
            (i, j-1),
            (i, j+1)
        ]
        return [(i,j) for (i,j) in neighbors if is_in_bounds(i, j)]

    low_points = []

    for i in range(max_y + 1):
        for j in range(max_x + 1):
            v = hmap[i][j]
            neighbors = calc_adjacent_points(i, j)
            if all(hmap[ni][nj] > v for ni, nj in neighbors):
                low_points.append((i, j, v))

    print(low_points)

    risk = sum((v+1) for _, _, v in low_points)
    print(risk)

    basins = []
    for mi, mj, _ in low_points:
        basin = set()
        q = set([(mi, mj)])
        while q:
            pi, pj = q.pop()
            basin.add((pi, pj))
            for i, j in calc_adjacent_points(pi, pj):
                if (i,j) in basin or (i,j) in q:
                    continue
                if hmap[i][j] < 9:
                    q.add((i, j))
        print(basin)
        basins.append(basin)

    pprint(basins)
    blens = sorted([len(b) for b in basins], reverse=True)
    print(blens[0] * blens[1] * blens[2])


if __name__ == '__main__':
    # pt1()
    pt2()
