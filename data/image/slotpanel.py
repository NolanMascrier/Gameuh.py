"""A component that houses slots. Used for
inventories and such"""

from data.constants import SYSTEM
from data.image.slot import Slot
from data.image.draggable import Draggable

class SlotPanel:
    def __init__(self, x, y, slot_size=64, padding = 16, default = None):
        self._x = x
        self._y = y
        self._slot_size = slot_size
        self._background = SYSTEM["images"]["panel_back"]
        self._padding = padding
        if default is None:
            self._inventory = []
        else:
            self._inventory = default
        self._slots = []
        self._columns = (self._background.width - self._padding * 2) // slot_size

    def get_index(self):
        """Returns the index of the latest element."""
        elmts = len(self._slots)
        col = (elmts % self._columns) * self._slot_size + self._x + self._padding
        line = (elmts // self._columns) * self._slot_size + self._y + self._padding
        return (line, col)

    def is_hovered(self):
        """Returns true if the mouse is within the usable boundaries 
        of the panel."""
        if SYSTEM["mouse"][0] >= self._x + self._padding and\
            SYSTEM["mouse"][0] <= self._x + self._background.width - self._padding and\
            SYSTEM["mouse"][1] >= self._y + self._padding and\
            SYSTEM["mouse"][1] <= self._y + self._background.height - self._padding:
            return True
        return False

    def insert(self, drag: Draggable):
        """Inserts the draggable into the panel."""
        if drag is None:
            return
        y, x = self.get_index()
        sl = Slot(x, y)
        sl.insert(drag)
        drag.set_panel(self)
        SYSTEM["dragged"] = None
        self._slots.append(sl)

    def remove(self, drag: Draggable):
        """Removes stuff"""
        for slot in self._slots.copy():
            if slot.contains == drag:
                drag.clear_panel()
                slot.remove()

    def tick(self):
        """ticks down the panel. Removes empty slots."""
        for slot in self._slots.copy():
            if slot.contains.dragging:
                self._slots.remove(slot)
            else:
                slot.contains.tick()
        self._slots = [slot for slot in self._slots if not slot.empty\
                            and not slot.contains.dragging]
        if not SYSTEM["mouse_click"][0]:
            self.try_insert(SYSTEM["dragged"])
        return self

    def try_insert(self, draggable: Draggable):
        """Attempts to insert draggable if it's dropped on the slot."""
        if self.is_hovered():
            self.insert(draggable)
            return True
        return False

    def draw(self):
        """Draws the component."""
        SYSTEM["windows"].blit(self._background.image, (self._x, self._y))
        x = 0
        y = 0
        real_x = self._x + self._padding + x * self._slot_size
        real_y = self._y + self._padding + y * self._slot_size
        for slot in self._slots:
            if slot.contains is SYSTEM["dragged"]:
                continue
            real_x = self._x + self._padding + x * self._slot_size
            real_y = self._y + self._padding + y * self._slot_size
            slot.draw_alt(SYSTEM["windows"], real_x, real_y)
            slot.contains.set(real_x, real_y)
            x += 1
            if x > self._columns:
                x = 0
                y += 1
        real_x = self._x + self._padding + x * self._slot_size
        real_y = self._y + self._padding + y * self._slot_size
        if x > self._columns:
            x = 0
            y += 1
        SYSTEM["windows"].blit(SYSTEM["images"]["slot_empty"].image, (real_x, real_y))
