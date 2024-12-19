import sys
from pathlib import Path

sys.path.append(str(Path('')))
from utils.runner import runner
from utils.utils import read_file_to_string

year=2023
day_number = 3
part1_test_solution = 4361
part2_test_solution = None

test_input = read_file_to_string(f"{year}/data/day{day_number:02d}/test_input.txt")
input_raw = read_file_to_string(f"{year}/data/day{day_number:02d}/input.txt")

def parse_input(input_raw):
    lines = input_raw.splitlines()
    numbers = []
    objects = set()
    for row, line in enumerate(lines):
        nums = []
        for col, char in enumerate(line):
            # print(row, col, char, char.isnumeric(), nums)
            if char.isnumeric():
                # print('appending')
                nums.append((char, (row, col)))
                # print(nums)
            else:
                # print('non-numeric')
                if len(nums):
                    # print('flushing')
                    numbers.append(nums)
                    nums = []
                if char != '.':
                    objects.add((row, col))

    return numbers, objects

def process_number(number_entries, objects):
    value = int(''.join([x for x, y in number_entries]))
    valid = False
    for col in range(number_entries[0][1][1] -1,number_entries[-1][1][1] + 2):
        center_row = number_entries[0][1][0] 
        for row in range(center_row -1, center_row + 2):
            if (row, col) in objects:
                valid = True
                return value, valid
            
    return value, valid


def part1(input_raw: str):
    # print(input_raw)
    numbers, objects = parse_input(input_raw)
    processed = [process_number(number, objects) for number in numbers]
    return sum(value for value, valid in processed if valid)
    return [process_number(number, objects) for number in numbers]

def part2(input_raw: str):
    input = parse_input(input_raw)
    return input


runner(part1, part2, test_input, input_raw, part1_test_solution, part2_test_solution)