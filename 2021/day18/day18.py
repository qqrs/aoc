from pprint import pprint
from collections import namedtuple, Counter
from dataclasses import dataclass
import math
import json
import statistics
import functools
from queue import PriorityQueue
import unittest


class SNumIterator:
    def __init__(self, root):
        self.root = root
        self.last = self.root.parent
        self.n = self.root
        self.depth = 0

    def __iter__(self):
        return self

    def __next__(self):
        n = self.n
        depth = self.depth

        while True:
            tmp = n

            if n.is_leaf():
                # hit a leaf so go back up
                n = n.parent
                depth -= 1
            elif self.last is n.parent or self.last is None:
                # coming down so go left
                n = n.left
                depth += 1
            elif self.last is n.left:
                # coming up from left so go right
                n = n.right
                depth += 1
            elif self.last is n.right:
                # coming up from right so go back up
                n = n.parent
                depth -= 1
            else:
                ValueError

            self.last = tmp

            if n is self.root:
                raise StopIteration

            if n.is_leaf():
                self.n = n
                self.depth = depth
                return n


@dataclass
class SNum:
    def __init__(self, val=None, left=None, right=None, parent=None):
        self.val = val
        self.left = left
        self.right = right
        self.parent = parent

    def __repr__(self):
        if self.val is not None:
            return repr(self.val)
        else:
            return ''.join(('[', repr(self.left), ',', repr(self.right), ']'))

    def __iter__(self):
        return SNumIterator(self)

    def __eq__(a, b):
        if b is None:
            return False
        return a.val == b.val and a.left == b.left and a.right == b.right

    def __add__(a, b):
        n = SNum(left=a, right=b)
        # n.reduce()
        return n

    def is_leaf(self):
        return self.val is not None

    def reduce(self):
        def _try_explode(self):
            prev = None
            print(list(iter(self)))
            it = iter(self)
            for n in it:
                print((n, it.depth))
                if it.depth > 4:
                    parent = n.parent
                    left = n
                    right = next(it)
                    nxt = next(it)

                    if prev is not None:
                        prev.val += left.val
                    if nxt is not None:
                        nxt.val += right.val
                    parent.left = None
                    parent.right = None
                    parent.val = 0
                    return True

                prev = n
            return False

        def _try_split(self):
            return False

        # while _try_explode(self) or _try_split(self):
            # pass
        _try_explode(self)
        return self

    @classmethod
    def snumify(cls, v):
        if isinstance(v, SNum):
            return v
        elif isinstance(v, int):
            return SNum(val=v)
        elif isinstance(v, list) and len(v) == 2:
            left = SNum.snumify(v[0])
            right = SNum.snumify(v[1])
            snum = SNum(left=left, right=right)
            left.parent = snum
            right.parent = snum
            return snum
        else:
            raise TypeError


def parse():
    f = open('input.txt')

    snums = [json.loads(line) for line in f]
    a = SNum.snumify(snums[0])
    b = SNum.snumify(snums[1])

    return snums


def pt1():
    pass


def test():
    assert(
        s([1,2]) + s([[3,4],5]) == s([[1,2],[[3,4],5]])
    )

    assert(s([[[[[9,8],1],2],3],4]).reduce() == s([[[[0,9],2],3],4]))
    assert(s([7,[6,[5,[4,[3,2]]]]]).reduce() == s([7,[6,[5,[7,0]]]]))

    return
    # assert(sadd(
        # [1,2],
        # [[3,4],5])
        # == [[1,2],[[3,4],5]]
    # )

    a = SNum.snumify([[[[[9,8],1],2],3],4])
    a.reduce()
    # it = iter(a)
    # print(list(it))

    # import ipdb; ipdb.set_trace()

    # import ipdb; ipdb.set_trace()

    # pprint(a)
    # n = a
    # while n:
        # n = n.walk()
        # print(n)

    # a = SNum.snumify([[[[[9,8],1],2],3],4])
    # a.reduce()
    # pprint(a)

    # import ipdb; ipdb.set_trace()

    # assert(sreduce(
        # [[[[[9,8],1],2],3],4])
        # == [[[[0,9],2],3],4]
    # )



class TestSNum(unittest.TestCase):
    def test_snumify(self):
        s = SNum.snumify
        self.assertEqual(s(1), SNum(1))
        self.assertEqual(s([2,3]), SNum(None, SNum(2), SNum(3)))


    def test_reduce(self):
        s = SNum.snumify
        self.assertEqual(s([[[[[9,8],1],2],3],4]).reduce(),
                         s([[[[0,9],2],3],4]))
        self.assertEqual(s([7,[6,[5,[4,[3,2]]]]]).reduce(),
                         s([7,[6,[5,[7,0]]]]))

if __name__ == '__main__':
    # parse()
    # test()
    # pt1()
    # pt2()
    unittest.main()
