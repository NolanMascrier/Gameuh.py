"""An hoverable is a pop up that shows text when
the mouse is above it."""

import pygame
from data.constants import SYSTEM, K_LALT
from data.image.text import Text

class Hoverable():
    """Defines an hoverable."""
    def __init__(self, x:int, y:int, text:str, hoverable_text:str, color=(255, 255, 255),\
        surface: pygame.Surface = None, override: pygame.Surface = None,\
        alternative:pygame.Surface = None):
        self._x = x
        self._y = y
        if text is None:
            self._text = None
        else:
            if isinstance(text, str):
                text = [text]
            self._text = Text('\n'.join(text), font="item_desc")
        if hoverable_text is not None:
            if isinstance(hoverable_text, str):
                hoverable_text = [hoverable_text]
            self._hoverable = Text('\n'.join(hoverable_text), font="item_desc")
        else:
            self._hoverable = None
        self._attach = surface
        self._override = override
        self._alternative = alternative
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
            w = self._hoverable.width
            h = self._hoverable.height
            surface = SYSTEM["images"]["hoverable"].duplicate(w + 5, h + 5)
            sfc = pygame.Surface((surface.get_width(), surface.get_height()), pygame.SRCALPHA)
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

    def tick(self):
        """Checks whether or not the mouse is within the hoverable's\
        area, and displays the text if it does."""
        if self._text is not None:
            txt = self._text.width, self._text.height
        elif self._attach is not None:
            txt = self._attach.get_size()
        else:
            return
        if SYSTEM["mouse"][0] >= self._x and SYSTEM["mouse"][0] <= self._x + txt[0] and\
            SYSTEM["mouse"][1] >= self._y and SYSTEM["mouse"][1] <= self._y + txt[1]:
            if self._override is None:
                sfc = self._surface
            else:
                if SYSTEM["keys"][K_LALT]:
                    sfc = self._alternative
                else:
                    sfc = self._override
            w = sfc.get_width()
            h = sfc.get_height()
            SYSTEM["pop_up"] = (sfc, w, h)
        return self

    def draw(self, surface):
        """Draws the text to the window."""
        surface.blit(self._text.surface, (self._x, self._y))

    @property
    def height(self):
        """Returns the height of the hoverable surface."""
        return self._text.height

    @property
    def width(self):
        """Returns the width of the hoverable surface."""
        return self._text.width
