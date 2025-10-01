from collections.abc import Iterable

from data.api.surface import Surface

from data.image.slotpanel import SlotPanel
from data.image.slot import Slot
from data.image.draggable import Draggable
from data.interface.render import render
from data.constants import SYSTEM

class ShowCase(SlotPanel):
    def __init__(self, x, y, slot_size=64, padding=16, default=None,
                 background=None, immutable=True, display_filter=None,
                 anim_speed=0.12, start_scale=2.1):
        super().__init__(x, y, slot_size=slot_size, padding=padding,
                         default=None, background=background,
                         immutable=True, display_filter=display_filter)

        self._incoming = list(default) if isinstance(default, Iterable) else []
        self._current_anim = None
        self._anim_speed = float(anim_speed)
        self._start_scale = float(start_scale)
        self._immutable = True

    def _next_slot_info(self):
        i = len(self._slots)
        x = i % (self._columns + 1)
        y = i // (self._columns + 1)
        return i, x, y

    def _surface_from_item(self, item):
        return item.get_image().image

    def try_insert(self, draggable: Draggable):
        return False

    def remove(self, drag: Draggable):
        return

    def _coords_from_grid(self, col, line):
        real_x = self.x + self._padding + col * self._slot_size
        real_y = self.y + self._padding + (line - self._scroll) * self._slot_size
        return real_x, real_y

    def tick(self):
        if self._current_anim is None and len(self._incoming) > 0:
            next_item = self._incoming.pop(0)
            t_idx, t_col, t_line = self._next_slot_info()
            cols_per_row = self._columns + 1
            max_scroll = max(((len(self._slots)) // cols_per_row) - (self._lines + 1) + 1, 1)
            visible_bottom = self._scroll + self._lines
            if t_line > visible_bottom:
                new_scroll = t_line - (self._lines - 1)
                self._scroll = min(max_scroll, max(0, new_scroll))
            self._current_anim = {
                "item": next_item,
                "rarity": next_item.rarity,
                "progress": 0.0,
                "target_index": t_idx,
                "target_col": t_col,
                "target_line": t_line
            }
        if self._current_anim is not None:
            self._current_anim["progress"] += self._anim_speed
            if self._current_anim["progress"] >= 1.0:
                itm = self._current_anim["item"]
                col = self._current_anim["target_col"]
                line = self._current_anim["target_line"]
                real_x, real_y = self._coords_from_grid(col, line)
                drag = Draggable(None, real_x, real_y, itm, True)
                sl = Slot(real_x, real_y, immutable=True)
                sl.insert(drag)
                drag.set_panel(self)
                SYSTEM["dragged"] = None
                self._slots.append(sl)
                self._current_anim = None
        for slot in self._slots:
            if slot.contains is None:
                continue
            if self._filter is not None:
                if self._filter not in slot.contains.contains.flags:
                    continue
            slot.contains.tick()
        if self.is_hovered():
            if SYSTEM["mouse_wheel"][0][1] < SYSTEM["mouse_wheel"][1][1]:
                self._scroll = max(self._scroll - 1, 0)
            elif SYSTEM["mouse_wheel"][0][1] > SYSTEM["mouse_wheel"][1][1]:
                max_scroll = max(len(self._slots) // (self._columns + 1) - (self._lines + 1) + 1, 0)
                self._scroll = min(self._scroll + 1, max_scroll)
        return self

    def draw(self):
        render(self._background.get_image(), (self.x, self.y))
        diff_x = diff_y = 0
        x = y = 0
        for slot in self._slots:
            if slot.contains is not None and self._filter is not None:
                if self._filter not in slot.contains.contains.flags:
                    continue
            diff_x += 1
            if diff_x > self._columns:
                diff_x = 0
                diff_y += 1
            if diff_y < self._scroll:
                continue
            real_x = self.x + self._padding + x * self._slot_size
            real_y = self.y + self._padding + y * self._slot_size
            if y <= self._lines:
                slot.draw_alt(SYSTEM["windows"], real_x, real_y)
                slot.contains.set(real_x, real_y)
            x += 1
            if x > self._columns:
                x = 0
                y += 1
        if y <= self._lines:
            real_x = self.x + self._padding + x * self._slot_size
            real_y = self.y + self._padding + y * self._slot_size
            if x > self._columns:
                x = 0
                y += 1
            if self._current_anim is not None:
                match self._current_anim["rarity"]:
                    case 1:
                        render(SYSTEM["images"]["slot_magic"].image, (real_x, real_y))
                    case 2:
                        render(SYSTEM["images"]["slot_rare"].image, (real_x, real_y))
                    case 3:
                        render(SYSTEM["images"]["slot_exalted"].image, (real_x, real_y))
                    case 4:
                        render(SYSTEM["images"]["slot_unique"].image, (real_x, real_y))
                    case _:
                        render(SYSTEM["images"]["slot_empty"].image, (real_x, real_y))
            else:
                render(SYSTEM["images"]["slot_empty"].image, (real_x, real_y))
        if self._current_anim is not None:
            progress = max(0.0, min(1.0, self._current_anim["progress"]))
            scale = self._start_scale + (1.0 - self._start_scale) * progress
            col = self._current_anim["target_col"]
            line = self._current_anim["target_line"]
            real_x, real_y = self._coords_from_grid(col, line)
            surf = self._surface_from_item(self._current_anim["item"])
            if surf is not None and isinstance(surf, Surface):
                base = surf.copy()
                scaled_size = int(self._slot_size * scale)
                scaled = base.scale((scaled_size, scaled_size))
                center_x = real_x + self._slot_size // 2
                center_y = real_y + self._slot_size // 2
                draw_x = center_x - scaled.get_width() // 2
                draw_y = center_y - scaled.get_height() // 2
                render(scaled, (draw_x, draw_y))
