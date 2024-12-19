
from typing import Callable, Iterable, List, Optional, TypeVar, Union


T = TypeVar('T')
U = TypeVar('U')
V = TypeVar('V')

def chain(*functions: Callable) -> Callable:
    def the_func(x):
        for f in functions:
            x = f(x)
        return x
        
    return the_func

def lmap(fn: Callable[[U], T], l: Iterable[U]):
    return list(map(fn, l))



def parse_grid(s: str, delimiter = "", line_delimiter = None, transform_fn: Callable[[str], T] = lambda x:x) -> List[List[T]]:
    lines = s.split(line_delimiter) if line_delimiter else s.splitlines()
    parse_line: Callable[[str], List[str]] = lambda line: line.split(delimiter) if delimiter else list(line)
    parsed = lmap(parse_line, lines)
    return nested_map(transform_fn, parsed)

def nested_map(fn: Callable[[Optional[U], Optional[int], Optional[int]], T], nested_list: List[List[U]]) -> List[List[T]]:
    nargs = min(3, fn.__code__.co_argcount)
    return [
        [
            fn(*[x, row, col][:nargs]) for col, x in enumerate(inner_list)
        ] for row, inner_list in enumerate(nested_list)
    ]

def nested_join(g: List[list[T]], delimiter: str = ",", row_separator = '\n', map_fn: Callable[[T], str]  = str):
    rows = [delimiter.join(map_fn(x) for x in row) for row in g]
    return row_separator.join(rows)

def nested_foreach(fn: Callable[[U, int, int], T], grid: List[List[U]]):
    for i_row, row in enumerate(grid):
        for i_col, value in enumerate(row):
            fn(value, i_row, i_col)


def create_grid(nrows, ncols, filler: Union[Callable[[int, int], T], T] = None):
    return [
        [
            filler(row_i, col_i) if callable(filler) else filler for col_i in range(ncols)        
        ]
        for row_i in range(nrows)
    ]


