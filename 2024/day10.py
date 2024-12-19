from __future__ import annotations
from dataclasses import dataclass, field
from functools import cached_property
import sys
from pathlib import Path
from typing import List, Set, Tuple


sys.path.append(str(Path('')))
from utils.runner import runner
from utils.utils import read_file_to_string
from utils.helpers import nested_join, nested_map, parse_grid

year=2024
day_number = 10
part1_test_solution = 36
part2_test_solution = 81

test_input = read_file_to_string(f"{year}/data/day{day_number:02d}/test_input.txt")
input_raw = read_file_to_string(f"{year}/data/day{day_number:02d}/input.txt")

@dataclass(frozen=True)
class Point():
    coords: Tuple[int, int]
    value: int
    neighbours: Set[Point] = field(default_factory=set, repr=False, hash=False)

    def link(self, p: Point):
        self.neighbours.add(p)
        p.neighbours.add(self)

    @cached_property
    def ascenders(self) -> List[Point]:
        return [
            p for p in self.neighbours if p.value == self.value + 1
        ]
    @cached_property
    def reachable_9s(self) -> Set(Point):
        s = set()
        if self.value >= 9:
            s.add(self)
        else:
            for p in self.ascenders:
                s.update(p.reachable_9s)
            
        return s
    
    @cached_property
    def num_reachable_9s(self):
        return len(self.reachable_9s)

    @cached_property
    def num_paths_to_9(self) -> int:
        if self.value >= 9:
            return 1
        else:
            return sum(p.num_paths_to_9 for p in self.ascenders)
    


def parse_input(input_raw):
    g_raw = parse_grid(input_raw.strip())
    g = nested_map(lambda x, i, j: Point((i,j), int(x)), g_raw)
    points: Set[Point] = set()
    for row in range(len(g)):
        for col in range(len(g[0])):
            x = g[row][col]
            points.add(x)
            try:
                r = g[row][col +1]
                x.link(r)
            except:
                pass
   
            try:
                b = g[row + 1][col]
                x.link(b)             
            except:
                pass

    return points, g

def part1(input_raw: str):
    p: Point
    points, grid = parse_input(input_raw)
    zeros = [p for p in points if p.value == 0]
    # print([(p.coords, p.num_paths_to_9) for p in zeros])
    # print(nested_join(grid, delimiter = "  ", map_fn = lambda p: f"{p.value}[{p.num_reachable_9s:2d}]"))
    # print(nested_join(grid, delimiter = "  ", map_fn = lambda p: f"{p.value}[{len(p.neighbours)}]"))
    # print(nested_join(grid, delimiter = "", map_fn = lambda p: f"{p.value}") == input_raw.strip())
    return sum(p.num_reachable_9s for p in zeros)

def part2(input_raw: str):
    p: Point
    points, grid = parse_input(input_raw)
    zeros = [p for p in points if p.value == 0]
    # print([(p.coords, p.num_paths_to_9) for p in zeros])
    # print(nested_join(grid, delimiter = "  ", map_fn = lambda p: f"{p.value}[{p.num_reachable_9s:2d}]"))
    # print(nested_join(grid, delimiter = "  ", map_fn = lambda p: f"{p.value}[{len(p.neighbours)}]"))
    # print(nested_join(grid, delimiter = "", map_fn = lambda p: f"{p.value}") == input_raw.strip())
    return sum(p.num_paths_to_9 for p in zeros)


runner(part1, part2, test_input, input_raw, part1_test_solution, part2_test_solution)