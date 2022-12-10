from typing import List
import numpy as np


def read_file(filename):
    with open(filename) as f:
        return [line.strip() for line in f.readlines()]


def parse_input(data: List[str]) -> List[str]:
    s = "\n".join(data)
    points_s, folds_s = s.split("\n\n")
    points = [tuple(map(int, p.split(","))) for p in points_s.split("\n")]
    folds = [(f[11], int(f[13:])) for f in folds_s.split("\n")]
    return points, folds


def fold_int(x, at):
    return at - (x - at) if x >= at else x


assert fold_int(14, 7) == 0


def fold_coord(coord, fold):
    axis, at = fold
    x, y = coord
    if axis == "x":
        return (fold_int(x, at), y)
    elif axis == "y":
        return (x, fold_int(y, at))
    else:
        raise Exception("Unknown axis: {}".format(axis))


def fold_coords(coords, folds):
    for fold in folds:
        coords = [fold_coord(c, fold) for c in coords]
    return coords


def part1(data: List[str]) -> int:
    points, folds = parse_input(data)

    folded = fold_coords(points, folds[:1])
    return len(set(folded))


def part2(data: List[str]) -> int:
    points, folds = parse_input(data)
    folded = fold_coords(points, folds)
    max_x = max(x for x, y in folded)
    max_y = max(y for x, y in folded)
    grid = np.zeros((max_x + 1, max_y + 1), dtype=int)
    for x, y in folded:
        grid[x][y] = 1
    grid = grid.T
    pretty = "\n".join("".join(["#" if g else "." for g in row]) for row in grid)
    return pretty


test_input = [
    "6,10",
    "0,14",
    "9,10",
    "0,3",
    "10,4",
    "4,11",
    "6,0",
    "6,12",
    "4,1",
    "0,13",
    "10,12",
    "3,4",
    "3,0",
    "8,4",
    "1,10",
    "2,14",
    "8,10",
    "9,0",
    "",
    "fold along y=7",
    "fold along x=5",
]


DAY = 13
TEST_SOLUTION_1 = 17
TEST_SOLUTION_2 = """#####
#...#
#...#
#...#
#####"""

input_raw = read_file(f"2021/data/day{DAY:02d}/input.txt")

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
