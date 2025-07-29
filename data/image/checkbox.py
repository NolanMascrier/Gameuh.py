"""A checkbox is a box the user can check (duh) which sets the
given SYSTEM variable to True or False."""

from data.constants import SYSTEM, trad
from data.image.image import Image
from data.image.hoverable import Hoverable

class Checkbox():
    """Defines a checkbox.
    
    Args:
        name (str): Name of the box.
        unchecked (Image): Unchecked image of the box.
        checked (Image): Checked image of the box.
        variable (str): Which variable from SYSTEM["options"]\
        to change.
        """
    def __init__(self, name:str, unchecked: Image, checked: Image, variable):
        self._name = name
        self._unchecked = unchecked
        self._checked_image = checked
        self._variable = variable
        self._checked = SYSTEM["options"][variable]
        self._x = 0
        self._y = 0
        self._hover = Hoverable(0, 0, trad('options', name), trad('options_desc', name))

    def set(self, x, y):
        """Sets the box to the x;y positions."""
        self._x = x
        self._y = y
        return self

    def __is_mouse_over(self):
        """Checks whether or not the mouse is within the box."""
        if SYSTEM["mouse"][0] < self._x or SYSTEM["mouse"][0] > self._x + self.width:
            return False
        if SYSTEM["mouse"][1] < self._y or SYSTEM["mouse"][1] > self._y + self.height:
            return False
        return True

    def tick(self):
        """Ticks the box."""
        if SYSTEM["mouse_click"][0] and self.__is_mouse_over():
            if SYSTEM["cooldown"] <= 0:
                SYSTEM["cooldown"] = 0.3
                SYSTEM["options"][self._variable] = not SYSTEM["options"][self._variable]
                self._checked = not self._checked
        return self

    def draw(self, surface = None):
        """Draws the checkbox."""
        if surface is None:
            surface = SYSTEM["windows"]
        self._hover.set(self._x + self.width, self._y + self.height / 2 - self._hover.height / 2)\
            .tick().draw(surface)
        if self._checked:
            SYSTEM["windows"].blit(self._checked_image.image, (self._x, self._y))
        else:
            SYSTEM["windows"].blit(self._unchecked.image, (self._x, self._y))

    @property
    def width(self):
        """Returns the button's width."""
        return min(self._unchecked.width, self._checked_image.width)

    @property
    def height(self):
        """Returns the button's height."""
        return min(self._unchecked.height, self._checked_image.height)

