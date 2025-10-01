"""A checkbox is a box the user can check (duh) which sets the
given SYSTEM variable to True or False."""

from data.api.widget import Widget

from data.constants import SYSTEM, trad
from data.image.image import Image
from data.image.hoverable import Hoverable
from data.interface.render import render

class Checkbox(Widget):
    """Defines a checkbox.
    
    Args:
        name (str): Name of the box.
        unchecked (Image): Unchecked image of the box.
        checked (Image): Checked image of the box.
        variable (str): Which variable from SYSTEM["options"]\
        to change.
        """
    def __init__(self, name:str, unchecked: Image, checked: Image, variable):
        super().__init__()
        self._name = name
        self._image = (unchecked, checked)
        self._variable = variable
        self._checked = SYSTEM["options"][variable]
        self._hover = Hoverable(0, 0, trad('options', name), trad('options_desc', name))
        self.width = min(self._image[0].width, self._image[1].width)
        self.height = min(self._image[0].height, self._image[1].height)

    def set(self, x, y):
        """Sets the box to the x;y positions."""
        super().set(x, y)
        return self

    def __is_mouse_over(self):
        """Checks whether or not the mouse is within the box."""
        if SYSTEM["mouse"][0] < self.x or SYSTEM["mouse"][0] > self.x + self.width:
            return False
        if SYSTEM["mouse"][1] < self.y or SYSTEM["mouse"][1] > self.y + self.height:
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
        if surface is None or surface == SYSTEM["windows"]:
            self._hover.set(self.x + self.width,\
                            self.y + self.height / 2 - self._hover.height / 2)\
                .tick().draw()
            if self._checked:
                render(self._image[1].image, (self.x, self.y))
            else:
                render(self._image[0].image, (self.x, self.y))
            return
        self._hover.set(self.x + self.width, self.y + self.height / 2 - self._hover.height / 2)\
            .tick().draw(surface)
        if self._checked:
            SYSTEM["windows"].blit(self._image[1].image, (self.x, self.y))
        else:
            SYSTEM["windows"].blit(self._image[0].image, (self.x, self.y))
