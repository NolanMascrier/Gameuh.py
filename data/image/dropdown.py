"""A dropdown menu is a menu that allows the user to select
a value from the list."""

from data.api.widget import Widget

from data.constants import SYSTEM, trad
from data.image.text import Text
from data.interface.render import render

class DropDownTitle(Widget):
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
        super().__init__()
        self._hover = SYSTEM["images"]["dropdown_menu"].duplicate(width, height)
        self.width = self._hover.get_width()
        self.height = self._hover.get_height()
        self._parent = parent

    def is_mouse_over(self):
        """Checks whether or not the mouse is over the element."""
        if SYSTEM["mouse"][0] < self.x:
            return False
        if SYSTEM["mouse"][0] > self.x + self.width:
            return False
        if SYSTEM["mouse"][1] < self.y:
            return False
        if SYSTEM["mouse"][1] > self.y + self.height:
            return False
        return True

    def tick(self):
        """Ticks down the element."""
        if self.is_mouse_over() and SYSTEM["mouse_click"][0]:
            if SYSTEM["cooldown"] > 0:
                return self
            self._parent.closed = not self._parent.closed
            SYSTEM["cooldown"] = 0.35
        return self

    def set(self, x, y):
        """Sets the element's x;y positions."""
        super().set(x, y)
        return self

    def draw(self, surface = None):
        """Draws the element on the surface."""
        if surface is None or surface == SYSTEM["windows"]:
            render(self._hover, (self.x, self.y))
            render(self._value.image, (self.x + self.width / 2 - self._value.width / 2,\
                self.y + self.height / 2 - self._value.height / 2))
            return
        surface.blit(self._hover, (self.x, self.y), True)
        surface.blit(self._value.image, (self.x + self.width / 2 - self._value.width / 2,\
            self.y + self.height / 2 - self._value.height / 2), True)

class DropDownElement(Widget):
    """Subclass for DropDown elements.
    
    Args:
        index (int): Index of the element within the menu.
        value (Text): Display value.
        width (int): width of the element.
        height (int): height of the element.
        parent (DropDown): Parented menu.
    """
    def __init__(self, index: int, value: Text, width, height, parent):
        super().__init__()
        self._index = index
        self._value = value
        self._hover = SYSTEM["images"]["hoverable"].duplicate(width, height)
        self._default = SYSTEM["images"]["dropdown"].duplicate(width, height)
        self.width = self._hover.get_width()
        self.height = self._hover.get_height()
        self._parent = parent

    def is_mouse_over(self):
        """Checks whether or not the mouse is over the element."""
        if SYSTEM["mouse"][0] < self.x:
            return False
        if SYSTEM["mouse"][0] > self.x + self.width:
            return False
        if SYSTEM["mouse"][1] < self.y:
            return False
        if SYSTEM["mouse"][1] > self.y + self.height:
            return False
        return True

    def tick(self):
        """Ticks down the element."""
        if self.is_mouse_over() and SYSTEM["mouse_click"][0]:
            if SYSTEM["cooldown"] > 0:
                return self
            if self._parent.closed:
                return self
            self._parent.index = self._index
            self._parent.closed = True
            SYSTEM["cooldown"] = 0.35
        return self

    def set(self, x, y):
        """Sets the element's x;y positions."""
        super().set(x, y)
        return self

    def draw(self, surface = None):
        """Draws the element on the surface."""
        if surface is None or surface == SYSTEM["windows"]:
            if self.is_mouse_over():
                render(self._hover, (self.x, self.y))
            else:
                render(self._default, (self.x, self.y))
            render(self._value.image, (self.x + self.width / 2 - self._value.width / 2,\
                self.y + self.height / 2 - self._value.height / 2))
            return
        if self.is_mouse_over():
            surface.blit(self._hover, (self.x, self.y))
        else:
            surface.blit(self._default, (self.x, self.y))
        surface.blit(self._value.image, (self.x + self.width / 2 - self._value.width / 2,\
            self.y + self.height / 2 - self._value.height / 2))

class DropDown(Widget):
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
        super().__init__()
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
        self.width = width
        self.height = height
        self._max_height = max_height
        self._closed = True
        self._surface = []
        for i, text in enumerate(self._values):
            self._surface.append((DropDownElement(i, text, width, max_height, self),\
                DropDownTitle(text, self.width, max_height, self)))

    def is_mouse_over(self):
        """Checks whether the mouse is within the dropdown."""
        if not self._closed:
            return self._surface[self._index][1].is_mouse_over()
        for elmt, _ in self._surface:
            if elmt.is_mouse_over():
                return True
        return False

    def set(self, x, y):
        """Sets the menu position."""
        super().set(x, y)
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
        if SYSTEM["mouse_click"][0] and not self.is_mouse_over():
            self._closed = True
        SYSTEM["options"][self._variable] = self._states[self._index]
        return self

    def draw(self, surface = None):
        """Draws the menu on the surface."""
        if surface is None:
            self._surface[self._index][1].draw()
            for elmt, _ in self._surface:
                if not self._closed:
                    elmt.draw(surface)
            render(self._title.image, (self.x, self.y))
            return
        self._surface[self._index][1].draw(surface)
        for elmt, _ in self._surface:
            if not self._closed:
                elmt.draw(surface)
        surface.blit(self._title.image, (self.x, self.y))

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
