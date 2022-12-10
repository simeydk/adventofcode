from typing import List, Dict
from collections import Counter


def read_file(filename):
    with open(filename) as f:
        return [line.strip() for line in f.readlines()]


def parse_input(data: List[str]):
    start = data[0]
    insert_map = {key: value for key, value in map(lambda x: x.split(" -> "), data[2:])}
    return start, insert_map


Count_Dict = Dict[str, int]
Map_Dict = Dict[str, List[str]]


def step(counts: Count_Dict, map_dict: Map_Dict) -> Count_Dict:
    result: map_dict = {}
    for key, value in counts.items():
        new_keys = map_dict.get(key, [key])
        for new_key in new_keys:
            result[new_key] = result.get(new_key, 0) + value
    return result


def multi_step(counts: Count_Dict, map_dict: Map_Dict, n=1) -> Count_Dict:
    for _ in range(n):
        counts = step(counts, map_dict)
    return counts


def reduce_first_letter(d: Count_Dict) -> Count_Dict:
    result = {}
    for key, value in d.items():
        new_key = key[0]
        result[new_key] = result.get(new_key, 0) + value
    return result


def do_puzzle(data: List[str], n=10) -> int:
    start, insert_map = parse_input(data)
    pairs = [start[i : i + 2] for i in range(len(start))]
    counts = Counter(pairs)
    pair_map = {
        key: [key[0] + value, value + key[1]] for key, value in insert_map.items()
    }
    after = multi_step(counts, pair_map, n)
    first_letter = reduce_first_letter(after)
    return max(first_letter.values()) - min(first_letter.values())


def part1(data: List[str]) -> int:
    return do_puzzle(data, 10)


def part2(data: List[str]) -> int:
    return do_puzzle(data, 40)


test_input = [
    "NNCB",
    "",
    "CH -> B",
    "HH -> N",
    "CB -> H",
    "NH -> C",
    "HB -> C",
    "HC -> B",
    "HN -> C",
    "NN -> C",
    "BH -> H",
    "NC -> B",
    "NB -> B",
    "BN -> B",
    "BB -> N",
    "BC -> B",
    "CC -> N",
    "CN -> C",
]


DAY = 14
TEST_SOLUTION_1 = 1588
TEST_SOLUTION_2 = 2188189693529

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
