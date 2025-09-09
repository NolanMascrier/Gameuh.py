"""Class to hold stats. A stat is a numerical variable associated to creatures. 

It can be debuffed or buffed through increases (additives) or multipliers. 
Flat increase also exists, but should only be accessed through gear. 
The actual initial value should only be increased through level up, as it's gonna be
definitive."""

import json
from data.numerics.affliction import Affliction
from data.constants import Flags, trad
from data.image.hoverable import Hoverable

class Stat:
    """Initialize the stat.
    
    Args:
        val (float, optionnal): Initial value of the stat. defaults to 10.
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
    def __init__(self, val = 10, name = "stat",\
            max_cap:float = None, min_cap = None, precision:int = 2,\
            scaling_value:float = 0, mult_scaling = False):
        self._value = val
        self._name = name
        self._flats = []
        self._mults = []
        self._incr = []
        self._cap = (min_cap, max_cap)
        self._scaling_value = scaling_value
        self._mult_scaling = mult_scaling
        self._round = int(precision)

    def get_flats(self):
        """Returns the sum of the flat values"""
        final_flats = 0
        for flats in self._flats:
            final_flats += flats.value
        return final_flats

    def get_multipliers(self):
        """Returns the product of the mult values"""
        final_mults = 1
        for multiplier in self._mults:
            if Flags.HEX in multiplier.flags or Flags.CURSE in multiplier.flags:
                final_mults *= 1 - multiplier.value
            else:
                final_mults *= 1 + multiplier.value
        return final_mults

    def get_increases(self):
        """Returns the sum of the increases."""
        final_incr = 0
        for increase in self._incr:
            if Flags.HEX in increase.flags or Flags.CURSE in increase.flags:
                final_incr -= increase.value
            else:
                final_incr += increase.value
        return final_incr

    def get_value(self):
        """Returns the computed final value of the stat.
        
        Returns:
            float: value of the stat with computed increases \
            and multipliers."""
        final_incr = self.get_increases()
        final_flats = self.get_flats()
        final_mults = self.get_multipliers()
        final_value = round((self._value + final_flats) *\
                            (1 + final_incr) * final_mults, self._round)
        if self._cap[0] is not None:
            final_value = max(final_value, self._cap[0])
        if self._cap[1] is not None:
            final_value = min(final_value, self._cap[1])
        return final_value

    def _handle_affliction_list(self, list_name, affliction):
        """Appends the affliction to the corresponding list.
        If the affliction isn't stackable, the function will
        check if the affliction already exists. If it does, 
        it will refresh the duration and value.
        
        Args:
            list_name (str): Name of the list.
            affliction (Affliction): Affliction to apply.
        """
        target_list = getattr(self, list_name)
        if affliction.stackable:
            target_list.append(affliction)
            if affliction.refreshable:
                for aff in target_list:
                    if aff.name == affliction.name:
                        aff.duration = affliction.duration
        else:
            for i, existing_aff in enumerate(target_list):
                if existing_aff.name == affliction.name:
                    target_list[i] = affliction
                    return
            target_list.append(affliction)

    def afflict(self, affliction: Affliction):
        """Adds the debuff to the stat according to its
        flag.
        
        Args:
            affliction (Affliction): affliction to afflict."""
        if Flags.HEX in affliction.flags or Flags.BOON in affliction.flags:
            self._handle_affliction_list("_incr", affliction)
        if Flags.CURSE in affliction.flags or Flags.BLESS in affliction.flags:
            self._handle_affliction_list("_mults", affliction)
        if Flags.FLAT in affliction.flags:
            self._handle_affliction_list("_flats", affliction)

    def remove_affliction(self, affliction: Affliction):
        """Removes an affliction.
        
        Args:
            affliction (Afflicton): Affliction to remove.
        """
        for afflic in self._incr.copy():
            if afflic == affliction:
                self._incr.remove(afflic)
        for afflic in self._mults.copy():
            if afflic == affliction:
                self._mults.remove(afflic)
        for afflic in self._flats.copy():
            if afflic == affliction:
                self._flats.remove(afflic)

    def tick(self):
        """Ticks down all increases and multipliers durations.
        
        If a duration reaches 0, it'll be deleted. 
        If a duration is negative, it's considered infinite.  
        """
        for flats in self._flats.copy():
            if flats.expired:
                self._flats.remove(flats)
        for mults in self._mults.copy():
            if mults.expired:
                self._mults.remove(mults)
        for incr in self._incr.copy():
            if incr.expired:
                self._incr.remove(incr)

    def scale(self, level:int):
        """Scales the stat to the given level."""
        if self._mult_scaling:
            self._value *= self._scaling_value * level
        else:
            self._value += self._scaling_value * level

    def describe(self, is_percentage = True, is_tab = False):
        """Describe the stat as a surface."""
        if is_tab:
            name = f"{trad('descripts', f'{self.name}_tab')}: "
        else:
            name = f"{trad('descripts', self.name)}: "
        name_hover = Hoverable(0, 0, name, trad(self.name))
        if is_percentage:
            value = f"{round(self.get_value() * 100)}%"
            desc = f"{trad('meta_words', 'base')}: {self._value * 100}%\n" +\
                f"{trad('meta_words', 'flat')}: {self.get_flats() * 100}%\n" +\
                f"{trad('meta_words', 'increase')}: {self.get_increases() * 100}%\n" +\
                f"{trad('meta_words', 'mult')}: {self.get_multipliers() * 100}%\n"
        else:
            value = f"{round(self.get_value())}"
            desc = f"{trad('meta_words', 'base')}: {self._value}\n" +\
                f"{trad('meta_words', 'flat')}: {self.get_flats()}\n" +\
                f"{trad('meta_words', 'increase')}: {self.get_increases() * 100}%\n" +\
                f"{trad('meta_words', 'mult')}: {self.get_multipliers() * 100}%\n"
        value_hover = Hoverable(0, 0, value, desc)
        return name_hover, value_hover

    def gather_afflictions(self) -> list:
        """Gather all buffs and debuffs as a list. \
        Usefull for display purpose.
        
        Returns:
            list: List of afflictions.
        """
        result = []
        result.extend(self._flats)
        result.extend(self._incr)
        result.extend(self._mults)
        return result

    def clone(self):
        """Creates a copy of the stat."""
        copy = Stat(
            self._value,
            self._name
        )
        return copy

    def reset(self):
        """Resets the stat."""
        self._incr.clear()
        self._mults.clear()
        self._flats.clear()

    def export(self):
        """Serializes the affix as JSON."""
        data = {
            "type": "stat",
            "name": self._name,
            "value": self._value,
            "min_cap": self._cap[0],
            "max_cap": self._cap[1],
            "precision": self._round,
            "scaling": self._scaling_value,
            "multiplier_scaling": self._mult_scaling,
            "mults": [f.export() for f in self._mults],
            "incrs": [f.export() for f in self._incr],
            "flats": [f.export() for f in self._flats]
        }
        return json.dumps(data)

    @staticmethod
    def imports(data):
        """Reads a JSON tab and creates an affix from it."""
        stat = Stat(
            float(data["value"]),
            data["name"],
            float(data["max_cap"]) if data["max_cap"] is not None else None,
            float(data["min_cap"]) if data["min_cap"] is not None else None,
            float(data["precision"]),
            float(data["scaling"]),
            bool(data["multiplier_scaling"]),
        )
        for f in data["mults"]:
            stat.afflict(Affliction.imports(json.loads(f)))
        for f in data["incrs"]:
            stat.afflict(Affliction.imports(json.loads(f)))
        for f in data["flats"]:
            stat.afflict(Affliction.imports(json.loads(f)))
        return stat

    @property
    def value(self) -> float:
        """Returns the current value of the stat."""
        return self._value

    @value.setter
    def value(self, value):
        self._value = value

    @property
    def name(self) -> str:
        """Returns the stat's name."""
        return self._name

    @name.setter
    def name(self, value):
        self._name = value

    @property
    def flats(self):
        """Returns the list of the stat's flat increases."""
        return self._flats

    @flats.setter
    def flats(self, value):
        self._flats = value

    @property
    def mults(self):
        """Returns the list of the stat's multiplicative increases."""
        return self._mults

    @mults.setter
    def mults(self, value):
        self._mults = value

    @property
    def incr(self):
        """Returns the list of the stat's additive increases."""
        return self._incr

    @incr.setter
    def incr(self, value):
        self._incr = value

    @property
    def c_value(self):
        """Wrapper to get_value(). Return the computed
        value of the stat."""
        return self.get_value()
