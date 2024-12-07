from concurrent.futures import ThreadPoolExecutor
from functools import cmp_to_key
import re
from collections import Counter
from typing import Callable, Iterable, List, Set, Tuple, TypeVar

def read_file_to_one_big_string(filename):
    with open(filename) as f:
        return f.read()

year=2024
day_number = 6
part1_test_solution = 41
part2_test_solution = 6
test_input = """
""".strip(
    "\n"
)


test_input = read_file_to_one_big_string(f"{year}/data/day{day_number:02d}/test_input.txt")
input_raw = read_file_to_one_big_string(f"{year}/data/day{day_number:02d}/input.txt")


T = TypeVar("T")

def parse_csv(s:str, delimiter = ",", map_fn: Callable[[str], T] = lambda x: x):
    return [[map_fn(x) for x in (line.split(delimiter) if delimiter else line)] for line in s.splitlines()]

Vec = Tuple[int, int]

DIRECTIONS = [(0, -1), (1, 0), (0, 1), (-1, 0)]

def parse_input(input_raw):
    input = parse_csv(input_raw, '')
    h = len(input)
    w = len(input[0])
    things: Set[Vec] = set()
    player = (DIRECTIONS[0], (-1,-1))
    for y, line in enumerate(input):
        for x, val in enumerate(line):
            if val == '.': 
                pass
            elif val == '#':
                things.add((x, y))
            elif val == '^':
                player = (DIRECTIONS[0], (x, y))
            else:
                raise ValueError(f"entry {val} located at ({x}, {y})) which is unhandled in the code")
    if player[1] == (-1, -1):
        raise ValueError("No player found")
    return player, things, w, h




def process_puzzle(player, things, w, h):
    direction, position = player
    def in_bounds(v: Vec):
        x, y = v
        return (0 <= x < w) and (0 <= y < h)
    
    def turn(direction: Vec):
        i = DIRECTIONS.index(direction)
        i = (i + 1) % len(DIRECTIONS)
        return DIRECTIONS[i]

    tracks: Set[Vec] = set()
    seen: Set[Tuple[Vec, Vec]] = set() 
    while in_bounds(position):
        if (direction, position) in seen:
            return set()
        if len(seen) > w * h:
            return set()

        tracks.add(position)
        seen.add((direction, position))
        candidate_pos = (position[0] + direction[0], position[1] + direction[1])
        if candidate_pos in things:
            direction = turn(direction)
        else:
            position = candidate_pos
    return tracks

def part1(input_raw: str):
    player, things, w, h = parse_input(input_raw)
    return len(process_puzzle(player, things, w, h))


def threaded_map(map_fn, iter):
    with ThreadPoolExecutor() as tpe:
        return list(tpe.map(map_fn, iter))    
    


def part2(input_raw: str):
    player, things, w, h = parse_input(input_raw)
    loops = 0
    original_tracks = process_puzzle(player, things, w, h)
    candidates = original_tracks
    
    results = threaded_map(lambda c: test_candidate(player, things, w, h, c), candidates)
    return len([x for x in results if x == 0])
    

def test_candidate(player, things, w, h, candidate):
    new_things = things.copy()
    new_things.add(candidate)
    result = process_puzzle(player, new_things, w, h)
    return len(result)


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
