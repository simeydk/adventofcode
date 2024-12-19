from __future__ import annotations

from dataclasses import dataclass
import sys
from pathlib import Path
from typing import Generator, List

sys.path.append(str(Path('')))
from utils.runner import runner
from utils.utils import read_file_to_string

year=2024
day_number = 9
part1_test_solution = 1928
part2_test_solution = 2858

test_input = read_file_to_string(f"{year}/data/day{day_number:02d}/test_input.txt")
input_raw = read_file_to_string(f"{year}/data/day{day_number:02d}/input.txt")

def parse_input(input_raw):
    memory = []
    for i, char in enumerate(input_raw.strip()):
        is_data = (i % 2) == 0
        if is_data:
            file_id = i // 2
        else:
            file_id = None
        n = int(char)
        memory += [file_id] * n
    return memory

def part1(input_raw: str):
    memory = parse_input(input_raw)
    num_filled = len([x for x in memory if x is not None])
    a = 0
    b = len(memory) - 1
    while a < b:
        if memory[a] is None:
            if memory[b] is None:
                b -= 1
            else:
                memory[a] = memory[b]
                memory[b] = None
                a += 1
                b -= 1
        else:
            a += 1

    return sum(i * int(x) if x else 0 for i, x in enumerate(memory))

@dataclass
class File():
    id: int
    start: int
    size: int

    @property
    def end(self):
        return self.start + self.size

    def gap(self, b: File):
        start = b.end
        size = self.start - start
        return File(-1,start, size)

    @property
    def checksum(self):
        slots = range(self.start, self.start + self.size)
        return self.id * sum(slots)

def parse_input2(input_raw):
    memory = []
    start = 0
    for i, char in enumerate(input_raw.strip()):
        is_data = (i % 2) == 0
        size = int(char)
        if is_data:
            file_id = i // 2
            memory.append(File(file_id, start, size))
        start += size
    return memory

def get_gaps(l: List[File]) -> Generator[File, None, None]:
    for i in range(len(l) -1):
        gap = l[i+1].gap(l[i])
        yield gap

def part2(input_raw: str):
    memory = parse_input2(input_raw)
    ids = [f.id for f in reversed(memory)]
    for id in ids:
        curr_file: File
        for file in reversed(memory):
            if file.id == id:
                curr_file=file
                break
        for gap in get_gaps(memory):
            if gap.start > curr_file.start:
                break
            elif curr_file.size <= gap.size:
                curr_file.start = gap.start
                memory.sort(key=lambda x: x.start)
    return sum(f.checksum for f in memory)


runner(part1, part2, test_input, input_raw, part1_test_solution, part2_test_solution)