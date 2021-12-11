from typing import List, Union

def read_file(filename):
    with open(filename) as f:
        return [line.strip() for line in f.readlines()]

PAIRS = { '(': ')', '[': ']', '{': '}', '<': '>',}

OPENS = '([{<'
CLOSES = ')]}>'

POINTS = {
    ')': 3,
    ']': 57,
    '}': 1197,
    '>': 25137,
}

def test_line(string: str) -> Union[str, List[str]]:
    stack = []
    for char in string:
        if char in OPENS:
            stack.append(char)
        elif char in CLOSES:
            expected = PAIRS[stack[-1]]
            if char == expected:
                stack.pop(-1)
            else:
                return char
        else:
            raise Exception('Invalid character')
    return stack


def part1(data: List[str]):
    errors = [test_line(line) for line in data]
    points = [POINTS.get(e,0) for e in errors if type(e) == str]
    return sum(points)


test_input = [
    R'[({(<(())[]>[[{[]{<()<>>',
    R'[(()[<>])]({[<{<<[]>>(',
    R'{([(<{}[<>[]}>{[]{[(<()>',
    R'(((({<>}<{<{<>}{[]{[]{}',
    R'[[<[([]))<([[{}[[()]]]',
    R'[{[{({}]{}}([{[{{{}}([]',
    R'{<[[]]>}<{[{[{[]{()[[[]',
    R'[<(<(<(<{}))><([]([]()',
    R'<{([([[(<>()){}]>(<<{{',
    R'<{([{{}}[<[[[<>{}]]]>[]]',
]

input_raw = read_file('2021/data/day10/input.txt')

assert (part1(test_input)) == 26397
print(part1(input_raw))