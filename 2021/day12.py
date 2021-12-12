from typing import List, Set, Dict
from dataclasses import dataclass, field


@dataclass(frozen=True)
class Node:
    value: str
    connections: Set['Node'] = field(
        default_factory=set, hash=False, repr=False, compare=False)


@dataclass(frozen=True)
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
    nodes = {x: Node(x, set()) for s in edges_str for x in s}
    edges = [{nodes[s] for s in edge_str} for edge_str in edges_str]
    for edge in edges:
        start, end = list(edge)
        start.connections.add(end)
        end.connections.add(start)

    return Graph(edges, nodes)


def paths_between(start: Node, end: Node, visited: Set[Node] = None) -> List[List[str]]:
    if start == end:
        yield [start]
        return
    visited = visited or set()
    if start.value.lower() == start.value:
        visited = visited.union({start})
    for node in start.connections.difference(visited):
        for path in paths_between(node, end, visited):
            yield([start] + path)


def part1(data: List[str]):
    graph = parse_input(data)
    start_node = graph.nodes["start"]
    end_node = graph.nodes["end"]
    return len(list(paths_between(start_node, end_node)))


def paths_between_with_small_cave(start: Node, end: Node, visited: Set[Node] = None, small_cave_available: bool = True) -> List[List[str]]:
    
    print(f"{start.value} - {end.value}")

    if start == end:
        yield [start]
        return
    
    visited = set(visited) if visited else set()

    print(f"visited: {visited}")

    if start.value.lower() == start.value:
        visited = visited.union({start})
    
    if start.value == "start":
        visited = visited.union({start})
    elif start.value.lower() == start.value:
        if small_cave_available:
            small_cave_available = False
        else:
            visited = visited.union({start})
    for node in start.connections.difference(visited):
        for path in paths_between_with_small_cave(node, end, visited, small_cave_available):
            yield [start] + path


def part2(data: List[str]) -> int:
    return len(part2_paths(data))


def part2_paths(data) -> List[List[Node]]:
    graph = parse_input(data)
    start_node = graph.nodes["start"]
    end_node = graph.nodes["end"]
    paths = paths_between_with_small_cave(start_node, end_node)
    return list(paths)


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
test_input_3 = [
    'start-A',
    'start-b',
    'A-b',
    'A-end',
    'b-end',
]

DAY = 12
TEST_SOLUTION_1 = 10
TEST_SOLUTION_2 = None

input_raw = read_file(f'2021/data/day{DAY:02d}/input.txt')

# if TEST_SOLUTION_1:
#     assert part1(test_input) == TEST_SOLUTION_1
#     print(f"Solution 1:\n{part1(input_raw)}")
#     if TEST_SOLUTION_2:
#         assert part2(test_input) == TEST_SOLUTION_2
#         print(f"Solution 2:\n{part2(input_raw)}")
#     else:
#         print(f"Test 2:\n{part2(test_input)}")
# else:
#     print(f"Test 1:\n{part1(test_input)}")


def path_to_string(path: List[Node]) -> str:
    return ",".join(node.value for node in path)


def print_paths(paths: List[List[Node]]):
    for i, path in enumerate(paths):
        print(f"{i+1:02d} - " + ",".join(node.value for node in path))


print_paths(part2_paths(test_input))

part_2_test_input_paths = [
    'start,A,b,A,b,A,c,A,end',
    'start,A,b,A,b,A,end',
    'start,A,b,A,b,end',
    'start,A,b,A,c,A,b,A,end',
    'start,A,b,A,c,A,b,end',
    'start,A,b,A,c,A,c,A,end',
    'start,A,b,A,c,A,end',
    'start,A,b,A,end',
    'start,A,b,d,b,A,c,A,end',
    'start,A,b,d,b,A,end',
    'start,A,b,d,b,end',
    'start,A,b,end',
    'start,A,c,A,b,A,b,A,end',
    'start,A,c,A,b,A,b,end',
    'start,A,c,A,b,A,c,A,end',
    'start,A,c,A,b,A,end',
    'start,A,c,A,b,d,b,A,end',
    'start,A,c,A,b,d,b,end',
    'start,A,c,A,b,end',
    'start,A,c,A,c,A,b,A,end',
    'start,A,c,A,c,A,b,end',
    'start,A,c,A,c,A,end',
    'start,A,c,A,end',
    'start,A,end',
    'start,b,A,b,A,c,A,end',
    'start,b,A,b,A,end',
    'start,b,A,b,end',
    'start,b,A,c,A,b,A,end',
    'start,b,A,c,A,b,end',
    'start,b,A,c,A,c,A,end',
    'start,b,A,c,A,end',
    'start,b,A,end',
    'start,b,d,b,A,c,A,end',
    'start,b,d,b,A,end',
    'start,b,d,b,end',
    'start,b,end',
]

p2paths = part2_paths(test_input)
p2paths_str = [path_to_string(path) for path in p2paths]
for path in part_2_test_input_paths:
    if path not in p2paths_str:
        print(path)
    # assert path_to_string(p2paths[int(path.split(",")[0])-1]) == path
