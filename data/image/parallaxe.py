"""Class for parallaxes. Parallaxes
are scrolling background images."""

from data.api.surface import Surface

from data.constants import SCREEN_HEIGHT, SCREEN_WIDTH, SYSTEM
from data.image.animation import Animation
from data.interface.render import renders

class Parallaxe(Animation):
    """Defines a parallaxe.
    
    Args:
        uri(str|Image) : Which image to use as a base.
        frame_x (int): width of a single frame of the sequence.
        frame_y (int): height of a single frame of the sequence.
        scroll_left (bool, optionnal): Whether or not the parallaxe\
        scrolls to the left. Defaults to `True`.
        speeds(list, optionnal): List of speeds for the layers.\
        Defaults to `[0 ... 0]`. Should have the same amount of \
        value as there are layers.
        speed_factor(int, optionnal): default scrolling speed. \
        Defaults to 5.
        cut_factor(list, optionnal): list of points for each frame. Will be used to cut 'dead' \
        pixels from the parallaxes, aka those that are never displayed. Defaults to None.
    """
    def __init__(self, uri: str, frame_x:int, frame_y:int, scroll_left = True,\
        speeds = None, speed_factor = 5, cut_pixels = None):
        super().__init__(uri, frame_x, frame_y, animated=False)
        self._scroll_left = scroll_left
        if speeds is None:
            self._speeds = [0 for _ in range(len(self._sequence))]
        else:
            self._speeds = speeds
        self._diff_x = [0 for _ in range(len(self._sequence))]
        self._diff_y = [0 for _ in range(len(self._sequence))]
        self._speed_factor = speed_factor
        if cut_pixels is not None:
            i = 0
            for _ in self._sequence:
                seq = cut_pixels[i]
                dx = round(seq[2] / frame_x * SCREEN_WIDTH)
                dy = round(seq[3] / frame_y * SCREEN_HEIGHT)
                self._diff_y[i] = seq[1] / frame_y * SCREEN_HEIGHT
                print(seq, dx, dy, self._diff_y[i])
                self._sequence[i] = self._sequence[i].extracts(seq[0], seq[1], seq[2], seq[3])\
                    .scale(dy, dx)
                i += 1
        else:
            super().scale(SCREEN_HEIGHT, SCREEN_WIDTH)
        self._background = self._sequence[0].image
        self._cut_pixels = cut_pixels
        self._layers = [Surface(SCREEN_WIDTH * 2,
                                round(self._sequence[i].height / frame_y * SCREEN_HEIGHT))\
            for i in range(len(self._sequence))]
        for i in range(len(self._sequence) - 1):
            self._layers[i].blit(self._sequence[i + 1].image, (0, 0))
            self._layers[i].blit(self._sequence[i + 1].image, (SCREEN_WIDTH, 0))
        self._surface = Surface(SCREEN_WIDTH, SCREEN_HEIGHT)
        self._render = []

    def invert(self):
        """Flips the scrolling animation."""
        self._scroll_left = not self._scroll_left

    def draw(self, stops = False):
        """Draws the parallaxe."""
        shake, _ = SYSTEM["post_effects"].shake_factor
        self._render.clear()
        if not stops:
            if self._scroll_left:
                for i in range(len(self._sequence)):
                    self._diff_x[i] = (self._diff_x[i] + self._speeds[i] *\
                        self._speed_factor + shake) % SCREEN_WIDTH
            else:
                for i in range(len(self._sequence)):
                    self._diff_x[i] = (self._diff_x[i] - self._speeds[i] *\
                        self._speed_factor + shake) % SCREEN_WIDTH
        for layer, _ in enumerate(self._sequence):
            self._render.append(int(-self._diff_x[layer]))
        layer_blits = [(self._layers[i].subsurface((self._diff_x[i], 0, SCREEN_WIDTH, SCREEN_HEIGHT)),
                        (0, self._diff_y[(i + 1) % len(self._sequence)])) \
                       for i in range(len(self._sequence))]
        renders(layer_blits)

    @property
    def background(self):
        """Returns the Parallaxe's first layer."""
        return self._background

    @background.setter
    def background(self, value):
        self._background = value

    @property
    def diff_y(self):
        """Things"""
        return self._diff_y

    @property
    def surface(self) -> Surface:
        """returns the composite surface of the parallaxe."""
        return self._surface

    @surface.setter
    def surface(self, value):
        self._surface = value

    @property
    def as_background(self):
        """Prepares a list to be rendered."""
        return [(l.image, (0,0)) for l in self._sequence]
