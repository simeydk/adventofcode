from __future__ import annotations
from dataclasses import dataclass, field
from functools import cached_property
import sys
from pathlib import Path
from typing import Callable, Generic, Iterable, List, NamedTuple, Optional, Set, Tuple, TypeVar, Union


sys.path.append(str(Path('')))
from utils.runner import runner
from utils.utils import read_file_to_string
from utils.helpers import nested_join, nested_map, parse_grid

year=2024
day_number = 12
part1_test_solution = 1930
part2_test_solution = 1206

test_input = read_file_to_string(f"{year}/data/day{day_number:02d}/test_input.txt")
input_raw = read_file_to_string(f"{year}/data/day{day_number:02d}/input.txt")

global_counter:int = 0

T = TypeVar('T')
U = TypeVar('U')





class Cardinal(NamedTuple, Generic[T]):
    N: T
    E: T
    S: T
    W: T

    def map(self, fn: Callable[[T], U]) -> Cardinal[U]:
        return Cardinal(*map(fn, self))
    
    def turn(self, n: int = 1) -> Cardinal[T]:
        return Cardinal(
            *[self[i-n] for i in range(len(self))]
        )

assert((1,2) == (1,2))

SIDES: Cardinal[Tuple[int, int]] = Cardinal(
    (-1,0),
    (0,1),
    (1,0),
    (0,-1)
)

assert(Cardinal(1,2,3,4).turn() == Cardinal(4,1,2,3))

def coord_add(a: Tuple[int,int], b:Tuple[int,int]) -> Tuple[int,int]:
    return (a[0] + b[0], a[1] + b[1])

def get_by_attr(items: Iterable[T], key, value) -> Union[T, None]:
    for item in items:
        if object.__getattribute__(p, key) == value: # type: ignore
            return item

@dataclass(frozen=True)
class Point():
    coords: Tuple[int, int]
    value: str
    neighbours: Set[Point] = field(default_factory=set, repr=False, hash=False)

    _region: Set[Point] = field(init=False, default_factory=set, repr=False, hash=False)


    def link(self, p: Point):
        self.neighbours.add(p)
        p.neighbours.add(self)    

    @cached_property
    def same_neighbours(self):
        return {n for n in self.neighbours if n.value == self.value}
    

    @property
    def region(self):
        if self._region:
            return self._region
        region = self.compute_region()
        for point in region:
            object.__setattr__(point, '_region', region)
        return region
        

    def compute_region(self) -> Set[Point]:
        region: Set[Point] = set()
        queue: Set[Point] = set([self])
        while queue:
            candidate = queue.pop()
            region.add(candidate)
            for neighbour in candidate.same_neighbours:
                if neighbour not in region:
                    queue.add(neighbour)
        return region
    
    @cached_property
    def sn_coords(self):
        return [p.coords for p in self.same_neighbours]
    
    @cached_property
    def has_sn_cardinal(self):
        return [
            coord_add(self.coords, side) in self.sn_coords for side in SIDES
        ]
    
    @cached_property
    def cardinal(self):
        return PointsCardinal(self)
    
    def __repr__(self):
        return f"P({self.coords}, {self.value})"
    
    @cached_property
    def perimeter(self) -> int:
        return 4 - len(self.same_neighbours)
    
p = Point((0,0), "1")
assert (object.__getattribute__(p, 'value') == "1")

def get_point_by_coords(points: Iterable[Point], coords: Tuple[int, int]):
    for point in points:
        if point.coords == coords:
            return point

@dataclass(frozen=True)
class PointsCardinal:
    point: Point

    @cached_property
    def shift(self) -> Cardinal[Tuple[int, int]]:
        return SIDES.map(lambda x: coord_add(self.point.coords, x))

    @cached_property
    def same_neighbours(self) -> Cardinal[Optional[Point]]:
        return self.shift.map(lambda coords: get_point_by_coords(self.point.same_neighbours, coords))

    @cached_property
    def has_edge(self) -> Cardinal[bool]:
        return self.same_neighbours.map(lambda x: not x)
    
    @cached_property
    def first_edge(self) -> Cardinal[bool]:
        values: List[bool] = []
        for i, neighbour, has_edge in zip(range(4), self.same_neighbours.turn(), self.has_edge):
            if not(has_edge):
                values.append(False)
            elif type(neighbour) == Point:
                values.append(not neighbour.cardinal.has_edge[i])
            else:
                values.append(True)
        return Cardinal(*values)







def parse_input(input_raw):
    g_raw = parse_grid(input_raw.strip())
    g = nested_map(lambda x, i, j: Point((i,j), x), g_raw) # type: ignore
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


def unique_list(l: Iterable[T]) -> List[T]:
    result = list()
    for item in l:
        if item not in result:
            result.append(item)
    return result

def region_price(region: Set[Point]) -> int:
    area = len(region)
    perimeter = sum(p.perimeter for p in region)
    return area * perimeter

def part1(input_raw: str):
    p: Point
    points, grid = parse_input(input_raw)
    regions = unique_list(p.region for p in points)
    return sum(region_price(r) for r in regions)
    
def region_price_part2(region: Set[Point]) -> int:
    area = len(region)
    p =  list(region)[0]
    # print(f"{p.cardinal.first_edge=}")
    sides = sum(sum(p.cardinal.first_edge) for p in region)
    return area * sides

def part2(input_raw: str):
    p: Point
    points, grid = parse_input(input_raw)
    regions = unique_list(p.region for p in points)
    r = sorted(grid[0][0].region, key=lambda p:p.coords)
    print(r)
    
    return sum(region_price_part2(r) for r in regions)


runner(part1, part2, test_input, input_raw, part1_test_solution, part2_test_solution)