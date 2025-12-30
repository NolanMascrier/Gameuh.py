"""A wrapper for pygame's surfaces."""

import os
import pygame
from pygame.constants import DOUBLEBUF, HWSURFACE
from data.api.widget import Widget

def flip():
    """Wrapper toward pygame's flip."""
    pygame.display.flip()

def mouse_position():
    """Wrapper to pygame's mouse pos."""
    return pygame.mouse.get_pos()

def get_press():
    """Wrapper to pygame's mouse button."""
    return pygame.mouse.get_pressed()

def get_keys():
    """Wrapper to pygame's key event."""
    return pygame.key.get_pressed()

def get_events():
    """Wrapper for pygame's events."""
    return pygame.event.get()

def init_engine():
    """Inits the base engine."""
    os.environ['PYGAME_BLEND_ALPHA_SDL2'] = "1"
    pygame.init()
    pygame.font.init()

def set_screen(is_fullscreen = True, width = 1920, height = 1080, vsync=1):
    """Sets the primary screen for pygame."""
    flags = DOUBLEBUF | HWSURFACE | pygame.SCALED
    if is_fullscreen:
        flags |= pygame.FULLSCREEN
    return pygame.display.set_mode((width, height), flags, vsync=vsync)

class Surface(Widget):
    """Overrides a pygame's surface."""
    __slots__ = '_surface', "_"
    def __init__(self, width: float = 0, height: float = 0, x: float = 0, y: float = 0,\
                 is_alpha = True):
        super().__init__(x, y, width, height)
        self._surface = pygame.Surface((width, height), pygame.SRCALPHA if is_alpha else 0)

    def __getattr__(self, name):
        return getattr(self._surface, name)

    def blit(self, source, dest: tuple[float|float], premult = None):
        """Blits another surface to the current surface's."""
        if premult is None:
            fl = 0
        else:
            fl = pygame.BLEND_PREMULTIPLIED
        if isinstance(source, Surface):
            return self._surface.blit(source.surface, dest, special_flags=fl)
        return self._surface.blit(source, dest, special_flags=fl)

    def fill(self, color, rect=None):
        """Fills the surface with a color."""
        return self._surface.fill(color, rect)

    def get_size(self):
        """Returns the size of the surface."""
        return self._surface.get_size()

    def get_width(self):
        """Return the width of the surface."""
        return self._surface.get_width()

    def get_height(self):
        """Return the height of the surface."""
        return self._surface.get_height()

    def get_rect(self, **kwargs):
        """Returns the rect of the surface."""
        r = self._surface.get_rect(**kwargs)
        return r

    def scroll(self, dx: int, dy: int):
        """Scroll the surface pixels."""
        return self._surface.scroll(dx, dy)

    def blits(self, sources):
        """Batch blit multiple surfaces efficiently."""
        batch = [
            (src.surface if isinstance(src, Surface) else src, dest)
            for src, dest in sources
        ]
        return self._surface.blits(batch)

    def copy(self) -> "Surface":
        """Return a copy of this surface."""
        s = Surface(self.x, self.y, self._width, self._height)
        s.surface = self._surface.copy()
        return s

    def set_alpha(self, value: int | None):
        """Sets the surface's alpha value."""
        return self._surface.set_alpha(value)

    def get_alpha(self) -> int | None:
        """Returns the surface's alpha value."""
        return self._surface.get_alpha()

    def set_colorkey(self, color, flags: int = 0):
        """Sets the surface's colorkey."""
        return self._surface.set_colorkey(color, flags)

    def get_colorkey(self):
        """Sets the surface's colorkey."""
        return self._surface.get_colorkey()

    def get_at(self, pos: tuple[int, int]):
        """Returns the pixel of the given position."""
        return self._surface.get_at(pos)

    def set_at(self, pos: tuple[int, int], color):
        """Sets the pixel at the given position."""
        return self._surface.set_at(pos, color)

    def draw_rect(self, color, rect, width: int = 0):
        """Draw a rect on the surface."""
        return pygame.draw.rect(self._surface, color, rect, width)

    def draw_circle(self, color, center, radius: int, width: int = 0):
        """Draw a cirlce on the surface."""
        return pygame.draw.circle(self._surface, color, center, radius, width)

    def draw_line(self, color, start_pos, end_pos, width: int = 1):
        """Draw a line on the surface."""
        return pygame.draw.line(self._surface, color, start_pos, end_pos, width)

    def draw_ellipse(self, color, rect, width: int = 0):
        """Draw an ellipse on the surface."""
        return pygame.draw.ellipse(self._surface, color, rect, width)

    def draw_polygon(self, color, points, width: int = 0):
        """Draw a polygon on the surface."""
        return pygame.draw.polygon(self._surface, color, points, width)

    def draw_lines(self, color, closed: bool, points, width: int = 1):
        """Draw lines on the surface."""
        return pygame.draw.lines(self._surface, color, closed, points, width)

    def draw_arc(self, color, rect, start_angle, end_angle, width: int = 1):
        """Draw an arc on the surface."""
        return pygame.draw.arc(self._surface, color, rect, start_angle, end_angle, width)

    def scale(self, size: tuple[int, int] | None = None,
              width: int | None = None, height: int | None = None) -> "Surface":
        """Scale this surface to a new size (absolute)."""
        if size is not None:
            w, h = size
        else:
            w = width if width is not None else self._surface.get_width()
            h = height if height is not None else self._surface.get_height()
        if w == self.get_width() and h == self.get_height():
            return self
        self._surface = pygame.transform.scale(self._surface, (w, h))
        self._width, self._height = w, h
        return self

    def smoothscale(self, size: tuple[int, int] | None = None,
              width: int | None = None, height: int | None = None) -> "Surface":
        """Scale this surface to a new size (absolute)."""
        if size is not None:
            w, h = size
        else:
            w = width if width is not None else self._surface.get_width()
            h = height if height is not None else self._surface.get_height()
        if w == self.get_width() and h == self.get_height():
            return self
        self._surface = pygame.transform.smoothscale(self._surface, (w, h))
        self._width, self._height = w, h
        return self

    def rotate(self, angle: float) -> "Surface":
        """Rotate the surface and update width/height."""
        self._surface = pygame.transform.rotate(self._surface, angle)
        self._width, self._height = self._surface.get_size()
        return self

    def flip(self, flip_x: bool, flip_y: bool) -> "Surface":
        """Flip the surface horizontally/vertically."""
        self._surface = pygame.transform.flip(self._surface, flip_x, flip_y)
        return self

    def subsurface(self, rect: tuple[int, int, int, int]) -> "Surface":
        """Return a new Surface that references a portion of this one."""
        sub = self._surface.subsurface(rect)
        x, y, w, h = rect
        surf = Surface(x, y, w, h)
        surf.surface = sub
        return surf

    @classmethod
    def from_existing(cls, existing: pygame.Surface):
        """Wrap an existing pygame.Surface inside our Surface"""
        obj = cls(existing.get_width(), existing.get_height())
        obj._surface = existing
        return obj

    @classmethod
    def load(cls, filename: str) -> "Surface":
        """Loads a file as a surface."""
        img = pygame.image.load(filename).convert_alpha()
        w, h = img.get_size()
        surf = Surface(0, 0, w, h)
        surf._surface = img
        return surf

    def save(self, filename: str):
        """Saves a surface as an image."""
        return pygame.image.save(self._surface, filename)

    @property
    def surface(self) -> pygame.Surface:
        """Returns the surface's surface."""
        return self._surface

    @surface.setter
    def surface(self, sfc):
        self._surface = sfc
