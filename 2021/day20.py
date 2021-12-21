from typing import DefaultDict, Dict, List
import numpy as np
from collections import defaultdict

d = defaultdict(lambda: 0)

d[1] = 1
d[2] = 2
print(d[7])
print(d.items())

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
    pic_list = [hashperiod_to_binarray(line) for line in pic_raw.splitlines()]
    pic_dict = defaultdict(lambda: 0)
    for i in range(len(pic_list)):
        for j in range(len(pic_list[0])):
            pic_dict[(i,j)] = pic_list[i][j]
    return key, pic_dict

def append_zeros(mx: np.ndarray, n: int = 1) -> np.ndarray:
    mx = np.concatenate((np.zeros([mx.shape[0], n], dtype=np.int8), mx, np.zeros([mx.shape[0], n], dtype=np.int8)), axis = 1)
    mx = np.concatenate((np.zeros([n, mx.shape[1]], dtype=np.int8), mx, np.zeros([n, mx.shape[1]], dtype=np.int8)), axis = 0)
    return mx

def pic_dict():
    return defaultdict(lambda: 0)

def threegrid(d: Dict, i, j):
    return [
        d[(i-1,j-1)],
        d[(i-1,j)],
        d[(i-1,j+1)],
        d[(i,j-1)],
        d[(i,j)],
        d[(i,j+1)],
        d[(i+1,j-1)],
        d[(i+1,j)],
        d[(i+1,j+1)]
        ]

def step(start_pic, key):
    pic = pic_dict()
    coords = list(start_pic.keys())
    for coord in coords:
        print(coord)
        x, y = coord
        index_bin = ''.join(map(str, threegrid(start_pic, x, y)))
        index = int(index_bin, 2)
        val = key[index]
        pic[(x,y)] = val
        print(index_bin, index, val)
    return pic

def part1(data: str) -> int:
    key, start_pic = parse_input(data)
    pic = start_pic
    pic = step(pic, key)

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
    
