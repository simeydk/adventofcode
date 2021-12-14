from typing import List
from collections import Counter

def read_file(filename):
    with open(filename) as f:
        return [line.strip() for line in f.readlines()]

def parse_input(data: List[str]):
    start = data[0]
    split = map(lambda x: x.split(' -> '), data[2:])
    print(list(split))
    mapper = {key: value for key, value in map(lambda x: x.split(' -> '), data[2:])}
    return start, mapper

def step(s:str, map_fn) -> str:
    pairs = [s[i:i+2] for i in range(len(s))]
    mapped = map(map_fn, pairs)
    return ''.join(a[0] + b for a, b in (zip(pairs, mapped)))

def multi_step(s:str, map_fn, n:int) -> str:
    for _ in range(n):
        s = step(s, map_fn)
    return s

def part1(data: List[str]) -> int:
    start, mapper = parse_input(data)
    map_fn = lambda x, fallback = '': mapper.get(x, fallback)
    s =  multi_step(start, map_fn, 10)
    counts = Counter(s)
    return (max(counts.values())-min(counts.values()))


def part2(data: List[str]) -> int:
    pass

test_input = [
'NNCB',
'',
'CH -> B',
'HH -> N',
'CB -> H',
'NH -> C',
'HB -> C',
'HC -> B',
'HN -> C',
'NN -> C',
'BH -> H',
'NC -> B',
'NB -> B',
'BN -> B',
'BB -> N',
'BC -> B',
'CC -> N',
'CN -> C',
]


DAY = 14
TEST_SOLUTION_1 = 1588
TEST_SOLUTION_2 = None

input_raw = read_file(f'2021/data/day{DAY:02d}/input.txt')

if TEST_SOLUTION_1:
    assert part1(test_input) == TEST_SOLUTION_1
    print(f"Solution 1: {part1(input_raw)}")
    if TEST_SOLUTION_2:
        assert part2(test_input) == TEST_SOLUTION_2
        print(f"Solution 2: {part2(input_raw)}")
    else:
        print(f"Test 2: {part2(test_input)}")
else:
    print(f"Test 1: {part1(test_input)}")
    
