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

    def descript(self):
        """Generates a description of the affix."""
        if self._value == 0:
            return "\n"
        if Flags.DESC_FLAT not in self._flags:
            value = f"{self._value * 100}%"
        else:
            value = f"{self._value}"
        if Flags.BOON in self._flags:
            adds = f"{value} increased "
        elif Flags.HEX in self._flags:
            adds = f"{value} decreased "
        elif Flags.BLESS in self._flags:
            adds = f"{value} more"
        elif Flags.CURSE in self._flags:
            adds = f"x{value} less"
        elif Flags.FLAT in self._flags:
            if self._value < 0:
                adds = f"{value}"
            else:
                adds = f"+{value}"

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
    def flags(self):
        """Return's the affix flag."""
        return self._flags

    @flags.setter
    def flags(self, value):
        self._flags = value
