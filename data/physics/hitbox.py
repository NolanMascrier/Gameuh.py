"""Defines an hitbox, a basic square that can
be in collision with another one."""

from data.api.widget import Widget

class HitBox(Widget):
    """Defines an hitbox."""
    def __init__(self, x, y, w, h):
        super().__init__(x, y, w, h)
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
        return (self.x, self.y, self._width, self._height)

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
        self.x = pos[0]
        self.y = pos[1]

    def move_center(self, pos: tuple):
        """Moves the box's center to a new position."""
        self.center = pos

    def expand(self, height, width):
        """Expands the hitbox."""
        self.x -= width
        self.y -= height
        self._width += 2 * width
        self._height += 2 * height

    @property
    def center_offset(self):
        """Returns the x;y position of the box's
        including the offset."""
        x = self.left + self._offset[0]
        y = self.top + self._offset[1]
        return (x, y)
