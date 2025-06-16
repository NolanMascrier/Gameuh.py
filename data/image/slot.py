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
        draggable.set_parent(self)
        SYSTEM["dragged"] = None
        return old

    def remove(self):
        """Removes the current draggable."""
        old = self._contains
        if self._contains is not None:
            self._contains.clear_parent()
        self._contains = None
        return old

    def is_hovered(self):
        """Checks whether or not the component is hovered."""
        mx, my = SYSTEM["mouse"]
        return (self._x <= mx <= self._x + self._size[0] and
                self._y <= my <= self._y + self._size[1])

    def try_insert(self, draggable: Draggable):
        """Attempts to insert draggable if it's dropped on the slot."""
        if draggable is None:
            return False
        if self.is_hovered():
            self.insert(draggable)
            return True
        return False

    def tick(self):
        """tick"""
        if not SYSTEM["mouse_click"][0]:
            self.try_insert(SYSTEM["dragged"])
        return self

    def draw(self):
        """Draws the component on screen."""
        SYSTEM["windows"].blit(self._empty_image.image, (self._x, self._y))
        if self._contains is not None:
            SYSTEM["windows"].blit(self._contains.image, (self._x, self._y))

    def draw_alt(self, surface, x, y):
        """Draws the component on the surface at specified position."""
        surface.blit(self._empty_image.image, (x, y))
        if self._contains is not None:
            surface.blit(self._contains.image, (x, y))

    @property
    def contains(self):
        """Returns the component's contained draggable."""
        return self._contains

    @property
    def empty(self):
        """Returns whether or not the slot contains something."""
        return self._contains is None

    @property
    def height(self):
        """Returns the background's height."""
        return self._empty_image.height

    @property
    def width(self):
        """Returns the background's width."""
        return self._empty_image.width
