from typing import List
import numpy as np


def read_file(filename):
    with open(filename) as f:
        return [line.strip() for line in f.readlines()]


def parse_input(input_list: List[str]):
    list_of_lists = ([list(line) for line in input_list])
    mx = np.array(list_of_lists, dtype=int)
    return mx

def bit_list_to_dec(bit_list):
    return int(''.join(list(map(str, bit_list))), 2)

def part1(input_list):
    mx = parse_input(input_list)
    modes = (np.mean(mx, axis=0) > 0.5) * 1
    modes_neg = 1 - modes
    gamma = bit_list_to_dec(modes)
    epsilon = bit_list_to_dec(modes_neg)
    return gamma * epsilon


test_input = [
    '00100',
    '11110',
    '10110',
    '10111',
    '10101',
    '01111',
    '00111',
    '11100',
    '10000',
    '11001',
    '00010',
    '01010',
]

input_raw = read_file('2021/data/day03/input.txt')

assert part1(test_input) == 22 * 9

print(part1(input_raw))
