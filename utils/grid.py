
from __future__ import annotations
from collections.abc import Iterator
from dataclasses import dataclass
from typing import Any, Callable, List, Optional, Tuple, TypeVar, Union

T = TypeVar('T')
U = TypeVar('U')

class Foo():

    def __getitem__(self, *args, **kwargs):
        print("index access")
        print(F"{self=}, {args=}, {kwargs=}")


@dataclass()
class Grid():
    rows: List

    def __init__(self, l):
        self.__setattr__('rows', l)

    def __getitem__(self, indeces):
        print(f"{indeces=} (type={type(indeces)})")
        # return
        if type(indeces) == int:
            return self.rows[indeces]
        if len(indeces) == 2:
            return self.rows[indeces[0]][indeces[1]]
        
    def __setitem__(self, indeces: Union[int, Tuple[int, int]], value):
        if type(indeces) == int:
            self.rows[indeces] = value
        if type(indeces) == tuple:
            self.rows[indeces[0]][indeces[1]] = value
        
    def items(self):
        for i_row, row in self.rows:
            for i_col, value in row:
                yield value, i_row, i_col

    def foreach(self, fn: Callable[[Any, int, int]]):
        for value, i_row, i_col in self.items():
            fn(value, i_row, i_col)

    def map(self, fn:Callable[[T, int, int], U]) -> Grid[U]:
        n_args = min(3, fn.__code__.co_argcount)
        return Grid([
            [
                fn(*[x, i_row, i_col][:n_args]) for i_col, x in enumerate(row)
            ] for i_row, row in enumerate(self.rows)
        ])


            





    @staticmethod
    def from_string(s: str, delimiter: str = "", line_delimiter: Optional[str] = None) -> Grid:
        
        raw_lines = s.splitlines()
        lines = [line.split(line_delimiter) if line_delimiter else list(line) for line in raw_lines]

        return Grid(lines)


g = Foo()

g[0]
g[0,1]

g = Grid([[1,2,3], [4,5,6]])

print(g[0])
print(g[1,2])

g[1,2] = 88

print(g)
print(g.map(lambda x: str(x)))