"""An hoverable is a pop up that shows text when
the mouse is above it."""

import pygame

from data.api.surface import Surface

from data.constants import SYSTEM, K_LALT
from data.image.text import Text
from data.interface.render import render

class Hoverable():
    """Defines an hoverable."""
    def __init__(self, x:int, y:int, text:str, hoverable_text:str, text_color=(255, 255, 255),\
        surface: Surface = None, override: Surface = None,\
        alternative:Surface = None, hover_color=(255,255,255), scrollable = None):
        self._x = x
        self._y = y
        if text is None:
            self._text = None
        else:
            if isinstance(text, str):
                text = [text]
            self._text = Text('\n'.join(text), font="item_desc", default_color=text_color)
        if hoverable_text is not None:
            if isinstance(hoverable_text, str):
                hoverable_text = [hoverable_text]
            self._hoverable = Text('\n'.join(hoverable_text), font="item_desc",\
                                default_color=hover_color)
        else:
            self._hoverable = None
        self._attach = surface
        self._override = override
        self._alternative = alternative
        self._scrollable = scrollable
        self._surface = None
        self.update_surface()

    def set(self, x, y):
        """Sets the x;y position of the hoverable."""
        self._x = x
        self._y = y
        return self

    def update_surface(self):
        """Updates the surface."""
        if self._override is None:
            if self._hoverable is None:
                self._surface = None
                return
            w = self._hoverable.width
            h = self._hoverable.height
            surface = SYSTEM["images"]["hoverable"].duplicate(w + 5, h + 5)
            sfc = Surface(surface.get_width(), surface.get_height())
            sfc.blit(surface, (0, 0))
            sfc.blit(self._hoverable.surface, (7, 7))
            if SYSTEM["mouse"][0] - w < 0:
                w += SYSTEM["mouse"][0] - w
        else:
            if SYSTEM["keys"][K_LALT]:
                sfc = self._alternative
            else:
                sfc = self._override
        self._surface = sfc

    def __is_mouse_over(self):
        """Checks whether or not the mouse is over the hoverable surface."""
        if self._text is not None:
            txt = self._text.width, self._text.height
        elif self._attach is not None:
            txt = self._attach.get_size()
        else:
            return
        if SYSTEM["mouse"][0] >= self._x and SYSTEM["mouse"][0] <= self._x + txt[0] and\
            SYSTEM["mouse"][1] >= self._y and SYSTEM["mouse"][1] <= self._y + txt[1]:
            return True
        return False

    def tick(self):
        """Checks whether or not the mouse is within the hoverable's\
        area, and displays the text if it does."""
        if self.__is_mouse_over():
            if self._override is None:
                sfc = self._surface
            else:
                if SYSTEM["keys"][K_LALT]:
                    sfc = self._alternative
                else:
                    sfc = self._override
            if sfc is None:
                return self
            w = sfc.get_width()
            h = sfc.get_height()
            SYSTEM["pop_up"] = (sfc, w, h)
        return self

    def draw(self, surface = None):
        """Draws the text to the window."""
        if surface is None:
            render(self._text.surface, (self._x, self._y))
            return
        surface.blit(self._text.surface, (self._x, self._y))

    @property
    def height(self):
        """Returns the height of the hoverable surface."""
        if self._attach is not None:
            return self._attach.get_height()
        return self._text.height

    @property
    def width(self):
        """Returns the width of the hoverable surface."""
        if self._attach is not None:
            return self._attach.get_width()
        return self._text.width
