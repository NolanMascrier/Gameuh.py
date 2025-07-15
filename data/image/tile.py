"""A tile is a special type of image.
Rather than stretching the original image, a tile
will section the image in 9 and will repeat those sections
as needed."""

import pygame
from data.image.image import Image

class Tile(Image):
    """Creates a tiled image, an image that repeats subsections
    rather than stretch the original image.
    
    For optimal result, use an image of a size divisible by 3
    and a multiple of 64 (ie 192) since 64 is the default size
    of "tiles" for this game (slots for items and spells)
    
    Args:
        uri (str, optional): URI of the image to open. Defaults\
        to None (default image).
        width (int, optional): How many times should the tile be\
        repeated x-wise. Defaults to 5.
        height (int, optional): How many times should the tile be\
        repeated y-wise. Defaults to 5.
    """
    def __init__(self, uri=None, width = 5, height = 5):
        super().__init__(uri)
        self.scale(192, 192)
        self._tile_width = self._width // 3
        self._tile_height = self._height // 3
        self._render_height = height * self._tile_height
        self._render_width = width * self._tile_width
        self._lin = self._render_height // self._tile_height
        self._col = self._render_width // self._tile_width
        self._tiles = {
            0 : {
                0: self.extracts(0, 0, self._tile_width, self._tile_height),
                1: self.extracts(self._tile_width, 0, self._tile_width,\
                                            self._tile_height),
                self._col - 1: self.extracts(self._tile_width * 2, 0,\
                                            self._tile_width, self._tile_height),    
            },
            1: {
                0: self.extracts(0, self._tile_height,\
                                            self._tile_width, self._tile_height),
                1: self.extracts(self._tile_width, self._tile_height,\
                                            self._tile_width, self._tile_height),
                self._col - 1: self.extracts(self._tile_width * 2, self._tile_height,\
                                            self._tile_width, self._tile_height),    
            },
            self._lin - 1: {
                0: self.extracts(0, self._tile_height * 2,\
                                            self._tile_width, self._tile_height),
                1:  self.extracts(self._tile_width, self._tile_height * 2,\
                                            self._tile_width, self._tile_height),
                self._col - 1: self.extracts(self._tile_width * 2, self._tile_height * 2,\
                                            self._tile_width, self._tile_height),    
            }
        }
        self._image = self.create_image()
        self._width = self._render_width
        self._height = self._render_height

    def redraw(self, width, height):
        """Resize the tile."""
        self._tile_width = self._width // 3
        self._tile_height = self._height // 3
        self._render_height = height * self._tile_height
        self._render_width = width * self._tile_width
        self._lin = self._render_height // self._tile_height
        self._col = self._render_width // self._tile_width
        self._tiles = {
            0 : {
                0: self.extracts(0, 0, self._tile_width, self._tile_height),
                1: self.extracts(self._tile_width, 0, self._tile_width,\
                                            self._tile_height),
                self._col - 1: self.extracts(self._tile_width * 2, 0,\
                                            self._tile_width, self._tile_height),    
            },
            1: {
                0: self.extracts(0, self._tile_height,\
                                            self._tile_width, self._tile_height),
                1: self.extracts(self._tile_width, self._tile_height,\
                                            self._tile_width, self._tile_height),
                self._col - 1: self.extracts(self._tile_width * 2, self._tile_height,\
                                            self._tile_width, self._tile_height),    
            },
            self._lin - 1: {
                0: self.extracts(0, self._tile_height * 2,\
                                            self._tile_width, self._tile_height),
                1:  self.extracts(self._tile_width, self._tile_height * 2,\
                                            self._tile_width, self._tile_height),
                self._col - 1: self.extracts(self._tile_width * 2, self._tile_height * 2,\
                                            self._tile_width, self._tile_height),    
            }
        }
        self._image = self.create_image()
        self._width = self._render_width
        self._height = self._render_height
        return self

    def create_image(self) -> pygame.Surface:
        """Generates the surface."""
        sfc = pygame.Surface((self._render_width, self._render_height), pygame.SRCALPHA)
        for y in range(0, self._lin):
            for x in range(0, self._col):
                if y not in self._tiles:
                    if x not in self._tiles[1]:
                        sfc.blit(self._tiles[1][1].image,\
                                    (x * self._tile_width, y * self._tile_height))
                    else:
                        sfc.blit(self._tiles[1][x].image,\
                                    (x * self._tile_width, y * self._tile_height))
                else:
                    if x not in self._tiles[y]:
                        sfc.blit(self._tiles[y][1].image,\
                                    (x * self._tile_width, y * self._tile_height))
                    else:
                        sfc.blit(self._tiles[y][x].image,\
                                    (x * self._tile_width, y * self._tile_height))
        return sfc

    def get_image(self):
        return self._image
