"""To render text with more options than basic pygame"""

import pygame
from data.constants import SYSTEM, RESSOURCES

class Text():
    """Reads a text in str form to create a pygame surface
    with line breaks and colors. to denote a color, use
    #c#(r, g, b) before a word.
     
    Args:
        text (str): Text to display.
        centered (bool, optional): Whether or not to center the\
        text on the surface. Defaults to False.
        font (str, optional): Which font to use. Defaults to "font_detail_small".
        force_x (int, optional): Overrides the automatic width calculation. Defaults\
        to -1 (disabled).
        force_y (int, optional): Overrides the automatic height calculation. Defaults\
        to -1 (disabled).
    """
    def __init__(self, text: str, centered = False,\
                font = "tiny", force_x = -1, force_y = -1,\
                size = 20, bold = False, italic = False):
        self._data = []
        self._surfaces = []
        self._centered = centered
        self._surface = None
        self._width = 0
        self._height = 0
        self._font = pygame.freetype.Font(f'{RESSOURCES}/fonts/{font}.ttf', size)
        if bold:
            self._font.strong = True
        data = text.split('\n')
        #Creates the list
        buffer = [t.split('#c') for t in data]
        for tab in buffer:
            cell_buffer = []
            for cell in tab:
                if cell[0:2] == "#(":
                    index = cell.find(")")
                    colors = tuple(map(int, cell[2:index].split(",")))
                    value = cell[index + 1:]
                else:
                    colors = (255, 255, 255)
                    value = cell
                cell_buffer.append((colors, value))
            self._data.append(cell_buffer)
        #Generating the surfaces
        for tab in self._data:
            cell_buffer = []
            for cell in tab:
                sfc, _ = self._font.render(\
                    f'{cell[1]}', fgcolor=cell[0])
                cell_buffer.append(sfc)
            self._surfaces.append(cell_buffer)
        self.generate_surface(force_x, force_y)

    def generate_surface(self, force_x, force_y):
        """Creates the text surface."""
        self._height = 0
        self._width = 0
        for tab in self._surfaces:
            w_temp = 0
            self._height += tab[0].get_rect().height + 5
            for cell in tab:
                w_temp += cell.get_rect().width + 3
            self._width = max(self._width, w_temp)
        if force_x > 0:
            self._width = force_x
        if force_y > 0:
            self._width = force_y
        self._surface = pygame.Surface((self._width, self._height), pygame.SRCALPHA)
        y_temp = 0
        for tab in self._surfaces:
            x_temp = 0
            if self._centered:
                x_line = 0
                for cell in tab:
                    x_line += cell.get_rect().width + 3
                x_temp = int((self._width - x_line) / 2)
            for cell in tab:
                self._surface.blit(cell, (x_temp, y_temp))
                x_temp += cell.get_rect().width + 3
            y_temp += tab[0].get_rect().height + 5

    def draw(self, x, y):
        """Renders the text at the x;y position."""
        SYSTEM["windows"].blit(self._surface, (x, y))

    @property
    def width(self):
        """Returns the text's width."""
        return self._width

    @property
    def height(self):
        """Returns the text's height."""
        return self._height

    @property
    def surface(self):
        """Returns the text's surface."""
        return self._surface
