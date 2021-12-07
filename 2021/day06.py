import numpy as np
from collections import Counter

def read_file(filename):
    with open(filename) as f:
        return [line.strip() for line in f.readlines()]

def parse_input(input_list):
    return Counter([int(x) for x in input_list[0].split(',')])

def step(fish):
    result = {(k - 1): v for k, v in fish.items()}
    result[6] = result.get(6,0) + result.get(-1, 0)
    result[8] = result.get(8,0) + result.get(-1, 0)
    result.pop(-1, None)
    return result

def part1(input_list):
    fish = parse_input(input_list)
    for _ in range(80):
        fish = step(fish)
    return sum(fish.values())

def part2(input_list):
    fish = parse_input(input_list)
    for _ in range(256):
        fish = step(fish)
    return sum(fish.values())


test_input = [
    '3,4,3,1,2'
]

input_raw = read_file('2021/data/day06/input.txt')

assert part1(test_input) == 5934

print(part1(input_raw))

assert part2(test_input) == 26984457539

print(part2(input_raw))