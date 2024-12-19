from collections import Counter
import sys
from pathlib import Path
from typing import Generator, Iterable, List

sys.path.append(str(Path('')))
from utils.runner import runner
from utils.utils import read_file_to_string

year=2024
day_number = 11
part1_test_solution = 55312
part2_test_solution = 65601038650482

test_input = read_file_to_string(f"{year}/data/day{day_number:02d}/test_input.txt")
input_raw = read_file_to_string(f"{year}/data/day{day_number:02d}/input.txt")

def parse_input(input_raw):
    input = Counter([int(x) for x in input_raw.split()])
    return input

def counter_mul(c: Counter[int], n: int) -> Counter[int]:
    for key in c.keys():
        c[key] *= n
    return c


def blink_num(x) -> Counter[int]:
    if x == 0:
        return Counter([1])
    s = f"{x:d}"
    l = len(s)
    if l % 2 == 0:
        half = l // 2
        first = int(s[:half])
        second = int(s[half:])
        return Counter([first, second])
    else:
        return Counter([x * 2024])

def blink_counter(c: Counter[int], n: int = 1) -> Counter[int]:
    result: Counter[int] = Counter()
    for value, frequency in c.items():
        x = blink_num(value)
        x = counter_mul(x, frequency)
        result.update(x)
    if n == 1:
        return result
    else:
        return blink_counter(result, n-1)


def blink_list(l : Iterable[int]) -> List[int]:
    def inner(l):
        for item in l:
            yield from blink_num(item)
    return list(inner(l))


def part1(input_raw: str):
    x = parse_input(input_raw)
    n = 25
    result = sum(blink_counter(x, n).values())
    return result

def part2(input_raw: str):
    x = parse_input(input_raw)
    n = 75
    result = sum(blink_counter(x, n).values())
    return result


runner(part1, part2, test_input, input_raw, part1_test_solution, part2_test_solution)