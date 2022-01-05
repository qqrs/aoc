from pprint import pprint
from collections import namedtuple, Counter
import math
import statistics
import functools


def pt1():
    # f = open('example.txt')
    f = open('input.txt')

    total = 0
    for line in f:
        total += check_line(line.rstrip())

    print(total)


def opener_for_closer(ch):
    return {
        ')': '(',
        ']': '[',
        '}': '{',
        '>': '<'}[ch]


def value_for_closer_mismatch(ch):
    return {
        ')': 3,
        ']': 57,
        '}': 1197,
        '>': 25137}[ch]


def check_line(line):
    st = []
    for ch in line:
        if ch in '[({<':
            st.append(ch)
        elif ch in '])}>':
            expect = opener_for_closer(ch)
            opened = st.pop()

            if opened != expect:
                return value_for_closer_mismatch(ch)

    return 0


def pt2():
    # f = open('example.txt')
    f = open('input.txt')

    scores = []
    for line in f:
        score = get_line_completion_score(line.rstrip())
        if score > 0:
            scores.append(score)

    print(scores)
    best = statistics.median(scores)
    print(best)


def value_for_opener_completion(ch):
    return {
        '(': 1,
        '[': 2,
        '{': 3,
        '<': 4}[ch]


def get_line_completion_score(line):
    st = []
    for ch in line:
        if ch in '[({<':
            st.append(ch)
        elif ch in '])}>':
            expect = opener_for_closer(ch)
            opened = st.pop()

            if opened != expect:
                # corrupt line
                return 0

    score = 0
    for ch in reversed(st):
        score *= 5
        score += value_for_opener_completion(ch)
    return score


if __name__ == '__main__':
    # pt1()
    pt2()
