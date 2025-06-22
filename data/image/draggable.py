"""A draggable is a component that can be dragged
around by the mouse."""

from data.constants import SYSTEM
from data.image.image import Image
from data.image.hoverable import Hoverable
from data.item import Item

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
        self._contains = contains
        self._hover = None
        if isinstance(contains, Item):
            self._width = contains.get_image().width
            self._height = contains.get_image().height
            self._image = contains.get_image().clone().image
            self._hover = Hoverable(x, y, None, contains.describe(), surface=self._image)
        self._parent_slot = None
        self._last_slot = None
        self._parent_panel = None
        self._last_panel = None

    def tick(self):
        """Adjusts the position of the draggable if\
        dragged."""
        mouse_x, mouse_y = SYSTEM["mouse"]
        mouse_click = SYSTEM["mouse_click"]
        if self._hover is not None:
            self._hover.tick()
        if mouse_click[0]:
            if SYSTEM["dragged"] is None or SYSTEM["dragged"] is self:
                if self._dragging:
                    self._x = mouse_x
                    self._y = mouse_y
                    self.opacity(180)
                elif (self._x <= mouse_x <= self._x + self.width and
                        self._y <= mouse_y <= self._y + self.height):
                    self._dragging = True
                    self._last_slot = self._parent_slot
                    self._last_panel = self._parent_panel
                    if self._parent_panel is not None:
                        self._parent_panel.remove(self)
                        self._parent_panel = None
                    elif self._parent_slot is not None:
                        self._parent_slot.remove()
                        self._parent_slot = None
                    SYSTEM["dragged"] = self
        elif SYSTEM["dragged"] is None:
            if self._parent_panel is None and self._parent_slot is None:
                if self._last_panel is not None:
                    self._last_panel.insert(self)
                elif self._last_slot is not None:
                    self._last_slot.insert(self)
            self._dragging = False
            self.opacity(255)
        return self

    def set(self, x, y):
        """Sets the draggable position."""
        self._x = x
        self._y = y
        if self._hover is not None:
            self._hover.set(x, y)
        return self

    def draw(self):
        """Displays the draggable."""
        SYSTEM["windows"].blit(self._image, (self._x, self._y))

    def get_image(self):
        """Returns the image of the contained item, or the\
        image of the slot should the latter be None."""
        return self

    def set_parent(self, slot):
        """Sets the draggeable's parent."""
        self._parent_slot = slot

    def clear_parent(self):
        """Clears the parent."""
        self._parent_slot = None

    def set_panel(self, panel):
        """Sets the draggeable's parent."""
        self._parent_panel = panel

    def clear_panel(self):
        """Clears the parent."""
        self._parent_panel = None

    @property
    def dragging(self):
        """Returns whether or not the component is being dragged."""
        return self._dragging

    @dragging.setter
    def dragging(self, value):
        self._dragging = value

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
        return self._parent_slot
