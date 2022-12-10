from typing import List


def read_file_to_one_big_string(filename):
    with open(filename) as f:
        return f.read()


test_input = """
2-4,6-8
2-3,4-5
5-7,7-9
2-8,3-7
6-6,4-6
2-6,4-8
""".strip()


def contains(a, b):
    return (a[0] <= b[0]) and (a[1] >= b[1])


def contains_either(a, b):
    return contains(a, b) or contains(b, a)


def parse_row(row_str: str):
    a_str, b_str = row_str.split(",")
    a = tuple(map(int, a_str.split("-")))
    b = tuple(map(int, b_str.split("-")))
    return a, b


def part1(input_raw: str):
    rows = input_raw.splitlines()
    pairs = [parse_row(x) for x in rows]
    results = [contains_either(*pair) for pair in pairs]
    return sum(results)


def overlaps(a, b) -> bool:
    set_a = set(range(a[0], a[1] + 1))
    set_b = set(range(b[0], b[1] + 1))
    return bool(len(set_a.intersection(set_b)))


def part2(input_raw: str):
    rows = input_raw.splitlines()
    pairs = [parse_row(x) for x in rows]
    results = [overlaps(*pair) for pair in pairs]
    return sum(results)


input_raw = read_file_to_one_big_string("2022/data/day04/input.txt")

part1_test_solution = 2
part2_test_solution = 4

if part1_test_solution == None:
    print(f"Part 1 Test: {part1(test_input)}")
    quit()

assert part1(test_input) == part1_test_solution
print(f"Part 1: {part1(input_raw)}")

if part2_test_solution == None:
    print(f"Part 2 Test: {part2(test_input)}")
    quit()

assert part2(test_input) == part2_test_solution
print(f"Part 2: {part2(input_raw)}")
