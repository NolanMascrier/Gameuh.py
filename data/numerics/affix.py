"""An affix is a modifier for an item."""

from data.constants import Flags
from data.numerics.affliction import Affliction

class Affix():
    """An affix a single modifier for an item.

    Args:
        name (str): name of the modifier.
        value (float): value of the modifier.
        flags (list[Flags]): Flag of the modifier.
    """
    def __init__(self, name, value, flag):
        self._name = name
        self._value = value
        self._flags = flag

    def as_affliction(self) -> Affliction:
        """Makes the affix into an affliction."""
        flags = self._flags.copy()
        flags.append(Flags.GEAR)
        return Affliction(f"{self._name}_effect", self._value, -1, flags)

    @property
    def name(self):
        """Return the affix's name."""
        return self._name

    @name.setter
    def name(self, value):
        self._name = value

    @property
    def value(self):
        """Return the affix's value."""
        return self._value

    @value.setter
    def value(self, value):
        self._value = value

    @property
    def flag(self):
        """Return's the affix flag."""
        return self._flag

    @flag.setter
    def flag(self, value):
        self._flag = value
