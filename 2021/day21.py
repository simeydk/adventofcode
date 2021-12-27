from collections import Counter, defaultdict, namedtuple
from typing import DefaultDict, Generator, List, NamedTuple, Tuple
from dataclasses import dataclass, field
from itertools import product

DAY = 21
TEST_SOLUTION_1 = 739785
TEST_SOLUTION_2 = 444356092776315

def read_file(filename) -> str:
    with open(filename, encoding="UTF-8") as f:
        return f.read()

def parse_input(data: str) -> List[int]:
    lines = data.splitlines()
    starts = tuple([int(line.split(': ')[1]) for line in lines])
    return starts

def get_deterministic_die(n = 100) -> Generator[int, None, None]:
    while True:
        for i in range(1, n+1):
            yield i

class Deterministic_Die:

    def __init__(self, n = 100):
        self.count = 0
        self.generator = get_deterministic_die(n)

    def roll(self, n = 1):  
        self.count += n
        return [next(self.generator) for _ in range(n)]

    def __repr__(self):
        return f"Deterministic_Die({self.count})"

@dataclass
class Player:
    position: int
    score: int = field(init=False, default=0)

    def move(self, n) -> bool:
        self.position = (self.position + n - 1) % 10 + 1 
        self.score += self.position
        return self.won

    @property
    def won(self):
        return self.score >= 1000

def play(start_a: int, start_b: int):
    a = Player(start_a)
    b = Player(start_b)
    players = [a, b]
    die = Deterministic_Die()
    while True:
        for i, player in enumerate(players):
            roll = sum(die.roll(3))
            if player.move(roll):
                return die.count * players[int(not i)].score

def part1(data: str) -> int:
    starts = parse_input(data)
    return play(*starts)
    

MOVES = Counter(sum(values) for values in product(range(1,4), repeat = 3))

WINNING_SCORE = 21

def move(current, move_by):
    return (current + move_by - 1) % 10 + 1

class Vector(NamedTuple):
    a: int
    b: int

    def __add__(self, other):
        return Vector(self.a + other.a, self.b + other.b)

    def __mul__(self, other):
        return Vector(self.a * other, self.b * other)

    def __repr__(self):
        return f"Vector({self.a}, {self.b})"

class Game(NamedTuple):
    a_pos: int
    b_pos: int
    a_score: int = 0
    b_score: int = 0
    # weight: int = 1
    a_next: bool = True

    def moves(self) -> Generator[Tuple['Game', int], None, None]:
        for move_by, move_weight in MOVES.items():
            yield self.play_move(move_by), move_weight

    def play_move(self, move_amount):
        if self.a_next:
            a_pos = move(self.a_pos, move_amount)
            return Game(
                a_pos = a_pos,
                b_pos = self.b_pos,
                a_score = self.a_score + a_pos,
                b_score = self.b_score,
                a_next = False,
            )
        else:
            b_pos = move(self.b_pos, move_amount)
            return Game(
                a_pos = self.a_pos,
                b_pos = move(self.b_pos, move_amount),
                a_score = self.a_score,
                b_score = self.b_score + b_pos,
                a_next = True,
            )

    @property
    def winner(self) -> Vector:
        if self.a_score >= WINNING_SCORE: return Vector(1,0)
        if self.b_score >= WINNING_SCORE: return Vector(0,1)

    def __repr__(self):
        return f"Game({self.a_pos}, {self.b_pos}, {self.a_score}, {self.b_score}, {self.a_next})"



assert Game(0,0).play_move(17).play_move(23) == Game(7,3,7,3,True)

@dataclass
class Multiverse_Game:
    states: DefaultDict[Game, int]
    wins: Vector = Vector(0,0)

    def step(self: 'Multiverse_Game') -> 'Multiverse_Game':
        states = defaultdict(int)
        wins = self.wins
        for game, weight in self.states.items():
            if game.winner:
                wins = wins + Vector(game.winner.a * weight, game.winner.b * weight)
            else:
                for new_game, new_weight in game.moves():
                    states[new_game] += weight * new_weight
        return Multiverse_Game(states, wins)

def part2(data: str) -> int:
    starts = parse_input(data)
    game = Game(*starts)
    multiverse_game = Multiverse_Game({game: 1})
    while multiverse_game.states:
        multiverse_game = multiverse_game.step()
    return max(multiverse_game.wins)

test_input = """Player 1 starting position: 4
Player 2 starting position: 8"""

input_raw = """Player 1 starting position: 3
Player 2 starting position: 4"""


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
    
