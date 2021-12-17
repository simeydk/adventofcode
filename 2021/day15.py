import numpy as np
import heapq
from dataclasses import dataclass, field
from typing import Tuple, DefaultDict, Dict, List, Set
from collections import defaultdict

def read_file(filename):
    with open(filename) as f:
        return [line.strip() for line in f.readlines()]

def parse_input(data: List[str]) -> np.ndarray:
    return np.array([[c for c in line] for line in  data], dtype = int)

INFINITY = float('inf')

Coords = Tuple[int, int]

Path = List['Node']


@dataclass
class Node:
    coords: Coords
    cost: int

    path_to: DefaultDict['Node', Path] = field(default_factory=lambda: defaultdict(lambda: (INFINITY, [])), repr=False)

    connections: List['Node'] = field(default_factory=list, repr=False)

    def __post_init__(self):
        self.path_to[self] = (0, [self])

    def __hash__(self) -> int:
        return hash(self.coords)

    def __str__(self) -> str:
        return f'{self.coords}: {self.cost}'

    def __repr__(self):
        return f'{self}'

    def __lt__(self, other):
        return self.coords < other.coords


a = Node((0,0), 5)
b = Node((0,1), 2)


def make_nodes(mx: np.ndarray) -> Dict[Coords, Node]:
    nodes: Dict[Coords, Node] = {}
    for i in range(mx.shape[0]):
        for j in range(mx.shape[1]):
            c = (i,j)
            nodes[c] = Node(c, mx[i,j])
    for i in range(mx.shape[0] - 1):
        for j in range(mx.shape[1]):
            a = nodes[(i,j)]
            b = nodes[(i+1,j)]
            a.connections.append(b)
            b.connections.append(a)
    for i in range(mx.shape[0]):
        for j in range(mx.shape[1]-1):
            a = nodes[(i,j)]
            b = nodes[(i,j+1)]
            a.connections.append(b)
            b.connections.append(a)
    return nodes

def dijkstra(a: Node, b: Node):
    queue: List[Node] = []
    completed: Set[Node] = set()
    heapq.heappush(queue, (a.path_to[a][0], a))
    while queue:
        cost, node = heapq.heappop(queue)
        if node in completed: continue
        if node is b: return node
        cost, path = node.path_to[a]
        for child in node.connections:
            if child in completed: continue
            new_cost = cost + child.cost
            if new_cost < child.path_to[a][0]:
                child.path_to[a] = (new_cost, path + [child])
                heapq.heappush(queue, (new_cost, child))
        completed.add(node)



def part1(inputs: List[str]):
    mx = parse_input(inputs)
    nodes = make_nodes(mx)
    nodes_list = list(nodes.values())
    start, end = nodes_list[0], nodes_list[-1]
    dj =  dijkstra(start, end)
    # for node in dj.path_to[start][1]:
    #     print(f"{node} -> {node.path_to[start][0]}")
    return dj.path_to[start][0]


def expand_map(mx: np.ndarray, n = 5):
    increment = lambda mx, n: np.mod(mx + n - 1, 9) + 1
    result = mx
    result = np.concatenate([increment(mx, i) for i in range(n)], axis=1)
    result = np.concatenate([increment(result, i) for i in range(n)], axis=0)

    return result

def part2(inputs: List[str]):
    mx = parse_input(inputs)
    mx = expand_map(mx)
    nodes = make_nodes(mx)
    nodes_list = list(nodes.values())
    start, end = nodes_list[0], nodes_list[-1]
    dj =  dijkstra(start, end)
    return dj.path_to[start][0]
    

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

print(part2(['11','88']))



DAY = 15
TEST_SOLUTION_1 = 40
TEST_SOLUTION_2 = 315

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
