
def read_file_to_one_big_string(filename):
    with open(filename) as f:
        return f.read()

test_input = """
A Y
B X
C Z
""".strip()

scores_map = {
    'A': 0,
    'B': 1,
    'C': 2,
    'X': 0, 
    'Y': 1, 
    'Z': 2, 
}

diff_to_game_score = {
    0: 3,
    1: 0,
    2: 6,
}

letter_score_map = {
    'X': 1,
    'Y': 2,
    'Z': 3,
}

def parse_game(s: str):
    letters = s.split(' ')
    a, b = (scores_map[x] for x in letters)
    diff = (a - b + 3) % 3
    game_score = diff_to_game_score[diff]
    letter_score = letter_score_map[letters[1]]
    return game_score + letter_score



def part1(input_raw: str):
    games_raw = input_raw.split('\n')
    return sum(parse_game(x) for x in games_raw)

part2_map = {
    'A X': 0 + 3 ,
    'A Y': 3 + 1 ,
    'A Z': 6 + 2 ,
    'B X': 0 + 1 ,
    'B Y': 3 + 2 ,
    'B Z': 6 + 3 ,
    'C X': 0 + 2 ,
    'C Y': 3 + 3 ,
    'C Z': 6 + 1 ,
}

def part2(input_raw: str):
    return sum(part2_map[x] for x in input_raw.splitlines())

input_raw = read_file_to_one_big_string('2022/data/day02/input.txt')

assert part1(test_input) == 15

print(f"Part1: {part1(input_raw)}")

assert part2(test_input) == 12

print(f"Part2: {part2(input_raw)}")



