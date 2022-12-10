from collections import defaultdict
import heapq
import itertools
from typing import DefaultDict, Dict, Generator, List, NamedTuple, Optional, Set, Tuple
from enum import Enum
from itertools import combinations
from dataclasses import dataclass, field
from functools import cached_property, lru_cache
from datetime import datetime
import math

DAY = 11
TEST_SOLUTION_1 = None
TEST_SOLUTION_2 = None


def read_file(filename) -> str:
    with open(filename, encoding="UTF-8") as f:
        return f.read()


Pod = str
Position = Tuple[int, int]

Pair = Tuple[Pod, Position]
Move = Tuple[Position, Position]
Path = List[Move]

get_cost: Dict[Pod, int] = {
    "A": 1,
    "B": 10,
    "C": 100,
    "D": 1000,
}


@dataclass(frozen=True)
class Burrow:
    pairs: Tuple[Pair, ...]
    positions: List[Position] = field(hash=False, repr=False, compare=False)
    connections: Dict[Position, List[Position]] = field(
        hash=False, repr=False, compare=False
    )

    @cached_property
    def occupied_positions(self) -> Set[Position]:
        return {pos for _, pos in self.pairs}

    def possible_moves(self) -> Generator[Move, None, None]:
        for pair in self.pairs:
            pod, position = pair
            for connection in self.connections[position]:
                if (
                    connection not in self.occupied_positions
                    and pair not in self.pods_in_place
                ):
                    yield (position, connection)

    def move(self, move: Move) -> Tuple["Burrow", int]:
        curr_pos, new_pos = move
        pod = self.pod_at(curr_pos)
        if type(pod) == Pod:
            cost = get_cost[pod]
            pairs = tuple(
                (pair[0], new_pos) if pair[1] == curr_pos else pair
                for pair in self.pairs
            )
            return Burrow(pairs, self.positions, self.connections), cost
        else:
            raise Exception(f"Move Error: No pod at {curr_pos} to move to {new_pos}")

    def pod_at(self, position: Position) -> Optional[Pod]:
        for pod, pos in self.pairs:
            if pos == position:
                return pod

    @cached_property
    def pods_in_place(self) -> List[Pair]:
        pods = {pos: pod for pod, pos in self.pairs}
        pairs: List[Pair] = []
        for col, letter in [(3, "A"), (5, "B"), (7, "C"), (9, "D")]:
            if pods.get((3, col)) == letter:
                pairs.append((letter, (3, col)))
                if pods.get((2, col)) == letter:
                    pairs.append((letter, (2, col)))
        return pairs

    def solve(self) -> Optional[Tuple[int, "Burrow", Path]]:
        # Initialise trackers
        queue: List[Tuple[Tuple[int, ...], Burrow, Path]] = []
        completed: Set[Burrow] = set()
        best_cost: DefaultDict[Burrow, int] = defaultdict(lambda: 10**99999)
        ticker = itertools.count()
        tick = lambda: next(ticker)

        heapq.heappush(queue, ((8, 0, tick()), self, []))
        best_cost[self] = 0

        while queue:
            costs, burrow, path = heapq.heappop(queue)
            if burrow in completed:
                continue
            cost = costs[1]
            if burrow.solved:
                return cost, burrow, path
            for move in burrow.possible_moves():
                new_burrow, extra_cost = burrow.move(move)
                new_cost = cost + extra_cost
                if new_cost < best_cost[new_burrow]:
                    new_path = path + [move]
                    t = tick()
                    heapq.heappush(queue, ((8, new_cost, t), new_burrow, new_path))
                    best_cost[new_burrow] = new_cost
                    if t % 500 == 0:
                        print(str(new_burrow))
                        print(t, cost, len(path))
            completed.add(burrow)
        return None

    @cached_property
    def solved(self):
        return self == Burrow.solution

    def __str__(self):
        grid = [[" " for _ in range(13)] for _ in range(5)]
        for pos in self.positions:
            pod = self.pod_at(pos)
            grid[pos[0]][pos[1]] = pod if type(pod) == Pod else "."
        return "\n".join(["".join(row) for row in grid])

    # @lru_cache
    # def __repr__(self):
    #     pair_str = ", ".join(f"({pod.type.name}: ({pos.x}, {pos.y}))" for pod, pos in self.pairs)
    #     return f"B({pair_str})"

    def __eq__(self, other):
        return str(self) == str(other)

    @classmethod
    @lru_cache(maxsize=100)
    def from_string(cls, data: str) -> "Burrow":
        positions: List[Position] = []
        pairs: List[Tuple[Pod, Position]] = []
        connections: DefaultDict[Position, List[Position]] = defaultdict(list)
        for i, line in enumerate(data.splitlines()):
            for j, char in enumerate(line):
                if char in ".ABCD":
                    position = (i, j)
                    positions.append(position)
                    if char in "ABCD":
                        pod = char
                        pairs.append((pod, position))
        for pos_a, pos_b in combinations(positions, 2):
            diff = (pos_a[0] - pos_b[0], pos_a[1] - pos_b[1])
            if diff in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
                connections[pos_a].append(pos_b)
                connections[pos_b].append(pos_a)
        return Burrow(tuple(pairs), positions, connections)

    @classmethod
    @property
    def solution(cls) -> "Burrow":
        return Burrow.from_string(
            """#############
#...........#
###A#B#C#D###
  #A#B#C#D#
  #########"""
        )


solution_str = """#############
#...........#
###A#B#C#D###
  #A#B#C#D#
  #########"""

b = Burrow.from_string(solution_str)
s = Burrow.solution

print(s)

assert Burrow.solution.solved

assert b == s


def part1(data: str) -> int:
    start = Burrow.from_string(data)
    print(str(start))
    for move in start.possible_moves():
        burrow, _ = start.move(move)
        print(move)
        print(str(burrow))
        print(burrow.solved)
    solution = start.solve()
    print(solution)
    return solution[0]


def part2(data: str) -> int:
    pass


test_input = """#############
#...........#
###B#C#B#D###
  #A#D#C#A#
  #########"""

b = Burrow.from_string((test_input))
print(b.pods_in_place)

# test_input = """#############
# #...........#
# ###B#A#C#D###
#   #A#B#C#D#
#   #########"""

input_raw = """#############
#...........#
###D#D#C#B###
  #B#A#A#C#
  #########"""


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
