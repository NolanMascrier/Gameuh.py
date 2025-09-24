"""A slot is a component that can hold a draggable."""

from collections.abc import Iterable
from data.constants import SYSTEM
from data.image.draggable import Draggable
from data.item import Item
from data.interface.render import render

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
        on_remove(function, optionnal): Function to call when inserting\
        a draggable into the slot while there's already something in here.\
        Defaults to None.
        flags (list, optionnal): List of flags. Used for internal\
        logic. Defaults to [].
        default (Any, optionnal): Default containable of the slot.\
        Defaults to None.
        left (bool, optionnal): Very specific parameter only used for\
        rings slot. Denotes whether or not the slot is for the left hand\
        ring. Defaults to None.
        immutable (bool, optional): Whether or not this slot is immutable.\
        If it is, the user can take the content, but not replace it. Furthermore,\
        taking the content will NOT remove it from the slot. Defualts to `False`.
        accept_only (type|Iterable[type]): Types that can be slotted inside.\
        Defaults to None. If this is set to None, any kind of object can be slotted.
    """
    def __init__(self, x, y, back_image = None, on_slot = None,\
        on_remove = None, on_overwrite = None,\
        flag = None, default = None, left = False, immutable = False,\
        accept_only = None):
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
        self._on_overwrite = on_overwrite
        self._flag = flag
        self._left = left
        self._immutable = immutable
        if isinstance (accept_only, type):
            self._accept_only = accept_only
        elif isinstance (accept_only, Iterable):
            self._accept_only = tuple(accept_only)
        else:
            self._accept_only = None
        if default is not None:
            dr = Draggable(contains=default, immutable=immutable)
            dr.set(self._x, self._y)
            dr.set_parent(self)
            self._contains = dr

    def insert(self, draggable: Draggable):
        """Insert a draggable inside the slot."""
        SYSTEM["dragged"] = None
        if self._contains is not None:
            self.overwrite()
        old = self._contains
        self._contains = draggable
        draggable.dragging = False
        draggable.set(self._x, self._y)
        draggable.set_parent(self)
        if self._on_slot is not None:
            self._on_slot(draggable.contains, self)
        return old

    def overwrite(self):
        """Calls the overwriting function."""
        old = self._contains
        if self._contains is not None:
            self._contains.clear_parent()
        if self._on_overwrite is not None:
            self._on_overwrite(old, self)
        self._contains = None
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
            if self._accept_only is not None and\
                not isinstance(draggable.contains, self._accept_only):
                return False
            if self._immutable:
                draggable.set_panel(None)
                draggable.set_parent(None)
                SYSTEM["dragged"] = None
                return True
            draggable.immutable = self._immutable
            self.insert(draggable)
            return True
        return False

    def set(self, x, y):
        """Sets the slot at the x;y position."""
        self._x = x
        self._y = y
        if self._contains is not None:
            self._contains.set(x, y)
        return self

    def tick(self):
        """tick"""
        if self._contains is not None:
            self._contains.tick().draw()
        if not SYSTEM["mouse_click"][0]:
            self.try_insert(SYSTEM["dragged"])
        return self

    def draw(self):
        """Draws the component on screen."""
        render(self._empty_image.image, (self._x, self._y))
        if self._contains is not None:
            render(self._contains.get_image().image, (self._x, self._y))

    def draw_alt(self, surface, x, y):
        """Draws the component on the surface at specified position."""
        if surface is None or surface == SYSTEM["windows"]:
            if self._contains is not None:
                if isinstance(self._contains.contains, Item):
                    match self._contains.contains.rarity:
                        case 0:
                            render(self._empty_image.image, (x, y))
                        case 1:
                            render(SYSTEM["images"]["slot_magic"].image, (x, y))
                        case 2:
                            render(SYSTEM["images"]["slot_rare"].image, (x, y))
                        case 3:
                            render(SYSTEM["images"]["slot_exalted"].image, (x, y))
                        case 4:
                            render(SYSTEM["images"]["slot_unique"].image, (x, y))
                    if self._contains.contains.gray_out():
                        render(self._contains.contains.get_image().opacity(100).image, (x, y))
                    else:
                        render(self._contains.contains.get_image().opacity(255).image, (x, y))
                else:
                    render(self._contains.contains.icon.get_image(), (x, y))
                    render(SYSTEM["images"]["skill_top"].image, (x, y))
            else:
                render(self._empty_image.image, (x, y))
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
                    case 4:
                        surface.blit(SYSTEM["images"]["slot_unique"].image, (x, y))
                if self._contains.contains.gray_out():
                    surface.blit(self._contains.contains.get_image().opacity(100).image, (x, y))
                else:
                    surface.blit(self._contains.contains.get_image().opacity(255).image, (x, y))
            else:
                surface.blit(self._contains.contains.icon.get_image(), (x, y))
                surface.blit(SYSTEM["images"]["skill_top"].image, (x, y))
        else:
            surface.blit(self._empty_image.image, (x, y))

    @property
    def contains(self):
        """Returns the component's contained draggable."""
        return self._contains

    @contains.setter
    def contains(self, value):
        self._contains = value

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

    @property
    def x(self):
        """Returns the slot x position."""
        return self._x

    @x.setter
    def x(self, value):
        self._x = value

    @property
    def y(self):
        """Returns the slot y position."""
        return self._y

    @y.setter
    def y(self, value):
        self._y = value
