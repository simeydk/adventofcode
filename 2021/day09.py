import numpy as np
from typing import List, NamedTuple
from math import prod



def read_file(filename):
    with open(filename) as f:
        return [line.strip() for line in f.readlines()]

Coords = NamedTuple('Coords', [('x', int), ('y', int)])


def get_local_minimum(mx: np.ndarray):
    lower_than_south = (np.diff(mx, axis=0, append = 10) > 0) * 1
    lower_than_north = (- np.diff(mx, axis=0, prepend = 10) > 0) * 1
    lower_than_east = (np.diff(mx, axis=1, append = 10) > 0) * 1
    lower_than_west = (- np.diff(mx, axis=1, prepend = 10) > 0) * 1
    local_minimum = lower_than_south * lower_than_north * lower_than_east * lower_than_west
    return local_minimum

def part1(str_list: List[str]):
    mx =  np.array([[c for c in x] for x in str_list], dtype=np.int8)
    local_minimum = get_local_minimum(mx)
    local_minimum_values = local_minimum * (mx + 1)
    return sum(sum(local_minimum_values))


def part2(str_list: List[str]):
    mx =  np.array([[c for c in x] for x in str_list], dtype=np.int8)
    local_minimum = get_local_minimum(mx)
    basin_starts = non_zero_to_coords(local_minimum)
    is_basin = mx != 9
    basins = [trace(is_basin, start) for start in basin_starts]
    basin_sizes = [sum(sum(b)) for b in basins]
    basin_sizes.sort(reverse=True)
    return prod(basin_sizes[:3])

def non_zero_to_coords(mx: np.ndarray):
    return [(x,y) for x in range(mx.shape[0]) for y in range(mx.shape[1]) if mx[x][y]]

def trace(mx: np.ndarray, start: Coords):

    result = np.zeros(mx.shape, dtype=np.int8)
    queue = [start]
    checked = set()

    def enqueue(c: Coords):
        if c in checked: return
        if (0 <= c[0] < mx.shape[0]) and (0 <= c[1] < mx.shape[1]):
            queue.append(c)
            checked.add(c)
    
    while len(queue) > 0:
        current = queue.pop(0)
        x, y = current
        if mx[x][y]:
            result[x][y] = mx[x][y]
            for n in [(x-1, y), (x+1, y), (x, y-1), (x, y+1)]:
                enqueue(n)
    return result

test_input = [
    '2199943210',
    '3987894921',
    '9856789892',
    '8767896789',
    '9899965678',
]

input_raw = read_file('2021/data/day09/input.txt')



assert part1(test_input) == 15

print(part1(input_raw))

assert part2(test_input) == 1134

print(part2(input_raw))