"""An affliction is a debuff or a buff. It has
a name, a value, a duration, flags."""

import json
from data.constants import trad, META_FLAGS, Flags
from data.image.hoverable import Hoverable
from data.numerics.damage import Damage

ORANGE = (255, 210, 48)

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
        damage (Damage, optionnal): Damage applied each tick.
        max_stacks (int, optional): Maximum number of stacks should this buff be stackable.\
        Defaults to 10.
        tick_rate (float, optional): Time in seconds between each tick. Defaults to 0.016.
        dot_tick (float, optional): Time in seconds between each damage tick. Defaults to 1.
        dot_color (tuple, optional): Color of the damage text for DOT effects. Defaults to ORANGE.
        is_debuff (bool, optional): Wether or not the affliction is a debuff. Defaults to False.
    """
    def __init__(self, name, value, duration = 1, flags: list = None, stackable = False,
                 refreshable = False, damage: Damage = None, max_stacks = 10, tick_rate = 0.016,
                 dot_tick = 1, dot_color = ORANGE, is_debuff = False):
        self._name = name
        self._value = value
        self._duration = duration
        if flags is None:
            self._flags = []
        else:
            self._flags = flags
        self._max_duration = duration
        self._expire = duration != -1
        self._stackable = stackable
        self._refreshable = refreshable
        self._damage = damage
        self._max_stacks = max_stacks
        self._tick_rate = tick_rate
        self._dot_tick = dot_tick
        self._dot_timer = 0.0
        self._dot_amount = 0
        self._dot_color = dot_color
        self._is_debuff = is_debuff

    def tick(self):
        """Ticks down the timer.
        """
        self._dot_timer += self._tick_rate
        if self._dot_timer >= self._dot_tick:
            self._dot_timer -= self._dot_tick
            self._dot_amount += 1
        if self._duration >= 0:
            self._duration -= 0.016

    def clone(self, is_debuff = False):
        """Returns a copy of the affliction."""
        return Affliction(
            self._name,
            self._value,
            self._duration,
            self._flags,
            self._stackable,
            self._refreshable,
            self._damage.clone() if self._damage is not None else None,
            self._max_stacks,
            self._tick_rate,
            self._dot_tick,
            self._dot_color,
            is_debuff
        )

    def __str__(self):
        return f"{self._name}: value {self._value}," +\
            f" duration {self._duration}, flags {self._flags}, tick rate {self._tick_rate}\n"

    def __eq__(self, other):
        if not isinstance(other, Affliction):
            return False
        if self._name != other._name:
            return False
        if self._value != other._value:
            return False
        if self._duration != other.duration:
            return False
        if self._flags != other.flags:
            return False
        return True

    def __ne__(self, other):
        if not isinstance(other, Affliction):
            return True
        return not self == other

    def describe(self, is_buff = False) -> Hoverable:
        """Returns a hoverable about the affliction. Used for skills description."""
        name = f"{trad('meta_words', 'buffs' if is_buff else 'debuffs')} " +\
            f"{trad('affliction_name', self._name)} " +\
            f"{trad('meta_words', 'for')} {self._duration} {trad('meta_words', 'seconds')}"
        desc = trad('affliction_desc', self._name)
        return Hoverable(0, 0, name, desc, (0,0,0))

    def tree_describe(self):
        """Returns a text description of the affliction. Used for the tree."""
        desc = ""
        for f in self._flags:
            if f not in META_FLAGS:
                desc += f"{trad('meta_words', 'grants')} {self._value} " +\
                    f"{trad('descripts', f.value)} \n"
        return desc

    def export(self):
        """Serializes the affliction as JSON."""
        data = {
            "type":"affliction",
            "name": self._name,
            "value": self._value,
            "duration": self._duration,
            "flags": self._flags,
            "stackable": self._stackable,
            "refreshable": self._refreshable,
            "dot": self._damage.export() if self._damage is not None else None
        }
        return json.dumps(data)

    @staticmethod
    def imports(data):
        """Reads a JSON tab and creates an affliction from it."""
        return Affliction(
            data["name"],
            float(data["value"]),
            float(data["duration"]),
            [Flags(f) for f in data["flags"]],
            bool(data["stackable"]),
            bool(data["refreshable"]),
            Damage.imports(json.loads(data["dot"])) if data["dot"] is not None else None
        )

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
    def damage(self):
        """Returns the affliction's damage."""
        return self._damage

    @damage.setter
    def damage(self, value):
        self._damage = value

    @property
    def elapsed(self):
        """Returns the relative elapsed time of the debuff."""
        return round(self._duration / self._max_duration * 255)

    @property
    def expired(self):
        """"Returns true whether or not the affliction's expired."""
        if not self._expire:
            return False
        else:
            return self._duration <= 0

    @property
    def max_stacks(self):
        """Returns the maximum amounts of stacks."""
        return self._max_stacks

    @max_stacks.setter
    def max_stacks(self, value):
        self._max_stacks = value

    @property
    def tick_rate(self):
        """Returns the dot's tick rate."""
        return self._tick_rate

    @tick_rate.setter
    def tick_rate(self, value):
        self._tick_rate = value

    @property
    def dot_tick(self):
        """Returns the dot's tick amount."""
        return self._dot_tick

    @dot_tick.setter
    def dot_tick(self, value):
        self._dot_tick = value

    @property
    def dot_amount(self):
        """Returns the amount of dot ticks that have occured."""
        dt = self._dot_amount
        self._dot_amount = 0
        return dt

    @property
    def dot_color(self):
        """Returns the color of the dot effect."""
        return self._dot_color

    @dot_color.setter
    def dot_color(self, value):
        self._dot_color = value

    @property
    def is_debuff(self):
        """Returns whether or not the affliction is a debuff."""
        return self._is_debuff

    @is_debuff.setter
    def is_debuff(self, value):
        self._is_debuff = value
