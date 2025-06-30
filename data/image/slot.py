"""A slot is a component that can hold a draggable."""

from data.constants import SYSTEM
from data.image.draggable import Draggable
from data.item import Item
from data.game.spell import Spell

class Slot():
    """Defines a draggable image, an image that can be
    dragged around and inserted into slots.
    
    Args:
        x (int): x position of the component.    
        y (int): y position of the component.
        back_image (str, optionnal): name of the image to\
        use as a background. Needs to be loaded into the system.\
        Defaults to `back_image`.
        on_slot (function, optionnal): Function to call when a draggable\
        has been slotted inside. The function will need to take two\
        arguments, which is the `contains` field of the\
        draggable and the slot. Defaults to None.
        on_remove(function, optionnal): Function to call when the slot\
        is emptied. The function will need to take two\
        arguments, which is the `contains` field of the\
        draggable and the slot. Defaults to None.
        flags (list, optionnal): List of flags. Used for internal\
        logic. Defaults to [].
        default (Any, optionnal): Default containable of the slot.\
        Defaults to None.
        left (bool, optionnal): Very specific parameter only used for\
        rings slot. Denotes whether or not the slot is for the left hand\
        ring. Defaults to None.
    """
    def __init__(self, x, y, back_image = None, on_slot = None,\
        on_remove = None, flag = None, default = None, left = False):
        if back_image is None:
            self._empty_image = SYSTEM["images"]["slot_empty"]
        else:
            self._empty_image = SYSTEM["images"][back_image]
        self._x = x
        self._y = y
        self._size = (self._empty_image.width, self._empty_image.height)
        self._contains = None
        self._on_slot = on_slot
        self._on_remove = on_remove
        self._flag = flag
        self._left = left
        if default is not None:
            dr = Draggable(contains=default)
            dr.set(self._x, self._y)
            dr.set_parent(self)
            self._contains = dr

    def insert(self, draggable: Draggable):
        """Insert a draggable inside the slot."""
        if self._contains is not None:
            self.remove()
        old = self._contains
        self._contains = draggable
        draggable.dragging = False
        draggable.set(self._x, self._y)
        draggable.set_parent(self)
        SYSTEM["dragged"] = None
        if self._on_slot is not None:
            self._on_slot(draggable.contains, self)
        return old

    def remove(self):
        """Removes the current draggable."""
        old = self._contains
        if self._contains is not None:
            self._contains.clear_parent()
        if self._on_remove is not None:
            self._on_remove(old, self)
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
        if self._contains is not None:
            self._contains.tick().draw()
        if not SYSTEM["mouse_click"][0]:
            self.try_insert(SYSTEM["dragged"])
        return self

    def draw(self):
        """Draws the component on screen."""
        SYSTEM["windows"].blit(self._empty_image.image, (self._x, self._y))
        if self._contains is not None:
            SYSTEM["windows"].blit(self._contains.get_image().image, (self._x, self._y))

    def draw_alt(self, surface, x, y):
        """Draws the component on the surface at specified position."""
        if self._contains is not None:
            if isinstance(self._contains.contains, Item):
                match self._contains.contains.rarity:
                    case 0:
                        surface.blit(self._empty_image.image, (x, y))
                    case 1:
                        surface.blit(SYSTEM["images"]["slot_magic"].image, (x, y))
                    case 2:
                        surface.blit(SYSTEM["images"]["slot_rare"].image, (x, y))
                    case 3:
                        surface.blit(SYSTEM["images"]["slot_exalted"].image, (x, y))
                surface.blit(self._contains.contains.get_image().image, (x, y))
            else:
                surface.blit(self._contains.contains.icon.get_image(), (x, y))
                surface.blit(SYSTEM["images"]["skill_top"].image, (x, y))
        else:
            surface.blit(self._empty_image.image, (x, y))

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

    @property
    def flag(self):
        """Returns the slot's flag."""
        return self._flag

    @property
    def left(self):
        """Returns whether or not the slot is marked for\
        the left hand ring."""
        return self._left 
