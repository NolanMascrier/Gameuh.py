"""An hoverable is a pop up that shows text when
the mouse is above it."""

from data.api.surface import Surface, Widget

from data.constants import SYSTEM
from data.image.text import Text
from data.interface.render import render

class Hoverable(Widget):
    """Defines an hoverable."""
    def __init__(self, x:int, y:int, text:str, hoverable_text:str, text_color=(255, 255, 255),\
        surface: Surface = None, override: Surface = None,\
        alternative:Surface = None, hover_color=(255,255,255), scrollable = None):
        super().__init__(x, y)
        if text is None:
            self._text = None
        else:
            if isinstance(text, str):
                text = [text]
            self._text = Text('\n'.join(text), font="item_desc", default_color=text_color)
        if hoverable_text is not None:
            if isinstance(hoverable_text, str):
                hoverable_text = [hoverable_text]
            self._hoverable = Text('\n'.join(hoverable_text), font="item_desc",\
                                default_color=hover_color)
        else:
            self._hoverable = None
        self._attach = surface
        self._override = override
        self._alternative = alternative
        self._scrollable = scrollable
        self._surface = None
        if self._attach is not None:
            self.width = self._attach.width
            self.height = self._attach.height
        else:
            self.width = self._text.width
            self.height = self._text.height
        self.update_surface()

    def set(self, x, y):
        """Sets the x;y position of the hoverable."""
        super().set(x, y)
        return self

    def update_surface(self):
        """Updates the surface."""
        if self._override is None:
            if self._hoverable is None:
                self._surface = None
                return
            w = self._hoverable.width
            h = self._hoverable.height
            surface = SYSTEM["images"]["hoverable"].duplicate(w + 5, h + 5)
            sfc = Surface(surface.get_width(), surface.get_height())
            sfc.blit(surface, (0, 0), True)
            sfc.blit(self._hoverable.surface, (7, 7), True)
            if SYSTEM["mouse"][0] - w < 0:
                w += SYSTEM["mouse"][0] - w
        else:
            if "alt_popup" in SYSTEM["keys"]:
                sfc = self._alternative
            else:
                sfc = self._override
        self._surface = sfc

    def __is_mouse_over(self):
        """Checks whether or not the mouse is over the hoverable surface."""
        if self._text is not None:
            txt = self._text.width, self._text.height
        elif self._attach is not None:
            txt = self._attach.get_size()
        else:
            return False
        if SYSTEM["mouse"][0] >= self.x and SYSTEM["mouse"][0] <= self.x + txt[0] and\
            SYSTEM["mouse"][1] >= self.y and SYSTEM["mouse"][1] <= self.y + txt[1]:
            return True
        return False

    def tick(self):
        """Checks whether or not the mouse is within the hoverable's\
        area, and displays the text if it does."""
        if self.__is_mouse_over():
            if self._override is None:
                sfc = self._surface
            else:
                if "alt_popup" in SYSTEM["keys"]:
                    sfc = self._alternative
                else:
                    sfc = self._override
            if sfc is None:
                return self
            w = sfc.get_width()
            h = sfc.get_height()
            SYSTEM["pop_up"] = (sfc, w, h)
        return self

    def draw(self, surface = None):
        """Draws the text to the window."""
        if surface is None:
            render(self._text.surface, (self.x, self.y))
            return
        surface.blit(self._text.surface, (self.x, self.y), True)
