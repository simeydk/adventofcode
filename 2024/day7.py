import sys
from pathlib import Path

sys.path.append(str(Path('')))
from utils.runner import runner
from utils.utils import read_file_to_string

import itertools
from typing import Callable, Iterable, List, Set, Tuple, TypeVar




year=2024
day_number = 7
part1_test_solution = 3749
part2_test_solution = 11387


test_input = read_file_to_string(f"{year}/data/day{day_number:02d}/test_input.txt")
input_raw = read_file_to_string(f"{year}/data/day{day_number:02d}/input.txt")

def parse_line(line: str):
    result_str, num_str = line.split(": ")
    result = int(result_str)
    nums = [int(x) for x in num_str.split(' ')]
    return result, nums

def parse_input(input_raw):
    lines = input_raw.splitlines()
    return [parse_line(line) for line in lines]
    
def generate_operations(length, operations = ['+', '*']):
    return list(itertools.product(operations, repeat = length))

add = lambda x, y: x + y
mul = lambda x, y: x * y
sub = lambda x, y: x - y
div = lambda x, y: x / y
con = lambda x, y: int(f"{x}{y}")

def step_line(numbers: List[int], operations: List[Callable[[int, int], int]] = [add, mul]):
    if len(numbers) == 2:
        raise ValueError("Less than 2 numbers supplied: {numbers}")
    x, y, * rest = numbers
    for f in operations:
        yield [f(x,y),  *rest]


def process_line(line, operations: List[Callable[[int, int], int]] = [add, mul]):
    if len(line) < 2:
        raise ValueError("Less than 2 numbers supplied: {line}")
    x, y, *rest = line
    if len(line) == 2:
        for f in operations:
            yield f(x, y)
    else:
        for f in operations:
            yield from process_line([f(x,y), *rest], operations) 
    
def evaluate_line(test_val, iter: Iterable):
    for x in iter:
        if x == test_val:
            return True
    return False

def part1(input_raw: str):
    input = parse_input(input_raw)
    test_val, line = input[1]
    n = 0
    for row in input:
        test_val, line = row
        if evaluate_line(test_val, process_line(line)):
            n += test_val
    return n

def part2(input_raw: str):
    input = parse_input(input_raw)
    test_val, line = input[1]
    n = 0
    for row in input:
        test_val, line = row
        if evaluate_line(test_val, process_line(line, [add, mul, con])):
            n += test_val
    return n



runner(part1, part2, test_input, input_raw, part1_test_solution, part2_test_solution)

# if part1_test_solution is None:
#     print(f"Part 1 Test: {part1(test_input)}")
#     quit()

# assert part1(test_input) == part1_test_solution
# print(f"Part 1: {part1(input_raw)}")

# if part2_test_solution is None:
#     print(f"Part 2 Test: {part2(test_input)}")
#     quit()

# assert part2(test_input) == part2_test_solution
# print(f"Part 2: {part2(input_raw)}")
