
def read_file(filename):
    with open(filename) as f:
        return [line.strip() for line in f.readlines()]


def parse_instruction(instruction):
    direction, size_string = instruction.split(' ')
    size = int(size_string)
    if direction == 'forward':
        return [size, 0]
    elif direction == 'backward':
        return [-size, 0]
    elif direction == 'down':
        return [0,size]
    elif direction == 'up':
        return [0,-size]

def add_vectors(vectors):
    x = sum(v[0] for v in vectors)
    y = sum(v[1] for v in vectors)
    return [x,y]        

def part1(instructions):
    vectors = [parse_instruction(instruction) for instruction in instructions]
    result = add_vectors(vectors)
    return result[0] * result[1] 


test_input = [
    "forward 5",
    "down 5",
    "forward 8",
    "up 3",
    "down 8",
    "forward 2",
]

input_raw = read_file('2021/data/day02/input.txt')

assert part1(test_input) == 150

print(part1(input_raw))
