"""A component that houses slots. Used for
inventories and such"""

from collections.abc import Iterable
from data.constants import SYSTEM
from data.image.slot import Slot
from data.image.draggable import Draggable
from data.interface.render import render

class SlotPanel:
    """Defines a slot pannel, a group of slots.
    
    Ags:
        x (int): x position of the panel.
        y (int): y position of the panel.
        slot_size (int, optional): Size of a slot. Defaults\
        to the default size of a slot, 64.
        padding (int, optional): How much padding in pixels should\
        be done on each inner side of the pannel. Defaults to 16.
        default (list, optional): A list of default items that should\
        be inside the panel by default. Can be anything containable inside\
        a draggable. Defaults to []
        background (Image, optional): Background image of the panel. Defaults\
        to SYSTEM["images"]["tile_panel_back"].
        immutable (bool, optional): Whether or not the panel should be immutable\
        , ie the user can't add items inside, and if they take one, it'll stay inside.\
        Defaults to `False`.
        filter (Flags, optional): What flag to use to filter out the data. Defaults\
        to None.
    """
    def __init__(self, x, y, slot_size=64, padding = 16, default = None, background = None,\
        immutable = False, filter = None):
        self._x = x
        self._y = y
        self._slot_size = slot_size
        if background is None:
            self._background = SYSTEM["images"]["tile_panel_back"]
        else:
            self._background = background
        self._padding = padding
        self._slots = []
        self._columns = (self._background.width - self._padding * 2) // slot_size - 1
        self._lines = (self._background.height - self._padding * 2) // slot_size - 1
        self._default = default
        self._scroll = 0
        self._immutable = immutable
        self._filter = filter
        if isinstance(default, Iterable):
            for item in default:
                y, x = self.get_index()
                drag = Draggable(None, x, y, item, immutable)
                self.insert(drag)

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

    def refresh(self):
        """Refresh the content of the panel and redraws them."""
        self._slots.clear()
        if isinstance(self._default, Iterable):
            for item in self._default:
                y, x = self.get_index()
                drag = Draggable(None, x, y, item)
                self.insert(drag)

    def insert(self, drag: Draggable, pos = None, as_item = None):
        """Inserts the draggable into the panel."""
        y, x = self.get_index()
        if drag is None and as_item is not None:
            drag = Draggable(None, x, y, as_item, self._immutable)
        if drag is None:
            return
        sl = Slot(x, y, immutable=self._immutable)
        sl.insert(drag)
        drag.set_panel(self)
        SYSTEM["dragged"] = None
        if pos is not None:
            self._slots.insert(pos, sl)
            self._default.remove(drag.contains)
            self._default.insert(pos, drag.contains)
        else:
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
            if slot.contains is not None and self._filter is not None\
                and self._filter not in slot.contains.contains.flags:
                continue
            elif slot.contains.dragging:
                self._slots.remove(slot)
            else:
                slot.contains.tick()
        self._slots = [slot for slot in self._slots if not slot.empty\
                            and not slot.contains.dragging]
        if not SYSTEM["mouse_click"][0]:
            self.try_insert(SYSTEM["dragged"])
        if self.is_hovered():
            if SYSTEM["mouse_wheel"][0][1] < SYSTEM["mouse_wheel"][1][1]:
                self._scroll = max(self._scroll - 1, 0)
            elif SYSTEM["mouse_wheel"][0][1] > SYSTEM["mouse_wheel"][1][1]:
                self._scroll = min(self._scroll + 1, len(self._slots) // (self._columns + 1)\
                    - (self._lines + 1) + 1)
        return self

    def __get_pos(self):
        """Attemps to search the position"""
        i = 0
        lin = 0
        col = 0
        for _ in self._slots:
            x = self._x + col * self._slot_size
            y = self._y + lin * self._slot_size
            if SYSTEM["mouse"][0] > x and SYSTEM["mouse"][0] < x + self._slot_size and\
                SYSTEM["mouse"][1] > y and SYSTEM["mouse"][1] < y + self._slot_size:
                return i
            col += 1
            if col > self._columns:
                col = 0
                lin += 1
            i += 1
        return None

    def try_insert(self, draggable: Draggable):
        """Attempts to insert draggable if it's dropped on the slot."""
        if draggable is None:
            return False
        if self.is_hovered():
            pos = self.__get_pos()
            if self._immutable != draggable.immutable:
                SYSTEM["dragged"] = None
                return False
            if self._immutable:
                draggable.set_panel(None)
                draggable.set_parent(None)
                SYSTEM["dragged"] = None
                return True
            self.insert(draggable, pos)
            return True
        return False

    def draw(self):
        """Draws the component."""
        render(self._background.get_image(), (self._x, self._y))
        diff_x, x = 0, 0
        diff_y, y = 0, 0
        real_x = self._x + self._padding + x * self._slot_size
        real_y = self._y + self._padding + y * self._slot_size
        for slot in self._slots:
            if slot.contains is not None and self._filter is not None\
                and self._filter not in slot.contains.contains.flags:
                continue
            diff_x += 1
            if diff_x > self._columns:
                diff_x = 0
                diff_y += 1
            if diff_y < self._scroll:
                continue
            if slot.contains is SYSTEM["dragged"]:
                continue
            real_x = self._x + self._padding + x * self._slot_size
            real_y = self._y + self._padding + y * self._slot_size
            if SYSTEM["dragged"] is not None and not self._immutable and\
                SYSTEM["mouse"][0] > real_x and SYSTEM["mouse"][0] < real_x + self._slot_size and\
                SYSTEM["mouse"][1] > real_y and SYSTEM["mouse"][1] < real_y + self._slot_size:
                x += 1
                if x > self._columns:
                    x = 0
                    y += 1
                real_x = self._x + self._padding + x * self._slot_size
                real_y = self._y + self._padding + y * self._slot_size
            if y <= self._lines:
                slot.draw_alt(SYSTEM["windows"], real_x, real_y)
                slot.contains.set(real_x, real_y)
            x += 1
            if x > self._columns:
                x = 0
                y += 1
        if y <= self._lines:
            real_x = self._x + self._padding + x * self._slot_size
            real_y = self._y + self._padding + y * self._slot_size
            if x > self._columns:
                x = 0
                y += 1
            render(SYSTEM["images"]["slot_empty"].image, (real_x, real_y))

    @property
    def slots(self):
        """Returns the slots."""
        return self._slots

    @slots.setter
    def slots(self, value):
        self._slots = value
