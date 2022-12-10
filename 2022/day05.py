import re
from typing import List


def read_file_to_one_big_string(filename):
    with open(filename) as f:
        return f.read()


input_raw = read_file_to_one_big_string("2022/data/day05/input.txt")

test_input = """
    [D]    
[N] [C]    
[Z] [M] [P]
 1   2   3 

move 1 from 2 to 1
move 3 from 1 to 3
move 2 from 2 to 1
move 1 from 1 to 2
""".strip(
    "\n"
)

part1_test_solution = "CMZ"
part2_test_solution = "MCD"


def parse_cranes(s: str):
    lines = s.split("\n")
    numbers_raw = lines.pop()
    numbers = [int(x) for x in numbers_raw.strip().split("   ")]
    num_stacks = max(numbers)
    stacks = [[] for _ in range(num_stacks)]
    for line in lines:
        for iStack, stack in enumerate(stacks):
            text = line[4 * iStack : 4 * iStack + 3]
            text = text.strip(" []")
            if text:
                stack.append(text)
    for stack in stacks:
        stack.reverse()
    return stacks


def parse_instruction(s):
    findall = re.findall(r"move (\d+) from (\d+) to (\d+)", s)[0]
    amount, src, dest = [int(x) for x in findall]
    src -= 1
    dest -= 1
    return amount, src, dest


def parse_instructions(s):
    lines = s.splitlines()
    return [parse_instruction(x) for x in lines]


def parse_input(s: str):
    cranes_raw, instructions_raw = s.split("\n\n")
    cranes = parse_cranes(cranes_raw)
    instructions = parse_instructions(instructions_raw)
    return cranes, instructions


def process_instruction(cranes, instruction):
    amount, src, dest = instruction

    for _ in range(amount):
        crate = cranes[src].pop()
        cranes[dest].append(crate)


def part1(input_raw: str):
    cranes, instructions = parse_input(input_raw)
    for instruction in instructions:
        process_instruction(cranes, instruction)
    return "".join(crane[-1] for crane in cranes)


def process_instruction_part2(cranes, instruction):
    amount, src, dest = instruction

    crates = cranes[src][-amount:]
    cranes[src] = cranes[src][:-amount]
    cranes[dest].extend(crates)


def part2(input_raw: str):
    cranes, instructions = parse_input(input_raw)
    for instruction in instructions:
        process_instruction_part2(cranes, instruction)
    return "".join(crane[-1] for crane in cranes)


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
