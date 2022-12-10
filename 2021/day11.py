from typing import List, NamedTuple
import numpy as np


def read_file(filename):
    with open(filename) as f:
        return [line.strip() for line in f.readlines()]


Coords = NamedTuple("Coords", [("x", int), ("y", int)])
Coords.__repr__ = lambda self: f"({self.x}, {self.y})"


def neighbour_coords(coords: Coords, mx: np.ndarray) -> List[Coords]:
    x, y = coords
    # exclude the current coord
    results: List[Coords] = [
        Coords(x + i, y + j)
        for i in [-1, 0, 1]
        for j in [-1, 0, 1]
        if not (i == 0 and j == 0)
    ]
    # exclude out of bounds coords
    results = [
        c for c in results if (0 <= c.x < mx.shape[0] and 0 <= c.y < mx.shape[1])
    ]
    return results


# step
# increment all by 1
# find all at 10
# find all neighbours
# incremen


def step(mx: np.ndarray) -> np.ndarray:

    FLASH_SCORE = 10

    flashed = set()
    flash_queue = []

    # add to the queue if not added already
    def enqueue(coords: Coords):
        if coords not in flashed:
            flash_queue.append(coords)

    # Increment all neighours by 1 and enqueue those at 9
    def flash(coords: Coords):
        flashed.add(coords)

        neighbours = neighbour_coords(coords, mx)
        for coord in neighbours:
            mx[coord.x][coord.y] += 1
            if mx[coord.x][coord.y] == FLASH_SCORE:
                enqueue(coord)

    mx = mx + 1

    # find the first list of coords to flash
    for x in range(mx.shape[0]):
        for y in range(mx.shape[1]):
            if mx[x][y] == FLASH_SCORE:
                enqueue(Coords(x, y))

    while len(flash_queue) > 0:
        flash(flash_queue.pop())

    flashed = mx >= FLASH_SCORE
    mx[flashed] = 0
    num_flashed = np.sum(flashed)

    return mx, num_flashed


def multistep(mx: np.ndarray, num_steps: int) -> int:
    num_flashes = 0
    for _ in range(num_steps):
        mx, flashes = step(mx)
        num_flashes += flashes
    return mx, num_flashes


def part1(data: List[str]) -> int:
    mx = np.array([[c for c in x] for x in data], dtype=np.int8)
    mx, num_flashes = multistep(mx, 100)
    return num_flashes


def part2(data: List[str]) -> int:
    mx = np.array([[c for c in x] for x in data], dtype=np.int8)
    num_flashes = 0
    n = 0
    while num_flashes < 100:
        n += 1
        mx, num_flashes = multistep(mx, 1)
    return n


test_input = [
    "5483143223",
    "2745854711",
    "5264556173",
    "6141336146",
    "6357385478",
    "4167524645",
    "2176841721",
    "6882881134",
    "4846848554",
    "5283751526",
]


DAY = 11
TEST_SOLUTION_1 = 1656
TEST_SOLUTION_2 = 195

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
