from pprint import pprint
from collections import namedtuple, Counter
import math
import statistics
import functools
import itertools

import numpy as np


EXAMPLE = """Player 1 starting position: 4
Player 2 starting position: 8"""


def pt1():
    # txt = EXAMPLE
    txt = open('input.txt').read()

    starts = [int(line.rstrip().split(': ')[-1]) for line in txt.splitlines()]

    die = itertools.cycle(range(1, 101))

    pos = starts.copy()
    score = [0, 0]
    rolls = 0

    i = 0
    while max(score) < 1000:
        rolls += 3
        move = next(die) + next(die) + next(die)
        pos[i] += move
        pos[i] = ((pos[i] - 1) % 10) + 1
        score[i] += pos[i]

        i ^= 1
        print('{} {} {}'.format(rolls, pos, score))

    print(min(score) * rolls)

    sauce = np.array(
        [1 if ch == '#' else 0 for ch in f.readline().rstrip()],
        dtype=bool)


def pt2():
    # txt = EXAMPLE
    txt = open('input.txt').read()

    starts = [int(line.rstrip().split(': ')[-1]) for line in txt.splitlines()]

    # precalculate all 27 possible moves resulting from 3 rolls of a 3-sided die
    rolls_per_turn = list(Counter(
        [i+j+k for i in range(1,4)
         for j in range(1,4)
         for k in range(1,4)]).items())

    wins = [0, 0]

    # score 1, score 2, pos 1, pos 2
    shape = (21, 21, 11, 11)
    s = np.zeros(shape=shape, dtype=np.uint64)
    s[0, 0, starts[0], starts[1]] = 1

    def possible_states():
        for score1 in range(20, -1, -1):
            for score2 in range(20, -1, -1):
                for pos1 in range(10, 0, -1):
                    for pos2 in range(10, 0, -1):
                        yield (score1, score2, pos1, pos2)

    i = 0
    has_unfinished_games = True
    while has_unfinished_games:
        has_unfinished_games = False
        for st in possible_states():
            if not s[st]:
                continue

            has_unfinished_games = True
            n_universes = s[st]
            s[st] = 0

            for move, n_roll in rolls_per_turn:
                # (score1, score2, pos1, pos2) = st
                score, pos = st[i], st[2 + i]
                pos += move
                pos = ((pos - 1) % 10) + 1
                score += pos
                n = n_universes * n_roll
                if score >= 21:
                    wins[i] += n
                else:
                    tt = list(st)
                    tt[i] = score
                    tt[2 + i] = pos
                    s[tuple(tt)] += n

        i ^= 1

        print('{:10d} {:20d} {:20d}'.format(np.count_nonzero(s), int(wins[0]), int(wins[1])))

    # assert(wins == [444356092776315, 341960390180808])
    print(max(wins))
    print(sum(wins))


if __name__ == '__main__':
    # pt1()
    pt2()
