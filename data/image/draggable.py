"""A draggable is a component that can be dragged
around by the mouse."""

from data.constants import SYSTEM
from data.image.image import Image

class Draggable(Image):
    """Defines a draggable.
    
    Args:
        uri (str, optionnal): URI to the image. Defaults\
        to None.
        x (int, optionnal): x position of the draggable.\
        Defaults to 0.
        y (int, optionnal): x position of the draggable.\
        Defaults to 0. 
        contains (Any, optionnal): Contained payload of\
        the draggable. Can be anything. Defaults to None.
    """
    def __init__(self, uri=None, x = 0, y = 0, contains = None):
        super().__init__(uri)
        self._x = x
        self._y = y
        self._dragging = False
        self._offset = (0, 0)
        self._contains = contains
        self._parent = None
        self._last = None

    def tick(self):
        """Adjusts the position of the draggable if\
        dragged."""
        mouse_x, mouse_y = SYSTEM["mouse"]
        mouse_click = SYSTEM["mouse_click"]
        if mouse_click[0]:
            if self._dragging:
                self._x = mouse_x + self._offset[0]
                self._y = mouse_y + self._offset[1]
                self.opacity(180)
            elif (self._x <= mouse_x <= self._x + self.width and
                    self._y <= mouse_y <= self._y + self.height):
                self._dragging = True
                self._offset = (mouse_x - self._x, mouse_y - self._y)
                self._last = self._parent
        else:
            self._dragging = False
            if self.parent is None:
                self._last.insert(self)
            self.opacity(255)
        return self

    def set(self, x, y):
        """Sets the draggable position."""
        self._x = x
        self._y = y
        return self

    def draw(self):
        """Displays the draggable."""
        SYSTEM["windows"].blit(self._image, (self._x, self._y))

    def set_parent(self, slot):
        """Sets the draggeable's parent."""
        self._parent = slot

    def clear_parent(self):
        """Clears the parent."""
        self._parent = None

    @property
    def contains(self):
        """Returns whatever the draggable contains."""
        return self._contains

    @contains.setter
    def contains(self, value):
        self._contains = value

    @property
    def parent(self):
        """Returns the parent."""
        return self._parent
