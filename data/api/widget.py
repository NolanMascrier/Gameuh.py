"""A widget is something that can be displayed at the screen. It has
a x.y position, a width, a height and a center."""

from data.api.vec2d import Vec2

class Widget():
    """Define a widget by its coordinates.

    Args:
        x (float, optional): x position of the widget.
        y (float, optional): y position of the widget.
        width (float, optional): width of the widget.
        height (float, optional): height of the widget.
    """
    def __init__(self, x: float = 0, y: float = 0, width: float = 0, height: float = 0):
        self._position = Vec2(x, y)
        self._width = width
        self._height = height

    def set(self, x, y):
        """Sets both coordinates."""
        self._position = Vec2(x, y)

    @property
    def left(self) -> float:
        """Return's the widget's leftmost x."""
        return self.x

    @property
    def right(self) -> float:
        """Return's the widget's rightmost x."""
        return self.x + self._width

    @property
    def top(self) -> float:
        """Return's the widget's top y."""
        return self.y

    @property
    def bottom(self) -> float:
        """Return's the widget's rightmost y."""
        return self.y + self._height

    @property
    def x(self) -> float:
        """Return's the widget x value."""
        return self._position.x

    @x.setter
    def x(self, value):
        self._position.x = value

    @property
    def y(self) -> float:
        """Return's the widget y value."""
        return self._position.y

    @y.setter
    def y(self, value):
        self._position.y = value

    @property
    def width(self) -> float:
        """Return's the widget width."""
        return self._width

    @width.setter
    def width(self, value):
        self._width = value

    @property
    def height(self) -> float:
        """Return's the widget height."""
        return self._height

    @height.setter
    def height(self, value):
        self._height = value

    @property
    def center_x(self) -> float:
        """Returns the x position of the widget's center."""
        return self.left + (self._width / 2)

    @property
    def center_y(self) -> float:
        """Returns the x position of the widget's center."""
        return self.top + (self._height / 2)

    @property
    def center(self) -> tuple[float|float]:
        """Returns the x;y position of the widget's
        center."""
        return (self.center_x, self.center_y)

    @center.setter
    def center(self, x:float|tuple, y:float = 0):
        center_x = x if isinstance(x, float) else x[0]
        center_y = y if isinstance(x, float) else x[1]
        self._position.x = center_x - self._width / 2
        self._position.y = center_y - self._height / 2
