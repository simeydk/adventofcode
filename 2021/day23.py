import heapq
import itertools
from typing import Generator, List, NamedTuple, Optional, Set, Tuple
from enum import Enum
from itertools import combinations
from dataclasses import dataclass, field
from functools import cached_property, lru_cache
from datetime import datetime

DAY = 11
TEST_SOLUTION_1 = None
TEST_SOLUTION_2 = None

def read_file(filename) -> str:
    with open(filename, encoding="UTF-8") as f:
        return f.read()


class PodType(Enum):
    A = 1
    B = 10
    C = 100
    D = 1000


@dataclass(frozen = True)
class Position:
    x: int
    y: int
    connections: List['Position'] = field(default_factory=list, hash=False, repr=False)

class Pod(NamedTuple):
    type: PodType

Pair = Tuple[Pod, Position]
@dataclass(frozen=True)
class Burrow:
    pairs:  Tuple[Pair, ...]
    positions: List[Position] = field(default_factory=list, hash=False, repr=False)
    _created: datetime = field(default_factory=datetime.now, hash=False, repr=False)


    @cached_property
    def occupied_positions(self) -> Set[Position]:
        return {pos for _, pos in self.pairs}

    def possible_moves(self) -> Generator[Pair, None, None]:
        for pod, position in self.pairs:
            for connection in position.connections:
                if connection not in self.occupied_positions:
                    yield (pod, connection)

    def move(self, pod: Pod, new_position: Position) -> 'Burrow':
        pairs = tuple((the_pod, new_position if the_pod is pod else pos) for the_pod, pos in self.pairs)
        return Burrow(pairs, self.positions)

    def pod_at(self, position: Position) -> Optional[Pod]:
        for pod, pos in self.pairs:
            if pos == position:
                return pod

    def solve(self) -> Optional[Tuple[int, 'Burrow', List[Pair]]]:
        queue: List[Tuple[int, int, Burrow, List[Pair]]] = []
        completed: Set[Burrow] = set()
        ticker = itertools.count()
        tick = lambda: next(ticker)
        heapq.heappush(queue, (0, tick(), self, []))
        while queue:
            cost, _, burrow, path = heapq.heappop(queue)
            if burrow in completed: continue
            if burrow == Burrow.solution: return cost, burrow, path
            for move in burrow.possible_moves():
                new_burrow = burrow.move(*move)
                new_cost = move[0].type.value + cost
                new_path = path + [move]
                heapq.heappush(queue, (new_cost, tick(), new_burrow, new_path))
            completed.add(burrow)
        return None 


    def __str__(self):
        grid = [[' ' for _ in range(13)] for _ in range(5)]
        for pos in self.positions:
            pod = self.pod_at(pos)
            grid[pos.x][pos.y] =  pod.type.name if type(pod) == Pod else "."
        return "\n".join(["".join(row) for row in grid])    

    def __lt__(self, other):
        return self._created < other._created

    @classmethod
    def from_string(cls, data: str) -> 'Burrow':
        positions = []
        pairs: List[Tuple[Pod, Position]] = []
        for i, line in enumerate(data.splitlines()):
            for j, char in enumerate(line):
                if char in ".ABCD":
                    position = Position(i, j)
                    positions.append(position)
                    if char in "ABCD":
                        pod = Pod(PodType[char])
                        pairs.append((pod, position))
        for pos_a, pos_b in combinations(positions, 2):
            diff = (pos_a.x - pos_b.x, pos_a.y - pos_b.y)
            if diff in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
                pos_a.connections.append(pos_b)
                pos_b.connections.append(pos_a)
        return Burrow(tuple(pairs), positions)


    @classmethod
    @property
    @lru_cache
    def solution(cls) -> 'Burrow':
        return Burrow.from_string("""#############
#...........#
###A#B#C#D###
  #A#B#C#D#
  #########""")


solution_str = """#############
#...........#
###A#B#C#D###
  #A#B#C#D#
  #########"""

assert Burrow.from_string(solution_str) == Burrow.solution

def part1(data: str) -> int:
    start = Burrow.from_string(data)
    print(str(start))
    print(start.occupied_positions)
    print(start.solve())

def part2(data: str) -> int:
    pass

test_input = """#############
#...........#
###B#C#B#D###
  #A#D#C#A#
  #########"""

test_input = """#############
#........D..#
###A#B#C#.###
  #A#B#C#D#
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
    
