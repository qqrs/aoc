from pprint import pprint
from collections import namedtuple, Counter
from itertools import groupby


Line = namedtuple('Line', ['patterns', 'outputs'])
Group = namedtuple('Group', ['pseg', 'dseg'])


def pt1():
    # f = open('example.txt')
    f = open('input.txt')

    lines = [Line(*[v.split() for v in line.split('|')]) for line in f]

    seglookup = {
        1: 2,
        4: 4,
        7: 3,
        8: 7}

    seeklen = set(seglookup.values())

    num_seek = sum(
        1 for line in lines for v in line.outputs
        if len(v) in seeklen)
    print(num_seek)


digitmap = {
    0: 'abcefg',
    1: 'cf',
    2: 'acdeg',
    3: 'acdfg',
    4: 'bcdf',
    5: 'abdfg',
    6: 'abdefg',
    7: 'acf',
    8: 'abcdefg',
    9: 'abcdfg'
}
digitmap = {k: set(v) for k, v in digitmap.items()}
digitlookup = {''.join(sorted(v)): k for k, v in digitmap.items()}

digitnseg = {}
for k, v in digitmap.items():
    digitnseg.setdefault(len(v), []).append(k)


def pt2():
    # f = open('example.txt')
    f = open('input.txt')

    total = 0
    lines = [Line(*[v.split() for v in line.split('|')]) for line in f]
    for line in lines:
        total += decode_line(line)
    print(total)

    # inline = 'acedgfb cdfbe gcdfa fbcad dab cefabd cdfgeb eafb cagedb ab | cdfeb fcadb cdfeb cdbaf'
    # decode_line(Line(*[v.split() for v in inline.split('|')]))


def decode_line(line):
    segmap = decode_segment_mappings(line.patterns)
    digits = [decode_digit(segmap, v) for v in line.outputs]

    result = 0
    for v in digits:
        result = result * 10 + v
    print(result)

    return result


def decode_digit(segmap, output):
    segments = set(segmap[v] for v in output)
    digit = digitlookup[''.join(sorted(segments))]
    return digit


def decode_segment_mappings(patterns):
    segmap = {k: set('abcdefg') for k in 'abcdefg'}

    # Look at groups of digits that have the same number of segments turned on.
    # For example, 1 is in a group by itself; 2, 3, 5 are in a group together.
    for n, xs in digitnseg.items():
        dcnt = Counter(v for x in xs for v in digitmap[x])

        ps = [p for p in patterns if len(p) == n]
        pcnt = Counter(v for p in ps for v in p)

        groups = {}
        for k, v in dcnt.items():
            groups.setdefault(v, Group(set(), set())).dseg.add(k)
        for k, v in pcnt.items():
            groups[v].pseg.add(k)
        groups = groups.values()

        for g in groups:
            p = g.pseg
            d = g.dseg
            segmap = {
                k: v & d if k in p else v - d
                for k, v in segmap.items()
            }

        pprint((n, xs))
        pprint(segmap)
        print('')

    return {k: list(v)[0] for k, v in segmap.items()}


def JUNK_decode_segment_mappings_zzz(patterns):
    segmap = {k: set('abcdefg') for k in 'abcdefg'}

    # The patterns for several digits can be definitively identified by the
    # number of segments turned on.
    for x in [1, 4, 7, 8]:
        # Get the segments that correspond to this digit when correctly wired.
        d = digitmap[x]

        # Find the miswired pattern that corresponds to this digit.
        p = next(p for p in patterns if len(p) == len(d))

        # Update our mapping of possible segment wiring. Use deductive logic
        # to eliminate impossible mappings.
        segmap = {
            k: v & d if k in p else v - d
            for k, v in segmap.items()
        }

    # pprint(segmap)
    # print('')

    xs = [2, 3, 5]
    ds = [''.join(digitmap[x]) for x in xs]
    dcnt = Counter(v for x in xs for v in digitmap[x])
    ps = [p for p in patterns if len(p) == 5]
    pcnt = Counter(v for p in ps for v in p)

    groups = {}
    for k, v in dcnt.items():
        groups.setdefault(v, Group(set(), set())).dseg.add(k)
    for k, v in pcnt.items():
        groups[v].pseg.add(k)
    groups = groups.values()

    for g in groups:
        p = g.pseg
        d = g.dseg
        segmap = {
            k: v & d if k in p else v - d
            for k, v in segmap.items()
        }

    # pprint(segmap)
    # print('')

    xs = [0, 6, 9]
    ds = [''.join(digitmap[x]) for x in xs]
    dcnt = Counter(v for x in xs for v in digitmap[x])
    ps = [p for p in patterns if len(p) == 6]
    pcnt = Counter(v for p in ps for v in p)

    groups = {}
    for k, v in dcnt.items():
        groups.setdefault(v, Group(set(), set())).dseg.add(k)
    for k, v in pcnt.items():
        groups[v].pseg.add(k)
    groups = groups.values()

    for g in groups:
        p = g.pseg
        d = g.dseg
        segmap = {
            k: v & d if k in p else v - d
            for k, v in segmap.items()
        }

    # pprint(segmap)
    # print('')

    return {k: list(v)[0] for k, v in segmap.items()}



if __name__ == '__main__':
    # pt1()
    pt2()
