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
            final_flats += flats[1]
        for multiplier in self._mults:
            final_mults *= multiplier[1]
        for increase in self._incr:
            final_incr += increase[1]
        return (self._value + final_flats) * final_incr * final_mults
    
    def add_flat(self, flat):
        """Adds a flat increase to the stat. Increases must \
        be a list name/value/duration.   
        Flat increases are direct modifiers to the value, and \
        are meant to be increased through gear rather than through \
        buffs.
        
        Args:
            increase (list): Name of the increase, value and duration.
        """
        self._incr.append(flat)

    def remove_flat(self, name):
        """Removes a flat increase by its name.
        
        Args:
            name (str): Flat increase to remove."""
        for flat in self._flats:
            if name == flat[0]:
                self._flats.remove(flat)
                break
    
    def add_increase(self, increase):
        """Adds an increase to the stat. Increases must \
        be a list name/value/duration.
        
        Args:
            increase (list): Name of the increase, value and duration.
        """
        self._incr.append(increase)

    def remove_increase(self, name):
        """Removes an increase by its name.
        
        Args:
            name (str): Increase to remove."""
        for increase in self._incr:
            if name == increase[0]:
                self._incr.remove(increase)
                break
    
    def add_multiplier(self, mult):
        """Adds a multiplier to the stat. Multipliers must \
        be a list name/value/duration.
        
        Args:
            mult (list): Name of the multiplier, value and duration.
        """
        self._mults.append(mult)
    
    def remove_multi(self, name):
        """Removes a Multiplier by its name.
        
        Args:
            name (str): Multiplier to remove."""
        for mult in self._mults:
            if name == mult[0]:
                self._mults.remove(mult)
                break

    def afflict(self, affliction: Affliction):
        """Adds the debuff to the stat according to its
        flag.
        
        Args:
            affliction (Affliction): affliction to afflict."""
        if Flags.HEX in affliction.flags or Flags.BOON in affliction.flags:
            self.add_increase(affliction.get())
        if Flags.CURSE in affliction.flags or Flags.BLESS in affliction.flags:
            self.add_multiplier(affliction.get())
        if Flags.GEAR in affliction.flags:
            self.add_flat(affliction.get())
    
    def tick(self):
        """Ticks down all increases and multipliers durations.
        
        If a duration reaches 0, it'll be deleted. 
        If a duration is negative, it's considered infinite.  
        """
        for flats in self._flats:
            if flats[2] > 0:
                flats[2] -= 1
            if flats[2] == 0:
                self.remove_flat(flats[0])
        for mults in self._mults:
            if mults[2] > 0:
                mults[2] -= 1
            if mults[2] == 0:
                self.remove_multi(mults[0])
        for incr in self._incr:
            if incr[2] > 0:
                incr[2] -= 1
            if incr[2] == 0:
                self.remove_increase(incr[0])
    
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
