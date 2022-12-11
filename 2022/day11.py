from dataclasses import dataclass, field
import math
from time import perf_counter
from typing import Callable


def read_file_to_one_big_string(filename):
    with open(filename) as f:
        return f.read()


day_number = 11
part1_test_solution = 10605
part2_test_solution = 2713310158


input_raw = read_file_to_one_big_string(f"2022/data/day{day_number:02d}/input.txt")
test_input = read_file_to_one_big_string(
    f"2022/data/day{day_number:02d}/test_input.txt"
)

# test_input = """
# """.strip('\n')

"""
Monkey 0:
  Starting items: 79, 98
  Operation: new = old * 19
  Test: divisible by 23
    If true: throw to monkey 2
    If false: throw to monkey 3
"""


@dataclass
class Monkey:
    index: int
    items: list[int]
    operation: Callable[[int], int] = field(repr=False)
    test_num: int
    if_true: int
    if_false: int
    num_items_inspected: int = 0
    worry_factor: int = 3

    def inspect_item(self, value: int) -> tuple[int, int]:
        new_value = self.operation(value) // self.worry_factor
        new_owner = self.if_true if (new_value % self.test_num) == 0 else self.if_false
        return new_value, new_owner

    def inspect_items(self) -> list[tuple[int,int]]:
        result = [self.inspect_item(value) for value in self.items]
        self.num_items_inspected += len(self.items)
        self.items = []
        return result


def parse_operation(op: str) -> Callable[[int], int]:
    match op.split():
        case ["old", "*", "old"]:
            return lambda x: x * x
        case ["old", "+", a]:
            return lambda x: x + int(a)
        case ["old", "*", a]:
            return lambda x: x * int(a)
        case _:
            raise ValueError(f'Invalid operation: {op}')

def parse_monkey(monkey_raw: str):
    lines = monkey_raw.splitlines()
    assert len(lines) == 6
    index = int(lines[0].replace("Monkey ", "").replace(":", ""))
    items = [int(x) for x in lines[1].strip().replace("Starting items: ", "").split(", ")]
    operation = parse_operation(lines[2].strip().replace("Operation: new = ", ""))
    test_num = int(lines[3].replace("Test: divisible by ", ""))
    if_true = int(lines[4].strip().replace("If true: throw to monkey ", ""))
    if_false = int(lines[5].strip().replace("If false: throw to monkey ", ""))
    return Monkey(
        index=index,
        items=items,
        operation=operation,
        test_num=test_num,
        if_true=if_true,
        if_false=if_false,
    )

def step(monkeys: list[Monkey], n = 1):
    # CREDIT: Without the Lowest Common Multiple (lcm) trick, the values get very large and 10k iterations takes forever
    # I got this from Jonathan Paulson's solution
    # his code: https://github.com/jonathanpaulson/AdventOfCode/blob/master/2022/11.py
    # his stream: https://www.youtube.com/watch?v=W9vVJ8gDxj4
    lcm = math.prod(m.test_num for m in monkeys)
    # for m in monkeys:
    #     lcm *= m.test_num
    for _ in range(n):
        for monkey in monkeys:
            tossed = monkey.inspect_items()
            for value, owner in tossed:
                value %= lcm
                monkeys[owner].items.append(value)

def monkeys_to_str(monkeys: list[Monkey]):
    return '\n'.join(str(monkey.items) + f" #{monkey.num_items_inspected}" for monkey in monkeys)

def parse_input(input_raw):
    monkeys_raw = input_raw.strip().split("\n\n")
    monkeys = [parse_monkey(m) for m in monkeys_raw]
    return monkeys


def part1(input_raw: str):
    monkeys = parse_input(input_raw)
    step(monkeys, 20)
    # print(monkeys_to_str(monkeys))
    inspected = [m.num_items_inspected for m in monkeys]
    inspected.sort(reverse=True)
    return inspected[0] * inspected[1]


def part2(input_raw: str):
    monkeys = parse_input(input_raw)
    for monkey in monkeys:
        monkey.worry_factor = 1
    start_time = perf_counter()
    step(monkeys, 10_000)
    end_time = perf_counter()
    print(f"{end_time - start_time:0f}s") 
    inspected = [m.num_items_inspected for m in monkeys]
    inspected.sort(reverse=True)
    return inspected[0] * inspected[1]
    return


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
