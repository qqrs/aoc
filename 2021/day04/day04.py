from pprint import pprint

marker = 'M'


def check_bingo(b, mi, mj):
    # check vertical
    if all(b[i][mj] == marker for i in range(len(b))):
        return True
    # check horizontal
    if all(b[mi][j] == marker for j in range(len(b[0]))):
        return True

    # check diagonal
    # if mi == mj and all(b[i][i] == marker for i in range(len(b))):
        # return True

    # check other diagonal
    # size = len(b)
    # if mi == size-mj-1 and all(b[i][size-i-1] == marker for i in range(len(b))):
        # return True

    return False


def count_unmarked(b):
    return sum(b[i][j]
               for i in range(len(b))
               for j in range(len(b[0]))
               if b[i][j] != marker)


def pt1():
    # f = open('example.txt')
    f = open('input.txt')
    line = f.readline()
    calls = [int(v) for v in line.rstrip().split(',')]

    boards = []
    while f.readline():
        rows = []
        for _ in range(5):
            line = f.readline()
            row = [int(v) for v in line.split()]
            rows.append(row)
        boards.append(rows)

    print(calls)

    for c in calls:
        for b in boards:
            for i in range(len(b)):
                for j in range(len(b[0])):
                    if b[i][j] == c:
                        b[i][j] = marker

                        if check_bingo(b, i, j):
                            print('BINGO!')
                            final_score = c * count_unmarked(b)
                            print(final_score)
                            return

        pprint(boards)


def pt2():
    # f = open('example.txt')
    f = open('input.txt')
    line = f.readline()
    calls = [int(v) for v in line.rstrip().split(',')]

    boards = []
    while f.readline():
        rows = []
        for _ in range(5):
            line = f.readline()
            row = [int(v) for v in line.split()]
            rows.append(row)
        boards.append(rows)

    print(calls)

    bingoed_boards = set()
    for c in calls:
        for bnum, b in enumerate(boards):
            if bnum in bingoed_boards:
                continue
            for i in range(len(b)):
                for j in range(len(b[0])):
                    if b[i][j] == c:
                        b[i][j] = marker

                        if check_bingo(b, i, j):
                            print('BINGO!')
                            if len(boards) - len(bingoed_boards) == 1:
                                print('FINAL BINGO!!!')
                                final_score = c * count_unmarked(b)
                                print(final_score)
                                return
                            bingoed_boards.add(bnum)

        pprint(boards)


if __name__ == '__main__':
    #pt1()
    pt2()
