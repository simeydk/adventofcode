from time import perf_counter
from typing import List
import numpy as np
from functools import lru_cache

DAY = 20
TEST_SOLUTION_1 = 35
TEST_SOLUTION_2 = 3351


def read_file(filename) -> str:
    with open(filename, encoding="UTF-8") as f:
        return f.read()


def hashperiod_to_binarray(s: str) -> List[int]:
    return [(c == "#") * 1 for c in s]


def parse_input(data: str):
    key_raw, pic_raw = data.split("\n\n")
    key = np.array(hashperiod_to_binarray(key_raw), dtype=np.int8)
    pic = np.array(
        [hashperiod_to_binarray(line) for line in pic_raw.splitlines()], dtype=np.int8
    )
    return key, pic


def shifts(mx: np.ndarray) -> np.ndarray:
    x = mx.shape[0] - 2
    y = mx.shape[1] - 2
    return np.stack(
        [mx[i : i + x, j : j + y] for i in range(3) for j in range(3)], axis=-1
    )


def pad(mx: np.ndarray, n=1, value=0) -> np.ndarray:
    return np.pad(mx, n, mode="constant", constant_values=value)


@lru_cache
def reverse_binary_array(n=9) -> np.ndarray:
    return 2 ** np.arange(n - 1, -1, -1)


def bin_array_to_int(a: np.array) -> int:
    return sum(a * reverse_binary_array(a.shape[0]))


def step(mx: np.ndarray, key_function, n=1) -> np.ndarray:
    f = np.vectorize(key_function)
    result = mx
    for run in range(n):
        constant_values = 1 if (key_function(1) == 1 and run % 2) else 0
        padded = pad(result, 2, constant_values)
        shifted = shifts(padded)
        indexes = np.apply_along_axis(bin_array_to_int, -1, shifted)
        result = f(indexes)
    return result


def to_string(mx: np.ndarray) -> str:
    return "\n".join(
        [
            "".join(
                map(str, map(lambda x: "#" if x == 1 else "." if x == 0 else "?", line))
            )
            for line in mx
        ]
    )


def part1(data: str, n=2) -> int:
    key, start_pic = parse_input(data)
    mapper = lambda x: key[x]
    pic = start_pic
    pic = step(start_pic, mapper, n)
    return np.sum(pic)


def part2(data: str) -> int:
    return part1(data, 50)


test_input = """..#.#..#####.#.#.#.###.##.....###.##.#..###.####..#####..#....#..#..##..###..######.###...####..#..#####..##..#.#####...##.#.#..#.##..#.#......#.###.######.###.####...#.##.##..#..#..#####.....#.#....###..#.##......#.....#..#..#..##..#...##.######.####.####.#.#...#.......#..#.#.#...####.##.#......#..#...##.#.##..#...##.#.##..###.#......#.#.......#.#.#.####.###.##...#.....####.#..#..#.##.#....##..#.####....##...##..#...#......#.#.......#.......##..####..#...#.#.#...##..#.#..###..#####........#..####......#..#

#..#.
#....
##..#
..#..
..###"""


input_raw = read_file(f"2021/data/day{DAY:02d}/input.txt")

if TEST_SOLUTION_1:
    assert part1(test_input) == TEST_SOLUTION_1
    print(f"Solution 1:\n{part1(input_raw)}")
    if TEST_SOLUTION_2:
        assert part2(test_input) == TEST_SOLUTION_2
        start = perf_counter()

        print(f"Solution 2:\n{part2(input_raw)}  ({perf_counter() - start:.2f}s)")
    else:
        print(f"Test 2:\n{part2(test_input)}")
else:
    print(f"Test 1:\n{part1(test_input)}")
