import itertools
import re
from collections import Counter

def read_file_to_one_big_string(filename):
    with open(filename) as f:
        return f.read()

year=2024
day_number = 4
part1_test_solution = 18
part2_test_solution = 9
test_input = """
""".strip(
    "\n"
)


test_input = read_file_to_one_big_string(f"{year}/data/day{day_number:02d}/test_input.txt")
input_raw = read_file_to_one_big_string(f"{year}/data/day{day_number:02d}/input.txt")

def transpose(M):
    lines = M.splitlines()
    ncols = len(lines)
    nrows = len(lines[0])
    new_rows = []
    for c in range(nrows):
        new_row = ''.join(line[c] for line in lines)
        new_rows.append(new_row)
    return '\n'.join(new_rows)
    return [[M[j][i] for j in range(len(M))] for i in range(len(M[0]))]

def skew_right(M, filler = '.'):
    lines = M.splitlines()
    length = len(lines[0])
    new_lines = []
    for i, line in enumerate(lines):
        before = filler * (length - i)
        after = filler * i
        new_line = before + line + after
        new_lines.append(new_line)
    return '\n'.join(new_lines)

def skew_left(M, filler = '.'):
    lines = M.splitlines()
    length = len(lines[0])
    new_lines = []
    for i, line in enumerate(lines):
        after = filler * (length - i)
        before = filler * i
        new_line = before + line + after
        new_lines.append(new_line)
    return '\n'.join(new_lines)

def parse_input(input_raw):
    t = transpose(input_raw)    
    sr = transpose(skew_right(input_raw))
    sl = transpose(skew_left(input_raw))
    
    return input_raw, t, sr, sl 

def part1(input_raw: str):
    w = 'XMAS'
    input = '\n\n'.join(parse_input(input_raw))
    return input.count(w) + input.count(w[::-1])

NW = (-1, -1)
N = (-1, 0)
NE = (-1, 1)
C = (0, 0)
W = (0, -1)
E = (0, 1)
SW = (1, -1)
S = (1, 0)
SE = (1, 1)

triples = [
    [NW, C, SE],
    # [N, C, S],
    [NE, C, SW],
    # [W, C, E],
]

triples = triples + [line[::-1] for line in triples]
print(triples)

def get_word(lines, x, y, offsets):
    return ''.join(lines[y + dy][x + dx] for dy, dx in offsets)

def get_words(lines, x, y, offset_sets):
    return [get_word(lines, x, y, offset) for offset in offset_sets]

# def get_words(lines, x,)

def process_point(lines, x, y):
    if lines[y][x] != 'A':
        return []
    words = get_words(lines, x, y, triples)
    return words

def part2(input_raw: str):
    lines = input_raw.splitlines()
    h = len(lines)
    w = len(lines[0])
    n = 0
    for x, y in itertools.product(range(1, w-1), range(1, h -1)):
        minigrid = '\n'.join([line[x-1:x+2] for line in lines[y-1:y+2]])
        if minigrid.splitlines()[1][1] != 'A':
            continue
        words = get_words(lines, x, y, triples)
        if words.count('MAS') > 1:
            n+=1
        # print(x, y)
        # print(minigrid)
        # print(words)
        # print('')
    return n


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
