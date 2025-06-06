"""An animation is a sequence of images."""

import pygame
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
    def __init__(self, uri: str|Image, frame_x: int, frame_y: int, lines = 1,\
                frame_rate = 1, frame_max = -1, loops = True, animated = True,\
                plays_once = False):
        if isinstance(uri, Image):
            self._base_image = uri
        else:
            self._base_image = Image(uri)
        self._frame_x = frame_x
        self._frame_y = frame_y
        self._frame_rate = frame_rate
        self._frame_max = frame_max
        self._loops = loops
        self._lines = lines
        self._sequence = []
        self.__sequencer()
        self._current_frame = 0
        self._animated = animated
        self._play_once = plays_once
        self._finished = False
        #
        self._scaled = (frame_y, frame_x)
        self._flipped = (False, False)
        self._rotated = 0

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

    def get_image(self) -> pygame.Surface:
        """Returns the current image of the sequence."""
        return self._sequence[int(self._current_frame)].image

    def tick(self):
        """Advance the sequence."""
        if not self._animated:
            return
        self._current_frame += self._frame_rate
        if self._current_frame > self._frame_max:
            if self._loops:
                self._current_frame = 0
            else:
                if self._play_once:
                    self._finished = True
                self._current_frame = self._frame_max

    def rotate(self, deg: float):
        """Rotates the sequence.
        
        Args:
            deg (float): degrees to rotate the sequence.
        """
        self._rotated = deg
        for frame in self._sequence:
            frame.rotate(deg)
        return self

    def scale(self, height: float, width: float):
        """Scales up or down the sequence.
        
        Args:
            height (float): New height of the sequence.
            width (float): New width of the sequence
        """
        self._scaled = (height, width)
        for frame in self._sequence:
            frame.scale(height, width)
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
        return Animation(
            self._base_image,
            self._frame_x,
            self._frame_y,
            self._lines,
            self._frame_rate,
            self._frame_max,
            self._loops,
            self._animated,
            self._play_once
        ).flip(self._flipped[0], self._flipped[1])\
        .rotate(self._rotated)\
        .scale(self._scaled[0], self._scaled[1])

    @property
    def width(self):
        """Returns the sequence's frame width."""
        return self._frame_x

    @property
    def height(self):
        """Returns the sequence's frame height."""
        return self._frame_y

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
