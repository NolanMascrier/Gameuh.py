"""Class for parallaxes. Parallaxes
are scrolling background images."""

from data.api.surface import Surface

from data.constants import SCREEN_HEIGHT, SCREEN_WIDTH, SYSTEM
from data.image.animation import Animation

class Parallaxe:
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
    """
    def __init__(self, uri: str, frame_x: int, frame_y: int, scroll_left=True,
                 speeds=None, speed_factor=5):
        temp_anim = Animation(uri, frame_x, frame_y, animated=False)
        temp_anim.scale(SCREEN_HEIGHT, SCREEN_WIDTH)
        self._sequence = temp_anim._sequence
        self._scroll_left = scroll_left
        if speeds is None:
            self._speeds = [0 for _ in range(len(self._sequence))]
        else:
            self._speeds = speeds
        self._diff_x = [0.0 for _ in range(len(self._sequence))]
        self._speed_factor = speed_factor
        self._background = self._sequence[0].image
        self._layers = [Surface(SCREEN_WIDTH * 2, SCREEN_HEIGHT)
                        for _ in range(len(self._sequence))]
        for i in range(len(self._sequence) - 1):
            layer_img = self._sequence[i + 1].image
            self._layers[i].blit(layer_img, (0, 0), True)
            self._layers[i].blit(layer_img, (SCREEN_WIDTH, 0), True)
        self._surface = Surface(SCREEN_WIDTH, SCREEN_HEIGHT)
        self._blit_list = [(None, None) for _ in range(len(self._sequence))]
        self._layer_count = len(self._sequence)
        self._speed_mults = [speed * self._speed_factor for speed in self._speeds]

    def invert(self):
        """Flips the scrolling animation."""
        self._scroll_left = not self._scroll_left

    def draw(self, stops=False):
        """Draws the parallaxe - HEAVILY OPTIMIZED."""
        shake, _ = SYSTEM["post_effects"].shake_factor
        if not stops:
            if self._scroll_left:
                for i in range(self._layer_count):
                    self._diff_x[i] += self._speed_mults[i] + shake
                    if self._diff_x[i] >= SCREEN_WIDTH:
                        self._diff_x[i] -= SCREEN_WIDTH
            else:
                for i in range(self._layer_count):
                    self._diff_x[i] -= self._speed_mults[i] - shake
                    if self._diff_x[i] < 0:
                        self._diff_x[i] += SCREEN_WIDTH
        for i in range(self._layer_count):
            self._blit_list[i] = (self._layers[i], (int(-self._diff_x[i]), 0))
        if self._layer_count > 0:
            self._surface.blit(self._layers[0], (int(-self._diff_x[0]), 0), True)
            if self._layer_count > 1:
                self._surface.blits(self._blit_list[1:])

    def get_render_list(self):
        """Returns the pre-built blit list for external rendering.
        This avoids calling renders() in draw()."""
        return self._blit_list

    @property
    def background(self):
        """Returns the Parallaxe's first layer."""
        return self._background

    @background.setter
    def background(self, value):
        self._background = value

    @property
    def surface(self) -> Surface:
        """returns the composite surface of the parallaxe."""
        return self._surface

    @surface.setter
    def surface(self, value):
        self._surface = value

    @property
    def as_background(self):
        """Prepares a list to be rendered - CACHED."""
        if not hasattr(self, '_background_cache'):
            self._background_cache = [(l.image, (0, 0)) for l in self._sequence]
        return self._background_cache
