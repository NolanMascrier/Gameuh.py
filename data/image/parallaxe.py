"""Class for parallaxes. Parallaxes
are scrolling background images."""

import pygame
from data.constants import SCREEN_HEIGHT, SCREEN_WIDTH, SYSTEM
from data.image.animation import Animation

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
    """
    def __init__(self, uri: str, frame_x:int, frame_y:int, scroll_left = True,\
        speeds = None, speed_factor = 5):
        super().__init__(uri, frame_x, frame_y, animated=False)
        super().scale(SCREEN_HEIGHT, SCREEN_WIDTH)
        self._scroll_left = scroll_left
        if speeds is None:
            self._speeds = [0 for _ in range(len(self._sequence))]
        else:
            self._speeds = speeds
        self._diff_x = [0 for _ in range(len(self._sequence))]
        self._speed_factor = speed_factor

    def invert(self):
        """Flips the scrolling animation."""
        self._scroll_left = not self._scroll_left

    def draw(self) -> pygame.Surface:
        """Draws the parallaxe."""
        values = [(self._sequence[0].image, (0, 0))]
        if self._scroll_left:
            for i in range(len(self._sequence)):
                self._diff_x[i] = (self._diff_x[i] + self._speeds[i] *\
                    self._speed_factor) % SCREEN_WIDTH
            for layer, image in enumerate(self._sequence):
                for y in range(0, 2):
                    x = int((y * SCREEN_WIDTH) - self._diff_x[layer])
                    values.append((image.image, (x, 0)))
        else:
            for i in range(len(self._sequence)):
                self._diff_x[i] = (self._diff_x[i] - self._speeds[i] *\
                    self._speed_factor) % SCREEN_WIDTH
            for layer, image in enumerate(self._sequence):
                for y in range(0, 2):
                    x = int((y * SCREEN_WIDTH) - self._diff_x[layer])
                    values.append((image.image, (x, 0)))
        SYSTEM["windows"].blits(values)
