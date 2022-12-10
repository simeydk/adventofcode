from ast import Tuple
from typing import List


def read_file_to_one_big_string(filename):
    with open(filename) as f:
        return f.read()


input_raw = read_file_to_one_big_string("2020/data/day22/input.txt")

test_input = """
Player 1:
9
2
6
3
1

Player 2:
5
8
4
7
10
""".strip()

part1_test_solution = 306
part2_test_solution = None


def parse_player(s: str):
    lines = s.splitlines()
    lines = lines[1:]
    return [int(x) for x in lines]


def parse_input(s: str):
    a, b = s.split("\n\n")
    return parse_player(a), parse_player(b)


def play_round(a: List[int], b: List[int]) -> tuple[List[int], List[int]]:
    a_card = a.pop(0)
    b_card = b.pop(0)
    if a_card > b_card:
        a.extend([a_card, b_card])
    else:
        b.extend([b_card, a_card])
    return a, b


def calc_score(a):
    a = [*a]
    a.reverse()
    return sum(x * (i + 1) for i, x in enumerate(a))


def part1(input_raw: str):
    a, b = parse_input(input_raw)
    while min(len(x) for x in [a, b]) > 0:
        a, b = play_round(a, b)
    winner = a or b
    return calc_score(winner)


def game_str(a, b):
    return str((a, b))


def play_round_part2(
    a: List[int], b: List[int], history
) -> tuple[List[int], List[int]]:
    s = game_str(a, b)
    if s in history:
        print("recursion! A wins!")
        return a, b
    history.push(s)
    a_card = a.pop(0)
    b_card = b.pop(0)
    if a_card > b_card:
        a.extend([a_card, b_card])
    else:
        b.extend([b_card, a_card])
    return a, b


def play_recursion(a, b):
    pass


def part2(input_raw: str):
    a, b = parse_input(input_raw)
    while min(len(x) for x in [a, b]) > 0:
        a, b = play_round(a, b)
    winner = a or b
    return calc_score(winner)


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
