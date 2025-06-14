"""A slot is a component that can hold a draggable."""

from data.constants import SYSTEM
from data.image.draggable import Draggable

class Slot():
    def __init__(self, x, y):
        self._empty_image = SYSTEM["images"]["slot_empty"]
        self._x = x
        self._y = y
        self._size = (self._empty_image.width, self._empty_image.height)
        self._contains = None

    def insert(self, draggable: Draggable):
        """Insert a draggable inside the slot."""
        old = self._contains
        self._contains = draggable
        draggable.set(self._x, self._y)
        if draggable.parent is not None:
            draggable.parent.remove()
        draggable.set_parent(self)
        return old

    def remove(self):
        """Removes the current draggable."""
        old = self._contains
        self._contains = None
        if self._contains is not None:
            self._contains.clear_parent()
        return old

    def is_hovered(self):
        """Checks whether or not the component is hovered."""
        mx, my = SYSTEM["mouse"]
        return (self._x <= mx <= self._x + self._size[0] and
                self._y <= my <= self._y + self._size[1])

    def try_insert(self, draggable: Draggable):
        """Attempts to insert draggable if it's dropped on the slot."""
        if self.is_hovered():
            self.insert(draggable)
            return True
        return False

    def draw(self):
        """Draws the component."""
        if self._contains is not None:
            SYSTEM["windows"].blit(self._contains.image, (self._x, self._y))
        SYSTEM["windows"].blit(self._empty_image.image, (self._x, self._y))
