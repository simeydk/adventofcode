def read_file(filename):
    with open(filename) as f:
        return [line.strip() for line in f.readlines()]


def read_file_to_one_big_string(filename):
    with open(filename) as f:
        return f.read()


test_input_raw = read_file_to_one_big_string("2022/data/day01/test_input.txt")
input_raw = read_file_to_one_big_string("2022/data/day01/input.txt")


def parse_elf(text: str):
    strings = text.splitlines()
    return sum(int(string) for string in strings)


def part1(input_raw: str):
    elves_lists = input_raw.split("\n\n")
    elves_totals = map(parse_elf, elves_lists)
    return max(elves_totals)


def part2(input_raw: str):
    elves_lists = input_raw.split("\n\n")
    elves_totals = [parse_elf(x) for x in elves_lists]
    elves_totals.sort()
    return sum(elves_totals[-3:])


assert part1(test_input_raw) == 24000

print(f"Part 1: {part1(input_raw)}")

assert part2(test_input_raw) == 45000

print(f"Part 2: {part2(input_raw)}")
