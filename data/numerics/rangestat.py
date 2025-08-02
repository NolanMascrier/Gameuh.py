"""A range stat is a special stat that has an upper and lower bound."""

import json
import random
from data.numerics.stat import Stat
from data.numerics.affliction import Affliction
from data.constants import trad
from data.image.hoverable import Hoverable

class RangeStat():
    """Defines a range stat.

    lower (float, optionnal): Initial lower value of the stat. defaults to 10.
    upper (float, optionnal): Initial upper value of the stat. defaults to 10.
    name (str, optionnal): Name of the stat. 
    max_cap (float, optionnal): At what value the stat should cap\
    ie what it is its maximum value. Defaults to None (no cap).
    min_cap (float, optionnal): At what value the stat should cap\
    ie what it is its minimum value. Defaults to None (no cap).
    precision (int, optionnal): How many decimals should the final\
    value be rounded to. Defaults to 2.
    scaling_value (float, optionnal): How much level influence\
    this stat. Only for enemies. Defaults to 1.
    mult_scaling (bool, optionnal): Whether or not the stat\
    scales multiplicatively. Defaults to `False` (additive).
    """
    def __init__(self, lower = 1, upper = 10, name = "stat",\
            max_cap:float = None, min_cap = None, precision:int = 2,\
            scaling_value:float = 0, mult_scaling = False):
        self._name = name
        self._cap = (min_cap, max_cap)
        self._precision = precision
        self._scaling_value = scaling_value
        self._mult_scaling = mult_scaling
        if isinstance(upper, Stat):
            self._upper = upper
        else:
            self._upper = Stat(upper, f"{name}_upper", max_cap, min_cap,\
                           precision, scaling_value, mult_scaling)
        if isinstance(lower, Stat):
            self._lower = lower
        else:
            self._lower = Stat(lower, f"{name}_lower", max_cap, min_cap,\
                           precision, scaling_value, mult_scaling)

    def get_value(self):
        """Returns the computed final value of the stat.
        
        Returns:
            tuple: values of the stat with computed increases \
            and multipliers."""
        return self._upper.get_value(), self._lower.get_value()

    def afflict(self, affliction: Affliction):
        """Adds the debuff to the stat according to its
        flag.
        
        Args:
            affliction (Affliction): affliction to afflict."""
        if affliction.name[len(affliction.name) - 4:] == "_min":
            self._lower.afflict(affliction)
        elif affliction.name[len(affliction.name) - 4:] == "_max":
            self._upper.afflict(affliction)
        else:
            self._upper.afflict(affliction)
            self._lower.afflict(affliction)

    def remove_affliction(self, affliction: Affliction):
        """Removes an affliction.
        
        Args:
            affliction (Afflicton): Affliction to remove.
        """
        if affliction.name[len(affliction.name) - 4:] == "_min":
            self._lower.remove_affliction(affliction)
        elif affliction.name[len(affliction.name) - 4:] == "_max":
            self._upper.remove_affliction(affliction)
        else:
            self._upper.remove_affliction(affliction)
            self._lower.remove_affliction(affliction)

    def tick(self):
        """Ticks down all increases and multipliers durations.
        
        If a duration reaches 0, it'll be deleted. 
        If a duration is negative, it's considered infinite.  
        """
        self._upper.tick()
        self._lower.tick()

    def scale(self, level:int):
        """Scales the stat to the given level."""
        self._upper.scale(level)
        self._lower.scale(level)

    def describe(self, is_percentage = True,  is_tab = False):
        """Describe the stat as a surface."""
        is_percentage = not is_percentage
        if is_tab:
            name = f"{trad('descripts', f'{self._name}_tab')}: "
        else:
            name = f"{trad('descripts', self._name)}: "
        name_hover = Hoverable(0, 0, name, trad(self._name))
        value = f"{round(self.get_value()[1])}-{round(self.get_value()[0])}"
        desc = f"{trad('meta_words', 'base')}: {self._lower.value}-{self._upper.value}\n" +\
            f"{trad('meta_words', 'flat')}: " +\
                f"{self._lower.get_flats()}-{self._upper.get_flats()}\n" +\
            f"{trad('meta_words', 'increase')}: " +\
                f"{self._lower.get_increases() * 100}-{self._upper.get_increases() * 100}%\n" +\
            f"{trad('meta_words', 'mult')}: " +\
                f"{self._lower.get_multipliers() * 100}-{self._upper.get_multipliers() * 100}%\n"
        value_hover = Hoverable(0, 0, value, desc)
        return name_hover, value_hover

    def roll(self):
        """Rolls a random value between the upper and the lower
        bounds."""
        roll = random.uniform(self._lower.get_value(),\
                              self._upper.get_value())
        return roll

    def reset(self):
        """Resets the stats."""
        self._upper.reset()
        self._lower.reset()

    def export(self):
        """Serializes the affix as JSON."""
        data = {
            "type": "rangestat",
            "name": self._name,
            "min_cap": self._cap[0],
            "max_cap": self._cap[1],
            "precision": self._precision,
            "scaling": self._scaling_value,
            "multiplier_scaling": self._mult_scaling,
            "upper": self._upper.export(),
            "lower": self._lower.export()
        }
        return json.dumps(data)

    @staticmethod
    def imports(data):
        """Reads a JSON tab and creates an affix from it."""
        stat = RangeStat(
            Stat.imports(json.loads(data["lower"])),
            Stat.imports(json.loads(data["upper"])),
            data["name"],
            float(data["max_cap"]) if data["max_cap"] is not None else None,
            float(data["min_cap"]) if data["min_cap"] is not None else None,
            float(data["precision"]),
            float(data["scaling"]),
            bool(data["multiplier_scaling"]),
        )
        return stat

    @property
    def name(self):
        """Returns the range state's name."""
        return self._name

    @name.setter
    def name(self, value):
        self._name = value

    @property
    def upper(self):
        """Returns the range state's upper value."""
        return self._upper

    @upper.setter
    def upper(self, value):
        self._upper = value

    @property
    def lower(self):
        """Returns the range state's lower value."""
        return self._lower

    @lower.setter
    def lower(self, value):
        self._lower = value
