def read_file_to_one_big_string(filename):
    with open(filename) as f:
        return f.read()


day_number = 10
part1_test_solution = 13140
part2_test_solution = """
01  ##..##..##..##..##..##..##..##..##..##..
02  ###...###...###...###...###...###...###.
03  ####....####....####....####....####....
04  #####.....#####.....#####.....#####.....
05  ######......######......######......####
06  #######.......#######.......#######....."""


input_raw = read_file_to_one_big_string(f"2022/data/day{day_number:02d}/input.txt")
test_input = read_file_to_one_big_string(
    f"2022/data/day{day_number:02d}/test_input.txt"
)

# test_input = """
# noop
# addx 3
# addx -5
# """.strip('\n')


def parse_input(input_raw):
    lines = input_raw.splitlines()
    value = 1
    results = [value]
    for line in lines:
        words = line.split()
        match words[0]:
            case "noop":
                results.append(value)
            case "addx":
                results.append(value)
                value += int(words[1])
                results.append(value)
            case other:
                raise ValueError(f"Invalid Instruction {other}")
    return results


def part1(input_raw: str):
    results = [1] + parse_input(input_raw)
    # return results
    entries = [i for i in range(20, min(len(results), 220 + 1), 40)]
    return sum([(results[i] * i) for i in entries])


def chunk_list(arr, chunk_size):
    result = []
    arr = list(arr)
    for i in range(0, len(arr), chunk_size):
        result.append(arr[i : i + chunk_size])
    return result


def pixels_to_str(pixels):
    s = ""
    for i, chunk in enumerate(chunk_list(pixels, 40)):
        s += f"\n{i+1:02d}  "
        s += "".join(chunk)
    return s


def part2(input_raw: str):
    sprite_positions = parse_input(input_raw)
    pixels = [
        "#" if abs((i % 40) - sprite_positions[i]) <= 1 else "." for i in range(240)
    ]
    s = pixels_to_str(pixels)
    return s


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
