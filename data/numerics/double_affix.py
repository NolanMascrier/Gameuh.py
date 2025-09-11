"""A double affix is a modifier for an item that adds a range."""

import random
import json
from data.constants import Flags
from data.numerics.affliction import Affliction
from data.constants import trad, META_FLAGS, GEAR_FLAGS

class DoubleAffix():
    """An affix a single modifier for an item.

    Args:
        name (str): name of the modifier.
        value (float): value of the modifier.
        flags (list[Flags]): Flag of the modifier.
        lower_bound(float, optional): Lower bound multiplier\
        for the random roll. Defaults to 80%.
        upper_bound(float, optional): Upper bound multiplier\
        for the random roll. Defaults to 120%.
    """
    def __init__(self, name, value_min, value_max, flag,\
                 lower_bound:float = 0.8, upper_bound:float = 1.2,\
                 lower_bound_max:float = 0.8, upper_bound_min:float = 1.2):
        self._name = name
        self._value_min = value_min
        self._value_max = value_max
        self._flags = flag
        self._bounds_min = (lower_bound, upper_bound)
        self._bounds_max = (lower_bound_max, upper_bound_min)
        self._seal = False

    def as_affliction(self) -> Affliction:
        """Makes the affix into an affliction."""
        flags = self._flags.copy()
        flags.append(Flags.GEAR)
        return (Affliction(f"{self._name}_effect_min", self._value_min, -1, flags, True),\
                Affliction(f"{self._name}_effect_max", self._value_max, -1, flags, True))

    def roll(self):
        """Creates a copy of the affix with a randomly rolled value."""
        lower_min = self._bounds_min[0] * self._value_min
        upper_min = self._bounds_min[1] * self._value_min
        lower_max = self._bounds_max[0] * self._value_max
        upper_max = self._bounds_max[1] * self._value_max
        value_min = round(random.uniform(lower_min, upper_min))
        value_max = round(random.uniform(lower_max, upper_max))
        return DoubleAffix(
            self._name,
            value_min,
            value_max,
            self._flags,
            lower_min,
            upper_min,
            lower_max,
            upper_max
        )

    def reroll(self):
        """Rerolls an affix within its bounds."""
        if not self._seal:
            self._value_min = random.uniform(self._bounds_min[0], self._bounds_min[1])
            self._value_max = random.uniform(self._bounds_max[0], self._bounds_max[1])

    def seal(self, seals: bool):
        """Sets the seal or unseals it."""
        self._seal = seals

    def describe(self):
        """Generates a description of the affix."""
        adds = ""
        if self._seal:
            col = "#c#(194, 168, 107)"
        else:
            col = "#c#(255, 255, 255)"
        value = (f"{round(self._value_min)}", f"{round(self._value_max)}")
        if self._value_max < 0:
            adds = f"{trad('meta_words', 'remove')} {value[0]}" +\
                f"{trad('meta_words', 'to')} {value[1]}"
        else:
            adds = f"{trad('meta_words', 'adds')} {value[0]} {trad('meta_words', 'to')} {value[1]}"
        affx = []
        if Flags.DESC_UNIQUE in self._flags:
            adds = ""
        for aff in self._flags:
            if aff not in [Flags.DESC_FLAT, Flags.DESC_PERCENT, Flags.BOON, Flags.HEX,\
                Flags.BLESS, Flags.CURSE, Flags.FLAT, Flags.DESC_UNIQUE]:
                affx.append(trad("descripts", aff.value))
        lst = ", ".join(affx)
        return f"{col}{adds} {lst}"

    def describe_details(self):
        """Generates a detailed description of the affix."""
        adds = ""
        deets = ""
        if self._seal:
            col = "#c#(194, 168, 107)"
        else:
            col = "#c#(255, 255, 255)"
        deets = (f"({round(self._bounds_min[0])}-{round(self._bounds_min[1])})",\
                 f"({round(self._bounds_max[0])}-{round(self._bounds_max[1])})")
        value = (f"{round(self._value_min)} {deets[0]}",
                 f"{round(self._value_max)} {deets[1]}")
        if self._value_max < 0:
            adds = f"{trad('meta_words', 'remove')} {value[0]}" +\
                f"{trad('meta_words', 'to')} {value[1]}"
        else:
            adds = f"{trad('meta_words', 'adds')} {value[0]} {trad('meta_words', 'to')} {value[1]}"
        affx = []
        for aff in self._flags:
            if aff not in [Flags.DESC_FLAT, Flags.DESC_PERCENT, Flags.BOON, Flags.HEX,\
                Flags.BLESS, Flags.CURSE, Flags.FLAT, Flags.DESC_UNIQUE]:
                affx.append(trad("descripts", aff.value))
        lst = ", ".join(affx)
        if Flags.DESC_UNIQUE in self._flags:
            deets = f"{trad('descript_alt', self._name)}"
            return f"{lst}\n{deets}"
        return f"{col}{adds} {lst}"

    def export(self):
        """Serializes the affix as JSON."""
        data = {
            "type":"double_affix",
            "name": self._name,
            "value_min": self._value_min,
            "value_max": self._value_max,
            "flags": self._flags,
            "bounds_min": self._bounds_min,
            "bounds_max": self._bounds_max,
            "sealed": self._seal
        }
        return json.dumps(data)

    @staticmethod
    def imports(data):
        """Reads a JSON tab and creates an affix from it."""
        afx = DoubleAffix(
            data["name"],
            data["value_min"],
            data["value_max"],
            [Flags(f) for f in data["flags"]],
            data["bounds_min"][0],
            data["bounds_min"][1],
            data["bounds_max"][0],
            data["bounds_max"][1]
        )
        if bool(data["sealed"]):
            afx.seal(True)
        return afx

    def __eq__(self, o):
        if not isinstance(o, DoubleAffix):
            return False
        if self._name != o.name:
            return False
        if self.value != o.value:
            return False
        if self._flags != o._flags:
            return False
        return True

    def __ne__(self, o):
        if not isinstance(o, DoubleAffix):
            return True
        return not self == o

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
        return self._value_min, self._value_max

    @value.setter
    def value(self, value):
        self._value_min, self._value_max = value

    @property
    def flags(self):
        """Return's the affix flag."""
        return self._flags

    @flags.setter
    def flags(self, value):
        self._flags = value

    @property
    def sealed(self) -> bool:
        """returns whether or not the affix is sealed."""
        return self._seal

    @property
    def price_factor(self) -> tuple:
        """Returns the price factor depending on how well the affix
        is rolled."""
        tier = int(self._name[len(self._name) - 1:len(self._name)])
        roll1 = (self._value_min - self._bounds_min[0]) /\
            (self._bounds_min[1] - self._bounds_min[0] + 1)
        roll2 = (self._value_max - self._bounds_max[0]) /\
            (self._bounds_max[1] - self._bounds_max[0] + 1)
        roll = roll1 * 0.7 + roll2 * 0.7
        return tier, roll

    @property
    def flag_key(self):
        """Get the name of the first flag of the affix.
        Used for name generation."""
        for f in self._flags:
            if f not in META_FLAGS and f not in GEAR_FLAGS:
                return f.value
        return None
