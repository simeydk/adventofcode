from typing import Iterable, List, TypeVar, Union
import json
from dataclasses import dataclass



DAY = 18
TEST_SOLUTION_1 = None
TEST_SOLUTION_2 = None

@dataclass 
class Number:
    value: int
    parent: 'Pair' = None

    def __str__(self):
        return f"{self.value}"

    def copy(self, parent = None):
        return Number(self.value, parent)


@dataclass
class Pair:
    x: Union[Number, 'Pair']
    y: Union[Number, 'Pair']
    parent: 'Pair' = None

    @property
    def level(self) -> int:
        return 1 + (self.parent.level if self.parent else 0)

    @property
    def simple(self) -> bool:
        return (type(self.x) == Number) and (type(self.y) == Number)

    def sub_pairs(self) -> Iterable['Pair']:
        if type(self.x) == type(self):
            if self.x.simple: 
                yield self.x
            else:
                yield from self.x.sub_pairs()
        if type(self.y) == type(self):
            if self.y.simple:
                yield self.y
            else:
                yield from self.y.sub_pairs()

    def numbers(self) -> Iterable[Number]:
        if type(self.x) == Number:
            yield self.x
        else:
            yield from self.x.numbers()
        if type(self.y) == Number:
            yield self.y
        else:
            yield from self.y.numbers()

    def __str__(self):
        return f"P({self.x}, {self.y})"

    def copy(self, parent: 'Pair' = None):
        x = self.x.copy()
        y = self.y.copy()
        p = Pair(x, y, parent)
        x.parent = p
        y.parent = p
        return p

    @classmethod
    def from_json(cls, l: list, parent: 'Pair' = None):
        x = Number(l[0]) if type(l[0]) == int else Pair.from_json(l[0])
        y = Number(l[1]) if type(l[1]) == int else Pair.from_json(l[1])
        p = cls(x, y, parent)
        x.parent = p
        y.parent = p
        # print(f"{p.level} {p.simple} {p}")
        return p




    def explode(self) -> bool:
        numbers = list(self.numbers())
        for a in ['x', 'y']:
            if type(self[a]) == type(self):
                if self[a].simple:
                    if self[a].level >= 4:
                        i = numbers.index(self[a].x)
                        if i > 1: numbers[i-1].value += self[a].x.value
                        j = numbers.index(self[a].y)
                        if j < len(numbers) - 1: numbers[j+1].value += self[a].y.value
                        self[a] = Number(0, self)
                        return True
                else:
                    if self[a].explode():
                        return True
        return False



    def split(self) -> bool:
        for a in ['x', 'y']:
            if type(self[a]) == Number:
                if self[a] >= 10:
                    self[a] = Pair(self[a]//2, self[a] //2 + 1, self)
                    return True
            elif self[a].split():
                return True
            return False


    def reduce(self) -> 'Pair':
        pass



P = Pair.from_json

p = P([[[[[4,3],4],4],[7,[[8,4],9]]],[1,1]])
print(p)
p.explode()
print(p)
p.explode()
print(p)
p.explode()
print(p)
p.split()
print(p)

def read_file(filename) -> str:
    with open(filename, encoding="UTF-8") as f:
        return f.read()

def parse_input(data:str):
    lines = data.splitlines()
    s = f"[{','.join(lines)}]"
    return json.loads(s)


def part1(data: str) -> int:
    data = parse_input(data)
    p = Pair.from_json(data)
    p.explode()
    for pair in p.sub_pairs():
        print(f"{pair.level} {'x' if pair.simple else ' '} {pair}")
    for i, number in enumerate(p.numbers()):
        print(f"{i:2d} {number}")
    print(f"{Pair.from_json(data)}")

def part2(data: str) -> int:
    pass

test_input = """[[[0,[5,8]],[[1,7],[9,6]]],[[4,[1,2]],[[1,4],2]]]
[[[5,[2,8]],4],[5,[[9,9],0]]]
[6,[[[6,2],[5,6]],[[7,6],[4,7]]]]
[[[6,[0,7]],[0,9]],[4,[9,[9,0]]]]
[[[7,[6,4]],[3,[1,3]]],[[[5,5],1],9]]
[[6,[[7,3],[3,2]]],[[[3,8],[5,7]],4]]
[[[[5,4],[7,7]],8],[[8,3],8]]
[[9,3],[[9,9],[6,[4,9]]]]
[[2,[[7,7],7]],[[5,8],[[9,3],[0,2]]]]
[[[[5,2],5],[8,[3,7]]],[[5,[7,5]],[4,4]]]"""


input_raw = read_file(f'2021/data/day{DAY:02d}/input.txt')

if TEST_SOLUTION_1:
    assert part1(test_input) == TEST_SOLUTION_1
    print(f"Solution 1:\n{part1(input_raw)}")
    if TEST_SOLUTION_2:
        assert part2(test_input) == TEST_SOLUTION_2
        print(f"Solution 2:\n{part2(input_raw)}")
    else:
        print(f"Test 2:\n{part2(test_input)}")
else:
    print(f"Test 1:\n{part1(test_input)}")
    
