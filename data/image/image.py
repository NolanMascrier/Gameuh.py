"""Simple wrapper for image surfaces in Pygame."""

import pygame
from data.constants import RESSOURCES

class Image():
    """Defines an image. If the URI does not points
    toward and existing image, it'll load up a default image
    instead.
    
    Args:
        uri (str): URI pointing to the image in /ressources/"""
    def __init__(self, uri = None):
        self._uri = uri
        try:
            self._image = pygame.image.load(f"{RESSOURCES}/{uri}").convert_alpha()
        except FileNotFoundError:
            self._image = pygame.image.load(f"{RESSOURCES}/default.png").convert_alpha()
        self._width = self._image.get_width()
        self._height = self._image.get_height()
        self._visible = True

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
        subsurface = Image(None)
        subsurface.image = self._image.subsurface((x, y, width, height))
        subsurface.width = width
        subsurface.height = height
        return subsurface

    def clone(self):
        """Returns a deep copy of the image."""
        return Image(self._uri)

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
