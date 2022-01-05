from pprint import pprint
from collections import namedtuple, Counter
from dataclasses import dataclass
from copy import deepcopy
import math
import json
import statistics
import functools
import itertools
from queue import PriorityQueue

import unittest


def parse_line(line):
    parsed = json.loads(line)
    return squish_line(parsed)


def squish_line(line):
    depth = 0
    snums = []

    def _walk(n):
        nonlocal depth
        nonlocal snums

        if isinstance(n, int):
            snums.append([n, depth])
        else:
            depth += 1
            _walk(n[0])
            _walk(n[1])
            depth -= 1

    _walk(line)
    return snums

class Pair:
    def __init__(self, left=None, right=None):
        self.left = left
        self.right = right

    def __repr__(self):
        return ''.join(('[', repr(self.left), ', ', repr(self.right), ']'))

    def is_full(self):
        return self.left is not None and self.right is not None

    def append(self, v):
        if self.left is None:
            self.left = v
        elif self.right is None:
            self.right = v
        else:
            raise Exception('Pair is full')

        return v

def unsquish(n):
    root = Pair()
    p = root
    st = [p]

    for v, d in n:
        while d > len(st):
            p = p.append(Pair())
            st.append(p)

        p.append(v)

        while p.is_full() and p is not root:
            st.pop()
            p = st[-1]

    return root


def smag(n):
    def _mag(p):
        v = 0
        v += 3 * (_mag(p.left) if isinstance(p.left, Pair) else p.left)
        v += 2 * (_mag(p.right) if isinstance(p.right, Pair) else p.right)
        return v

    root = unsquish(n)
    return _mag(root)


def ssum(ns):
    acc = ns[0]
    for n in ns[1:]:
        acc = sadd(acc, n)
    return acc


def sadd(a, b):
    for v in a:
        v[1] += 1
    for v in b:
        v[1] += 1
    n = a + b
    sreduce(n)
    return n


def sreduce(n):
    def _try_reduce(n):
        for i, v in enumerate(n):
            if v[1] > 4:
                sexplode(n, i)
                return True
        for i, v in enumerate(n):
            if v[0] >= 10:
                ssplit(n, i)
                return True
        return False

    while _try_reduce(n):
        pass
    return n


def sexplode(n, i):
    left, right = n[i: i+2]
    if i-1 >= 0:
        n[i-1][0] += left[0]
    if i+2 < len(n):
        n[i+2][0] += right[0]
    n[i][0] = 0
    n[i][1] -= 1
    del n[i+1]
    return n


def ssplit(n, i):
    left = n[i]
    left[1] += 1
    right = [0, left[1]]
    v = left[0]
    left[0] = v // 2
    right[0] = v // 2 + v % 2
    n.insert(i+1, right)
    return n


def pt1():
    # f = open('example.txt')
    f = open('input.txt')

    ns = [parse_line(line) for line in f]
    print(smag(ssum(ns)))


def pt2():
    # f = open('example.txt')
    f = open('input.txt')

    ns = [parse_line(line) for line in f]
    # print(smag(ssum(ns)))

    # js = list(itertools.permutations(range(len(ns)), 2))

    # for i, j in js:
        # print((i,j))
        # a = deepcopy(ns[i])
        # b = deepcopy(ns[j])
        # print(a)
        # print(b)
        # z = sadd(a, b)
        # print(z)
        # print(smag(z))
        # print('')

    smax = max(smag(sadd(deepcopy(a), deepcopy(b)))
               for a, b in itertools.permutations(ns, 2))
    print(smax)

    f.close()


class TestSNum(unittest.TestCase):

    def test_sexplode(self):
        s = squish_line
        self.assertEqual(
            sexplode(
                s([[[[[9,8],1],2],3],4]),
                0),
            s([[[[0,9],2],3],4]))

    def test_ssplit(self):
        s = squish_line
        self.assertEqual(
            ssplit(
                s([[[[0,7],4],[[7,8],[0,13]]],[1,1]]),
                6),
            s([[[[0,7],4],[[7,8],[0,[6,7]]]],[1,1]]))

    def test_reduce(self):
        s = squish_line
        self.assertEqual(sreduce(s([[[[[9,8],1],2],3],4])),
                         s([[[[0,9],2],3],4]))
        self.assertEqual(sreduce(s([7,[6,[5,[4,[3,2]]]]])),
                         s([7,[6,[5,[7,0]]]]))
        self.assertEqual(sreduce(s([[3,[2,[8,0]]],[9,[5,[4,[3,2]]]]])),
                         s([[3,[2,[8,0]]],[9,[5,[7,0]]]]))

    def test_add(self):
        s = squish_line
        self.assertEqual(sadd(
                            s([1, [2, 3]]),
                            s([4, 5])),
                         s([[1, [2, 3]], [4, 5]]))
        self.assertEqual(sadd(
                            s([[[[4,3],4],4],[7,[[8,4],9]]]),
                            s([1,1])),
                         s([[[[0,7],4],[[7,8],[6,0]]],[8,1]]))

    def test_sum(self):
        s = squish_line
        p = lambda txt: [parse_line(line) for line in txt.split('\n')]
    
        txt = (
"""[1,1]
[2,2]
[3,3]
[4,4]""")
        exp = [[[[1,1],[2,2]],[3,3]],[4,4]]
        self.assertEqual(ssum(p(txt)), s(exp))

        txt = (
"""[1,1]
[2,2]
[3,3]
[4,4]
[5,5]""")
        exp = [[[[3,0],[5,3]],[4,4]],[5,5]]
        self.assertEqual(ssum(p(txt)), s(exp))

        txt = (
"""[1,1]
[2,2]
[3,3]
[4,4]
[5,5]
[6,6]""")
        exp = [[[[5,0],[7,4]],[5,5]],[6,6]] 
        self.assertEqual(ssum(p(txt)), s(exp))

        txt = (
"""[[[0,[4,5]],[0,0]],[[[4,5],[2,6]],[9,5]]]
[7,[[[3,7],[4,3]],[[6,3],[8,8]]]]
[[2,[[0,8],[3,4]]],[[[6,7],1],[7,[1,6]]]]
[[[[2,4],7],[6,[0,5]]],[[[6,8],[2,8]],[[2,1],[4,5]]]]
[7,[5,[[3,8],[1,4]]]]
[[2,[2,2]],[8,[8,1]]]
[2,9]
[1,[[[9,3],9],[[9,0],[0,7]]]]
[[[5,[7,4]],7],1]
[[[[4,2],2],6],[8,7]]""")
        exp = [[[[8,7],[7,7]],[[8,6],[7,7]]],[[[0,7],[6,6]],[8,7]]] 
        self.assertEqual(ssum(p(txt)), s(exp))

    def test_unsquish(self):
        exp = [[[[3,0],[5,3]],[4,4]],[5,5]] 
        self.assertEqual(repr(unsquish(squish_line(exp))), repr(exp))

        exp = [[[[8,7],[7,7]],[[8,6],[7,7]]],[[[0,7],[6,6]],[8,7]]]
        self.assertEqual(repr(unsquish(squish_line(exp))), repr(exp))

    def test_smag(self):
        s = squish_line
        self.assertEqual(143, smag(s([[1,2],[[3,4],5]])))
        self.assertEqual(1384, smag(s([[[[0,7],4],[[7,8],[6,0]]],[8,1]])))
        self.assertEqual(445, smag(s([[[[1,1],[2,2]],[3,3]],[4,4]])))
        self.assertEqual(791, smag(s([[[[3,0],[5,3]],[4,4]],[5,5]])))
        self.assertEqual(1137, smag(s([[[[5,0],[7,4]],[5,5]],[6,6]])))
        self.assertEqual(3488, smag(s([[[[8,7],[7,7]],[[8,6],[7,7]]],[[[0,7],[6,6]],[8,7]]])))

    def test_all(self):
        s = squish_line
        p = lambda txt: [parse_line(line) for line in txt.split('\n')]
    
        txt = (
"""[[[0,[5,8]],[[1,7],[9,6]]],[[4,[1,2]],[[1,4],2]]]
[[[5,[2,8]],4],[5,[[9,9],0]]]
[6,[[[6,2],[5,6]],[[7,6],[4,7]]]]
[[[6,[0,7]],[0,9]],[4,[9,[9,0]]]]
[[[7,[6,4]],[3,[1,3]]],[[[5,5],1],9]]
[[6,[[7,3],[3,2]]],[[[3,8],[5,7]],4]]
[[[[5,4],[7,7]],8],[[8,3],8]]
[[9,3],[[9,9],[6,[4,9]]]]
[[2,[[7,7],7]],[[5,8],[[9,3],[0,2]]]]
[[[[5,2],5],[8,[3,7]]],[[5,[7,5]],[4,4]]]""")
        exp = [[[[6,6],[7,6]],[[7,7],[7,0]]],[[[7,7],[7,7]],[[7,8],[9,9]]]]
        self.assertEqual(4140, smag(ssum(p(txt))))

    def test_unsquish_example(self):
        f = open('example.txt')

        for line in f:
            n = parse_line(line)
            self.assertEqual(repr(unsquish(n)), json.dumps(json.loads(line)))

        f.close()


if __name__ == '__main__':
    # parse()
    # test()
    # pt1()
    pt2()
    # unittest.main()
