from typing import List, Union
from statistics import median


def read_file(filename):
    with open(filename) as f:
        return [line.strip() for line in f.readlines()]


PAIRS = {
    "(": ")",
    "[": "]",
    "{": "}",
    "<": ">",
}

OPENS = "([{<"
CLOSES = ")]}>"

POINTS = {
    ")": 3,
    "]": 57,
    "}": 1197,
    ">": 25137,
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
            raise Exception("Invalid character")
    return stack


def part1(data: List[str]):
    errors = [test_line(line) for line in data]
    points = [POINTS.get(e, 0) for e in errors if type(e) == str]
    return sum(points)


AUTOCOMPLETE_POINTS = {
    "(": 1,
    "[": 2,
    "{": 3,
    "<": 4,
}


def calc_autocomplete_score(missing_stack: List[str]):
    missing_stack.reverse()
    score = 0
    for char in missing_stack:
        score = score * 5 + AUTOCOMPLETE_POINTS[char]
    return score


def part2(data: List[str]):
    errors = [test_line(line) for line in data]
    scores = [calc_autocomplete_score(e) for e in errors if type(e) == list]
    return median(scores)


test_input = [
    R"[({(<(())[]>[[{[]{<()<>>",
    R"[(()[<>])]({[<{<<[]>>(",
    R"{([(<{}[<>[]}>{[]{[(<()>",
    R"(((({<>}<{<{<>}{[]{[]{}",
    R"[[<[([]))<([[{}[[()]]]",
    R"[{[{({}]{}}([{[{{{}}([]",
    R"{<[[]]>}<{[{[{[]{()[[[]",
    R"[<(<(<(<{}))><([]([]()",
    R"<{([([[(<>()){}]>(<<{{",
    R"<{([{{}}[<[[[<>{}]]]>[]]",
]

input_raw = read_file("2021/data/day10/input.txt")

assert (part1(test_input)) == 26397

print(part1(input_raw))

assert (part2(test_input)) == 288957

print(part2(input_raw))
