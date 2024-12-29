from __future__ import annotations

import sys
from pathlib import Path
sys.path.append(str(Path('')))

from functools import cached_property
from typing import Generic, NamedTuple, Optional, TypeVar


from utils.vector import Vector as V

T = TypeVar('T')

class TRBL(NamedTuple, Generic[T]):
    t: T
    r: T
    b: T
    l: T

    def __repr__(self):
        return f"{self.__class__.__name__}({', '.join(x.__repr__() for x in self)})"

class Rectangle(NamedTuple):
    top_left: V = V(0,0)
    size: V = V(1,1)

    @property
    def bottom_right(self):
        return self.top_left + self.size
    
    @property
    def trbl(self):
        t, l = self.top_left
        b, r = self.bottom_right
        return TRBL(t, r, b, l)
    
    @property
    def t(self):
        return self.trbl.t

    @property
    def r(self):
        return self.trbl.r

    @property
    def b(self):
        return self.trbl.b

    @property
    def l(self):
        return self.trbl.l


    def intersection(self, rect: Rectangle) -> Optional[Rectangle]:    

        x = self.trbl
        y = rect.trbl

        t = max(x.t, y.t)
        b = min(x.b, y.b)
        if t >= b: return

        l = max(x.l, y.l)
        r = min(x.r, y.r)
        if l >= r: return

        return Rectangle(V(t, l), V(b - t, r - l))
    

    def move(self, delta: V):
        return Rectangle(self.top_left + delta, self.size)
    
    def __repr__(self):
        return f"R({', '.join(x.__repr__() for x in self)})"


def test_bottomright():
    r = Rectangle(V(1,2), V(10,20))
    assert r.bottom_right == V(11,22)

def test_trbl():
    r = Rectangle(V(1,2), V(10,20))
    assert r.trbl == (1,22,11,2)
    assert r.trbl == (r.t, r.r, r.b, r.l) 

def test_move():
    a = Rectangle(V(2,3), V(1,1))
    delta = V(20,30)
    b = Rectangle(V(22,33), V(1,1))
    assert a.move(delta) == b

def test_intersection():
    a = Rectangle(V(0, 0), V(3,5))
    b = Rectangle(V(1, 2), V(3,5))
    c = Rectangle(V(0,0), V(100, 100))
    i = Rectangle(V(1,2), V(2,3))

    assert a.intersection(b) == i

    assert a.move(V(100,100)).intersection(a) == None
    assert a.intersection(c) == a

    for x, y in [(a,b), (a,c), (b,c),  (a, i)]:
        assert x.intersection(y) == y.intersection(x)
    

if __name__ == "__main__":
    test_bottomright()
    test_intersection()
    test_intersection()