"""An affliction is a debuff or a buff. It has
a name, a value, a duration, flags."""

from data.constants import SYSTEM, trad
from data.image.hoverable import Hoverable

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
        refreshable (bool, optionnal): Wether or not the affliction\
        refreshes on getting a stack. Defaults to `False`.
    """
    def __init__(self, name, value, duration = 1, flags: list = None, stackable = False,\
                 refreshable = False):
        self._name = name
        self._value = value
        self._duration = duration
        if flags is None:
            self._flags = []
        else:
            self._flags = flags
        self._expire = duration != -1
        self._stackable = stackable
        self._refreshable = refreshable

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
        if self._duration >= 0:
            self._duration -= float(SYSTEM["options"]["fps"])
        

    def clone(self):
        """Returns a copy of the affliction."""
        return Affliction(
            self._name,
            self._value,
            self._duration,
            self._flags,
            self._stackable,
            self._refreshable
        )

    def __str__(self):
        return f"{self._name} with value {self._value} and flags {self._flags}\n"

    def __eq__(self, other):
        if not isinstance(other, Affliction):
            return False
        if self._name == other._name:
            return True
        return False

    def describe(self, is_buff = False) -> Hoverable:
        """Returns a hoverable about the affliction."""
        name = f"{trad('meta_words', 'buffs' if is_buff else 'debuffs')} " +\
            f"{trad('affliction_name', self._name)} " +\
            f"{trad('meta_words', 'for')} {self._duration} {trad('meta_words', 'seconds')}"
        desc = trad('affliction_desc', self._name)
        return Hoverable(0, 0, name, desc, (0,0,0))

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

    @property
    def refreshable(self):
        """Returns wether or not the affliction is refreshable."""
        return self._refreshable

    @refreshable.setter
    def refreshable(self, value):
        self._refreshable = value

    @property
    def expired(self):
        """"Returns true whether or not the affliction's expired."""
        if not self._expire:
            return False
        else:
            return self._duration <= 0
