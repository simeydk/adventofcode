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

def get_modes(bit_mx):
    return (np.mean(bit_mx, axis=0) >= 0.5) * 1

def part1(input_list):
    mx = parse_input(input_list)
    modes = get_modes(mx)
    modes_neg = 1 - modes
    gamma = bit_list_to_dec(modes)
    epsilon = bit_list_to_dec(modes_neg)
    return gamma * epsilon

def get_oxy_bits(mx):
    for i in range(mx.shape[1]):
        modes = get_modes(mx)
        mx = mx[mx[:,i] == modes[i]]
        if mx.shape[0] == 1:
            break
    return mx[0]

def get_co2_bits(mx):
    for i in range(mx.shape[1]):
        modes = get_modes(mx)
        mx = mx[mx[:,i] == (1 - modes[i])]
        if mx.shape[0] == 1:
            break
    return mx[0]

def part2(input_list) -> int:
    mx = parse_input(input_list)
    oxy = bit_list_to_dec(get_oxy_bits(mx))
    co2 = bit_list_to_dec(get_co2_bits(mx))
    return oxy * co2


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

assert part2(test_input) == 23 * 10

print(part2(input_raw))