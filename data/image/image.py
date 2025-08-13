"""Simple wrapper for image surfaces in Pygame."""

from collections import Counter
from functools import lru_cache
import pygame
from data.constants import RESSOURCES

def load(path):
    """Loads an image through pygame, then attempts to detect its alpha key.
    Then converts the image with its needed method (convert, convert with colorkey,
    convert alpha) depending on the picture."""
    img = pygame.image.load(path)
    if img.get_alpha() is None and not img.get_masks()[3]:
        return img.convert()
    img = img.convert_alpha()
    w, h = img.get_size()
    transparent_colors = Counter()
    opaque_colors = set()
    has_partial_alpha = False
    for y in range(h):
        for x in range(w):
            r, g, b, a = img.get_at((x, y))
            if a == 0:
                transparent_colors[(r, g, b)] += 1
            elif a == 255:
                opaque_colors.add((r, g, b))
            else:
                has_partial_alpha = True
    if has_partial_alpha or not transparent_colors:
        return img.convert_alpha()
    colorkey = transparent_colors.most_common(1)[0][0]
    if colorkey not in opaque_colors:
        img_no_alpha = img.convert()
        img_no_alpha.set_colorkey(colorkey)
        return img_no_alpha
    return img.convert_alpha()

class Image():
    """Defines an image. If the URI does not points
    toward and existing image, it'll load up a default image
    instead.
    
    Args:
        uri (str): URI pointing to the image in /ressources/"""
    def __init__(self, uri = None):
        self._uri = uri
        if uri is None:
            self._image = None
            self._uri = None
            self._width = 0
            self._height = 0
        elif isinstance(uri, Image):
            self._image = uri.clone().image
            self._uri = uri.uri
            self._width = self._image.get_width()
            self._height = self._image.get_height()
        else:
            try:
                self._image = load(f"{RESSOURCES}/{uri}")
            except FileNotFoundError:
                print(f"Couldn't find file {uri}. Using default image.")
                self._uri = "default.png"
                self._image = load(f"{RESSOURCES}/default.png")
            self._width = self._image.get_width()
            self._height = self._image.get_height()
        self._visible = True

    def get_image(self) -> pygame.Surface:
        """Returns the image."""
        return self.image

    def rotate(self, deg: float):
        """Rotates the image.
        
        Args:
            deg (float): degrees to rotate the image.
        """
        self._image = pygame.transform.rotate(self._image, deg)
        self._width = self._image.get_width()
        self._height = self._image.get_height()
        return self

    def scale(self, height: float, width: float):
        """Scales up or down the image.
        
        Args:
            height (float): New height of the image.
            width (float): New width of the image
        """
        self._image = pygame.transform.scale(self._image, (width, height))
        self._width = self._image.get_width()
        self._height = self._image.get_height()
        return self

    def flip(self, vertical: bool, horizontal: bool):
        """Flips the image.
        
        Args:
            vertical (bool): Flip the image on the y axis.
            horizontal (bool): Flip the image on the x axis.
        """
        self._image = pygame.transform.flip(self._image, horizontal, vertical)
        self._width = self._image.get_width()
        self._height = self._image.get_height()
        return self

    def extracts(self, x, y, width, height):
        """Extracts and return a subimage from the image.
        
        Args:
            x (int): x coordinate of the start of the subimage.
            y (int): y coordinate of the start of the subimage.
            width (int): width of the subimage.
            height (int): height of the subimage.
        """
        subsurface = Image()
        subsurface.image = self._image.subsurface((x, y, width, height))
        subsurface.width = width
        subsurface.height = height
        return subsurface

    def opacity(self, opacity:int):
        """Sets the opacity of the image."""
        opacity = max(opacity, 0)
        opacity = min(opacity, 255)
        if self._image.get_alpha() != opacity:
            self._image.set_alpha(opacity)
        return self

    @lru_cache(maxsize=32)
    def clone(self):
        """Returns a deep copy of the image."""
        new = Image.__new__(Image)
        new.uri = self._uri
        new.image = self._image.copy()
        new.width, new._height = self._width, self._height
        new.visible = self._visible
        return new

    @property
    def image(self) -> pygame.Surface:
        """Returns the image surface."""
        return self._image

    @image.setter
    def image(self, value):
        self._image = value

    @property
    def width(self):
        """Returns the image's width."""
        return self._width

    @width.setter
    def width(self, value):
        self._width = value

    @property
    def height(self):
        """Returns the image's height."""
        return self._height

    @height.setter
    def height(self, value):
        self._height = value

    @property
    def visible(self) -> bool:
        """Returns whether or not the image should
        be drawn."""
        return self._visible

    @visible.setter
    def visible(self, value):
        self._visible = value

    @property
    def uri(self):
        """Returns the image's uri."""
        return self._uri

    @uri.setter
    def uri(self, value):
        self._uri = value
