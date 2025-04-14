from constants import *

class Sprite:
    """Loads a sprite in memory. A sprite is made of \
    multiple tiles of the same size.

    Args:
        image (str, optionnal): URI to image file. Defaults to \
        None.
        h (int, optionnal): height of a single tile. Defaults \
        to 32.
        w (int, optionnal): width of a single tile. Defaults \
        to 32.
        c (int, optionnal): number of tiles in a line. Defaults \
        to 8.
        l (int, optionnal): number of lines in the image. Defaults \
        to 8.
    """
    def __init__(self, image = None, h = 32, w = 32, c = 8, l = 8):
        self._image = pygame.image.load(image).convert_alpha()
        self._h = h
        self._w = w
        self._c = c
        self._l = l
        self._set = [
            [self._image.subsurface(x, y, self._w, self._h) for x in range(0, self._c * self._w, self._w)] \
                for y in range(0, self._l * self._h, self._h)
        ]

    def debug_print(self, window):
        """Displays the full sprite set on the window."""
        FONT = pygame.font.SysFont('Comic Sans MS', 8)
        y = 0
        for line in self._set:
            x = 0
            for img in line:
                txt = FONT.render(f"({x/self._w},{y/self._h})", False, (0xFF, 0xFF, 0xFF))
                window.blit(img, (x, y))
                window.blit(txt, (x, y))
                x += self._w
            y += self._h

    @property
    def image(self):
        return self._image

    @image.setter
    def image(self, value):
        self._image = value

    @property
    def h(self):
        return self._h

    @h.setter
    def h(self, value):
        self._h = value

    @property
    def w(self):
        return self._w

    @w.setter
    def w(self, value):
        self._w = value

    @property
    def c(self):
        return self._c

    @c.setter
    def c(self, value):
        self._c = value

    @property
    def l(self):
        return self._l

    @l.setter
    def l(self, value):
        self._l = value

    @property
    def set(self):
        return self._set

    @set.setter
    def set(self, value):
        self._set = value


    