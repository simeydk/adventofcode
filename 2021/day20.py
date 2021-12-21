from typing import DefaultDict, Dict, List
import numpy as np
from collections import defaultdict

DAY = 20
TEST_SOLUTION_1 = None
TEST_SOLUTION_2 = None

def read_file(filename) -> str:
    with open(filename, encoding="UTF-8") as f:
        return f.read()

def hashperiod_to_binarray(s: str) -> List[int]:
    return [(c == '#') * 1 for c in s]

def parse_input(data: str):
    key_raw, pic_raw = data.split('\n\n')
    key = hashperiod_to_binarray(key_raw)
    pic = np.array([hashperiod_to_binarray(line) for line in pic_raw.splitlines()])
    return key, pic

def append_zeros(mx: np.ndarray, n: int = 1) -> np.ndarray:
    mx = np.concatenate((np.zeros([mx.shape[0], n], dtype=np.int8), mx, np.zeros([mx.shape[0], n], dtype=np.int8)), axis = 1)
    mx = np.concatenate((np.zeros([n, mx.shape[1]], dtype=np.int8), mx, np.zeros([n, mx.shape[1]], dtype=np.int8)), axis = 0)
    return mx

def np_text_concat(ndarrays):
    strings = [ndarray.astype(str) for ndarray in ndarrays]
    result = strings[0]
    for string in strings[1:]:
        result =  np.core.defchararray.add(result, string)
    return result

def pad_and_grid_concat(m, fill = 0):
    padded = np.pad(m, 1, mode='constant', constant_values=fill)



def step(mx, map_fn, n = 1):
    for _ in range(n):
        padded = np.pad(mx, 2)
        w, h = mx.shape
        shifts = [padded[i:i+w+1, j:j+h+1] for i in range(1,4) for j in range(1,4)]
        concat = np_text_concat(shifts)
        mx = map_fn(concat)
    return mx

def to_string(mx: np.ndarray) -> str:
    return '\n'.join([''.join(map(str, map(lambda x: "#" if x else ".", line))) for line in mx])

def part1(data: str) -> int:
    key, start_pic = parse_input(data)
    mapper = np.vectorize(lambda x: key[int(x, 2)])
    pic = start_pic
    pic = step(pic, mapper)
    print(to_string(start_pic))
    print('')
    print(to_string(pic))
    # print(key)
    # print(pic)
    # print(append_zeros(pic, 2))

def part2(data: str) -> int:
    pass

test_input = """..#.#..#####.#.#.#.###.##.....###.##.#..###.####..#####..#....#..#..##..###..######.###...####..#..#####..##..#.#####...##.#.#..#.##..#.#......#.###.######.###.####...#.##.##..#..#..#####.....#.#....###..#.##......#.....#..#..#..##..#...##.######.####.####.#.#...#.......#..#.#.#...####.##.#......#..#...##.#.##..#...##.#.##..###.#......#.#.......#.#.#.####.###.##...#.....####.#..#..#.##.#....##..#.####....##...##..#...#......#.#.......#.......##..####..#...#.#.#...##..#.#..###..#####........#..####......#..#

#..#.
#....
##..#
..#..
..###"""


input_raw = read_file(f'2021/data/day{DAY:02d}/input.txt')

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
    
