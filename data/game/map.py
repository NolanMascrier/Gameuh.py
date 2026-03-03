"""A game map can contains obstacle. It replaces parallaxes as the levels background."""

from data.constants import SCREEN_HEIGHT, SCREEN_WIDTH

from data.api.surface import Surface
from data.image.tileset import Tileset

class Map():
    """Defines a map.
    
    Args:
        tileset (Tileset): Which tileset to use for the map.
        width (int): Amount of horizontal tiles in the map.
        height (int): Amount of vertical tiles in the map.
    """
    __slots__ = ('_tileset', '_width', '_height', '_max_x', '_max_y', '_surface', '_camera_x',
                 '_camera_y', "_cached_cuts")
    def __init__(self, tileset: Tileset, width: int, height: int):
        self._tileset = tileset
        self._width = width
        self._height = height
        self._max_x = tileset.width * width
        self._max_y = tileset.height * height
        self._surface = Surface(self._max_x, self._max_y)
        self._camera_x = 0
        self._camera_y = 0
        self._cached_cuts = {}
        for y in range(height):
            for x in range(width):
                tile = tileset.get_at(0, 0) #TODO: Replace with a real map generation algorithm ...
                if tile is not None:
                    self._surface.blit(tile.image, (tileset.width * x, tileset.height * y))

    def draw(self, x, y) -> Surface:
        """Draws the map using the x.y pos as a camera."""
        if (x, y) not in self._cached_cuts:
            w = SCREEN_WIDTH
            h = SCREEN_HEIGHT
            x = min(max(0, x - w // 2), self._max_x - SCREEN_WIDTH)
            y = min(max(0, y - h // 2), self._max_y - SCREEN_HEIGHT)
            self._camera_x = x
            self._camera_y = y
            self._cached_cuts[(x, y)] = self._surface.subsurface((x, y, w, h))
        return self._cached_cuts[(x, y)]

    @property
    def camera_offset(self):
        """Returns the current camera offset (world position of top-left corner of screen)."""
        return (self._camera_x, self._camera_y)

    @property
    def width(self):
        """Returns the map's width."""
        return self._max_x

    @property
    def height(self):
        """Returns the map's height."""
        return self._max_y
