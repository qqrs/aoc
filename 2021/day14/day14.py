from pprint import pprint
from collections import namedtuple, defaultdict, Counter
from io import StringIO
import math
import statistics
import functools

import os
import time


def pt1():
    f = open('example.txt')
    # f = open('input.txt')

    template = f.readline().rstrip()
    assert(not f.readline().rstrip())

    rules = {}
    for line in f:
        match, ins = line.rstrip().split(' -> ')
        rules[match] = ins

    print(template)
    pprint(rules)

    polymer = template
    for i in range(40):
        polymer = grow_polymer(polymer, rules)
        print(i)
        # print(polymer)

    cnt = Counter(polymer)
    comm = cnt.most_common()

    print(comm[0][1] - comm[-1][1])


def grow_polymer(template, rules):
    peek = iter(template)
    peck = iter(template)

    polymer = StringIO()
    polymer.write(next(peek))

    for x, y in zip(peck, peek):
        ins = rules.get(x + y)
        if ins is not None:
            polymer.write(ins)
        polymer.write(y)

    return polymer.getvalue()


def pt2():
    # f = open('example.txt')
    f = open('input.txt')

    template = f.readline().rstrip()
    assert(not f.readline().rstrip())

    rules = {}
    for line in f:
        match, ins = line.rstrip().split(' -> ')
        rules[match] = ins

    print(template)
    pprint(rules)

    pairs = get_polymer_pairs(template)
    print(pairs)
    for i in range(40):
        pairs = grow_polymer_pairs(pairs, rules)
        # print(pairs)

    cnt = Counter()
    for p, n in pairs.items():
        cnt[p[1]] += n
    cnt[template[0]] += 1

    print(cnt)
    comm = cnt.most_common()

    print(comm[0][1] - comm[-1][1])


def get_polymer_pairs(template):
    peek = iter(template)
    next(peek)
    peck = iter(template)

    pairs = Counter()
    for x, y in zip(peck, peek):
        pairs[x + y] += 1

    return pairs


def grow_polymer_pairs(prevpairs, rules):
    pairs = Counter()
    for pair, n in prevpairs.items():
        if pair in rules:
            ins = rules[pair]
            pairs[pair[0] + ins] += n
            pairs[ins + pair[1]] += n
        else:
            pairs[pair] += n

    return pairs


if __name__ == '__main__':
    # pt1()
    pt2()
