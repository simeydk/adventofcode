
from __future__ import annotations
from collections.abc import Iterator
from dataclasses import dataclass
from typing import Any, Callable, Generic, List, Optional, Tuple, TypeVar, Union

T = TypeVar('T')
U = TypeVar('U')

class Foo():

    def __getitem__(self, *args, **kwargs):
        print("index access")
        print(F"{self=}, {args=}, {kwargs=}")

T = TypeVar('T')

@dataclass()
class Grid(Generic[T]):
    rows: List[List[T]]

    def __init__(self, l: List[List[T]]):
        self.__setattr__('rows', l)

    def __getitem__(self, indeces: Union[int, Tuple[int, int]]):
        print(f"{indeces=} (type={type(indeces)})")
        # return
        if type(indeces) == int:
            return self.rows[indeces]
        elif type(indeces) == tuple:
            return self.rows[indeces[0]][indeces[1]]
        else:
            raise ValueError(f"index '{indeces}' of Type '{type(indeces)}' is not a valid index entry")
        
    def __setitem__(self, indeces: Union[int, Tuple[int, int]], value):
        if type(indeces) == int:
            self.rows[indeces] = value
        elif type(indeces) == tuple:
            self.rows[indeces[0]][indeces[1]] = value
        else:
            raise ValueError(f"index '{indeces}' of Type '{type(indeces)}' is not a valid index entry")
        
    def items(self):
        for i_row, row in enumerate(self.rows):
            for i_col, value in enumerate(row):
                yield value, i_row, i_col

    def for_each(self, fn: Callable[[T, int, int]]):
        self.map(fn)

    def map(self, fn:Callable[[T, int, int], U]) -> Grid[U]:
        n_args = min(3, fn.__code__.co_argcount)
        return Grid([
            [
                fn(*[x, i_row, i_col][:n_args]) for i_col, x in enumerate(row)
            ] for i_row, row in enumerate(self.rows)
        ])

    @staticmethod
    def from_string(s: str, col_separator: str = "", row_separator: Optional[str] = None) -> Grid:
        
        raw_lines = s.split(row_separator) if row_separator else s.splitlines()
        lines = [line.split(col_separator) if col_separator else list(line) for line in raw_lines]

        return Grid(lines)
    
    @staticmethod
    def create(n_rows: int, n_cols: int, filler: T = None]):
        g = Grid(
            [ 
                [
                    filler if type(filler) == T else  for i_col in range(n_cols)
                ]
                for i_row in range(n_rows)]
        )
