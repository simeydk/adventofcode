def read_file_to_one_big_string(filename):
    with open(filename) as f:
        return f.read()

year = 2024
day_number = 6
part1_test_solution = None
part2_test_solution = None
test_input = """
""".strip(
    "\n"
)


input_raw = read_file_to_one_big_string(f"{year}/data/day{day_number:02d}/input.txt")


def part1(input_raw: str):
    return 0


def part2(input_raw: str):
    return 0


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
