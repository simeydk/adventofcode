import re
import sys
from pathlib import Path
from typing import List, Tuple

sys.path.append(str(Path('')))
from utils.runner import runner
from utils.utils import read_file_to_string

year=2023
day_number = 4
part1_test_solution = 13
part2_test_solution = None

test_input = read_file_to_string(f"{year}/data/day{day_number:02d}/test_input.txt")
input_raw = read_file_to_string(f"{year}/data/day{day_number:02d}/input.txt")

def parse_input(input_raw):
    lines = input_raw.splitlines()
    return [parse_line(line) for line in lines]

def parse_line(line: str):
    a, b, c = line.replace(': ', " | ").split(" | ")
    winners = [int(x) for x in b.split()]
    mine = [int(x) for x in c.split()]
    return winners, mine

def process_line(inputs: Tuple[List[int], List[int]]):
    winners, mine = inputs
    matches = [x for x in mine if x in winners]
    if matches:
        return 2 ** (len(matches) - 1)
    else:
        return 0

def part1(input_raw: str):
    input = parse_input(input_raw)
    return sum(process_line(line) for line in input)



def part2(input_raw: str):
    input = parse_input(input_raw)
    return sum(process_line(line) for line in input)


runner(part1, part2, test_input, input_raw, part1_test_solution, part2_test_solution)