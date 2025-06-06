"""Defines a spatial grid, an optimisation technique for\
handling many hitboxes on the screen. Rather than simply\
comparing all hitboxes one by one, it'll only compare those\
in neighbouring cells on the grid."""

from collections import defaultdict

class SpatialGrid:
    """Defines a spatial grid.
    
    Args:
        cell_size(int, optionnal): The size of a single cell.\
        Defaults to 64.
    """
    def __init__(self, cell_size:int =64):
        self._cell_size = cell_size
        self._grid = defaultdict()

    def _get_cells(self, hitbox):
        """Yields the cells."""
        l = int(hitbox.left // self._cell_size)
        r = int(hitbox.right // self._cell_size)
        t = int(hitbox.top // self._cell_size)
        b = int(hitbox.bottom // self._cell_size)
        for x in range(l, r + 1):
            for y in range(t, b + 1):
                yield (x, y)

    def clear(self):
        """Empties the grid."""
        self._grid.clear()

    def add(self, obj, hitbox):
        """Adds the object in the grid by its hitbox."""
        for cell in self._get_cells(hitbox):
            self._grid.setdefault(cell, []).append(obj)

    def query(self, hitbox):
        """Returns the neighboring objects."""
        seen = set()
        for cell in self._get_cells(hitbox):
            for obj in self._grid.get(cell, []):
                if obj not in seen:
                    seen.add(obj)
                    yield obj
