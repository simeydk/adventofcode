from typing import Tuple, List, DefaultDict
from dataclasses import dataclass, field
from collections import defaultdict
import cached_property from functools


INFINITY = float('inf')

Coordinates = Tuple[int, int]

Path = List['Node']

@dataclass
class Node:
    coords: Coordinates
    risk: int = field(hash=False)
    children: List['Node'] = field(default_factory = list)
    cost: DefaultDict['Node', Tuple['Path', int]] = field(default_factory = lambda: defaultdict(lambda: ([], INFINITY)))

    def __post_init__(self):
        self.cost[self] = ([], 0)

    @cached_property
    def total_risk(self):
        if not self.children: return 0
        return self.risk + min(child.total_risk for child in self.children)

    def __repr__(self) -> str:
        return f'{self.coords}: {self.risk}'

    def __hash__(self) -> int:
        return hash(self.coords)


