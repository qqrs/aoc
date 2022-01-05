import time
import os

import numpy as np
import scipy.signal


def cls():
    os.system('clear')


def main():
    # f = open('example.txt')
    f = open('input.txt')

    board_gen = [[int(ch) for ch in line.rstrip()] for line in f]
    board = np.array(board_gen)
    max_flash = board.shape[0] * board.shape[1]

    total_flashes = 0
    for step in range(1, 901):
        print('step={} total_flashes={}'.format(step, total_flashes))
        num_flashed = run_step(board)
        total_flashes += num_flashed

        if num_flashed == max_flash:
            print('they all flashed on step={}'.format(step))
            return


def run_step(board):
    board += 1

    flashed = np.zeros_like(board).astype(bool)

    while True:
        flashes = np.logical_and(board > 9, ~flashed)

        if not flashes.any():
            break

        boosts = (scipy.signal.convolve2d(
            flashes, np.ones((3,3)), mode='same').astype(int))

        board += boosts
        flashed = np.logical_or(flashes, flashed)

        # cls(); print(flashed.astype(int)); time.sleep(0.1)

    # cls(); print(flashed.astype(int)); time.sleep(0.5)

    board[flashed] = 0
    num_flashed = np.count_nonzero(flashed)
    return num_flashed


if __name__ == '__main__':
    main()
