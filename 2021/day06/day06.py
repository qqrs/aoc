from pprint import pprint
from collections import namedtuple, Counter


class FishSim:
    def __init__(self, fish):
        self.fish = fish

    def step(self):
        fish = self.fish
        for i in range(len(fish)):
            if fish[i] == 0:
                fish[i] = 6
                fish.append(8)
            else:
                fish[i] -= 1

    def count(self):
        return len(self.fish)


class FastFishSim:
    def __init__(self, fish):
        self.fish = Counter(fish)

    def step(self):
        num_spawn = self.fish[0]
        self.fish = Counter({k-1: v
                             for k, v in self.fish.iteritems()
                             if k > 0})
        self.fish[8] += num_spawn
        self.fish[6] += num_spawn

    def count(self):
        return sum(self.fish.values())


def pt1():
    f = open('example.txt')
    # f = open('input.txt')

    line = f.readline()
    fish = [int(v) for v in line.rstrip().split(',')]
    print('Initial state: {}'.format(fish))

    # sim = FishSim(fish)
    sim = FastFishSim(fish)

    num_days = 80
    for day in range(1, num_days + 1):
        sim.step()
        # print('After {:3d} days: {}'.format(day, fish))

    print('After {:3d} days there are {} fish'.format(day, sim.count()))


def pt2():
    # f = open('example.txt')
    f = open('input.txt')

    line = f.readline()
    fish = [int(v) for v in line.rstrip().split(',')]
    print('Initial state: {}'.format(fish))

    # sim = FishSim(fish)
    sim = FastFishSim(fish)

    num_days = 256
    for day in range(1, num_days + 1):
        sim.step()

    print('After {:3d} days there are {} fish'.format(day, sim.count()))



if __name__ == '__main__':
    # pt1()
    pt2()
