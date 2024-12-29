from __future__ import annotations
from collections import Counter
from functools import cached_property
import math
import re
import sys
from pathlib import Path
from typing import Generic, Iterable, List, NamedTuple, Optional, SupportsIndex, Tuple, TypeVar, Union
from unicodedata import numeric

sys.path.append(str(Path('')))
from utils.helpers import create_grid, nested_join
from utils.runner import runner
from utils.utils import read_file_to_string

year=2024
day_number = 14
part1_test_solution = 12
part2_test_solution = None

test_input = read_file_to_string(f"{year}/data/day{day_number:02d}/test_input.txt")
input_raw = read_file_to_string(f"{year}/data/day{day_number:02d}/input.txt")

Numeric = Union[int, float]

INFINITY = float('inf')

class V(NamedTuple):
    x: Numeric
    y: Numeric

    def __repr__(self) -> str:
        return f"V({self.x}, {self.y})"
    
    @cached_property
    def slope(self):
        return self.y / self.x
    
    def __add__(self, b: V) -> V:
        return V(self.x + b.x, self.y + b.y)

    def __sub__(self, b: V) -> V:
        return V(self.x - b.x, self.y - b.y)

    def __mul__(self, b: Numeric) -> V:
        return V(self.x * b, self.y * b)
    
    def __truediv__(self, b: Numeric) -> V:
        return V(self.x / b, self.y / b)
    
    def __mod__(self, b: Union[Numeric, V]) -> V:
        if type(b) == V:
            return V(self.x % b.x, self.y % b.y)
        else:
            n = float(b) # type: ignore
            return V(self.x % n, self.y % n)

    def to_int(self) -> V:
        return V(int(self.x), int(self.y))

    def piecewise_div(self, b: V):
        return self.x / b.x, self.y / b.y

    def is_multiple_of(self, b:V):
        x, y = self.piecewise_div(b)
        if x == y and x.is_integer():
            return int(x)
        else:
            return None



class Robot(NamedTuple):
    p: V
    v: V

    def __repr__(self) -> str:
        return f"Robot({', '.join([str(x) for x in self])})"
    
    def step(self, n=1, board: V = V(INFINITY, INFINITY)):
        x, y = self.p + self.v * n
        p = V(x,y) % board        
        return Robot(p, self.v)



def parse_robot(machine_text:str):
    pattern = r'[-+]?\d+'
    # Find all matches
    numbers = re.findall(pattern, machine_text)
    # Convert matches to integers
    ay, ax, by, bx = list(map(int, numbers))
    return Robot(V(ax,ay), V(bx,by)) 

def parse_input(input_raw):
    robots_raw = input_raw.strip().splitlines()
    robots = [parse_robot(s) for s in robots_raw]
    return robots

def quadrant_split(x: Numeric) -> Tuple[int, int, int, int]:
    h = int(x // 2)
    return 0, h, h+1, int(x)

class Quadrant(NamedTuple):
    start: V
    end: V

    def contains(self, v: V) -> bool:
        return (self.start.x <= v.x < self.end.x) and (self.start.y <= v.y < self.end.y)


    @staticmethod
    def from_board(board: V):
        half = (board / 2).to_int()
        x = quadrant_split(board.x)
        y = quadrant_split(board.y)
        return (
            Quadrant(V(x[0], y[0]), V(x[1], y[1])),
            Quadrant(V(x[0], y[2]), V(x[1], y[3])),
            Quadrant(V(x[2], y[0]), V(x[3], y[1])),
            Quadrant(V(x[2], y[2]), V(x[3], y[3])),
        )

def print_board(board: V, robots: List[Robot] = []):
    grid: list[list[int]] = create_grid(board.x, board.y, 0) # type: ignore
    for robot in robots:
        grid[robot.p.x][robot.p.y] += 1
    print(nested_join(grid, delimiter="", map_fn=lambda x: str(x) if x else "."))

def find_quadrant(robot: Robot, quadrants: Iterable[Quadrant]) -> Optional[int]:
    for i, q in enumerate(quadrants):
        if q.contains(robot.p):
            return i + 1
    

def part1(input_raw: str):
    robots = parse_input(input_raw)
    board: V
    if len(robots) < 100:
        board = V(7, 11)
    else:
        board = V(103, 101)
    quadrants = Quadrant.from_board(board)

    stepped = [r.step(100, board) for r in robots]
    counts = Counter(find_quadrant(r, quadrants) for r in stepped)
    return (math.prod(value for key, value in counts.items() if key))

def part2(input_raw: str):
    return None

runner(part1, part2, test_input, input_raw, part1_test_solution, part2_test_solution)