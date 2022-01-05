import numpy as np
from matplotlib import pyplot as plt

np.set_printoptions(linewidth=1000)
np.set_printoptions(formatter={'bool': lambda x: '█' if x else ' '})

plt.ion()


def main():
    # f = open('example.txt')
    f = open('input.txt')

    dots = []
    folds = []
    for line in f:
        line = line.rstrip()
        if not line:
            break
        x, y = line.split(',')
        dots.append((int(x), int(y)))

    for line in f:
        assert(line.startswith('fold along '))
        axis, ofs = line.rstrip().split(' ')[-1].split('=')
        axis = 0 if axis == 'y' else 1
        ofs = int(ofs)
        folds.append((axis, ofs))

    shape = [1 + 2 * max(ofs for axis, ofs in folds if axis == i)
             for i in range(2)]

    sheet = np.zeros(shape, dtype=bool)
    for x, y in dots:
        sheet[y][x] = 1

    for fold in folds:
        sheet = fold_sheet(sheet, *fold)
        # plt.imshow(sheet, interpolation='nearest'); plt.draw(); plt.pause(0.5)

    print(sheet)

    num_dots = np.count_nonzero(sheet)
    print(num_dots)


def fold_sheet(sheet, axis, ofs):
    top, _, bot = np.split(sheet, [ofs, ofs+1], axis)
    bot = np.flip(bot, axis=axis)
    assert(top.shape == bot.shape)
    return top + bot


if __name__ == '__main__':
    main()
