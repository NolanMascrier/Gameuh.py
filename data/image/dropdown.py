"""A dropdown menu is a menu that allows the user to select
a value from the list."""

import pygame
from data.constants import SYSTEM, trad
from data.image.text import Text

class DropDownTitle():
    """Subclass for DropDown title, aka the clickable button to open
    the menu.
    
    Args:
        value (Text): Display value.
        width (int): width of the element.
        height (int): height of the element.
        parent (DropDown): Parented menu.
    """
    def __init__(self, value: Text, width, height, parent):
        self._value = value
        self._x = 0
        self._y = 0
        self._hover = SYSTEM["images"]["dropdown_menu"].duplicate(width, height)
        self._width = self._hover.get_width()
        self._height = self._hover.get_height()
        self._parent = parent

    def __is_mouse_over(self):
        """Checks whether or not the mouse is over the element."""
        if SYSTEM["mouse"][0] < self._x:
            return False
        if SYSTEM["mouse"][0] > self._x + self._width:
            return False
        if SYSTEM["mouse"][1] < self._y:
            return False
        if SYSTEM["mouse"][1] > self._y + self._height:
            return False
        return True

    def tick(self):
        """Ticks down the element."""
        if self.__is_mouse_over() and SYSTEM["mouse_click"][0]:
            self._parent.closed = not self._parent.closed
        elif SYSTEM["mouse_click"][0]:
            self._parent.closed = True
        return self

    def set(self, x, y):
        """Sets the element's x;y positions."""
        self._x = x
        self._y = y
        return self

    def draw(self, surface = None):
        """Draws the element on the surface."""
        if surface is None:
            surface = SYSTEM["windows"]
        surface.blit(self._hover, (self._x, self._y))
        surface.blit(self._value.image, (self._x + self._width / 2 - self._value.width / 2,\
            self._y + self._height / 2 - self._value.height / 2))

    @property
    def width(self):
        """Returns the element's width."""
        return self._width

    @property
    def height(self):
        """Returns the element's height."""
        return self._height

class DropDownElement():
    """Subclass for DropDown elements.
    
    Args:
        index (int): Index of the element within the menu.
        value (Text): Display value.
        width (int): width of the element.
        height (int): height of the element.
        parent (DropDown): Parented menu.
    """
    def __init__(self, index: int, value: Text, width, height, parent):
        self._index = index
        self._value = value
        self._x = 0
        self._y = 0
        self._hover = SYSTEM["images"]["hoverable"].duplicate(width, height)
        self._default = SYSTEM["images"]["dropdown"].duplicate(width, height)
        self._width = self._hover.get_width()
        self._height = self._hover.get_height()
        self._parent = parent

    def __is_mouse_over(self):
        """Checks whether or not the mouse is over the element."""
        if SYSTEM["mouse"][0] < self._x:
            return False
        if SYSTEM["mouse"][0] > self._x + self._width:
            return False
        if SYSTEM["mouse"][1] < self._y:
            return False
        if SYSTEM["mouse"][1] > self._y + self._height:
            return False
        return True

    def tick(self):
        """Ticks down the element."""
        if self.__is_mouse_over() and SYSTEM["mouse_click"][0]:
            self._parent.index = self._index
            self._parent.closed = True
        return self

    def set(self, x, y):
        """Sets the element's x;y positions."""
        self._x = x
        self._y = y
        return self

    def draw(self, surface = None):
        """Draws the element on the surface."""
        if surface is None:
            surface = SYSTEM["windows"]
        if self.__is_mouse_over():
            surface.blit(self._hover, (self._x, self._y))
        else:
            surface.blit(self._default, (self._x, self._y))
        surface.blit(self._value.image, (self._x + self._width / 2 - self._value.width / 2,\
            self._y + self._height / 2 - self._value.height / 2))

    @property
    def width(self):
        """Returns the element's width."""
        return self._width

    @property
    def height(self):
        """Returns the element's height."""
        return self._height

class DropDown():
    """Defines a dropdown.
    
    Args:
        name (str): Name of the dropdown that will be displayed above it.
        values (list): List of displayed values.
        states (list): List of states that will be selected through the menu.
        variable (str): Variable from SYSTEM that will be changed through the dropdown.
        default_index (int, optional): Index of value that should be displayed by default.\
        Defaults to 0.
    """
    def __init__(self, name, values, states, variable, default_index = 0):
        self._name = name
        self._values = []
        self._states = states
        self._variable = variable
        self._index = default_index
        self._title = Text(trad('buttons', name), size=40, font="item_desc")
        width = 0
        height = 0
        max_height = 0
        for v in values:
            t = Text(v, size=40, font="item_desc")
            self._values.append(t)
            width = max(width, t.width)
            max_height = max(max_height, t.height)
            height += t.height
        self._width = width
        self._height = height
        self._max_height = max_height
        self._x = 0
        self._y = 0
        self._closed = True
        self._surface = []
        for i, text in enumerate(self._values):
            self._surface.append((DropDownElement(i, text, width, max_height, self),\
                DropDownTitle(text, self._width, max_height, self)))

    def set(self, x, y):
        """Sets the menu position."""
        self._x = x
        self._y = y
        i = 1
        for elmt, title in self._surface:
            elmt.set(x, y + i * elmt.height + self._title.height)
            title.set(x, y + self._title.height)
            i += 1
        return self

    def tick(self):
        """Ticks down the menu."""
        for elmt, title in self._surface:
            elmt.tick()
            title.tick()
        SYSTEM["options"][self._variable] = self._states[self._index]
        return self

    def draw(self, surface = None):
        """Draws the menu on the surface."""
        if surface is None:
            surface = SYSTEM["windows"]
        self._surface[self._index][1].draw(surface)
        for elmt, _ in self._surface:
            if not self._closed:
                elmt.draw(surface)
        surface.blit(self._title.image, (self._x, self._y))

    @property
    def index(self):
        """Returns the menu's index."""
        return self._index

    @index.setter
    def index(self, value):
        self._index = value

    @property
    def closed(self):
        """Returns whether or not the menu is closed."""
        return self._closed

    @closed.setter
    def closed(self, value):
        self._closed = value
