from pprint import pprint
from collections import namedtuple, Counter

Point = namedtuple('Point', ['x', 'y'])


def parse_line(line):
    p1, p2 = line.split(' -> ')
    return (parse_point(p1), parse_point(p2))


def parse_point(s):
    x, y = s.split(',')
    return Point(int(x), int(y))


def get_points_on_line(p1, p2):
    # horizontal
    if p1.x == p2.x:
        x = p1.x
        if p1.y > p2.y:
            (p1, p2) = (p2, p1)
        return [Point(x, y) for y in range(p1.y, p2.y + 1)]

    # vertical
    if p1.y == p2.y:
        y = p1.y
        if p1.x > p2.x:
            (p1, p2) = (p2, p1)
        return [Point(x, y) for x in range(p1.x, p2.x + 1)]

    # diagonal
    if p1.x > p2.x:
        (p1, p2) = (p2, p1)
    m = (p2.y - p1.y) / (p2.x - p1.x)
    return [Point(x, y)
            for x, y in zip(range(p1.x, p2.x + 1),
                            range(p1.y, p2.y + m, m))]


def pt1():
    # f = open('example.txt')
    f = open('input.txt')

    lines = [parse_line(v) for v in f]

    # filter to horizontal and vertical
    lines = [v for v in lines if v[0].x == v[1].x or v[0].y == v[1].y]

    counts = Counter()
    for line in lines:
        counts.update(get_points_on_line(*line))

    num_overlap = sum(1 for p, cnt in counts.iteritems() if cnt > 1)
    print(num_overlap)


def pt2():
    # f = open('example.txt')
    f = open('input.txt')

    lines = [parse_line(v) for v in f]

    counts = Counter()
    for line in lines:
        counts.update(get_points_on_line(*line))

    num_overlap = sum(1 for p, cnt in counts.iteritems() if cnt > 1)
    print(num_overlap)


if __name__ == '__main__':
    # pt1()
    pt2()
