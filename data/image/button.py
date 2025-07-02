"""A button is an image that can be clicked, and calls an
action when doing so."""

from data.image.image import Image
from data.image.text import Text

class Button():
    """Defines a button. A button is a clickable image with two states (clicked
    and not clicked), and does an action when clicked."""
    def __init__(self, image:Image, pressed:Image = None, action = None, text:str = ""):
        self._image = image
        self._pressed = pressed
        self._clicked = False
        self._action = action
        self._x = 0
        self._y = 0
        self._width = image.width
        self._height = image.height
        self._text = Text(text, True, "font_detail", force_x=self._width)

    def draw(self, surface):
        """Draws the image to the surface."""
        if self._clicked and self._pressed is not None:
            surface.blit(self._pressed.image, (self._x, self._y))
        else:
            surface.blit(self._image.image, (self._x, self._y))
        y = self._y + self._text.height / 2
        surface.blit(self._text.surface, (self._x, y))

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
            self._clicked = True
        else:
            self._clicked = False

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
