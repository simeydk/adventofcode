
def read_file_to_one_big_string(filename):
    with open(filename) as f:
        return f.read()

day_number = 10
part1_test_solution = 13140
part2_test_solution = None


input_raw = read_file_to_one_big_string(f'2022/data/day{day_number:02d}/input.txt')
test_input = read_file_to_one_big_string(f'2022/data/day{day_number:02d}/test_input.txt')

# test_input = """
# noop
# addx 3
# addx -5
# """.strip('\n')


def part1(input_raw: str):
    lines = input_raw.splitlines()
    value = 1
    results = [0, value]
    for line in lines:
        words = line.split()
        match words[0]:
            case 'noop':
                results.append(value)
            case 'addx':
                results.append(value)
                value += int(words[1])
                results.append(value)
            case other:
                raise ValueError(f'Invalid Instruction {other}')
    # return results
    entries =  [i for i in range(20, min(len(results), 220+1), 40)]
    return sum([(results[i] * i) for i in entries])

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




