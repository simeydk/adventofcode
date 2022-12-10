from typing import List, Set, Dict
from dataclasses import dataclass, field
from collections import Counter


@dataclass(frozen=True)
class Node:
    value: str
    connections: Set["Node"] = field(
        default_factory=set, hash=False, repr=False, compare=False
    )

    def __repr__(self) -> str:
        return f"{self.value}"


@dataclass(frozen=True)
class Graph:
    edges: List[Set[Node]]
    nodes: Dict[str, Node]


def read_file(filename):
    with open(filename) as f:
        return [line.strip() for line in f.readlines()]


def parse_input(data: List[str]) -> List[set]:
    edges_str = [set(line.split("-")) for line in data]
    nodes = {x: Node(x) for s in edges_str for x in s}
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
            yield ([start] + path)


def part1(data: List[str]):
    graph = parse_input(data)
    start_node = graph.nodes["start"]
    end_node = graph.nodes["end"]
    return len(list(paths_between(start_node, end_node)))


def paths_between_with_small_cave(
    start: Node, end: Node, prefix: List[Node] = []
) -> List[List[str]]:
    prefix = prefix + [start]
    if start == end:
        yield prefix
        return

    max_prev_lower = get_max_prev_lower(prefix)

    for node in start.connections:
        if node.value == "start":
            continue
        if node.value.islower() and node in prefix and max_prev_lower >= 2:
            continue

        yield from paths_between_with_small_cave(node, end, prefix)


def get_max_prev_lower(prefix):
    prev_lowers = Counter(node for node in prefix if node.value.islower())
    max_prev_lower = max(prev_lowers.values())
    return max_prev_lower


def part2(data: List[str]) -> int:
    return len(part2_paths(data))


def part2_paths(data: List[str]) -> List[List[Node]]:
    graph = parse_input(data)
    start_node = graph.nodes["start"]
    end_node = graph.nodes["end"]
    paths = paths_between_with_small_cave(start_node, end_node)
    return list(paths)


test_input = [
    "start-A",
    "start-b",
    "A-c",
    "A-b",
    "b-d",
    "A-end",
    "b-end",
]

DAY = 12
TEST_SOLUTION_1 = 10
TEST_SOLUTION_2 = 36

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
