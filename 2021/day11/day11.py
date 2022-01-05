from pprint import pprint
from collections import namedtuple, Counter
import math
import statistics
import functools
import numpy as np
import scipy.signal

import os
import time


def cls():
    os.system('clear')


def pt1():
    # f = open('example.txt')
    f = open('input.txt')

    board_gen = [[int(ch) for ch in line.rstrip()] for line in f]
    board = np.array(board_gen)
    max_flash = board.shape[0] * board.shape[1]

    num_flashes = 0
    for step in range(1, 901):
        # print('step={} num_flashes={}'.format(step, num_flashes))
        # print(board)
        num_flashed = run_step(board)
        num_flashes += num_flashed

        if num_flashed == max_flash:
            print('they all flashed on step={}'.format(step))
            return


def run_step(board):
    board += 1

    flashed = np.zeros_like(board).astype(bool)

    while True:
        flashes = np.logical_and(board > 9, ~flashed)
        # print('flashes'); print(flashes.astype(int))

        if not flashes.any():
            break

        boosts = (scipy.signal.convolve2d(
            flashes, np.ones((3,3)), mode='same').astype(int))
        # print('boosts'); print(boosts.astype(int))

        board += boosts
        flashed = np.logical_or(flashes, flashed)

        # cls()
        # print('flashed'); print(flashed.astype(int))
        # time.sleep(0.1)

    # cls()
    # print('flashed'); print(flashed.astype(int))
    # time.sleep(0.5)
    board[flashed.astype(bool)] = 0
    num_flashed = np.count_nonzero(flashed)
    return num_flashed


if __name__ == '__main__':
    pt1()
    # pt2()
