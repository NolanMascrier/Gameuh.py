"""A widget is something that can be displayed at the screen. It has
a x.y position, a width, a height and a center."""

class Widget():
    """Define a widget by its coordinates.

    Args:
        x (float, optional): x position of the widget.
        y (float, optional): y position of the widget.
        width (float, optional): width of the widget.
        height (float, optional): height of the widget.
    """
    def __init__(self, x: float = 0, y: float = 0, width: float = 0, height: float = 0):
        self._x = x
        self._y = y
        self._width = width
        self._height = height

    @property
    def left(self) -> float:
        """Return's the widget's leftmost x."""
        return self._x

    @property
    def right(self) -> float:
        """Return's the widget's rightmost x."""
        return self._x + self._width

    @property
    def top(self) -> float:
        """Return's the widget's top y."""
        return self._y

    @property
    def bottom(self) -> float:
        """Return's the widget's rightmost y."""
        return self._y + self._height

    @property
    def x(self) -> float:
        """Return's the widget x value."""
        return self._x

    @x.setter
    def x(self, value):
        self._x = value

    @property
    def y(self) -> float:
        """Return's the widget y value."""
        return self._y

    @y.setter
    def y(self, value):
        self._y = value

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
        self._x = x if isinstance(x, float) else x[0]
        self._y = y if isinstance(x, float) else x[1]
