"""Class to hold stats. A stat is a numerical variable associated to creatures. 

It can be debuffed or buffed through increases (additives) or multipliers. 
Flat increase also exists, but should only be accessed through gear. 
The actual initial value should only be increased through level up, as it's gonna be
definitive."""

from data.numerics.Affliction import Affliction
from data.constants import Flags

class Stat:
    """Initialize the stat.
    
    Args:
        val (float, optionnal): Initial value of the stat. defaults to 10.
        name (str, optionnal): Name of the stat.    
    """
    def __init__(self, val = 10, name = "stat"):
        self._value = val
        self._name = name
        self._flats = []
        self._mults = []
        self._incr = []

    def get_value(self):
        """Returns the computed final value of the stat.
        
        Returns:
            float: value of the stat with computed increases \
            and multipliers."""
        final_mults = 1
        final_incr = 1
        final_flats = 0
        for flats in self._flats:
            final_flats += flats.value
        for multiplier in self._mults:
            final_mults *= multiplier.value
        for increase in self._incr:
            final_incr += increase.value
        return round((self._value + final_flats) * final_incr * final_mults, 2)

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
        if Flags.GEAR in affliction.flags:
            self._handle_affliction_list("_flats", affliction)
    
    def tick(self):
        """Ticks down all increases and multipliers durations.
        
        If a duration reaches 0, it'll be deleted. 
        If a duration is negative, it's considered infinite.  
        """
        for flats in self._flats.copy():
            if flats.duration == 0:
                self._flats.remove(flats)
        for mults in self._mults.copy():
            if mults.duration == 0:
                self._mults.remove(mults)
        for incr in self._incr.copy():
            if incr.duration == 0:
                self._incr.remove(incr)
    
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
    
    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, value):
        self._value = value

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        self._name = value

    @property
    def flats(self):
        return self._flats

    @flats.setter
    def flats(self, value):
        self._flats = value

    @property
    def mults(self):
        return self._mults

    @mults.setter
    def mults(self, value):
        self._mults = value

    @property
    def incr(self):
        return self._incr

    @incr.setter
    def incr(self, value):
        self._incr = value
