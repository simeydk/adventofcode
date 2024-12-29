from __future__ import annotations
from functools import cached_property
import re
import sys
from pathlib import Path
from typing import Generic, List, NamedTuple, Optional, SupportsIndex, Tuple, TypeVar, Union
from unicodedata import numeric

sys.path.append(str(Path('')))
from utils.runner import runner
from utils.utils import read_file_to_string

year=2024
day_number = 13
part1_test_solution = 480
part2_test_solution = 875318608908

test_input = read_file_to_string(f"{year}/data/day{day_number:02d}/test_input.txt")
input_raw = read_file_to_string(f"{year}/data/day{day_number:02d}/input.txt")

Numeric = Union[int, float]

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
    
    def piecewise_div(self, b: V):
        return self.x / b.x, self.y / b.y
    
    def is_multiple_of(self, b:V):
        x, y = self.piecewise_div(b)
        if x == y and x.is_integer():
            return int(x)
        else:
            return None


class Machine(NamedTuple):
    a: V
    b: V
    prize: V

    def __repr__(self) -> str:
        return f"Machine({', '.join([str(x) for x in self])})"

def parse_machine(machine_text:str):
    pattern = r'[-+]?\d+'
    # Find all matches
    numbers = re.findall(pattern, machine_text)
    # Convert matches to integers
    ax, ay, bx, by, px, py = list(map(int, numbers))
    return Machine(V(ax,ay), V(bx,by), V(px,py)) 

# def assess_machine(M:Machine, max_n = 100) -> Optional[Tuple[int,int]]:
#     max_n = int(min(max_n, max(*M.prize.piecewise_div(M.a))))
#     for n in range(0, max_n + 1):
#         a_mul = M.a * n
#         rest = M.prize - a_mul
#         m = rest.is_multiple_of(M.b)
#         if m:
#             return n, m

def parse_input(input_raw):
    machines_raw = input_raw.strip().split('\n\n')
    machines = [parse_machine(s) for s in machines_raw]
    return machines

def part1(input_raw: str):
    machines = parse_input(input_raw)
    assessed = [assess_machine(m) for m in machines]
    costs = [x[0] * 3 + x[1] if x else 0 for x in assessed]
    return sum(costs)

def modify_machines_for_part2(machines: List[Machine]) -> List[Machine]:
    TO_ADD = V(1, 1) * 10 ** 13
    return [
        Machine(m.a, m.b, m.prize + TO_ADD) for m in machines
    ]

def invert(n: V, m: V):
    a, b = n
    c, d = m
    det = (a * d - b * c)
    return (d / det, -b / det), (-c / det, a / det)

def mxmult(A, x):
    A1, A2 = A
    a, b = A1
    c, d = A2
    x1, x2 = x
    return a * x1 + b * x2, c * x1 + d * x2

def assess_machine(m: Machine):
    a = (m.prize.x * m.b.y - m.prize.y * m.b.x) / (m.a.x * m.b.y - m.a.y * m.b.x)
    b = (m.a.x*m.prize.y - m.a.y*m.prize.x) / (m.a.x * m.b.y - m.a.y * m.b.x)
    if a.is_integer() and b.is_integer():
        test = m.a * a + m.b * b - m.prize
        assert(test == V(0,0))
        return a, b


def part2(input_raw: str):
    machines = parse_input(input_raw)
    machines = modify_machines_for_part2(machines)
    assessed = [assess_machine(m) for m in machines]
    costs = [x[0] * 3 + x[1] if x else 0 for x in assessed]
    return sum(costs)

runner(part1, part2, test_input, input_raw, part1_test_solution, part2_test_solution)