from pprint import pprint


def pt1():
    # f = open('example.txt')
    f = open('input.txt')

    counts = None
    for line in f.readlines():
        row = [int(v) for v in line.rstrip()]

        if counts is None:
            counts = [0] * len(row)

        for i in range(len(row)):
            counts[i] += 1 if row[i] else -1

    gamma = 0
    for v in counts:
        gamma <<= 1
        x = int(v > 0)
        gamma |= x
        print((x, '{:b}'.format(gamma)))

    ones = (2 << len(counts) - 1) - 1
    eps = gamma ^ ones

    print(gamma, eps)
    print(gamma * eps)


def pt2():
    # f = open('example.txt')
    f = open('input.txt')

    rows = []
    for line in f.readlines():
        row = [int(v) for v in line.rstrip()]
        rows.append(row)

    nbits = len(rows[0])

    o2_rows = rows
    for i in range(nbits):
        count = 0
        for row in o2_rows:
            count += 1 if row[i] else -1

        mcb = 1 if count >= 0 else 0
        lcb = mcb ^ 1

        o2_rows = [row for row in o2_rows if row[i] == mcb]

        if len(o2_rows) <= 1:
            break

    co2_rows = rows
    for i in range(nbits):
        count = 0
        for row in co2_rows:
            count += 1 if row[i] else -1

        mcb = 1 if count >= 0 else 0
        lcb = mcb ^ 1

        co2_rows = [row for row in co2_rows if row[i] == lcb]

        if len(co2_rows) <= 1:
            break

    o2_rating = atob(o2_rows[0])
    co2_rating = atob(co2_rows[0])

    pprint((o2_rating, co2_rating))
    pprint(o2_rating * co2_rating)


def atob(a):
    b = 0
    for v in a:
        b <<= 1
        x = int(v > 0)
        b |= x
    return b


if __name__ == '__main__':
    # pt1()
    pt2()
