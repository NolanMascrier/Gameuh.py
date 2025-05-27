"""An affliction is a debuff or a buff. It has
a name, a value, a duration, flags."""

class Affliction():
    """Defines an affliction. An affliction is a temporary \
    stat modifier.
    
    Args:
        name (str): Name of the affliction.
        value (float): Value of the affliction.
        duration (int, optionnal): Duration in turns of the\
        affliction. Defaults to 1.
        flags (list, optionnal): Flags of the afflictions.\
        Defaults to `None`.
        stackable (bool, optionnal): Wether or not the affliction\
        is stackable. Defaults to `False`.
    """
    def __init__(self, name, value, duration = 1, flags: list = None, stackable = False):
        self._name = name
        self._value = value
        self._duration = duration
        if flags is None:
            self._flags = []
        else:
            self._flags = flags
        self._stackable = stackable

    @DeprecationWarning
    def get(self):
        """Returns the affliction as a list to use \
        in Stats and ressources.

        Returns:
            list : Formatted affliction.
        """
        return [self._name, self._value, self._duration]

    def tick(self):
        """Ticks down the timer.
        """
        if self._duration > 0:
            self._duration -= 0.016

    def __eq__(self, other):
        if not isinstance(other, Affliction):
            return False
        if self._name == other._name:
            return True
        return False

    @property
    def name(self) -> str:
        """Returns the affliction's name."""
        return self._name

    @name.setter
    def name(self, value):
        self._name = value

    @property
    def value(self) -> float:
        """Returns the affliction's value."""
        return self._value

    @value.setter
    def value(self, value):
        self._value = value

    @property
    def duration(self) -> int:
        """Returns the affliction's duration."""
        return self._duration

    @duration.setter
    def duration(self, value):
        self._duration = value

    @property
    def flags(self):
        """Returns the affliction's flag list."""
        return self._flags

    @flags.setter
    def flags(self, value):
        self._flags = value

    @property
    def stackable(self) -> bool:
        """Returns wether or not the affliction is stackable."""
        return self._stackable

    @stackable.setter
    def stackable(self, value):
        self._stackable = value
