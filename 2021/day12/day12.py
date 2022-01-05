from pprint import pprint
from collections import namedtuple, defaultdict, Counter
import math
import statistics
import functools

import os
import time


# Path = namedtuple('Path', 'cave1', 'cave2')

def is_big(cave):
    return cave.isupper()


def pt1():
    # f = open('example1.txt')
    # f = open('example2.txt')
    # f = open('example3.txt')
    f = open('input.txt')

    graph = defaultdict(set)

    for line in f:
        cave1, cave2 = line.rstrip().split('-')
        graph[cave1].add(cave2)
        graph[cave2].add(cave1)

    result = dfs(graph, 'start', 'end', set(), False)
    print(result)


def dfs(graph, curr, dest, visited, revisit_used):
    if curr == dest:
        return 1
    elif curr in visited:
        if curr in ('start', 'end') or revisit_used:
            return 0
        else:
            revisit_used = True

    if not is_big(curr):
        visited.add(curr)

    return sum(dfs(graph, c, dest, set(visited), revisit_used)
               for c in graph[curr])


if __name__ == '__main__':
    pt1()
    # pt2()
