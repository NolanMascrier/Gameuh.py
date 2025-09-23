"""An affix is a modifier for an item."""

import random
import json
from data.constants import Flags
from data.numerics.affliction import Affliction
from data.constants import trad, META_FLAGS, GEAR_FLAGS

class Affix():
    """An affix a single modifier for an item.

    Args:
        name (str): name of the modifier.
        value (float): value of the modifier.
        flags (list[Flags]): Flag of the modifier.
        lower_bound(float, optional): Lower bound multiplier\
        for the random roll. Defaults to 80%.
        upper_bound(float, optional): Upper bound multiplier\
        for the random roll. Defaults to 120%.
        level_modifier (bool, optional): Whether or not the affix describes a level modifier.\
        Impacts the describe function. Defaults to `False`.
    """
    def __init__(self, name, value, flag, lower_bound:float = 0.8, upper_bound:float = 1.2,\
                level_modifier = False):
        self._name = name
        self._value = value
        self._flags = flag
        self._bounds = (lower_bound, upper_bound)
        self._seal = False
        self._level_modifier = level_modifier

    def as_affliction(self) -> Affliction:
        """Makes the affix into an affliction."""
        flags = self._flags.copy()
        flags.append(Flags.GEAR)
        return Affliction(f"{self._name}_effect", self._value, -1, flags, True)

    def roll(self):
        """Creates a copy of the affix with a randomly rolled value."""
        lower = self._bounds[0] * self._value
        upper = self._bounds[1] * self._value
        value = round(random.uniform(lower, upper), 2)
        return Affix(
            self._name,
            value,
            self._flags,
            lower,
            upper,
            self._level_modifier
        )

    def copy(self):
        """Creates a deep copy of the item."""
        return Affix(
            self._name,
            self._value,
            self._flags.copy(),
            self._bounds[0],
            self._bounds[1],
            self._level_modifier
        )

    def reroll(self):
        """Rerolls an affix within its bounds."""
        if not self._seal:
            self._value = random.uniform(self._bounds[0], self._bounds[1])

    def seal(self, seals: bool):
        """Sets the seal or unseals it."""
        self._seal = seals

    def describe(self):
        """Generates a description of the affix."""
        adds = ""
        if self._value == 0:
            return "\n"
        if self._seal:
            col = "#c#(194, 168, 107)"
        else:
            col = "#c#(255, 255, 255)"
        if self._level_modifier:
            mod = f"{trad('meta_words', 'enemies')} "
        else:
            mod = ""
        if Flags.DESC_FLAT in self._flags:
            value = f"{round(self._value)}"
        elif Flags.DESC_PERCENT in self._flags:
            value = f"{round(self._value)}%"
        else:
            value = f"{round(self._value * 100)}%"
        if Flags.BOON in self._flags:
            adds = f"{value} {trad('meta_words', 'increased')}"
        elif Flags.HEX in self._flags:
            adds = f"{value} {trad('meta_words', 'decreased')} "
        elif Flags.BLESS in self._flags:
            adds = f"{value} {trad('meta_words', 'more')}"
        elif Flags.CURSE in self._flags:
            adds = f"{value} {trad('meta_words', 'less')}"
        elif Flags.FLAT in self._flags:
            if self._value < 0:
                adds = f"{value}"
            else:
                adds = f"+{value}"
        affx = []
        if Flags.DESC_UNIQUE in self._flags:
            adds = ""
        for aff in self._flags:
            if aff not in [Flags.DESC_FLAT, Flags.DESC_PERCENT, Flags.BOON, Flags.HEX,\
                Flags.BLESS, Flags.CURSE, Flags.FLAT, Flags.DESC_UNIQUE, Flags.TRIGGER]:
                affx.append(trad("descripts", aff.value))
        lst = ", ".join(affx)
        return f"{mod}{col}{adds} {lst}"

    def describe_details(self):
        """Generates a detailed description of the affix."""
        adds = ""
        deets = ""
        if self._seal:
            col = "#c#(194, 168, 107)"
        else:
            col = "#c#(255, 255, 255)"
        if self._value == 0:
            return "\n"
        if Flags.DESC_FLAT in self._flags:
            value = f"{round(self._value)}"
            deets = f"({round(self._bounds[0])}-{round(self._bounds[1])})"
        elif Flags.DESC_PERCENT in self._flags:
            value = f"{round(self._value)}%"
            deets = f"({round(self._bounds[0])}%-{round(self._bounds[1])}%)"
        else:
            value = f"{round(self._value * 100)}%"
            deets = f"({round(self._bounds[0] * 100)}%-{round(self._bounds[1] * 100)}%)"
        if Flags.BOON in self._flags:
            adds = f"{value} {trad('meta_words', 'increased')}"
        elif Flags.HEX in self._flags:
            adds = f"{value} {trad('meta_words', 'decreased')} "
        elif Flags.BLESS in self._flags:
            adds = f"{value} {trad('meta_words', 'more')}"
        elif Flags.CURSE in self._flags:
            adds = f"{value} {trad('meta_words', 'less')}"
        elif Flags.FLAT in self._flags:
            if self._value < 0:
                adds = f"{value}"
            else:
                adds = f"+{value}"
        affx = []
        for aff in self._flags:
            if aff not in [Flags.DESC_FLAT, Flags.DESC_PERCENT, Flags.BOON, Flags.HEX,\
                Flags.BLESS, Flags.CURSE, Flags.FLAT, Flags.DESC_UNIQUE, Flags.TRIGGER]:
                affx.append(trad("descripts", aff.value))
        lst = ", ".join(affx)
        if Flags.DESC_UNIQUE in self._flags:
            deets = f"{trad('descript_alt', self._name)}"
            return f"{lst}\n{deets}"
        return f"{col}{adds} {deets} {lst}"

    def export(self):
        """Serializes the affix as JSON."""
        data = {
            "type":"affix",
            "name": self._name,
            "value": self._value,
            "flags": self._flags,
            "bounds": self._bounds,
            "sealed": self._seal
        }
        return json.dumps(data)

    @staticmethod
    def imports(data):
        """Reads a JSON tab and creates an affix from it."""
        afx = Affix(
            data["name"],
            float(data["value"]),
            [Flags(f) for f in data["flags"]],
            float(data["bounds"][0]),
            float(data["bounds"][1])
        )
        if bool(data["sealed"]):
            afx.seal(True)
        return afx

    def __eq__(self, o):
        if not isinstance(o, Affix):
            return False
        if self._name != o.name:
            return False
        if self._value != o.value:
            return False
        if self._flags != o._flags:
            return False
        return True

    def __ne__(self, o):
        if not isinstance(o, Affix):
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

    @property
    def sealed(self) -> bool:
        """returns whether or not the affix is sealed."""
        return self._seal

    @property
    def price_factor(self) -> tuple:
        """Returns the price factor depending on how well the affix
        is rolled."""
        tier = int(self._name[len(self._name) - 1:len(self._name)])
        div = abs(self._bounds[1] - self._bounds[0]) + 1
        roll = (self._value - self._bounds[0]) / div
        return tier, roll

    @property
    def flag_key(self):
        """Get the name of the first flag of the affix.
        Used for name generation."""
        for f in self._flags:
            if f not in META_FLAGS and f not in GEAR_FLAGS:
                return f.value
        return None
