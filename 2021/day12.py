from typing import List, NamedTuple, Set, Dict, TypeVar
from dataclasses import dataclass, field


@dataclass(frozen = True)
class Node:
    value: str
    connections: Set['Node'] = field(default_factory = set, hash=False, repr=False, compare=False)

@dataclass(frozen = True)
class Graph:
    edges: List[Set[Node]]
    nodes: Dict[str, Node]        

Node.__repr__ = lambda self: self.value

# Graph = NamedTuple("Graph", [
#     ("edges", List[set]),
#     ("nodes", Set[Node]),
#     # ("connections", Dict[str, List[str]])
# ])

# Graph.find_node = lambda self, value: next(node for node in self.nodes if node.value == value)

def read_file(filename):
    with open(filename) as f:
        return [line.strip() for line in f.readlines()]


def parse_input(data: List[str]) -> List[set]:
    edges_str = [set(line.split("-")) for line in data]
    nodes = {x: Node(x,set()) for s in edges_str for x in s}
    edges = [{nodes[s] for s in edge_str} for edge_str in edges_str]
    for edge in edges:
        start, end = list(edge)
        start.connections.add(end)
        end.connections.add(start)

    return Graph(edges, nodes)



def paths_between(start: Node, end: Node, visited: Set[str] = set()) -> List[List[str]]:
    if start == end:
        yield [start]
    else:
        for node in start.connections.difference(visited):
            if start.value.upper() != start.value:
                visited = visited.union({start})
            for path in paths_between(node, end, visited):
                yield([start] + path)

# def find_paths(graph: Graph, start: str, end: str, visited: set(str) = {}) -> List[List[str]]:
#     paths = []
#     visited = set(visited)
#     if start == end:
#         return [[start]]
#     for node in graph.connections[start]:
#         for path in find_paths(graph, node, end):
#             paths.append([start] + path)
#     return paths

def part1(data: List[str]):
    graph = parse_input(data)
    start_node = graph.nodes["start"]
    end_node = graph.nodes["end"]
    return len(list(paths_between(start_node, end_node)))

def part2(data: List[str]) -> int:
    pass


test_input = [
    'start-A',
    'start-b',
    'A-c',
    'A-b',
    'b-d',
    'A-end',
    'b-end',
]

test_input_1 = ['start-end']
test_input_2 = ['start-A', 'A-end']


DAY = 12
TEST_SOLUTION_1 = 10
TEST_SOLUTION_2 = None

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
