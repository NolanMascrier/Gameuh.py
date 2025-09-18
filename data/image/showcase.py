"""Showcase panel, for level endings. Vibecoded because I was feeling lazy that day"""

from collections.abc import Iterable
import pygame

from data.image.slotpanel import SlotPanel
from data.image.slot import Slot
from data.image.draggable import Draggable
from data.interface.render import render
from data.constants import SYSTEM

class ShowCase(SlotPanel):
    """
    Showcase with one-by-one pop-in animation. Uses the exact same slot
    iteration logic as draw() to compute where the next (empty) slot will
    be displayed and locks that index+coords when an animation starts.
    Also auto-scrolls so the animating slot is visible.
    """
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
        """
        Returns a tuple:
          (insertion_index, target_x, target_y, target_col, target_line)
        Where target_col/target_line are the logical grid coordinates used
        by draw() (col=x, line=y) so we can compute visibility and scroll.
        """
        diff_x = diff_y = 0
        x = y = 0
        i = 0
        for slot in self._slots:
            if slot.contains is not None and self._filter is not None:
                try:
                    if self._filter not in slot.contains.contains.flags:
                        i += 1
                        continue
                except Exception:
                    i += 1
                    continue
            diff_x += 1
            if diff_x > self._columns:
                diff_x = 0
                diff_y += 1
            if diff_y < self._scroll:
                i += 1
                continue
            if slot.contains is SYSTEM["dragged"]:
                i += 1
                continue
            # compute the real draw position for this slot (but we also need grid coords)
            real_x = self._x + self._padding + x * self._slot_size
            real_y = self._y + self._padding + y * self._slot_size
            # advance the grid position exactly like draw()
            x += 1
            if x > self._columns:
                x = 0
                y += 1
            i += 1

        # after iterating existing slots, (x,y) are the column/line for the empty next slot
        if x > self._columns:
            x = 0
            y += 1
        target_x = self._x + self._padding + x * self._slot_size
        target_y = self._y + self._padding + y * self._slot_size
        return i, target_x, target_y, x, y

    def _surface_from_item(self, item):
        return item.get_image().image

    def try_insert(self, draggable: Draggable):
        return False

    def remove(self, drag: Draggable):
        return

    def __get_pos(self):
        return None

    def tick(self):
        # start next animation and lock target using simulated draw loop
        if self._current_anim is None and len(self._incoming) > 0:
            next_item = self._incoming.pop(0)
            t_idx, t_x, t_y, t_col, t_line = self._next_slot_info()

            # === AUTO-SCROLL: ensure target_line is visible ===
            visible_top = self._scroll
            visible_bottom = self._scroll + self._lines  # inclusive (y <= self._lines is visible)
            # compute max_scroll anticipating the incoming item
            cols_per_row = (self._columns + 1)
            max_scroll = max(((len(self._slots) + 1) // cols_per_row) - (self._lines + 1) + 1, 0)

            if t_line < visible_top:
                # scroll up so the target_line becomes top
                new_scroll = max(0, t_line)
                self._scroll = min(max_scroll, new_scroll)
            elif t_line > visible_bottom:
                # scroll down so the target_line becomes the bottom-most visible line
                new_scroll = t_line - self._lines
                self._scroll = min(max_scroll, max(0, new_scroll))
            # ===================================================

            self._current_anim = {
                "item": next_item,
                "progress": 0.0,
                "target_index": t_idx,
                "target_x": t_x,
                "target_y": t_y,
                "target_col": t_col,
                "target_line": t_line
            }

        # advance animation and finalize at locked coords/index
        if self._current_anim is not None:
            self._current_anim["progress"] += self._anim_speed
            if self._current_anim["progress"] >= 1.0:
                itm = self._current_anim["item"]
                t_idx = self._current_anim["target_index"]
                t_x = self._current_anim["target_x"]
                t_y = self._current_anim["target_y"]
                drag = Draggable(None, t_x, t_y, itm, True)
                sl = Slot(t_x, t_y, immutable=True)
                sl.insert(drag)
                drag.set_panel(self)
                SYSTEM["dragged"] = None
                if t_idx >= len(self._slots):
                    self._slots.append(sl)
                else:
                    self._slots.insert(t_idx, sl)
                self._current_anim = None

        # contained items tick
        for slot in self._slots:
            if slot.contains is None:
                continue
            if self._filter is not None:
                try:
                    if self._filter not in slot.contains.contains.flags:
                        continue
                except Exception:
                    pass
            try:
                slot.contains.tick()
            except Exception:
                pass

        # keep scroll logic from user wheel (no insertion allowed)
        if self.is_hovered():
            if SYSTEM["mouse_wheel"][0][1] < SYSTEM["mouse_wheel"][1][1]:
                self._scroll = max(self._scroll - 1, 0)
            elif SYSTEM["mouse_wheel"][0][1] > SYSTEM["mouse_wheel"][1][1]:
                max_scroll = max(len(self._slots) // (self._columns + 1) - (self._lines + 1) + 1, 0)
                self._scroll = min(self._scroll + 1, max_scroll)
        return self

    def draw(self):
        render(self._background.get_image(), (self._x, self._y))
        diff_x = diff_y = 0
        x = y = 0
        for slot in self._slots:
            if slot.contains is not None and self._filter is not None:
                try:
                    if self._filter not in slot.contains.contains.flags:
                        continue
                except Exception:
                    pass
            diff_x += 1
            if diff_x > self._columns:
                diff_x = 0
                diff_y += 1
            if diff_y < self._scroll:
                continue
            real_x = self._x + self._padding + x * self._slot_size
            real_y = self._y + self._padding + y * self._slot_size
            if y <= self._lines:
                slot.draw_alt(SYSTEM["windows"], real_x, real_y)
                try:
                    slot.contains.set(real_x, real_y)
                except Exception:
                    pass
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
            try:
                render(SYSTEM["images"]["slot_empty"].image, (real_x, real_y))
            except Exception:
                try:
                    render(SYSTEM["images"]["slot_empty"].get_image(), (real_x, real_y))
                except Exception:
                    pass
        if self._current_anim is not None:
            progress = max(0.0, min(1.0, self._current_anim["progress"]))
            scale = self._start_scale + (1.0 - self._start_scale) * progress

            t_x = self._current_anim["target_x"]
            t_y = self._current_anim["target_y"]
            surf = self._surface_from_item(self._current_anim["item"])
            if surf is not None and isinstance(surf, pygame.Surface):
                scaled_size = int(round(self._slot_size * scale))
                try:
                    scaled = pygame.transform.smoothscale(surf, (scaled_size, scaled_size))
                except Exception:
                    scaled = pygame.transform.scale(surf, (scaled_size, scaled_size))
                center_x = t_x + self._slot_size // 2
                center_y = t_y + self._slot_size // 2
                draw_x = center_x - scaled.get_width() // 2
                draw_y = center_y - scaled.get_height() // 2
                render(scaled, (draw_x, draw_y))
