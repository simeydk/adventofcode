from typing import List

def read_file_to_one_big_string(filename):
    with open(filename) as f:
        return f.read()

input_raw = read_file_to_one_big_string('2022/data/day08/input.txt')

test_input = """
30373
25512
65332
33549
35390
""".strip()

part1_test_solution = 21
part2_test_solution = 8

def parse_input(input_raw: str) -> list[list[int]]:
    lines = input_raw.splitlines()
    return [[int(x) for x in line] for line in lines]

def is_visible(i,j, grid):
    value = grid[i][j]
    up, down, left, right = True, True, True, True
    for di in range(len(grid)):
        dvalue = grid[di][j]
        if dvalue >= value:
            if di < i:
                # print('up', (i,j), value, (di, j), dvalue)
                up = False
            if di > i:
                # print('down', (i,j), value, (di, j), dvalue)
                down = False
    for dj in range(len(grid[0])):
        dvalue = grid[i][dj]
        if dvalue >= value:
            if dj < j:
                # print('left', (i,j), value, (i, dj), dvalue)
                left = False
            if dj > j:
                # print('right', (i,j), value, (i, dj), dvalue)
                right = False 
    return up or down or left or right

def part1(input_raw: str):
    grid = parse_input(input_raw)
    num_visible = 0
    for i in range(len(grid)):
        for j in range(len(grid[0])):
            visible = is_visible(i, j, grid)
            num_visible += visible
    return num_visible

def scenic_score(i,j, grid):
    value = grid[i][j]
    up, down, left, right = 0, 0, 0, 0
    for di in range(i-1, -1, -1):
        up += 1
        dvalue = grid[di][j]
        if dvalue >= value:
            break
    for di in range(i+1, len(grid), 1):
        down += 1
        dvalue = grid[di][j]
        if dvalue >= value:
            break
    for dj in range(j-1, -1, -1):
        left += 1
        dvalue = grid[i][dj]
        if dvalue >= value:
            break
    for dj in range(j+1, len(grid), 1):
        right += 1
        dvalue = grid[i][dj]
        if dvalue >= value:
            break 
    return up * down * left * right

def part2(input_raw: str):
    grid = parse_input(input_raw)
    best = 0
    # print(scenic_score(3,2,grid))
    for i in range(len(grid)):
        for j in range(len(grid[0])):
            best = max(best, scenic_score(i,j,grid))
    return best


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




