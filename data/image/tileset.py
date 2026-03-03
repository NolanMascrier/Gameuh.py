"""A tileset is a set of tiles (yeah no shit)"""

from data.image.image import Image

class Tileset():
    """Defines a tileset.
    
    Args:
        base_image (str): URI of the tileset image file.
        frame_x (int): Width of a single tile.
        frame_y (int): Height of a single tile.
    """
    def __init__(self, base_image: str, frame_x: int, frame_y: int):
        self._base_image = Image(base_image)
        self._base_w = self._base_image.width
        self._base_h = self._base_image.height
        self._frame_x = frame_x
        self._frame_y = frame_y
        self._tile = {}
        self._max_x = self._base_image.width // frame_x
        self._max_y = self._base_image.height // frame_y
        for y in range(self._max_y):
            for x in range(self._max_x):
                sub = self._base_image.extracts(x * frame_x, y * frame_y, frame_x, frame_y)
                self._tile[(x, y)] = sub

    def get_at(self, x, y) -> Image | None:
        """Returns the tile at the x;y position."""
        if (x, y) in self._tile:
            return self._tile[(x, y)]
        return None

    def scale(self, width, height) -> "Tileset":
        """Rescales the tileset."""
        self._base_image.scale(self._base_h * height, self._base_w * width)
        self._frame_x = width
        self._frame_y = height
        for tile in self._tile.values():
            tile.scale(self._frame_y, self._frame_x)
        return self

    @property
    def width(self):
        """Returns the tileset's tile width."""
        return self._frame_x

    @property
    def height(self):
        """Returns the tileset's tile height."""
        return self._frame_y
