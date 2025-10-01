"""2D Vector class to replace pygame's."""

import numpy as np

class Vec2:
    """Replace a pygame 2D vector."""
    __slots__ = ("arr",)

    def __init__(self, x=0.0, y=0.0):
        if isinstance(x, tuple):
            self.arr = np.array([float(x[0]), float(x[1])], dtype=np.float32)
        else:
            self.arr = np.array([float(x), float(y)], dtype=np.float32)

    @property
    def x(self):
        """Returns the vector's x value."""
        return round(float(self.arr[0]), 4)

    @property
    def y(self):
        """Returns the vector's x value."""
        return round(float(self.arr[1]), 4)

    @x.setter
    def x(self, v):
        self.arr[0] = v

    @y.setter
    def y(self, v):
        self.arr[1] = v

    def __add__(self, other):
        return Vec2(*(self.arr + other.arr))

    def __sub__(self, other):
        return Vec2(*(self.arr - other.arr))

    def __mul__(self, scalar):
        return Vec2(*(self.arr * scalar))

    def __truediv__(self, scalar):
        return Vec2(*(self.arr / scalar))

    def __getitem__(self, key):
        return float(self.arr[key])

    def length(self):
        """Returns the vector's length."""
        return float(np.linalg.norm(self.arr))

    def normalize(self):
        """Return the normalized vector."""
        norm = self.length()
        return self if norm == 0 else Vec2(*(self.arr / norm))

    def copy(self):
        """Returns a copy of the vector."""
        return Vec2(*self.arr)

    def to_tuple(self):
        """Returns the vector's as a tuple."""
        return (self.x, self.y)

    def __repr__(self):
        return f"Vec2({self.x:.2f}, {self.y:.2f})"
