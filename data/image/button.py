"""A button is an image that can be clicked, and calls an
action when doing so."""

from data.constants import SYSTEM
from data.image.image import Image

class Button(Image):
    def __init__(self, uri = None, action = None, text:str = ""):
        super().__init__(uri)
        self._action = action
        self._x = 0
        self._y = 0
        self._text = text

    def draw(self, surface):
        """Draws the image to the surface."""
        text = SYSTEM["font_crit"].render(self._text, False, (0, 0, 0))
        size = text.get_size()
        surface.blit(self._image, (self._x, self._y))
        center = (self._x + self._width / 2 - size[0] / 2,\
                  self._y + self._height / 2 - size[1] / 2)
        surface.blit(text, center)

    def set(self, x, y):
        """Sets the button to the x;y position."""
        self._x = x
        self._y = y
        return self

    def press(self, mouse_pos):
        """Checks if the mouse is clicking on the button.
        If it is, executes the action."""
        if mouse_pos[0] >= self._x and mouse_pos[0] <= self._x + self._width and\
            mouse_pos[1] >= self._y and mouse_pos[1] <= self._y + self._height:
            self._action()

    @property
    def x(self):
        """Returns the button's x position."""
        return self._x

    @x.setter
    def x(self, value):
        self._x = value

    @property
    def y(self):
        """Returns the button's y position."""
        return self._y

    @y.setter
    def y(self, value):
        self._y = value

    @property
    def action(self):
        """Returns the action."""
        return self._action

    @action.setter
    def action(self, value):
        self._action = value
