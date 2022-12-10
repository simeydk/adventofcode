from typing import List
import numpy as np
import re


def read_file(filename):
    with open(filename) as f:
        return [line.strip() for line in f.readlines()]


def parse_grid(grid_str: str):
    grid = [[int(x) for x in re.split("\s+", line)] for line in grid_str.split("\n")]
    return np.array(grid, dtype=int)


def parse_input(inputs: List[str]):
    nums = [int(x) for x in inputs[0].split(",")]
    grids_str = ("\n".join(inputs[2:])).split("\n\n")
    grids = [parse_grid(grid) for grid in grids_str]
    return nums, grids


def max_score(grid: np.ndarray):
    is_nan = np.isnan(grid)
    rows = np.sum(is_nan, axis=1)
    cols = np.sum(is_nan, axis=0)
    return max([max(rows), max(cols)])


def play_number(grid, number):
    return np.where(grid == number, np.nan, grid)


def part1(inputs):
    nums, grids = parse_input(inputs)
    for num in nums:
        for i in range(len(grids)):
            grids[i] = play_number(grids[i], num)
            if max_score(grids[i]) == 5:
                return int(np.sum(np.nan_to_num(grids[i]))) * num


def part2(inputs):
    nums, grids = parse_input(inputs)
    for num in nums:
        for i in range(len(grids)):
            grids[i] = play_number(grids[i], num)
        # if more than one grid is left, remove solved grids
        if len(grids) > 1:
            grids = [grid for grid in grids if max_score(grid) != 5]
        else:  # if only one grid is left, check if it won and return the score
            if max_score(grids[0]) == 5:
                return int(np.sum(np.nan_to_num(grids[0]))) * num


test_input = [
    "7,4,9,5,11,17,23,2,0,14,21,24,10,16,13,6,15,25,12,22,18,20,8,19,3,26,1",
    "",
    "22 13 17 11  0",
    "8  2 23  4 24",
    "21  9 14 16  7",
    "6 10  3 18  5",
    "1 12 20 15 19",
    "",
    "3 15  0  2 22",
    "9 18 13 17  5",
    "19  8  7 25 23",
    "20 11 10 24  4",
    "14 21 16 12  6",
    "",
    "14 21 17 24  4",
    "10 16 15  9 19",
    "18  8 23 26 20",
    "22 11 13  6  5",
    "2  0 12  3  7",
]

input_raw = read_file("2021/data/day04/input.txt")

assert part1(test_input) == 188 * 24

print(part1(input_raw))

assert part2(test_input) == 148 * 13

print(part2(input_raw))
