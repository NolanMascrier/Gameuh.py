"""An hoverable is a pop up that shows text when
the mouse is above it."""

import pygame
from data.constants import SYSTEM

class Hoverable():
    """Defines an hoverable."""
    def __init__(self, x:int, y:int, text:str, hoverable_text:str, color=(255, 255, 255)):
        self._x = x
        self._y = y
        self._text = SYSTEM["font_detail"].render(f'{text}', False, color)
        self._hoverable = [SYSTEM["font_detail_small"].render(f'{t}', False, color)\
                           for t in hoverable_text]

    def tick(self):
        """Checks whether or not the mouse is within the hoverable's\
        area, and displays the text if it does."""
        txt = self._text.get_size()
        if SYSTEM["mouse"][0] >= self._x and SYSTEM["mouse"][0] <= self._x + txt[0] and\
            SYSTEM["mouse"][1] >= self._y and SYSTEM["mouse"][1] <= self._y + txt[1]:
            w = 0
            h = 0
            for text in self._hoverable:
                w = max(w, text.get_size()[0])
                h = text.get_size()[1] + 26
            sfc = pygame.Surface((w + 15, h + 15))
            surface = SYSTEM["images"]["hoverable"].clone().scale(h + 15,\
                                                                  w + 15).image
            sfc.blit(surface, (0, 0))
            for i, text in enumerate(self._hoverable):
                sfc.blit(text, (7, 14 * i + 7))
            SYSTEM["windows"].blit(sfc, (SYSTEM["mouse"][0] - w - 15,\
                                         SYSTEM["mouse"][1]))

    def draw(self, surface):
        """Draws the text to the window."""
        surface.blit(self._text, (self._x, self._y))
