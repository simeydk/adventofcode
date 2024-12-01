import re
from collections import Counter

def read_file_to_one_big_string(filename):
    with open(filename) as f:
        return f.read()

year=2024
day_number = 1
part1_test_solution = 11
part2_test_solution = 31
test_input = """
""".strip(
    "\n"
)


test_input = read_file_to_one_big_string(f"{year}/data/day{day_number:02d}/test_input.txt")
input_raw = read_file_to_one_big_string(f"{year}/data/day{day_number:02d}/input.txt")


def part1(input_raw: str):
    lines = input_raw.splitlines()
    pairs = [[int(x) for x in re.split('\s+', line)] for line in lines]
    print(pairs)
    a, b = [list(x) for x in zip(*pairs)]
    a.sort()
    b.sort()
    print(a, b)
    c = [abs(x - y) for x, y in zip(a,b)]
    print(c)
    return sum(c)


def part2(input_raw: str):
    lines = input_raw.splitlines()
    pairs = [[int(x) for x in re.split('\s+', line)] for line in lines]
    print(pairs)
    a, b = [list(x) for x in zip(*pairs)]
    counts = Counter(b)
    print(counts)
    c = [x * counts[x] for x in a]
    print(c)
    return sum(c)


if part1_test_solution is None:
    print(f"Part 1 Test: {part1(test_input)}")
    quit()

assert part1(test_input) == part1_test_solution
print(f"Part 1: {part1(input_raw)}")

if part2_test_solution is None:
    print(f"Part 2 Test: {part2(test_input)}")
    quit()

assert part2(test_input) == part2_test_solution
print(f"Part 2: {part2(input_raw)}")
