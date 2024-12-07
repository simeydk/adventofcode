from functools import cmp_to_key
import re
from collections import Counter
from typing import Callable, Iterable, List, Tuple, TypeVar

def read_file_to_one_big_string(filename):
    with open(filename) as f:
        return f.read()

year=2024
day_number = 5
part1_test_solution = 143
part2_test_solution = 123
test_input = """
""".strip(
    "\n"
)


test_input = read_file_to_one_big_string(f"{year}/data/day{day_number:02d}/test_input.txt")
input_raw = read_file_to_one_big_string(f"{year}/data/day{day_number:02d}/input.txt")

def transpose(M):
    return [[M[j][i] for j in range(len(M))] for i in range(len(M[0]))]

def parse_csv(s:str, delimiter = ",", map_fn = int):
    return [[map_fn(x) for x in line.split(delimiter)] for line in s.splitlines()]

def parse_rules(rules:str):
    return [[int(x) for x in line.split('|')] for line in  rules.splitlines()]

def parse_input(input_raw: str):
    rules_raw, updates_raw = input_raw.split('\n\n')
    rules = parse_csv(rules_raw, "|")
    updates = parse_csv(updates_raw)
    return rules, updates

def process_update(update: List[int], rules: List[List[int]]):
    for x, y in rules:
        if x in update and y in update:
            if update.index(x) > update.index(y):
                return 0
    mid_index = int((len(update)) / 2)         
    return update[mid_index]


T = TypeVar("T")

def sort_comp(l: Iterable[T], cmp: Callable):
    f = cmp_to_key(cmp)
    return sorted(l, key=f)

def order_update(update: List[int], rules: List[List[int]]):
    def compare(a, b):
        if [a, b] in rules:
            result = -1
        elif [b, a] in rules:
            result = 1
        else:
            result = 0
        return result
    return sort_comp(update, compare)
    

def part1(input_raw: str):
    rules, updates = parse_input(input_raw)
    return sum(process_update(update, rules) for update in updates)


def part2(input_raw: str):
    rules, updates = parse_input(input_raw)
    unordered = [u for u in updates if process_update(u, rules) == 0]
    ordered = [order_update(u, rules) for u in unordered]
    return sum(process_update(update, rules) for update in ordered)


if part1_test_solution is None:
    print(f"Part 1 Test: {part1(test_input)}")
    quit()

assert part1(test_input) == part1_test_solution
print(f"Part 1: {part1(input_raw)}")

if part2_test_solution is None:
    print(f"Part 2 Test: {part2(test_input)}")
    quit()

assert part2(test_input) == part2_test_solution
print(f"Part 2: {part2(input_raw)}")
