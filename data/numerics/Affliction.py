"""An affliction is a debuff or a buff. It has
a name, a value, a duration, flags."""

from data.constants import Flags

class Affliction():
    def __init__(self, name, value, duration = 1, flags: list[Flags] = [], stackable = False):
        self._name = name
        self._value = value
        self._duration = duration
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
            self._duration -= 1
    
    def __eq__(self, other):
        if not isinstance(other, Affliction):
            return False
        if self._name == other._name:
            return True
        return False

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        self._name = value

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, value):
        self._value = value

    @property
    def duration(self):
        return self._duration

    @duration.setter
    def duration(self, value):
        self._duration = value

    @property
    def flags(self):
        return self._flags

    @flags.setter
    def flags(self, value):
        self._flags = value
    
    @property
    def stackable(self):
        return self._stackable

    @stackable.setter
    def stackable(self, value):
        self._stackable = value