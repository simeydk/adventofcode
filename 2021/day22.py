from typing import List, NamedTuple
import re
import numpy as np

DAY = 22
TEST_SOLUTION_1 = 590784
TEST_SOLUTION_2 = None

def read_file(filename) -> str:
    with open(filename, encoding="UTF-8") as f:
        return f.read()

def parse_line(line: str):
    result = re.findall('(\w+) x=(-?\d+)..(-?\d+),y=(-?\d+)..(-?\d+),z=(-?\d+)..(-?\d+)', line)[0]
    on = result[0] == 'on'
    x_min, x_max, y_min, y_max, z_min, z_max = [int(x) for x in result[1:]]
    x_max = x_max + 1
    y_max = y_max + 1
    z_max = z_max + 1
    return on, np.array([x_min, x_max]), np.array([y_min, y_max]), np.array([z_min, z_max])

def parse_input(data: str):
    return [parse_line(line) for line in data.splitlines()]


def clamp_instruction(instruction, grid_ranges):
    on, x_range, y_range, z_range = instruction
    x_range = x_range.clip(*grid_ranges[0])
    y_range = y_range.clip(*grid_ranges[1])
    z_range = z_range.clip(*grid_ranges[2])
    new_instruction = on, x_range, y_range, z_range
    print(f"{instruction} => {new_instruction}")
    return new_instruction


def part1(data: str) -> int:
    instructions = parse_input(data)
    grid_ranges = [(-50,51), (-50,51), (-50,51)]
    clamped_instructions = [clamp_instruction(instruction, grid_ranges) for instruction in instructions]
    grid = np.zeros([hi - low for low, hi in grid_ranges], dtype=bool)
    for on, x_range, y_range, z_range in clamped_instructions:
        x_range -= grid_ranges[0][0]
        y_range -= grid_ranges[1][0]
        z_range -= grid_ranges[2][0]
        grid[x_range[0]:x_range[1], y_range[0]:y_range[1], z_range[0]:z_range[1]] = on
    return np.sum(grid)

def part2(data: str) -> int:
    pass

test_input = """on x=-20..26,y=-36..17,z=-47..7
on x=-20..33,y=-21..23,z=-26..28
on x=-22..28,y=-29..23,z=-38..16
on x=-46..7,y=-6..46,z=-50..-1
on x=-49..1,y=-3..46,z=-24..28
on x=2..47,y=-22..22,z=-23..27
on x=-27..23,y=-28..26,z=-21..29
on x=-39..5,y=-6..47,z=-3..44
on x=-30..21,y=-8..43,z=-13..34
on x=-22..26,y=-27..20,z=-29..19
off x=-48..-32,y=26..41,z=-47..-37
on x=-12..35,y=6..50,z=-50..-2
off x=-48..-32,y=-32..-16,z=-15..-5
on x=-18..26,y=-33..15,z=-7..46
off x=-40..-22,y=-38..-28,z=23..41
on x=-16..35,y=-41..10,z=-47..6
off x=-32..-23,y=11..30,z=-14..3
on x=-49..-5,y=-3..45,z=-29..18
off x=18..30,y=-20..-8,z=-3..13
on x=-41..9,y=-7..43,z=-33..15
on x=-54112..-39298,y=-85059..-49293,z=-27449..7877
on x=967..23432,y=45373..81175,z=27513..53682"""

# test_input = """on x=10..12,y=10..12,z=10..12
# on x=11..13,y=11..13,z=11..13
# off x=9..11,y=9..11,z=9..11
# on x=10..10,y=10..10,z=10..10"""

input_raw = read_file(f'2021/data/day{DAY:02d}/input.txt')

if TEST_SOLUTION_1:
    assert part1(test_input) == TEST_SOLUTION_1
    print(f"Solution 1:\n{part1(input_raw)}")
    if TEST_SOLUTION_2:
        assert part2(test_input) == TEST_SOLUTION_2
        print(f"Solution 2:\n{part2(input_raw)}")
    else:
        print(f"Test 2:\n{part2(test_input)}")
else:
    print(f"Test 1:\n{part1(test_input)}")
    
