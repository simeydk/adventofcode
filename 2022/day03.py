from typing import List


def read_file_to_one_big_string(filename):
    with open(filename) as f:
        return f.read()


test_input = """
vJrwpWtwJgWrhcsFMMfFFhFp
jqHRNqRjqzjGDLGLrsFMfFZSrLrFZsSL
PmmdzqPrVvPwwTWBwg
wMqvLMZHhHMvwLHjbvcjnnSBnvTQFn
ttgJtRGJQctTZtZT
CrZsJsPPZsGzwwsLwLmpwMDw
""".strip()


def score_char(s: str) -> int:
    if s == s.lower():
        return ord(s) - ord("a") + 1
    else:
        return ord(s) - ord("A") + 1 + 26


def parse_bag(bag_str: str):
    length = len(bag_str)
    compartment_size = length // 2

    a = bag_str[:compartment_size]
    b = bag_str[compartment_size:]
    overlaps = set(a).intersection(set(b))
    if len(overlaps) > 1:
        raise ValueError("more than one overlap!")
    return score_char(list(overlaps)[0])


def chunk_list(the_list, chunk_size=3):
    for n in range(0, len(the_list), chunk_size):
        yield the_list[n : n + chunk_size]


def part1(input_raw: str):
    bags = input_raw.splitlines()

    return sum(map(parse_bag, bags))


def parse_group(group: List[str]):
    sets = [set(x) for x in group]
    overlaps = sets[0].intersection(sets[1]).intersection(sets[2])
    return score_char(list(overlaps)[0])


def part2(input_raw: str):
    bags = input_raw.splitlines()
    groups = chunk_list(bags, 3)
    group_scores = [parse_group(x) for x in groups]
    return sum(group_scores)


input_raw = read_file_to_one_big_string("2022/data/day03/input.txt")

part1_test_solution = 157
part2_test_solution = 70

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
