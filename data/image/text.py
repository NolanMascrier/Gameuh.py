"""To render text with more options than basic pygame"""

import pygame
import re
from data.constants import SYSTEM, RESSOURCES

MARKER_REGEX = re.compile(r"#([a-z])#\((.*?)\)")


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
        style = {"color": (255, 255, 255), "size": size, "bold": bold, "italic": italic}
        self._data = []
        self._surfaces = []
        self._styles = []
        self._centered = centered
        self._surface = None
        self._width = 0
        self._height = 0
        self._font = pygame.freetype.Font(f'{RESSOURCES}/fonts/{font}.ttf', size)
        data = text.split('\n')
        #Creates the list
        for line in data:
            pos = 0
            style_buff = style.copy()
            styled_line = []
            while pos < len(line):
                match = MARKER_REGEX.search(line, pos)
                if match is None:
                    if pos < len(line):
                        styled_line.append((style_buff.copy(), line[pos:]))
                    break
                start, end = match.span()
                if start > pos:
                    styled_line.append((style_buff.copy(), line[pos:start]))
                key, value = match.groups()
                match key:
                    case 'c':
                        style_buff["color"] = tuple(map(int, value.split(',')))
                    case 's':
                        style_buff["size"] = int(value)
                    case 'b':
                        style_buff["bold"] = value == "1"
                    case 'i':
                        style_buff["italic"] = value == "1"
                pos = end
            if len(styled_line) == 0:
                continue
            self._data.append(styled_line)
        #Generating the surfaces
        for tab in self._data:
            cell_buffer = []
            for cell in tab:
                style_buff, text_buff = cell
                flags = 0
                if style["bold"]:
                    flags |= pygame.freetype.STYLE_STRONG
                if style["italic"]:
                    flags |= pygame.freetype.STYLE_OBLIQUE
                font_buff = pygame.freetype.Font(f'{RESSOURCES}/fonts/{font}.ttf',\
                    style_buff["size"])
                sfc, _ = font_buff.render(\
                    f'{text_buff}', fgcolor=style_buff["color"], style=flags)
                cell_buffer.append(sfc)
            self._surfaces.append(cell_buffer)
        self.generate_surface(force_x, force_y)

    def get_size(self):
        """Returns the surface's size"""
        return self._surface.get_size()

    def opacity(self, opacity: int):
        """Sets the opacity of the text."""
        opacity = min(max(opacity, 0), 255)
        self._surface.set_alpha(opacity)

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

    @property
    def image(self):
        """Returns the text's surface."""
        return self._surface
