"""A scrollable is a surface that can be moved  around
by clicking and dragging the mouse."""

import pygame
from data.constants import SYSTEM
from data.image.animation import Animation, Image
from data.interface.render import render

class Scrollable():
    """Defines a scrollable surface, which contains another that
    can be moved around."""
    def __init__(self, x, y, width, height, padding = 5,\
        background:Image|Animation = None, contains: pygame.Surface = None):
        self._x = x
        self._y = y
        self._width = width
        self._height = height
        self._padding = padding
        self._background = background
        self._contains = contains
        self._diff_x = 0
        self._diff_y = 0
        self._prev_diff_x = 0
        self._prev_diff_y = 0
        self._dragging = False
        self._subsurface = pygame.Surface((width - padding * 2, height - padding * 2),\
                                                                    pygame.SRCALPHA)

    def mouse_inside(self):
        """Checks whether or not the mouse is inside the scrollable area."""
        if SYSTEM["mouse"][0] < self._x + self._padding:
            return False
        if SYSTEM["mouse"][0] > self._x - self._padding + self._width:
            return False
        if SYSTEM["mouse"][1] < self._y + self._padding:
            return False
        if SYSTEM["mouse"][1] > self._y - self._padding + self._height:
            return False
        return True

    def coordinates(self, x, y):
        """Converts the x;y position of the contained surface
        into 'real' coordinates (on screen).
        Returns -1; -1 if the coordinates are not on screen."""
        screen_x = self._x + self._padding + x + self._diff_x
        screen_y = self._y + self._padding + y + self._diff_y

        # Determine bounds of the visible area
        view_x1 = self._x + self._padding
        view_y1 = self._y + self._padding
        view_x2 = view_x1 + self._width - self._padding * 2
        view_y2 = view_y1 + self._height - self._padding * 2

        # If the adjusted coordinate is outside the visible area, return -1, -1
        if not (view_x1 <= screen_x < view_x2 and view_y1 <= screen_y < view_y2):
            return -1, -1

        return screen_x, screen_y

    def coordinates_rectangle(self, x, y, h, w):
        """Converts a rectangle made of 4 data (x;y position of
        upper left corner, width and height) into a rectangle that
        is within the scrollable area (ie resize the clickable area
        of a button). Returns None if the button is fully unreachable.
        """
        screen_x = self._x + self._padding + x + self._diff_x
        screen_y = self._y + self._padding + y + self._diff_y

        view_x1 = self._x + self._padding
        view_y1 = self._y + self._padding
        view_x2 = view_x1 + self._width - self._padding * 2
        view_y2 = view_y1 + self._height - self._padding * 2

        rect_x2 = screen_x + w
        rect_y2 = screen_y + h

        # Fully outside
        if screen_x >= view_x2 or rect_x2 <= view_x1 or \
        screen_y >= view_y2 or rect_y2 <= view_y1:
            return None

        # Clip to viewport
        clipped_x = max(screen_x, view_x1)
        clipped_y = max(screen_y, view_y1)
        clipped_w = min(rect_x2, view_x2) - clipped_x
        clipped_h = min(rect_y2, view_y2) - clipped_y

        return clipped_x, clipped_y, clipped_w, clipped_h

    def tick(self):
        """Ticks down the scrollable."""
        if self.mouse_inside() and SYSTEM["mouse_click"][0]:
            self._dragging = True
        elif not SYSTEM["mouse_click"][0]:
            self._dragging = False
            self._prev_diff_x = self._diff_x
            self._prev_diff_y = self._diff_y
        if self._dragging:
            self._diff_x = SYSTEM["mouse"][0] - SYSTEM["mouse_previous"][0] + self._prev_diff_x
            self._diff_y = SYSTEM["mouse"][1] - SYSTEM["mouse_previous"][1] + self._prev_diff_y
            self._diff_x = max(min(self._diff_x, 0),\
                self._subsurface.get_width() - self._contains.get_width())
            self._diff_y = max(min(self._diff_y, 0),\
                self._subsurface.get_height() - self._contains.get_height())
        return self

    def draw(self):
        """Draws the surface and the contained surface."""
        if self._background is not None:
            render(self._background.get_image(), (self._x, self._y))
        self._subsurface = pygame.Surface((self._width - self._padding * 2,\
                                            self._height - self._padding * 2),\
                                                                    pygame.SRCALPHA)
        if self._contains is not None:
            self._subsurface.blit(self._contains, (self._diff_x, self._diff_y))
        render(self._subsurface, (self._x + self._padding, self._y + self._padding))

    @property
    def x(self):
        """Returns the scrollable's x value."""
        return self._x

    @x.setter
    def x(self, value):
        self._x = value

    @property
    def y(self):
        """Returns the scrollable's x value."""
        return self._y

    @y.setter
    def y(self, value):
        self._y = value

    @property
    def width(self):
        """Returns the scrollable's width."""
        return self._width

    @width.setter
    def width(self, value):
        self._width = value

    @property
    def height(self):
        """Returns the scrollable's height value."""
        return self._height

    @height.setter
    def height(self, value):
        self._height = value

    @property
    def padding(self):
        """Returns the scrollable's padding."""
        return self._padding

    @padding.setter
    def padding(self, value):
        self._padding = value

    @property
    def background(self):
        """Returns the scrollable's background."""
        return self._background

    @background.setter
    def background(self, value):
        self._background = value

    @property
    def contains(self):
        """Returns the scrollable's contained surface."""
        return self._contains

    @contains.setter
    def contains(self, value):
        self._contains = value

    @property
    def diff_x(self):
        """Returns the scrollable's x difference."""
        return self._diff_x

    @property
    def diff_y(self):
        """Returns the scrollable's y difference."""
        return self._diff_y
