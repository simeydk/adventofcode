from abc import ABC, abstractmethod
from typing import Iterable, List, Tuple, TypeVar, Union
from dataclasses import dataclass, field
import json
import math

DAY = 18
TEST_SOLUTION_1 = 4140
TEST_SOLUTION_2 = None

def read_file(filename) -> str:
    with open(filename, encoding="UTF-8") as f:
        return f.read()

P = TypeVar('Pair')

class Element(ABC):
    pass
    # @property
    # @abstractmethod
    # def parent(self) -> P:
    #     pass    

@dataclass
class Number(Element):
    value: int
    # parent: P = None

    def __str__(self) -> str:
        return f"{self.value}"

    def __repr__(self) -> str:
        return self.__str__()

    def __eq__(self, __o: object) -> bool:
        return self is __o


Element = Union['Pair_List', Number]
Pair_List = List[Element]

def parse_list(l: list) -> Pair_List:
    items = [Number(x) if type(x) == int else parse_list(x) for x in l]
    return items

def parse_input(data: str) -> Pair_List:
    return [parse_list(json.loads(line)) for line in data]

def split_number(number: Number):
    x = number.value /2
    return [Number(math.floor(x)), Number(math.ceil(x))]

def split(pair_list: Pair_List) -> True:
    for i, element in enumerate(pair_list):
        if type(element) == Number:
            if element.value > 9:
                pair_list[i] = split_number(element)
                return True
        else:
            if split(element) == True:
                return True
    return False 

def numbers_list(pair_list: Pair_List) -> Iterable[Number]:
    for element in pair_list:
        if type(element) == Number:
            yield element
        elif type(element) == list:
            yield from numbers_list(element)
        else:
            raise Exception(f"Unknown type: {str(type(element))}")

def is_simple_pair(pair_list: Pair_List) -> bool:
    return all(type(element) == Number for element in pair_list)

def simple_pairs(pair_list: Pair_List, depth: int = 1, parent = None) -> Iterable[Tuple[Pair_List, int]]:
    if is_simple_pair(pair_list):
        yield pair_list, depth, parent
    else:
        for element in (element for element in pair_list if type(element) == list):
             yield from simple_pairs(element, depth + 1, pair_list)

def explode(pair_list: Pair_List, depth: int = 1) -> bool:
    numbers = list(numbers_list(pair_list))
    for simple_pair, depth, parent in simple_pairs(pair_list):
        if depth > 4:
            first, second = simple_pair
            # increase number to the left
            i = numbers.index(first) - 1
            if i >= 0:
                numbers[i].value += first.value
            # increase number to the right
            j = numbers.index(second) + 1
            if j < len(numbers):
                numbers[j].value += second.value
            # replace original with zero
            parent[parent.index(simple_pair)] = Number(0)
            return True
    return False

def step(pair_list: Pair_List):
    if explode(pair_list):
        return True
    elif split(pair_list):
        return True
    else:
        return False

def reduce(pair_list: Pair_List):
    while step(pair_list):
        pass
    return pair_list

def add(*pair_lists: List[Pair_List]) -> Pair_List:
    first, *rest = pair_lists
    result = first
    for item in rest:
        result = [result, item]
    return result

def magnitude(element: Element) -> int:
    if type(element) == Number:
        return element.value
    else:
    # elif type(element) == List:
        x, y, *rest = element
        return magnitude(x) * 3 + magnitude(y) * 2
    # else:
    #     raise Exception(f"Unknown type: {str(type(element))}")


example = """[[[0,[4,5]],[0,0]],[[[4,5],[2,6]],[9,5]]]
[7,[[[3,7],[4,3]],[[6,3],[8,8]]]]
[[2,[[0,8],[3,4]]],[[[6,7],1],[7,[1,6]]]]
[[[[2,4],7],[6,[0,5]]],[[[6,8],[2,8]],[[2,1],[4,5]]]]
[7,[5,[[3,8],[1,4]]]]
[[2,[2,2]],[8,[8,1]]]
[2,9]
[1,[[[9,3],9],[[9,0],[0,7]]]]
[[[5,[7,4]],7],1]
[[[[4,2],2],6],[8,7]]"""



def part1(data: str) -> int:
    lists = [parse_list(json.loads(x)) for x in data.splitlines()]
    result = lists[0]
    for item in lists[1:]:
        result = add(result, item)
        reduce(result)
    print(result)
    return magnitude(result)

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
    
