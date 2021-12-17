from typing import DefaultDict, List, Tuple, Dict
from collections import defaultdict
import numpy as np
from dataclasses import dataclass, field
from functools import cached_property
import heapq

import day15memo as memo

Coords = Tuple[int, int]

INFINITY = float('inf')


@dataclass
class Node:
    coords: Coords
    risk: int = field(hash=False)
    parents: List['Node'] = field(default_factory = list, repr=False, hash=False)
    children: List['Node'] = field(default_factory = list, repr=False, hash=False)
    cost: DefaultDict['Node', Tuple[List['Node'], int]] = field(default_factory = lambda: defaultdict(lambda: ([], INFINITY)), repr=False, hash=False)

    def __post_init__(self):
        self.cost[self] = ([], 0)

    @cached_property
    def total_risk(self):
        if not self.parents: return 0
        return self.risk + min(parent.total_risk for parent in self.parents)

    def __repr__(self) -> str:
        return f'{self.coords}: {self.risk}'

    def __hash__(self) -> int:
        return hash(self.coords)


def distance_from(start: Node, end: Node) -> int:
    done: Set[Node] = set()
    queue: List[Node] = []
    
    push = lambda node: heapq.heappush(queue, (node.cost[start], node))
    push(start)
    
    while queue:
        dist, parent_node = heapq.heappop(queue)
        for node in parent_node.children:
            cost = parent_node.cost[start]

        done.add(parent_node)        
            

n = Node((0,0), 0)
m = Node((0,1), 1)

print(n.cost is m.cost)
print(f'n.cost[m] = {n.cost[m]}')
print(f'm.cost[m] = {m.cost[m]}')
n.cost[m] = ([], 1)
print(f'n.cost[m] = {n.cost[m]}')
print(f'm.cost[m] = {m.cost[m]}')




def read_file(filename):
    with open(filename) as f:
        return [line.strip() for line in f.readlines()]

def parse_input(data: List[str]) -> np.ndarray:
    return np.array([[c for c in line] for line in  data], dtype = int)

def risk_node(mx: np.array):
    nodes: Dict[Coords, Node] = {}
    for i in range(mx.shape[0]):
        for j in range(mx.shape[1]):
            coords = (i, j)
            node = Node(coords, mx[i][j])
            if (i > 0): node.parents.append(nodes[(i-1, j)])
            if (j > 0): node.parents.append(nodes[(i, j-1)])
            nodes[coords] = node
    for i in range(1, mx.shape[0] - 1):
        for j in range(1, mx.shape[1] - 1):
            node = nodes[(i, j)]
            node.children.append(nodes[(i+1, j)])
            node.children.append(nodes[(i, j+1)])

    first = nodes[(0,0)]
    last = nodes[(mx.shape[0]-1, mx.shape[1]-1)]

    return nodes

def lowest_risk(mx: np.array) -> np.array:
    risk = np.zeros_like(mx, dtype = int)
    for i in range(1, mx.shape[0]):
        risk[i][0] = risk[i-1][0] + mx[i][0]
    for j in range(1, mx.shape[1]):
        risk[0][j] = risk[0][j-1] + mx[0][j]
    for i in range(1, mx.shape[0]):
        for j in range(1, mx.shape[1]):
            left = risk[i][j-1]
            above = risk[i-1][j]
            current = mx[i][j]
            risk[i][j] = current + min(left, above)
    return risk

def part1(data: List[str]) -> int:
    mx = parse_input(data)
    risk = risk_node(mx)[(9,9)]
    return risk.total_risk


def part2(data: List[str]) -> int:
    pass

tes_input_1 = [
    '123',
    '513',
    '192',
]

g = risk_node(parse_input(tes_input_1))
print(g)

test_input = [
    '1163751742',
    '1381373672',
    '2136511328',
    '3694931569',
    '7463417111',
    '1319128137',
    '1359912421',
    '3125421639',
    '1293138521',
    '2311944581',
]


DAY = 15
TEST_SOLUTION_1 = 40
TEST_SOLUTION_2 = None

input_raw = read_file(f'2021/data/day{DAY:02d}/input.txt')

print("memo test1:", memo.part1(parse_input(test_input)))
print("memo part1:", memo.part1(parse_input(input_raw)))

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
