from pprint import pprint
from collections import namedtuple, Counter

Line = namedtuple('Line', ['patterns', 'outputs'])


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


def pt2():
    # inline = 'acedgfb cdfbe gcdfa fbcad dab cefabd cdfgeb eafb cagedb ab | cdfeb fcadb cdfeb cdbaf'
    # decode_line(Line(*[v.split() for v in inline.split('|')]))

    f = open('example.txt')
    # f = open('input.txt')

    total = 0
    lines = [Line(*[v.split() for v in line.split('|')]) for line in f]
    for line in lines:
        total += decode_line(line)
    print(total)


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


def calc_signature(patterns, segment):
    return tuple(sorted(
        len(pattern) for pattern in patterns
        if segment in pattern))


def calc_signatures(patterns):
    SEGMENTS = 'abcdefg'
    return {segment: calc_signature(patterns, segment) for segment in SEGMENTS}


def decode_segment_mappings(patterns):
    digits = digitmap.values()

    digit_sigs = calc_signatures(digits)
    pattern_sigs = calc_signatures(patterns)

    digit_lookup = {v: k for k, v in digit_sigs.items()}
    segmap = {k: digit_lookup[sig] for k, sig in pattern_sigs.items()}

    return segmap


if __name__ == '__main__':
    # pt1()
    pt2()
