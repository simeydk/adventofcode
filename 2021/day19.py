# Credit to Josh B Duncan, whose solution I used to debug my own when it wasn't working
# https://gist.github.com/joshbduncan/d69cd900614939c9995e885e9cb1abcc

from collections import Counter
from functools import lru_cache
from typing import List, NamedTuple, Set, Tuple
from itertools import combinations, product

DAY = 19
TEST_SOLUTION_1 = 79
TEST_SOLUTION_2 = 3621

def read_file(filename) -> str:
    with open(filename, encoding="UTF-8") as f:
        return f.read()


def parse_scanner(string: str) -> 'Scanner':
    header_raw, *lines = string.splitlines()
    l = [map(int, line.split(',')) for line in lines]
    return {Coords(*line) for line in l}

def parse_input(data: str) -> List[List['Coords']]:
    scanners_raw = data.split('\n\n')
    return [parse_scanner(s) for s in scanners_raw]

class Coords(NamedTuple):
    x: int = 0
    y: int = 0
    z: int = 0

    def __add__(self, other):
        return Coords(self.x + other.x, self.y + other.y, self.z + other.z)

    def __neg__(self):
        return Coords(-self.x, -self.y, -self.z)

    def __sub__(self, other):
        return Coords(self.x - other.x, self.y - other.y, self.z - other.z)

    def __repr__(self):
        return f"C({self.x}, {self.y}, {self.z})"

    def rotate(self, n) -> 'Coords':
        x, y, z = self
        if n == 0: return Coords(x, y, z)
        if n == 1: return Coords(x, -z, y)
        if n == 2: return Coords(x, -y, -z)
        if n == 3: return Coords(x, z, -y)
        if n == 4: return Coords(-x, -y, z)
        if n == 5: return Coords(-x, -z, -y)
        if n == 6: return Coords(-x, y, -z)
        if n == 7: return Coords(-x, z, y)
        if n == 8: return Coords(y, x, -z)
        if n == 9: return Coords(y, -x, z)
        if n == 10: return Coords(y, z, x)
        if n == 11: return Coords(y, -z, -x)
        if n == 12: return Coords(-y, x, z)
        if n == 13: return Coords(-y, -x, -z)
        if n == 14: return Coords(-y, -z, x)
        if n == 15: return Coords(-y, z, -x)
        if n == 16: return Coords(z, x, y)
        if n == 17: return Coords(z, -x, -y)
        if n == 18: return Coords(z, -y, x)
        if n == 19: return Coords(z, y, -x)
        if n == 20: return Coords(-z, x, -y)
        if n == 21: return Coords(-z, -x, y)
        if n == 22: return Coords(-z, y, x)
        if n == 23: return Coords(-z, -y, -x)

    def manhattan(self, other) -> int:
        return abs(self.x - other.x) + abs(self.y - other.y) + abs(self.z - other.z)

Scanner = Set[Coords]

def find_transform(scanner: Scanner, ocean: Scanner) -> Tuple[Coords, int]:
    for rotation in range(24):
        offsets = [point.rotate(rotation) - beacon for beacon, point  in product(ocean, scanner)]
        counts = Counter(offsets)
        best_offset, best_count = counts.most_common(1)[0]
        if best_count >= 12:
            return -best_offset, rotation
    return None, None

def solve_scanners(scanners: List[Scanner]) -> Tuple[Scanner, List[Scanner]]:
    queue: List[Scanner] = [*scanners]
    scanner_positions: List[Coords] = []
    scanner = queue.pop(0)
    scanner_positions.append(Coords(0,0,0))
    ocean: Scanner = {*scanner}
    while queue:
        scanner = queue.pop(0)
        offset, rotation = find_transform(scanner, ocean)
        if offset:
            transformed = set(point.rotate(rotation) + offset for point in scanner)
            assert len(transformed.union(ocean)) >= 12
            ocean.update(transformed)
            scanner_positions.append(offset)
            # print(f"Found scanner at {offset} with rotation {rotation}")
        else:
            queue.append(scanner)
    return ocean, scanner_positions


@lru_cache(maxsize=None)
def solve_string(data: str) -> Tuple[Scanner, List[Coords]]:
    scanners = parse_input(data)
    return solve_scanners(scanners)

def part1(data: str) -> int:
    ocean, scanners = solve_string(data) 
    return len(ocean)

def part2(data: str) -> int:
    ocean, scanners = solve_string(data)
    return max(a.manhattan(b) for a, b in combinations(scanners, 2))



test_input = read_file(f'2021/data/day{DAY:02d}/test_input.txt')
input_raw = read_file(f'2021/data/day{DAY:02d}/input.txt')

if __name__ == "__main__":

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