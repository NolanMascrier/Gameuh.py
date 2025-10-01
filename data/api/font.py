"""Wrapper for pygame's fonts."""

import pygame
import pygame.freetype
from data.api.surface import Surface

STYLE_NORMAL    = pygame.freetype.STYLE_DEFAULT
STYLE_STRONG    = pygame.freetype.STYLE_STRONG
STYLE_OBLIQUE   = pygame.freetype.STYLE_OBLIQUE
STYLE_UNDERLINE = pygame.freetype.STYLE_UNDERLINE
STYLE_WIDE      = pygame.freetype.STYLE_WIDE

class Font:
    """Wrapper around pygame.freetype.Font"""
    def __init__(self, file: str, size: int):
        self._font = pygame.freetype.Font(file, size)

    def render(self, text: str, fgcolor=(255, 255, 255), bgcolor=None, style=0):
        """Render text -> returns Surface wrapper and rect"""
        surf, rect = self._font.render(text, fgcolor=fgcolor, bgcolor=bgcolor, style=style)
        return Surface(width=surf.get_width(), height=surf.get_height()).from_existing(surf), rect

    def size(self, text: str):
        """Returns the font's size."""
        return self._font.get_rect(text).size
