"""A sprite is a collection of animations that plays under certain conditions."""

from data.constants import ANIMATION_TRACKER
from data.image.animation import Image, Animation

class Sprite():
    """Defines a sprite. A sprite is a list of animations with names."""
    __slots__ = '_base_image', '_file', '_frame_max', '_frame_x', '_frame_y', '_keys', \
                '_frame_rates', '_frame_loops', '_lines', '_animations', '_akey', '_final', \
                '_flagged', '_scaled', '_flipped', '_rotated', '_loop_times'
    def __init__(self, file, frame_x, frame_y, keys: list, frame_rates, frame_limits, frame_loops,
                 final):
        self._base_image = Image(file)
        self._file = file
        self._frame_max = frame_limits
        self._frame_x = frame_x
        self._frame_y = frame_y
        self._keys = keys
        self._frame_rates = frame_rates
        self._frame_loops = frame_loops
        self._lines = int(self._base_image.height / frame_y)
        self._animations = {}
        self.__sequencer()
        self._akey = keys[0]
        self._final = final
        self._loop_times = {}
        i = 0
        for f in self._animations:
            self._loop_times[f] = final[i]
            i += 1
        self._flagged = False
        self._scaled = (1, 1, False)
        self._flipped = (False, False)
        self._rotated = 0

    def __sequencer(self):
        """Automatically cuts the image into frames."""
        for line in range(self._lines):
            frame_line = self._base_image.extracts(0, line * self._frame_y,
                                                    self._base_image.width, self._frame_y)
            self._animations[self._keys[line]]\
                = Animation(frame_line, self._frame_x, self._frame_y,
                            1, self._frame_rates[line],
                            self._frame_max[line], self._frame_loops[line],
                            True, True)

    def clone(self):
        """Returns a deep copy of the sprite."""
        return Sprite(
            self._file,
            self._frame_x,
            self._frame_y,
            self._keys,
            self._frame_rates,
            self._frame_max,
            self._frame_loops,
            self._final
        ).flip(self._flipped[0], self._flipped[1])\
        .rotate(self._rotated)\
        .scale(self._scaled[0], self._scaled[1], self._scaled[2])

    def play(self, key):
        """Plays an animation."""
        if key not in self._animations:
            return
        self._akey = key
        self._animations[key].reset()

    def tick(self):
        """Ticks down the sprite."""
        if self._akey not in self._animations:
            return
        self._animations[self._akey].tick()
        if self._animations[self._akey].finished:
            if self._loop_times[self._akey] < 0:
                self.play(self._keys[0])
            elif self._loop_times[self._akey] > 0:
                self._animations[self._akey].reset()
                self._loop_times[self._akey] -= 1
            if self._loop_times[self._akey] == 0:
                self._flagged = True

    def detach(self, key, x, y, center = False):
        """Detaches the sprite, allowing one of its animation to be played at a 
        specified location."""
        if key not in self._animations:
            return
        if center:
            x -= self.w / 2
            y -= self.h / 2
        self._animations[key].reset()
        ANIMATION_TRACKER.append((self._animations[key], x, y))

    def get_image(self):
        """Returns the current image."""
        return self._animations[self._akey].get_image()

    def rotate(self, deg: float):
        """Rotates the sequence.
        
        Args:
            deg (float): degrees to rotate the sequence.
        """
        for _, f in self._animations.items():
            f.rotate(deg)
        self._rotated = deg
        return self

    def scale(self, height: float, width: float, absolute = True):
        """Scales up or down the sequence.
        
        Args:
            height (float): New height of the sequence.
            width (float): New width of the sequence
            absolute (bool, optional): Whether or not to use absolute\
            values when scaling. If set to `True`, the image will be\
            resized to the given dimension. Otherwise, it'll be scaled\
            by the dimensions. Defaults to `True`.
        """
        for _, f in self._animations.items():
            f.scale(height, width, absolute)
        self._scaled = (height, width, absolute)
        return self

    def flip(self, vertical: bool, horizontal: bool):
        """Flips the sequence.
        
        Args:
            vertical (bool): Flip the sequence on the y axis.
            horizontal (bool): Flip the sequence on the x axis.
        """
        for _, f in self._animations.items():
            f.flip(vertical, horizontal)
        self._flipped = (vertical, horizontal)
        return self

    @property
    def width(self):
        """Returns the sequence's frame width."""
        return self._frame_x

    @property
    def height(self):
        """Returns the sequence's frame height."""
        return self._frame_y

    @property
    def w(self):
        """Returns the sequence's image width."""
        return self._animations[self._keys[0]].w

    @property
    def h(self):
        """Returns the sequence's image height."""
        return self._animations[self._keys[0]].h

    @property
    def frame(self):
        """Returns the current frame."""
        return self._animations[self._akey].frame

    @frame.setter
    def frame(self, value):
        self._animations[self._akey].frame = value

    @property
    def finished(self):
        """Returns whether or not the animation is finished."""
        return self._animations[self._akey].finished

    @finished.setter
    def finished(self, value):
        self._animations[self._akey].finished = value

    @property
    def frame_max(self):
        """Returns the maximum frame of the animation."""
        return self._frame_max

    @frame_max.setter
    def frame_max(self, value):
        self._frame_max = value

    @property
    def flagged(self):
        """Returns whether or not the animation is flagged for deletion."""
        return self._flagged

    @property
    def scale_factor(self):
        """Returns the factor of the latest scaling."""
        return self._scaled
