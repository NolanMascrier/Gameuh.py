"""A button is an image that can be clicked, and calls an
action when doing so."""

import pygame
from data.constants import SYSTEM
from data.image.image import Image
from data.image.text import Text
from data.image.scrollable import Scrollable
from data.interface.render import render

class Button():
    """Defines a button. A button is a clickable image with two states (clicked
    and not clicked), and does an action when clicked."""
    def __init__(self, image:Image, pressed:Image = None, action = None, text:str|Image = "",\
        scrollable_area: Scrollable = None, superimage: pygame.Surface = None):
        if isinstance(image, str):
            image = SYSTEM["images"][image]
        self._image = image
        self._pressed = pressed
        self._clicked = False
        self._action = action
        self._x = 0
        self._y = 0
        self._width = image.width
        self._height = image.height
        self._scrollable = scrollable_area
        self._superimage = superimage
        if text is None:
            self._text = None
        elif isinstance(text, Image):
            self._superimage = text.image
            self._text = None
        else:
            self._text = Text(text, True, "item_desc", force_x=self._width)

    def __mouse_default(self):
        """For mouse_inside() with no scrollable."""
        if SYSTEM["mouse"][0] < self._x :
            return False
        if SYSTEM["mouse"][0] > self._x + self._width:
            return False
        if SYSTEM["mouse"][1] < self._y:
            return False
        if SYSTEM["mouse"][1] > self._y + self._height:
            return False
        return True

    def __mouse_scrollable(self):
        """For mouse_inside() within a scrollable."""
        rect = self._scrollable.coordinates_rectangle(self._x, self._y, self._height, self._width)
        if rect is None:
            return False
        x, y, w, h = rect
        if x == -1 and y == -1:
            return False
        if SYSTEM["mouse"][0] < x :
            return False
        if SYSTEM["mouse"][0] > x + w:
            return False
        if SYSTEM["mouse"][1] < y:
            return False
        if SYSTEM["mouse"][1] > y + h:
            return False
        return True

    def mouse_inside(self):
        """Checks whether or not the mouse is inside the button's area.
        Should the button be inside a scrollable area, it'll check if the
        mouse is within the button's area with the scrollable's diffs."""
        if self._scrollable is not None:
            return self.__mouse_scrollable()
        return self.__mouse_default()

    def draw(self, surface = None):
        """Draws the image to the surface."""
        if surface is None or surface == SYSTEM["windows"]:
            if self._clicked and self._pressed is not None:
                render(self._pressed.image, (self._x, self._y))
            else:
                render(self._image.image, (self._x, self._y))
            if self._text is not None:
                y = self._y + self._text.height / 2
                render(self._text.image, (self._x, y))
            if self._superimage is not None:
                x_offset = self._x + self._width / 2 - self._superimage.get_width() / 2
                y_offset = self._y + self._height / 2 - self._superimage.get_height() / 2
                render(self._superimage, (x_offset, y_offset))
            return
        if self._clicked and self._pressed is not None:
            surface.blit(self._pressed.image, (self._x, self._y))
        else:
            surface.blit(self._image.image, (self._x, self._y))
        if self._text is not None:
            y = self._y + self._text.height / 2
            surface.blit(self._text.image, (self._x, y))
        if self._superimage is not None:
            x_offset = self._x + self._width / 2 - self._superimage.get_width() / 2
            y_offset = self._y + self._height / 2 - self._superimage.get_height() / 2
            surface.blit(self._superimage, (x_offset, y_offset))

    def get_image(self):
        """Returns the current image."""
        return self._image.image

    def set(self, x, y, scrollable: Scrollable = None):
        """Sets the button to the x;y position."""
        self._x = x
        self._y = y
        self._scrollable = scrollable
        return self

    def tick(self):
        """Ticks the button, checking if is pressed."""
        if SYSTEM["mouse_click"][0] and SYSTEM["dragged"] is None:
            self.press()
        else:
            self._clicked = False
        return self

    def press(self):
        """Checks if the mouse is clicking on the button.
        If it is, executes the action."""
        if self.mouse_inside() and self._action is not None:
            if SYSTEM["cooldown"] > 0:
                return
            self._action()
            self._clicked = True
            SYSTEM["cooldown"] = 0.1

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

    @property
    def image(self):
        """Returns the image."""
        if self._pressed and self._pressed is not None:
            return self._pressed
        return self._image

    @property
    def width(self):
        """Returns the buttons' width."""
        return self._width

    @property
    def height(self):
        """Returns the buttons' height."""
        return self._height

