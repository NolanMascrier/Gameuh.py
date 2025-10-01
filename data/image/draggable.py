"""A draggable is a component that can be dragged
around by the mouse."""

from data.item import Item
from data.constants import SYSTEM
from data.image.image import Image
from data.image.hoverable import Hoverable
from data.game.spell import Spell
from data.interface.render import render

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
        immutable (bool, optional): Whether or not this draggable\
        is immutable. If it is, dragging it will instead create a copy.\
        Defaults to False.
    """
    def __init__(self, uri=None, x = 0, y = 0, contains = None, immutable = False):
        super().__init__(uri)
        self.x = x
        self.y = y
        self._dragging = False
        self._contains = contains
        self._hover = None
        self._immutable = immutable
        if isinstance(contains, Item):
            self._width = contains.get_image().width
            self._height = contains.get_image().height
            self._image = contains.get_image().clone().image
            self._hover = Hoverable(x, y, None, None, surface=self._image, override=contains.popup,\
                alternative=contains.popup_details)
        elif isinstance(contains, Spell):
            self._width = contains.icon.width
            self._height = contains.icon.height
            self._image = contains.icon.clone().get_image()
            self._hover = Hoverable(x, y, None, None,
                                    surface=self._image, override=contains.surface)
        self._parent_slot = None
        self._last_slot = None
        self._parent_panel = None
        self._last_panel = None
        self._slotted = False

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
                    self.x = mouse_x
                    self.y = mouse_y
                    self.opacity(180)
                elif (self.x <= mouse_x <= self.x + self.width and
                        self.y <= mouse_y <= self.y + self.height):
                    if SYSTEM["cooldown"] > 0:
                        return self
                    if SYSTEM["rune"] != -1:
                        self._contains.apply_rune()
                        self._hover = Hoverable(self.x, self.y, None, None, surface=self._image,\
                            override=self._contains.popup,\
                            alternative=self._contains.popup_details)
                        SYSTEM["cooldown"] = 0.1
                        return self
                    if self._immutable:
                        copy = Draggable(self._uri, self.x, self.y,\
                            self._contains, True)
                        copy.dragging = True
                        SYSTEM["dragged"] = copy
                        SYSTEM["cooldown"] = 0.5
                        return self
                    self._dragging = True
                    self._slotted = False
                    if self._parent_panel is not None:
                        self._last_panel = self._parent_panel
                        self._parent_panel.remove(self)
                        self._parent_panel = None
                    elif self._parent_slot is not None:
                        self._last_slot = self._parent_slot
                        self._parent_slot.remove()
                        self._parent_slot = None
                    SYSTEM["dragged"] = self
                    SYSTEM["cooldown"] = 0.5
        elif not mouse_click[0]:
            if not self._slotted and not self._immutable:
                if self._last_panel is not None:
                    self._last_panel.insert(self)
                elif self._last_slot is not None:
                    self._last_slot.insert(self)
            self._dragging = False
            self.opacity(255)
        return self

    def set(self, x, y):
        """Sets the draggable position."""
        self.x = x
        self.y = y
        if self._hover is not None:
            self._hover.set(x, y)
        return self

    def draw(self):
        """Displays the draggable."""
        render(self._image, (self.x, self.y))

    def get_image(self):
        """Returns the image of the contained item, or the\
        image of the slot should the latter be None."""
        return self

    def set_parent(self, slot):
        """Sets the draggeable's parent."""
        self._slotted = True
        self._parent_slot = slot
        self._last_slot = slot

    def clear_parent(self):
        """Clears the parent."""
        self._parent_slot = None

    def set_panel(self, panel):
        """Sets the draggeable's parent."""
        self._slotted = True
        self._parent_panel = panel
        self._last_panel = panel

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

    @property
    def immutable(self):
        """Returns whether or not the draggable is immutable."""
        return self._immutable

    @immutable.setter
    def immutable(self, value):
        self._immutable = value
