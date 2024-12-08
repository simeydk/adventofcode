from __future__ import annotations
from collections import defaultdict
from dataclasses import dataclass
import itertools
import math
import re
import sys
from pathlib import Path
from typing import List, Tuple

sys.path.append(str(Path('')))
from utils.runner import runner
from utils.utils import read_file_to_string

year=2024
day_number = 8
part1_test_solution = 14
part2_test_solution = 34

test_input = read_file_to_string(f"{year}/data/day{day_number:02d}/test_input.txt")
input_raw = read_file_to_string(f"{year}/data/day{day_number:02d}/input.txt")

@dataclass(eq=True, frozen=True)
class Vec:
    x: int
    y: int

    def slope(self):
        gcd = math.gcd(abs(self.x), abs(self.y))
        return self // gcd

    def __add__(self, v: Vec):
        return Vec(self.x + v.x, self.y + v.y)
    
    def __sub__(self, v: Vec):
        return Vec(self.x - v.x, self.y - v.y)
    
    def __neg__(self):
        return Vec(-self.x, -self.y)
    
    def __lt__(self, v: Vec):
        return self.x < v.x and self.y < v.y
    
    def __gt__(self, v: Vec):
        return self.x > v.x and self.y > v.y
    
    def __le__(self, v: Vec):
        return self.x <= v.x and self.y <= v.y
    
    def __ge__(self, v: Vec):
        return self.x >= v.x and self.y >= v.y

    def __floordiv__(self, b: int):
        return Vec(self.x // b, self.y // b)

    def __truediv__(self, b: int):
        return Vec(self.x // b, self.y // b)
    
    def __mul__(self, b: int):
        return Vec(self.x * b, self.y * b)
    
    def __len__(self):
        return 2

    def __getitem__(self, k):
        while k < 0:
            k += len(self)

        if k == 1:
            return self.x
        elif k ==2:
            return self.y
        else:
            raise IndexError(f"Index '{k}' out of range")

        


def parse_input(input_raw):
    lines = input_raw.splitlines()
    antennas: defaultdict[None, List[Vec]] = defaultdict(list)
    for y, line in enumerate(lines):        
        for x, char in enumerate(line):
            if char != '.':
                antennas[char].append(Vec(x, y))
    w = len(lines[0])
    h = len(lines)
    return Vec(w,h), antennas

def process_input1(antennas: defaultdict[None, List[Vec]]):
    antinodes: defaultdict[Vec, int] = defaultdict(int)

    for char, antennae in antennas.items():
        for a, b in itertools.combinations(antennae, 2):
            delta = b - a
            one = b + delta
            two = a - delta
            antinodes[one] += 1
            antinodes[two] += 1
    return antinodes

def part1(input_raw: str):
    board, antennas = parse_input(input_raw)
    antinodes = process_input1(antennas).keys()
    bounded = [a for a in antinodes if 0 <= a.x < board.x and 0 <= a.y < board.y]
    return len(bounded)

def process_input2(antennas: defaultdict[None, List[Vec]], board:Vec):
    antinodes: defaultdict[Vec, int] = defaultdict(int)

    for char, antennae in antennas.items():
        for a, b in itertools.combinations(antennae, 2):
            delta = b - a
            unit = delta.slope()
            
            cursor = a
            while ((0 <= cursor.x < board.x) and (0 <= cursor.y < board.y)):
                antinodes[cursor] += 1
                cursor += unit
            cursor = a - unit
            
            while ((0 <= cursor.x < board.x) and (0 <= cursor.y < board.y)):
                antinodes[cursor] += 1
                cursor -= unit

    return antinodes


def part2(input_raw: str):
    board, antennas = parse_input(input_raw)
    return len(process_input2(antennas, board).keys())


runner(part1, part2, test_input, input_raw, part1_test_solution, part2_test_solution)