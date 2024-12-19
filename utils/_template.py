import sys
from pathlib import Path

sys.path.append(str(Path('')))
from utils.runner import runner
from utils.utils import read_file_to_string

year=2024
day_number = 7
part1_test_solution = None
part2_test_solution = None

test_input = read_file_to_string(f"{year}/data/day{day_number:02d}/test_input.txt")
input_raw = read_file_to_string(f"{year}/data/day{day_number:02d}/input.txt")

def parse_input(input_raw):
    input = input_raw
    return input

def part1(input_raw: str):
    input = parse_input(input_raw)
    return input

def part2(input_raw: str):
    input = parse_input(input_raw)
    return input


runner(part1, part2, test_input, input_raw, part1_test_solution, part2_test_solution)