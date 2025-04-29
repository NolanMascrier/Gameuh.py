"""An item is something that can be held by
characters and used."""

from data.creature import Creature
from data.constants import Flags

class Item():
    """Creates an item.
    
    Args:
        name (str): name of the item.
        max_held(int, optionnal): Maximum amount of the \
        item that can be held in a single inventory slot. \
        Defaults to 64.
        flags (list, optionnal): List of the items's flags. \
        Defaults to [].
        affixes (list, optionnal): List of the item's affixes,\
        aka its effects. Defaults to [].
    """
    def __init__(self, name, max_held = 64, flags = None, affixes = None):
        self._name = name
        self._max_held = max_held
        if flags is None:
            self._flags = []
        else:
            self._flags = flags
        if affixes is None:
            self._affixes = []
        else:
            self._affixes = affixes

    def on_use(self, target: Creature):
        """Uses the item on the creature."""
        if Flags.GEAR in self._flags:
            pass
        else:
            pass

    @property
    def name(self):
        """Returns the item's name."""
        return self._name

    @name.setter
    def name(self, value):
        self._name = value

    @property
    def max_held(self) -> int:
        """Returns the item's max holdable value."""
        return self._max_held

    @max_held.setter
    def max_held(self, value):
        self._max_held = value

    @property
    def flags(self):
        """Returns the item's flag list."""
        return self._flags

    @flags.setter
    def flags(self, value):
        self._flags = value
