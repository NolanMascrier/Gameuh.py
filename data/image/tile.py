"""A tile is a special type of image.
Rather than stretching the original image, a tile
will section the image in 9 and will repeat those sections
as needed."""

from functools import lru_cache

from data.api.surface import Surface

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
    def __init__(self, uri=None, width = 5, height = 5, scale_factor:int = 1):
        super().__init__(uri)
        self.scale(72 * scale_factor, 72 * scale_factor)
        self._tile_width = self._width // 3
        self._tile_height = self._height // 3
        self._render_height = height * self._tile_height
        self._render_width = width * self._tile_width
        self._lin = self._render_height // self._tile_height
        self._col = self._render_width // self._tile_width
        self._tiles = [
            [
                self.extracts(0, 0, self._tile_width, self._tile_height),
                self.extracts(self._tile_width, 0, self._tile_width,\
                                            self._tile_height),
                self.extracts(self._tile_width * 2, 0,\
                                            self._tile_width, self._tile_height),
            ],
            [
                self.extracts(0, self._tile_height,\
                                            self._tile_width, self._tile_height),
                self.extracts(self._tile_width, self._tile_height,\
                                            self._tile_width, self._tile_height),
                self.extracts(self._tile_width * 2, self._tile_height,\
                                            self._tile_width, self._tile_height),
            ],
            [
                self.extracts(0, self._tile_height * 2,\
                                            self._tile_width, self._tile_height),
                self.extracts(self._tile_width, self._tile_height * 2,\
                                            self._tile_width, self._tile_height),
                self.extracts(self._tile_width * 2, self._tile_height * 2,\
                                            self._tile_width, self._tile_height),
            ]
        ]
        self._image = self.create_image()
        self._width = self._render_width
        self._height = self._render_height
        self._scale_factor = scale_factor

    @lru_cache(maxsize=32)
    def duplicate(self, width, height):
        """Duplicate the tile."""
        w = width // self._tile_width + 1
        h = height // self._tile_height + 1
        return self.create_image(w, h)

    def create_image(self, w = None, h = None) -> Surface:
        """Generates the surface."""
        if w is None:
            w = self._col
        if h is None:
            h = self._lin
        rw = self._tile_width * w
        rh = self._tile_height * h
        sfc = Surface(rw, rh)
        for y in range(0, h):
            for x in range(0, w):
                y_sel = min(1, y) if y < h - 1 else 2
                x_sel = min(1, x) if x < w - 1 else 2
                sfc.blit(self._tiles[y_sel][x_sel].image,\
                        (x * self._tile_width, y * self._tile_height), True)
        return sfc

    def get_image(self):
        return self._image
