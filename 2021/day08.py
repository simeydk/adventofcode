import re
from collections import Counter
from typing import List

def read_file(filename):
    with open(filename) as f:
        return [line.strip() for line in f.readlines()]

def parse_line(line):
    signal_str, output_str = line.split(' | ')
    signals = signal_str.split(' ')
    outputs = output_str.split(' ')
    return signals, outputs


def parse_input(lines):
    return [parse_line(line) for line in lines]

def flatten(l):
    return [item for sublist in l for item in sublist]

def part1(lines):
    parsed =  parse_input(lines)
    outputs = [output for signal, output in parsed]
    flattened = flatten(outputs)
    lens = [len(line) for line in flattened]
    counts = Counter(lens)
    return counts[2] + counts[3] + counts[4] + counts[7]

def parse_signals(signals: List[str]):


def part2(lines):
    parsed =  parse_input(lines)
    

test_input = [
    'be cfbegad cbdgef fgaecd cgeb fdcge agebfd fecdb fabcd edb | fdgacbe cefdb cefbgd gcbe',
    'edbfga begcd cbg gc gcadebf fbgde acbgfd abcde gfcbed gfec | fcgedb cgb dgebacf gc',
    'fgaebd cg bdaec gdafb agbcfd gdcbef bgcad gfac gcb cdgabef | cg cg fdcagb cbg',
    'fbegcd cbd adcefb dageb afcb bc aefdc ecdab fgdeca fcdbega | efabcd cedba gadfec cb',
    'aecbfdg fbg gf bafeg dbefa fcge gcbea fcaegb dgceab fcbdga | gecf egdcabf bgf bfgea',
    'fgeab ca afcebg bdacfeg cfaedg gcfdb baec bfadeg bafgc acf | gebdcfa ecba ca fadegcb',
    'dbcfg fgd bdegcaf fgec aegbdf ecdfab fbedc dacgb gdcebf gf | cefg dcbef fcge gbcadfe',
    'bdfegc cbegaf gecbf dfcage bdacg ed bedf ced adcbefg gebcd | ed bcgafe cdgba cbgef',
    'egadfb cdbfeg cegd fecab cgb gbdefca cg fgcdab egfdb bfceg | gbdfcae bgc cg cgb',
    'gcafb gcf dcaebfg ecagb gf abcdeg gaef cafbge fdbac fegbdc | fgae cfgab fg bagce',
    ]

input_raw = read_file('2021/data/day08/input.txt')

assert part1(test_input) == 26

print(part1(input_raw))
