import re
from collections import Counter
from typing import List

def read_file_to_one_big_string(filename):
    with open(filename) as f:
        return f.read()

year=2024
day_number = 2
part1_test_solution = 2
part2_test_solution = 4
test_input = """
""".strip(
    "\n"
)


test_input = read_file_to_one_big_string(f"{year}/data/day{day_number:02d}/test_input.txt")
input_raw = read_file_to_one_big_string(f"{year}/data/day{day_number:02d}/input.txt")

def parse_input(input_raw: str):
    lines = input_raw.splitlines()
    numbers = [[int(x) for x in line.strip().split(" ")] for line in lines]
    return numbers

def sign(x: int):
    if x == 0:
        return 0
    elif x > 0:
        return 1
    else:
        return -1


def all_equal(l: list) -> bool:
    if len(l) <= 1: return True

    a, *rest = l
    for b in rest:
        if b != a: return False
    return True
    


def process_line(line: List[int]):
    a = line[:-1]
    b = line[1:]
    diffs = [x - y for x, y in zip(a,b)]
    signs = [sign(diff) for diff in diffs]
    max_diff = max(abs(x) for x in diffs)
    max_diff_within_bounds = max_diff <= 3
    all_same_sign = all_equal(signs)

    return max_diff_within_bounds and all_same_sign


def part1(input_raw: str):
    lines =  parse_input(input_raw)
    # print(lines)
    return sum(process_line(line) for line in lines)

def drop_one(l: list):
    for i in range(len(l)):
        m = l[:i] + l[i+1:]
        yield m

def process_line_2(line: List[int]):
    if process_line(line): return True
    for sublist in drop_one(line):
        if process_line(sublist): return True
    return False

def part2(input_raw: str):
    lines =  parse_input(input_raw)
    return sum(process_line_2(line) for line in lines)
    return 0


if part1_test_solution is None:
    print(f"Part 1 Test: {part1(test_input)}")
    quit()

assert part1(test_input) == part1_test_solution
print(f"Part 1: {part1(input_raw)}")

if part2_test_solution is None:
    print(f"Part 2 Test: {part2(test_input)}")
    quit()

assert part2(test_input) == part2_test_solution
print(f"Part 2: {part2(input_raw)}")
