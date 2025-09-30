"""Defines an hitbox, a basic square that can
be in collision with another one."""

class HitBox():
    """Defines an hitbox."""
    def __init__(self, x, y, w, h):
        self._x = x
        self._y = y
        self._width = w
        self._height = h
        self._offset = (0, 0)

    def is_inside(self, pos: tuple) -> bool:
        """Checks wether the x;y position is inside the box.
        
        Returns:
            bool: `True` if the point is inside.
        """
        if pos[0] < self.left or pos[0] > self.right:
            return False
        if pos[1] < self.top or pos[1] > self.bottom:
            return False
        return True

    def is_colliding(self, other) -> bool:
        """Checks wether two hitboxes are colliding or not."""
        if not isinstance(other, HitBox):
            return False
        if self.left > other.right or self.right < other.left:
            return False
        if self.top > other.bottom or self.bottom < other.top:
            return False
        return True

    def get_rect(self) -> tuple:
        """Return's the hitbox as a rect tuple."""
        return (self._x, self._y, self._width, self._height)

    def resize(self, values, scale_factor = None):
        """Resizes the hitbox and recenters it.
        
        Args:
            values (tuple): Tuple of 4 values in that order: `width`, `height`,\
            `x offset` and `y_offset`.
            scale_factor (tuple, optional): Scale factor of the image. Resizes the\
            hitbox if the origin image was.
        """
        w, h, offset_x, offset_y = values
        center = self.center
        self._offset = (offset_x, offset_y)
        if scale_factor is not None:
            self._offset = (offset_x * scale_factor[0], offset_y * scale_factor[1])
        self._width *= w
        self._height *= h
        self.move_center(center)

    def move(self, pos: tuple):
        """Moves the box to a new position."""
        self._x = pos[0]
        self._y = pos[1]

    def move_center(self, pos: tuple):
        """Moves the box's center to a new position."""
        self._x = pos[0] - self._width / 2
        self._y = pos[1] - self._height / 2

    def expand(self, height, width):
        """Expands the hitbox."""
        self._x -= width
        self._y -= height
        self._width += 2 * width
        self._height += 2 * height

    @property
    def left(self):
        """Return's the box's leftmost x."""
        return self._x

    @property
    def right(self):
        """Return's the box's rightmost x."""
        return self._x + self._width

    @property
    def top(self):
        """Return's the box's top y."""
        return self._y

    @property
    def bottom(self):
        """Return's the box's rightmost y."""
        return self._y + self._height

    @property
    def x(self):
        """Return's the hitbox x value."""
        return self._x

    @x.setter
    def x(self, value):
        self._x = value

    @property
    def y(self):
        """Return's the hitbox y value."""
        return self._y

    @y.setter
    def y(self, value):
        self._y = value

    @property
    def width(self):
        """Return's the hitbox width."""
        return self._width

    @width.setter
    def width(self, value):
        self._width = value

    @property
    def height(self):
        """Return's the hitbox height."""
        return self._height

    @height.setter
    def height(self, value):
        self._height = value

    @property
    def center_x(self):
        """Returns the x position of the box's center."""
        return self.left + (self._width / 2)

    @property
    def center_y(self):
        """Returns the x position of the box's center."""
        return self.top + (self._height / 2)

    @property
    def center(self):
        """Returns the x;y position of the box's
        center."""
        x = self.left + (self._width / 2)
        y = self.top + (self._height / 2)
        return (x, y)

    @property
    def center_offset(self):
        """Returns the x;y position of the box's
        including the offset."""
        x = self.left + self._offset[0]
        y = self.top + self._offset[1]
        return (x, y)
