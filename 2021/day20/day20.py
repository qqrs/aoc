from pprint import pprint
from collections import namedtuple, Counter
import math
import statistics
import functools
import numpy as np
import scipy.signal

np.set_printoptions(linewidth=240)
np.set_printoptions(edgeitems=20)
np.set_printoptions(formatter={'bool': lambda x: '█' if x else '_'})

def pt1():
    # f = open('example.txt')
    f = open('input.txt')

    sauce = np.array(
        [1 if ch == '#' else 0 for ch in f.readline().rstrip()],
        dtype=bool)

    assert(not f.readline().rstrip())

    pic = np.array(
        [[1 if ch == '#' else 0 for ch in line.rstrip()] for line in f],
        dtype=bool)
    # print(pic)
    # print('')
    # print(sauce)

    frame = np.array([1 << i for i in range(9)]).reshape((3,3))
    # print(frame)

    pulled = (scipy.signal.convolve2d(
        pic, frame, mode='full').astype(int))

    pic2 = sauce[pulled]
    # print(pic2)
    # print('')

    pulled2 = (scipy.signal.convolve2d(
        pic2, frame, mode='full', fillvalue=1).astype(int))

    pic3 = sauce[pulled2]

    # print(pic3)

    num_lit = np.count_nonzero(pic3)
    print(num_lit)


def pt2():
    # f = open('example.txt')
    f = open('input.txt')

    sauce = np.array(
        [1 if ch == '#' else 0 for ch in f.readline().rstrip()],
        dtype=bool)

    assert(not f.readline().rstrip())

    pic = np.array(
        [[1 if ch == '#' else 0 for ch in line.rstrip()] for line in f],
        dtype=bool)
    # print(pic)
    # print('')
    # print(sauce)

    frame = np.array([1 << i for i in range(9)]).reshape((3,3))
    # print(frame)

    fill = 0

    for i in range(50):

        pulled = (scipy.signal.convolve2d(
            pic, frame, mode='full', fillvalue=fill).astype(int))

        pic = sauce[pulled]
        fill = sauce[0 if not fill else -1]

    num_lit = np.count_nonzero(pic)
    print(num_lit)


if __name__ == '__main__':
    # pt1()
    pt2()
