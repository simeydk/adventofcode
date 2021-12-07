from collections import Counter

def read_file(filename):
    with open(filename) as f:
        return [line.strip() for line in f.readlines()]

def parse_line(line):
    start, end = line.split(' -> ')
    start_coords = tuple(int(x) for x in start.split(','))
    end_coords = tuple(int(x) for x in end.split(','))
    return start_coords, end_coords

def parse_input(inputs):
    return [parse_line(x) for x in inputs]

def horizontal_or_vertical(start, end):
    return (start[0] == end[0]) or (start[1] == end[1])

def range_between(a, b):
    if a > b:
        return range(a, b-1, -1)
    else:
        return range(a, b+1)

def expand_line(line):
    start, end = line

    results = []
    for i in range_between(start[0], end[0]):
        for j in range_between(start[1], end[1]):
            results.append((i, j))
    return results

def flatten(list_of_lists):
    return [item for sublist in list_of_lists for item in sublist]

def part1(inputs):
    lines = parse_input(inputs)
    lines = [line for line in lines if horizontal_or_vertical(*line)]
    expanded = [expand_line(line) for line in lines]
    counts = Counter(flatten(expanded))
    return len([ value for _, value in  counts.items() if value > 1])




test_input = [
    '0,9 -> 5,9',
    '8,0 -> 0,8',
    '9,4 -> 3,4',
    '2,2 -> 2,1',
    '7,0 -> 7,4',
    '6,4 -> 2,0',
    '0,9 -> 2,9',
    '3,4 -> 1,4',
    '0,0 -> 8,8',
    '5,5 -> 8,2',
]

input_raw = read_file('2021/data/day05/input.txt')

assert part1(test_input) == 5

print(part1(input_raw))