from typing import Counter, List, NamedTuple
import re
from dataclasses import dataclass

DAY = 17
TEST_SOLUTION_1 = 45
TEST_SOLUTION_2 = 112


def read_file(filename) -> str:
    with open(filename, encoding="UTF-8") as f:
        return f.read()


def parse_input(data: str):
    match = re.findall(f"target area\: x=(-?\d+)..(-?\d+), y=(-?\d+)..(-?\d+)", data)[0]
    return [int(x) for x in match]


Coords = NamedTuple("Coords", [("x", int), ("y", int)])


@dataclass
class Object:
    x: int
    y: int
    v_x: int
    v_y: int

    def step(self):
        self.x += self.v_x
        self.y += self.v_y
        self.v_x = max(self.v_x - 1, 0)
        self.v_y -= 1

    def max_x(self):
        return self.v_x * (self.v_x + 1) // 2 + self.x

    def max_y(self):
        if self.v_y <= 0:
            return self.y
        return self.v_y * (self.v_y + 1) // 2 + self.y


def part1(data: str) -> int:
    x_min, x_max, y_min, y_max = parse_input(data)
    v_y = -y_min - 1
    return v_y * (v_y + 1) // 2


def do_step(x, y, v_x, v_y):
    return x + v_x, y + v_y, max(v_x - 1, 0), v_y - 1


def assess(x, y, v_x, v_y, range_x, range_y) -> str:
    if x in range_x and y in range_y:
        return "hit", ""
    elif x < min(range_x) and v_x <= 0:
        return "miss", " too little x velocity"
    elif x > max(range_x) and v_x >= 0:
        return "miss", "overshot x"
    elif y < min(range_y) and v_y < 0:
        return "miss", "overshot y"
    else:
        return "continue", ""


def part2(data: str) -> int:
    x_min, x_max, y_min, y_max = parse_input(data)
    x_range = range(x_min, x_max + 1)
    y_range = range(y_min, y_max + 1)

    starts = [(i, j) for i in range(x_max + 1) for j in range(y_min, -y_min + 1)]

    outcomes = [
        {"v": (i, j), "outcome": project(x_range, y_range, i, j)} for i, j in starts
    ]
    hits = [o for o in outcomes if o["outcome"][0] == "hit"]
    return len(hits)


def project(x_range, y_range, i, j):
    step = (0, 0, i, j)
    n = 0
    while (outcome := assess(*step, x_range, y_range))[0] == "continue":
        step = do_step(*step)
        n += 1
    return *outcome, n


test_input = """target area: x=20..30, y=-10..-5"""


input_raw = read_file(f"2021/data/day{DAY:02d}/input.txt")

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
