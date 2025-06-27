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
            self._text = SYSTEM["font_detail"].render(f'{text}', False, color)
        if text is not None:
            self._hoverable = Text('\n'.join(hoverable_text), font="font_detail")
        self._attach = surface
        self._override = override
        self._alternative = alternative

    def set(self, x, y):
        """Sets the x;y position of the hoverable."""
        self._x = x
        self._y = y
        return self

    def tick(self):
        """Checks whether or not the mouse is within the hoverable's\
        area, and displays the text if it does."""
        if self._text is not None:
            txt = self._text.get_size()
        elif self._attach is not None:
            txt = self._attach.get_size()
        else:
            return
        if SYSTEM["mouse"][0] >= self._x and SYSTEM["mouse"][0] <= self._x + txt[0] and\
            SYSTEM["mouse"][1] >= self._y and SYSTEM["mouse"][1] <= self._y + txt[1]:
            if self._override is None:
                w = self._hoverable.width
                h = self._hoverable.height
                sfc = pygame.Surface((w + 15, h + 15), pygame.SRCALPHA)
                surface = SYSTEM["images"]["hoverable"].clone().scale(h + 15,\
                                                                    w + 15).image
                sfc.blit(surface, (0, 0))
                sfc.blit(self._hoverable.surface, (7, 7))
                if SYSTEM["mouse"][0] - w < 0:
                    w += SYSTEM["mouse"][0] - w
            else:
                if SYSTEM["keys"][K_LALT]:
                    sfc = self._alternative
                else:
                    sfc = self._override
                w = sfc.get_width()
                h = sfc.get_height()
            SYSTEM["pop_up"] = (sfc, w, h)

    def draw(self, surface):
        """Draws the text to the window."""
        surface.blit(self._text, (self._x, self._y))
