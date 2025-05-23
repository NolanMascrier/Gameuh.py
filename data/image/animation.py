"""An animation is a sequence of images."""

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
    """
    def __init__(self, uri: str, frame_x: int, frame_y: int, lines = 1,\
                frame_rate = 1, frame_max = -1, loops = True):
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

    def __sequencer(self):
        """Automatically cuts the image into frames."""
        frame_per_line = self._base_image.width / self._lines
        for line in range(self._lines):
            sequence = [self._base_image.extracts(index * self._frame_x, \
                                                line * self._frame_y,\
                                                self._frame_x, self._frame_y)\
                for index in range(0, frame_per_line)]
            self._sequence.extend(sequence)

    def get_image(self) -> Image:
        """Returns the current image of the sequence."""
        return self._sequence[int(self._current_frame)]

    def tick(self):
        """Advance the sequence."""
        self._current_frame += self._frame_rate
        if self._current_frame > self._frame_max:
            if self._loops:
                self._current_frame = 0
            else:
                self._current_frame = self._frame_max

    def rotate(self, deg: float):
        """Rotates the sequence.
        
        Args:
            deg (float): degrees to rotate the sequence.
        """
        self._base_image.rotate(deg)
        self._sequence.clear()
        self.__sequencer()

    def scale(self, height: float, width: float):
        """Scales up or down the sequence.
        
        Args:
            height (float): New height of the sequence.
            width (float): New width of the sequence
        """
        self._base_image.scale(height, width)
        self._sequence.clear()
        self.__sequencer()

    def flip(self, vertical: bool, horizontal: bool):
        """Flips the sequence.
        
        Args:
            vertical (bool): Flip the sequence on the y axis.
            horizontal (bool): Flip the sequence on the x axis.
        """
        self._base_image.flip(vertical, horizontal)
        self._sequence.clear()
        self.__sequencer()
