def read_file(filename):
    with open(filename) as f:
        return [line.strip() for line in f.readlines()]


def part1(data):
    positions = [int(x) for x in data[0].split(',')]
    min_cost = 10 ** 10
    min_pos = -1
    for i in range(min(positions), max(positions) + 1):
        cost = sum([abs(x - i) for x in positions])
        if cost < min_cost:
            min_cost = cost
            min_pos = i
    return min_pos, min_cost

def cost_p2(dist):
    a = abs(dist)
    return a * (a + 1) // 2
    
def part2(data):
    positions = [int(x) for x in data[0].split(',')]
    min_cost = 10 ** 10
    min_pos = -1
    for i in range(min(positions), max(positions) + 1):
        cost = sum([cost_p2(x - i) for x in positions])
        if cost < min_cost:
            min_cost = cost
            min_pos = i
    return min_pos, min_cost


test_input = ['16,1,2,0,4,2,7,1,2,14']

input_raw = read_file('2021/data/day07/input.txt')

assert part1(test_input)[0] == 2

print(part1(input_raw))

assert part2(test_input) == (5, 168)

print(part2(input_raw))