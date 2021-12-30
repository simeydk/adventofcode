from typing import List, NamedTuple, Set
from enum import Enum
from itertools import combinations
from dataclasses import dataclass, field

DAY = 11
TEST_SOLUTION_1 = None
TEST_SOLUTION_2 = None

def read_file(filename) -> str:
    with open(filename, encoding="UTF-8") as f:
        return f.read()

class PodType(NamedTuple):
    type: str
    value: int

PodTypes = {
    'A': PodType('A', 1),
    'B': PodType('B', 10),
    'C': PodType('C', 100),
    'D': PodType('D', 1000),
}


@dataclass(frozen = True)
class Position:
    x: int
    y: int
    connections: List['Position'] = field(default_factory=list, hash=False, repr=False)
    contents: List['Pod'] = field(default_factory=list)

    def __hash__(self):
        return hash(self.__repr__())
    


class Pod(NamedTuple):
    type: PodType
    position: Position

    @property
    def possible_moves(self) -> List['Position']:
        return [p for p in self.position.connections if len(p.contents) == 0]


class Burrow(NamedTuple):
    positions: List[Position]
    pods: List[Pod]

    @property
    def possible_moves(self):
        moves = []
        for pod in self.pods:
            moves.extend([pod, move for move in pod.possible_moves])
        return moves

    def move(pod: Pod, to: Position):

    def __str__(self):
        grid = [[' ' for _ in range(13)] for _ in range(5)]
        for pos in self.positions:
            grid[pos.x][pos.y] =  pos.contents[0].type.type if pos.contents else "."

        return "\n".join(["".join(row) for row in grid])

    def __hash__(self):
        return hash(self.__repr__())



def parse_input(data: str) -> Burrow:
    positions = []
    pods = []
    for i, line in enumerate(data.splitlines()):
        for j, char in enumerate(line):
            if char in ".ABCD":
                position = Position(i, j)
                positions.append(position)
                if char in "ABCD":
                    pod = Pod(PodTypes[char], position)
                    position.contents.append(pod)
                    pods.append(pod)
    for pos_a, pos_b in combinations(positions, 2):
        diff = (pos_a.x - pos_b.x, pos_a.y - pos_b.y)
        if diff in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
            pos_a.connections.append(pos_b)
            pos_b.connections.append(pos_a)
    return Burrow(positions, pods)


def part1(data: str) -> int:
    start = parse_input(data)
    print(str(start))
    print(hash(start))
    pass

def part2(data: str) -> int:
    pass

test_input = """#############
#...........#
###B#C#B#D###
  #A#D#C#A#
  #########"""

input_raw = """#############
#...........#
###D#D#C#B###
  #B#A#A#C#
  #########"""


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
    
