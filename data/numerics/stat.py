"""Class to hold stats. A stat is a numerical variable associated to creatures. 

It can be debuffed or buffed through increases (additives) or multipliers. 
Flat increase also exists, but should only be accessed through gear. 
The actual initial value should only be increased through level up, as it's gonna be
definitive."""

from data.numerics.affliction import Affliction
from data.constants import Flags

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

    def get_value(self):
        """Returns the computed final value of the stat.
        
        Returns:
            float: value of the stat with computed increases \
            and multipliers."""
        final_mults = 1
        final_incr = 0
        final_flats = 0
        for flats in self._flats:
            final_flats += flats.value
        for multiplier in self._mults:
            final_mults *= 1 + multiplier.value
        for increase in self._incr:
            final_incr += increase.value
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
            if flats.duration <= 0:
                self._flats.remove(flats)
        for mults in self._mults.copy():
            if mults.duration <= 0:
                self._mults.remove(mults)
        for incr in self._incr.copy():
            if incr.duration <= 0:
                self._incr.remove(incr)

    def scale(self, level:int):
        """Scales the stat to the given level."""
        if self._mult_scaling:
            self._value *= self._scaling_value * level
        else:
            self._value += self._scaling_value * level

    def export(self):
        """Exports the stat data as a JSON list.
        
        Returns:
            list: JSON-Readable data of the stat."""
        export = {
            "name": self._name,
            "value": self._value,
            "flats": self._flats,
            "incrs": self._incr,
            "mults": self._mults
        }
        return export

    def import_json(self, json):
        """Reads a JSON list and updates the stat
        according to the data inside.
        
        Args:
            json (list): Data to parse.
        """
        for data in json:
            match (data):
                case "name":
                    self._name = str(json[data])
                case "value":
                    self._value = int(json[data])
                case "flats":
                    self._flats = [int(d) for d in json[data]]
                case "incrs":
                    self._incr = [float(d) for d in json[data]]
                case "mults":
                    self._mults = [float(d) for d in json[data]]
                case _:
                    raise IndexError("Unknown variable.")

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
