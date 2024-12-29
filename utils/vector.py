
from __future__ import annotations
from functools import cached_property
from typing import NamedTuple, Union, overload


Numeric = Union[int, float]

class Vector(NamedTuple):
    x: Numeric
    y: Numeric

    def __repr__(self) -> str:
        return f"V({self.x}, {self.y})"
    
    @cached_property
    def slope(self):
        return self.y / self.x
    
    def __add__(self, b: Vector) -> Vector:
        return Vector(self.x + b.x, self.y + b.y)

    def __sub__(self, b: Vector) -> Vector:
        return Vector(self.x - b.x, self.y - b.y)

    def __mul__(self, b: Numeric) -> Vector:
        return Vector(self.x * b, self.y * b)
    
    def __truediv__(self, b: Numeric) -> Vector:
        return Vector(self.x / b, self.y / b)
    
    @overload
    def __mod__(self, n: Numeric) -> Vector:
        return Vector(self.x % n, self.y % n)

    @overload
    def __mod__(self, b: Vector) -> Vector:
        return Vector(self.x % b.x, self.y % b.y)

    def to_int(self) -> Vector:
        return Vector(int(self.x), int(self.y))

    def piecewise_div(self, b: Vector):
        return self.x / b.x, self.y / b.y

    def is_multiple_of(self, b:Vector):
        x, y = self.piecewise_div(b)
        if x == y and x.is_integer():
            return int(x)
        else:
            return None