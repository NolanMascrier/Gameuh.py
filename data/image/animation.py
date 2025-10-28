"""An animation is a sequence of images."""

import json
from data.api.surface import Surface
from data.image.image import Image

class Animation():
    """Defines an animation, a sequence of images.
    
    Args:
        uri (str): URI to the base image.
        frame_x (int): width of a single frame of the sequence.
        frame_y (int): height of a single frame of the sequence.
        lines (int, optionnal): Numbers of frame lines in the images. \
        Defaults to 1.
        frame_rate (int, optionnal): speed at which a frame changes to\
        next one in the sequence. Defaults to 1.
        frame_max (int, optionnal): Limits the max amount of frames in\
        the sequence. Useful if the image has blank spaces at the end.\
        Defaults to -1. 
        loops (bool, optionnal): Wether or not the animation should loop.\
        defaults to True.
        animated (bool, optionnal): Whether or not the animation played.\
        Defaults to True. Used for conditionnal animations (like the life orb).
        plays_once (bool, optionnal): Whether or not the animation should play only\
        once. If set to `True`, the inner boolean finished will be set to `True`\
        once the animation is over. Defaults to False.
    """
    __slots__= '_base_image', '_frame_x', '_frame_y', '_frame_rate', '_frame_max', '_loops', \
               '_max_loop', '_lines', '_sequence', '_current_frame', '_animated', '_play_once', \
               '_finished', '_width', '_height', '_scaled', '_flipped', '_rotated', '_frame_loop'
    def __init__(self, uri: str|Image, frame_x: int, frame_y: int, lines = 1,\
                frame_rate = 1, frame_max = -1, loops: bool|int = True, animated = True,\
                plays_once = False, frame_loop = None):
        if isinstance(uri, Image):
            self._base_image = uri
        else:
            self._base_image = Image(uri)
        self._frame_x = frame_x
        self._frame_y = frame_y
        self._frame_rate = frame_rate
        self._frame_max = frame_max
        self._loops = loops if isinstance(loops, bool) else False
        self._max_loop = 0 if isinstance(loops, bool) else loops
        self._lines = lines
        self._sequence = []
        self.__sequencer()
        self._current_frame = 0
        self._animated = animated
        self._play_once = plays_once
        self._finished = False
        self._width = self._sequence[0].width
        self._height = self._sequence[0].height
        #
        self._scaled = (frame_y, frame_x, True)
        self._flipped = (False, False)
        self._rotated = 0
        self._frame_loop = frame_loop

    def __sequencer(self):
        """Automatically cuts the image into frames."""
        frame_per_line = int(self._base_image.width / self._frame_x)
        max_frame = 0
        for line in range(self._lines):
            sequence = [self._base_image.extracts(index * self._frame_x, \
                                                line * self._frame_y,\
                                                self._frame_x, self._frame_y)\
                for index in range(0, frame_per_line)]
            self._sequence.extend(sequence)
            max_frame += len(sequence) - 1
        if self._frame_max == -1:
            self._frame_max = max_frame
        self._frame_max = min(max_frame, self._frame_max)

    def reset(self):
        """Restarts the animation."""
        self._finished = False
        self._current_frame = 0

    def get_image(self, caller = None) -> Surface:
        """Returns the current image of the sequence."""
        if caller is not None:
            return self._sequence[int(caller[0])].image
        return self._sequence[int(self._current_frame)].image

    def tick(self, frame_modifier = 1):
        """Advance the sequence."""
        if not self._animated:
            return
        if frame_modifier is None:
            frame_modifier = 1
        start_frame = self._frame_loop[0] if self._frame_loop is not None else 0
        end_frame = self._frame_loop[1] if self._frame_loop is not None else self._frame_max
        self._current_frame += self._frame_rate * frame_modifier
        if self._current_frame > end_frame:
            if self._loops:
                self._current_frame = start_frame
            else:
                if self._play_once:
                    if self._max_loop > 0:
                        self._current_frame = start_frame
                        self._max_loop -= 1
                    else:
                        self._finished = True
                        self._current_frame = end_frame
                else:

                    self._current_frame = end_frame

    def rotate(self, deg: float):
        """Rotates the sequence.
        
        Args:
            deg (float): degrees to rotate the sequence.
        """
        self._rotated = deg
        for frame in self._sequence:
            frame.rotate(deg)
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
        self._scaled = (height, width, absolute)
        for frame in self._sequence:
            frame.scale(height, width, absolute)
        self._width = self._sequence[0].width
        self._height = self._sequence[0].height
        return self

    def flip(self, vertical: bool, horizontal: bool):
        """Flips the sequence.
        
        Args:
            vertical (bool): Flip the sequence on the y axis.
            horizontal (bool): Flip the sequence on the x axis.
        """
        self._flipped = (vertical, horizontal)
        for frame in self._sequence:
            frame.flip(vertical, horizontal)
        return self

    def clone(self):
        """Returns a deep clone of the animation."""
        ani = Animation(
            self._base_image.clone(),
            self._frame_x,
            self._frame_y,
            self._lines,
            self._frame_rate,
            self._frame_max,
            self._loops if self._loops else self._max_loop,
            self._animated,
            self._play_once,
            self._frame_loop
        ).flip(self._flipped[0], self._flipped[1])\
        .rotate(self._rotated)\
        .scale(self._scaled[0], self._scaled[1], self._scaled[2])
        ani.frame_max = self._frame_max
        return ani

    def export(self) -> str:
        """Serializes the animation as JSON."""
        data = {
            "uri": self._base_image.uri,
            "frame_x": self._frame_x,
            "frame_y": self._frame_y,
            "lines": self._lines,
            "frame_rate": self._frame_rate,
            "frame_max": self._frame_max,
            "loops": self._loops,
            "animated": self._animated,
            "play_once": self._play_once,
            "flipped": self._flipped,
            "rotated": self._rotated,
            "scaled": self._scaled
        }
        return json.dumps(data)

    @staticmethod
    def imports(data):
        """Creates an animation from a json data array."""
        anim = Animation(
            data["uri"],
            int(data["frame_x"]),
            int(data["frame_y"]),
            int(data["lines"]),
            int(data["frame_rate"]),
            int(data["frame_max"]),
            data["loops"],
            bool(data["animated"]),
            bool(data["play_once"])
        )
        anim.flip(bool(data["flipped"][0]), bool(data["flipped"][1]))
        anim.rotate(int(data["rotated"]))
        anim.scale(float(data["scaled"][0]), float(data["scaled"][1]), data["scaled"][2])
        anim.frame = 0
        return anim

    @property
    def image(self):
        """Returns the image."""
        return self.get_image()

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
        return self._width

    @property
    def h(self):
        """Returns the sequence's image height."""
        return self._height

    @property
    def frame(self):
        """Returns the current frame."""
        return self._current_frame

    @frame.setter
    def frame(self, value):
        self._current_frame = value

    @property
    def finished(self):
        """Returns whether or not the animation is finished."""
        return self._finished

    @finished.setter
    def finished(self, value):
        self._finished = value

    @property
    def frame_max(self):
        """Returns the maximum frame of the animation."""
        return self._frame_max

    @frame_max.setter
    def frame_max(self, value):
        self._frame_max = value

    @property
    def scale_factor(self):
        """Returns the factor of the latest scaling."""
        return self._scaled

    @property
    def animated(self):
        """Returns whether or not the animation is animated."""
        return self._animated

    @animated.setter
    def animated(self, value):
        self._animated = value

    @property
    def play_once(self):
        """Returns whether or not the animation plays only once."""
        return self._play_once

    @play_once.setter
    def play_once(self, value):
        self._play_once = value

    @property
    def frame_loop(self):
        """Returns the number of loop left for the animation left."""
        return self._frame_loop

    @frame_loop.setter
    def frame_loop(self, value):
        self._frame_loop = value

    @property
    def frame_rate(self):
        """Returns the animation's frame rate."""
        return self._frame_rate

    @frame_rate.setter
    def frame_rate(self, value):
        self._frame_rate = value

    @property
    def loops(self):
        """Returns the animation's current loop."""
        return self._loops

    @loops.setter
    def loops(self, value):
        self._loops = value
