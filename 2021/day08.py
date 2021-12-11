import re
from collections import Counter
from typing import List

def read_file(filename):
    with open(filename) as f:
        return [line.strip() for line in f.readlines()]

def sort_string(string):
    return ''.join(sorted(string))

def parse_line(line):
    signal_str, output_str = line.split(' | ')
    signals = map(sort_string, signal_str.split(' '))
    outputs = map(sort_string, output_str.split(' '))
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

def is_superset(a, b):
    return all(char in a["text"] for char in b["text"])

def solve_signals(signals_list: List[str]):
    signals = [{"text": x, "len":len(x), "value": None} for x in signals_list]
    solved = {}

    def assign(signal, value):
        signal['value'] = value
        solved[value] = signal

    for signal in signals:
        # ONE is the only digit with 2 strokes
        if signal["len"] == 2:
            assign(signal, 1)
        # FOUR is the only digit with 2 strokes
        if signal["len"] == 4:
            assign(signal, 4)
        # SEVEN is the only digit with 3 strokes
        elif signal["len"] == 3:
            assign(signal, 7)
        # EIGHT is the only digit with 7 strokes
        elif signal["len"] == 7:
            assign(signal, 8)
    for signal in signals:
        if signal['value'] != None: pass            
        # There are three digits with 6 strokes: 0, 6 and 9. 
        # NINE is the only digit with 6 strokes that is a superset of 4
        elif (signal["len"] == 6) and is_superset(signal, solved[4]):
            assign(signal, 9)
        # SIX is the only digit with 6 strokes that is not a superset of 1
        elif (signal["len"] == 6) and not (is_superset(signal, solved[1])):
            assign(signal, 6)
        # There are three digits with 5 strokes: 2, 3 and 5
        # THREE is the only digit with 5 strokes that is a superset of 7
        elif ((signal["len"] == 5) and is_superset(signal, solved[7])):
            assign(signal, 3)
    for signal in signals:
        if signal['value'] != None: pass
        # TWO is the only digit with 5 strokes that is a subset of 6
        elif ((signal["len"] == 5) and is_superset(solved[6], signal)):
            assign(signal, 5)
        # ZERO is the only remaining digit with 6 strokes
        elif (signal["len"] == 6) and signal["value"] == None:
            assign(signal, 0)
        # FIVE is the only remaining digit with 5 strokes
        elif (signal["len"] == 5) and signal["value"] == None:
            assign(signal, 2)

    incomplete = [signal for signal in signals if signal['value'] == None]
    if incomplete:
        raise Exception("Incomplete: {}".format(incomplete))
    return signals

def make_mapper(signals):
    return {signal['text']: signal['value'] for signal in signals}

            

def solve_line(parsed_line):
    solved  = solve_signals(parsed_line[0])
    mapper = make_mapper(solved)
    result = int(''.join([str(mapper[x]) for x in parsed_line[1]]))
    return result


def part2(lines):
    parsed =  parse_input(lines)
    values = [solve_line(x) for x in parsed]
    return sum(values)
    

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

assert part2(test_input) == 61229

print(part2(input_raw))