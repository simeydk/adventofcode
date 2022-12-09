from dataclasses import dataclass
from typing import List

def read_file_to_one_big_string(filename):
    with open(filename) as f:
        return f.read()

day = 9
input_raw = read_file_to_one_big_string(f'2022/data/day{day:02d}/input.txt')
test_input = read_file_to_one_big_string(f'2022/data/day{day:02d}/test_input.txt')

# test_input = """
# """.strip()

part1_test_solution = 13
part2_test_solution = None

@dataclass
class V():
    x: int = 0
    y: int = 0

    def move(self, dx: int, dy: int):
        self.x += dx
        self.y += dy

    def __sub__(self, b: 'V') -> 'V':
        return V(self.x - b.x, self.y - b.y)

    def __add__(self, b: 'V') -> 'V':
        return V(self.x + b.x, self.y + b.y)

    @property
    def tuple(self):
        return (self.x, self.y)

    @property
    def abs(self):
        return V(abs(self.x), abs(self.y))
    
    @property
    def norm(self):
        a = self.abs
        return V(
            self.x // self.abs.x if self.x else self.x,
            self.y // self.abs.y if self.y else self.y,
        )

MOVES = {
    'R': V(1,0),
    'L': V(-1,0),
    'U': V(0,1),
    'D': V(0,-1),

}

def part1(input_raw: str):
    head = V(0,0)
    tail = V(0,0)
    tail_hist: set[tuple[int, int]] = set([tail.tuple])

    for line in input_raw.splitlines():
        direction, amount = line.split()
        amount = int(amount)
        head_move = MOVES[direction]
        for _ in range(amount):
            head += head_move
            d = head - tail
            if d.abs.x <= 1 and d.abs.y <= 1:
                pass
            else:
                
                tail += d.norm
                tail_hist.add(tail.tuple)

    # print(head)
    return len(tail_hist)

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




