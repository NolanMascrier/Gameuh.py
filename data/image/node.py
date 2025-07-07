"""A node is part of a tree, a special button made for display
inside a scrollable area."""

from data.image.button import Button
from data.constants import SYSTEM

class NodeButton(Button):
    """Allows a button to be displayed inside a scrollable area.
    Works the same as a normal button, but recalculate the position
    of the clickable area factoring in the position of the scrollable."""
    def __init__(self, image, pressed = None, action=None, text = ""):
        super().__init__(image, pressed, action, text)
        self._display_x = 0
        self._display_y = 0

    def mouse_inside(self):
        """Checks whether or not the mouse is inside the scrollable area."""
        if SYSTEM["mouse"][0] < self._x :
            return False
        if SYSTEM["mouse"][0] > self._x + self._width:
            return False
        if SYSTEM["mouse"][1] < self._y:
            return False
        if SYSTEM["mouse"][1] > self._y + self._height:
            return False
        return True
