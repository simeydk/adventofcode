import math
import re
from typing import Tuple

def read_file_to_one_big_string(filename):
    with open(filename) as f:
        return f.read()

year = 2024
day_number = 3
part1_test_solution = 161
part2_test_solution = 48
test_input = """
""".strip(
    "\n"
)

test_input = read_file_to_one_big_string(f"{year}/data/day{day_number:02d}/test_input.txt")
input_raw = read_file_to_one_big_string(f"{year}/data/day{day_number:02d}/input.txt")

def process_match(m: Tuple[str, str]):
    a, b = m
    x = int(a)
    y = int(b)
    return x * y

def part1(input_raw: str):
    matches = re.findall(r'mul\((\d{1,3}),(\d{1,3})\)', input_raw)
    return sum(process_match(m) for m in matches)



def part2(input_raw: str):
    tmp = re.sub(r"don't()", "\nSKIP >> ", input_raw)
    lines = re.sub(r"do()", '\nDO >> ', tmp).splitlines()
    filtered = [line for line in lines if not line.startswith("SKIP")]
    joined = ''.join(filtered)
    return part1(joined)
    

    
    return filtered

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
