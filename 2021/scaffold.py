from typing import List

def read_file(filename):
    with open(filename) as f:
        return [line.strip() for line in f.readlines()]

def part1(data: List[str]) -> int:
    pass

def part2(data: List[str]) -> int:
    pass

test_input = [
    '#PASTE HERE'
]


DAY = 11
TEST_SOLUTION_1 = None
TEST_SOLUTION_2 = None

input_raw = read_file(f'2021/data/day{DAY:02d}/input.txt')

if TEST_SOLUTION_1:
    assert part1(test_input) == TEST_SOLUTION_1
    print(f"Solution 1: {part1(input_raw)}")
    if TEST_SOLUTION_2:
        assert part2(test_input) == TEST_SOLUTION_2
        print(f"Solution 2: {part2(input_raw)}")
    else:
        print(f"Test 2: {part2(test_input)}")
else:
    print(f"Test 1: {part1(test_input)}")
    
