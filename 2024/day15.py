from __future__ import annotations
from abc import ABC
from collections import defaultdict
from dataclasses import dataclass, field
from functools import cached_property
from typing import Generator, Generic, List, NamedTuple, Optional, Set, Tuple, TypeVar, overload
import sys
from pathlib import Path


sys.path.append(str(Path('')))
from utils.helpers import create_grid, nested_items, nested_join, parse_grid
from utils.runner import runner
from utils.utils import read_file_to_string
from utils.vector import Vector as V
from utils.rect import Rectangle as R

year=2024
day_number = 15
part1_test_solution = 10092
part2_test_solution = 9021

test_input = read_file_to_string(f"{year}/data/day{day_number:02d}/test_input.txt")
input_raw = read_file_to_string(f"{year}/data/day{day_number:02d}/input.txt")

T = TypeVar("T")

class Cardinal(NamedTuple, Generic[T]):
    N: T
    E: T
    S: T
    W: T


SHIFT: Cardinal[V] = Cardinal(
    V(-1, 0),
    V(0, 1),
    V(1, 0),
    V(0, -1)
)

SHIFTS = {
    '^' : V(-1,0),
    '<' : V(0, -1),
    'v' : V(1, 0),
    '>' : V(0,1),
}



@dataclass
class Game():
    board: defaultdict[V, Optional[str]] = field(default_factory=lambda : defaultdict(lambda: None))
    move_queue: list[str] = field(default_factory=list)


    def key_of(self, item:str) -> Optional[V]:
        for key, value in self.board.items():
            if value == item:
                return key

    @property
    def player_pos(self) -> V:
        result = self.key_of('@')
        if result == None:
            raise ValueError("Could not find player position")
        return result
    
    @property
    def crate_positions(self) -> Generator[V, None, None]:
        return (
            key for key, value in self.board.items() if value == 'O'
        )
    
    @property
    def gps_sum(self) -> int:
        return sum( (int(x * 100 + y) for x, y in self.crate_positions))

    @cached_property
    def board_size(self) -> V:
        return max(self.board.keys()) + V(1,1)

    @property
    def board_str(self) -> str:
        board_size = self.board_size
        grid: List[List[str]] = create_grid(board_size.x, board_size.y, " ") # type: ignore
        for pos, value in self.board.items():
            grid[int(pos.x)][int(pos.y)] = str(value)
        return nested_join(grid, delimiter="")

    def step(self, n = 1):
        n = min(n, len(self.move_queue))
        for _ in range(n):
            move_str = self.move_queue.pop(0)
            self.play_move(move_str)
    
    def play_move(self, move_str: str):
        shift = SHIFTS[move_str]
        player_pos = self.player_pos
        self.shift_item(player_pos, shift)


    def shift_item(self, src: V, delta: V) -> bool:
        dest = src + delta
        dest_item = self.board[dest]
        success: bool
        if dest_item == None:
            success = True
        elif dest_item == '#':
            success = False
        else:
            success = self.shift_item(dest, delta)

        if success:
            self._dangerous_move_item(src, dest)
        return success
        

    def move_item(self, src: V, dest: V):
        if self.board[dest]:
            return False
        else:
            self._dangerous_move_item(src, dest)
            return True

    def _dangerous_move_item(self, src: V, dest: V):
        board = self.board
        board[dest] = board[src]
        del board[src]

    @staticmethod
    def from_str(s: str) -> Game:
        g = Game()
        map_raw, moves_raw = s.strip().split('\n\n')
        grid_raw = parse_grid(map_raw)
        moves = [c for c in moves_raw if c in '^v<>']
        g.move_queue = moves
        for i_row, i_col, value in nested_items(grid_raw):
            if value != '.':
                g.board[V(i_row, i_col)] = value
            
        return g
    
@dataclass
class Entity():
    type: str = ''
    rect: R = R()

    def move(self, delta: V):
        self.rect = self.rect.move(delta)

    def move_to(self, new_position: V):
        self.rect = R(new_position, self.rect.size)

    def __repr__(self):
        return f"E('{self.type}', {self.rect})"

@dataclass
class GamePart2():
    player: Entity = field(default_factory=Entity)
    walls: List[Entity] = field(default_factory=list)
    boxes: List[Entity] = field(default_factory=list)

    move_queue: List[str] = field(default_factory=list)

    def pushable_items(self, src: Entity, delta: V) -> Generator[Tuple[Entity, V], None, None]:
        dest = src.rect.move(delta)
        
        for wall in self.walls:
            if dest.intersection(wall.rect):
                yield wall, wall.rect.top_left
            
        for box in self.boxes:
            if dest.intersection(box.rect):
                yield box, delta
                yield from self.pushable_items(box, delta)

    def move_player(self, delta: V):
        queue: List[Entity] = [self.player]
        to_move: List[Tuple[Entity, R]] = []
        seen: Set[R] = set()
        
        while queue:
            entity = queue.pop(0)
            dest = entity.rect.move(delta)
            
            to_move.append((entity, dest))

            for wall in self.walls:
                if dest.intersection(wall.rect):
                    return False
            
            for box in self.boxes:
                if dest.intersection(box.rect):
                    if box.rect not in seen:
                        seen.add(box.rect)
                        queue.append(box)
        
        for entity, dest in to_move:
            entity.rect = dest
        
        return True


    def step(self, n = 1):
        n = min(n, len(self.move_queue))
        for _ in range(n):
            move_str = self.move_queue.pop(0)
            self.play_move(move_str)
    
    def play_move(self, move_str: str):
        delta = SHIFTS[move_str]
        self.move_player(delta)

    @property
    def gps_sum(self) -> int:
        return sum( (int(ent.rect.t * 100 + ent.rect.l) for ent in self.boxes))

    @staticmethod
    def from_str(s: str) -> GamePart2:
        g = GamePart2()
        map_raw, moves_raw = s.strip().split('\n\n')
        grid_raw = parse_grid(map_raw)
        moves = [c for c in moves_raw if c in '^v<>']
        g.move_queue = moves
        for i_row, i_col, value in nested_items(grid_raw):
            if value == '.':
                continue
            p = V(i_row, i_col * 2)
            double = V(1,2)
            single = V(1,1)    
            if value == '#':
                g.walls.append(Entity("W", R(p, double)))
            elif value == '@':
                g.player = Entity('P', R(p))
            elif value == "O":
                g.boxes.append(Entity("B", R(p, double)))
            else:
                raise ValueError(f"Unknown value: {value}")
            
        return g
    
    @property
    def board_str(self) -> str:
        
        board_size = max(wall.rect.bottom_right for wall in self.walls) + V(1,1)
        grid: List[List[str]] = create_grid(board_size.x, board_size.y, " ") # type: ignore
        
        for wall in self.walls:
            x, y = [int(a) for a in wall.rect.top_left]
            grid[x][y] = "#"
            grid[x][y+1] = "#"

        for box in self.boxes:
            x, y = [int(a) for a in box.rect.top_left]
            grid[x][y] = "["
            grid[x][y+1] = "]"

        grid[int(self.player.rect.t)][int(self.player.rect.l)] = "@"

        return nested_join(grid, delimiter="")
    


def parse_input(input_raw):
    map_raw, moves_raw = input_raw.strip().split('\n\n')
    grid_raw = parse_grid(map_raw)
    moves = [c for c in moves_raw if c in '^v<>']
    return grid_raw, moves

def part1(input_raw: str):
    game = Game.from_str(input_raw)
    # print(game.board_str + '\n')
    while game.move_queue:
        game.step()
        # print(game.board_str)
        # print(game.gps_sum)
        # print("")
    return game.gps_sum

def part2(input_raw: str):
    game = GamePart2.from_str(input_raw)
    # print(game.board_str + '\n')
    while game.move_queue:
        game.step()
        # print(game.board_str)
        # print(game.gps_sum)
        # print("")
    return game.gps_sum


runner(part1, part2, test_input, input_raw, part1_test_solution, part2_test_solution)