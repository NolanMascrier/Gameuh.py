"""To render text with more options than basic pygame"""

import re
from functools import lru_cache
import pygame
from data.constants import RESSOURCES
from data.interface.render import render

MARKER_REGEX = re.compile(r"#([a-z])#\((.*?)\)")

@lru_cache(maxsize=16)
def open_font(font, size):
    """Opens up the font file."""
    return pygame.freetype.Font(font, size)

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
                size = 20, bold = False, italic = False,\
                default_color = (255, 255, 255), line_wrap=False):
        style = {"color": default_color, "size": size, "bold": bold,\
                 "italic": italic, "font": font}
        if text is None:
            text = ""
        self._data = []
        self._surfaces = []
        self._styles = []
        self._centered = centered
        self._surface = None
        self._width = 0
        self._height = 0
        self._font = open_font(f'{RESSOURCES}/fonts/{font}.ttf', size)
        if isinstance(text, str):
            data = text.split('\n')
        else:
            data = text
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
                    case 'f':
                        style_buff["font"] = value
                pos = end
            if force_x > 0 and line_wrap:
                wrapped_lines = []
                current_line = []
                current_width = 0
                for style_buff, text_buff in styled_line:
                    words = re.split(r'(\s+)', text_buff)
                    font_buff = open_font(f'{RESSOURCES}/fonts/{style_buff["font"]}.ttf',
                                        style_buff["size"])
                    for word in words:
                        if word == "":
                            continue
                        sfc, _ = font_buff.render(word, fgcolor=style_buff["color"])
                        word_width = sfc.get_rect().width
                        if current_line and current_width + word_width > force_x:
                            wrapped_lines.append(current_line)
                            current_line = []
                            current_width = 0
                        current_line.append((style_buff.copy(), word))
                        current_width += word_width + 3
                if current_line:
                    wrapped_lines.append(current_line)

                self._data.extend(wrapped_lines)
            else:
                if styled_line:
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
                font_buff = open_font(f'{RESSOURCES}/fonts/{style_buff["font"]}.ttf',\
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
            self._height = force_y
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
        render(self._surface, (x, y))

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
