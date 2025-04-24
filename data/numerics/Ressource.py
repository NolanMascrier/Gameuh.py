"""Class to hold Ressources. A ressource is a stat
that can be used, spent, damaged or replenished.

A ressource can have buffs or debuffs that modify the value 
each tick. It can also have increases and multipliers."""

from data.numerics.Stat import Stat
from data.numerics.Affliction import Affliction
from data.constants import Flags

class Ressource(Stat):
    def __init__(self, val = 100, name = "ressource", refresh = 0.05):
        super().__init__(self, val, name)
        self._max_value = val
        self._rate = Stat(refresh, "refresh_rate")
        self._buffs = []
        self._buffs_multi = []

    def get_max_value(self):
        """Returns the computed max value of the ressource.
        
        Returns:
            int : Computed max value."""
        final_mults = 1
        final_incr = 1
        final_flats = 0
        for flats in self._flats:
            final_flats += flats[1]
        for multiplier in self._mults:
            final_mults *= multiplier[1]
        for increase in self._incr:
            final_incr += increase[1]
        return (self._max_value + final_flats) * final_incr * final_mults

    def add_buff(self, buff):
        """Adds a buff to the ressource. Buffs must \
        be a list name/value/duration. 
        Buffs will restore or damage the ressource by \
        a flat value.
        
        Args:
            buff (list): Name of the buff, value and duration.
        """
        self._buffs.append(buff)
    
    def remove_buff(self, name):
        """Removes a buff by its name.
        
        Args:
            name (str): Buff to remove."""
        for buff in self._buffs:
            if name == buff[0]:
                self._buffs.remove(buff)
                break
    
    def add_buff_m(self, buff):
        """Adds a multi buff to the ressource. Buffs must \
        be a list name/value/duration. 
        Multi Buffs will restore or damage the ressource by \
        a relative value.
        
        Args:
            buff (list): Name of the buff, value and duration.
        """
        self._buffs_multi.append(buff)
    
    def remove_buff_m(self, name):
        """Removes a multi buff by its name.
        
        Args:
            name (str): Buff to remove."""
        for buff in self._buffs:
            if name == buff[0]:
                self._buffs_multi.remove(buff)
                break

    def afflict(self, affliction: Affliction):
        """Adds the debuff to the stat according to its
        flag.
        
        Args:
            affliction (Affliction): affliction to afflict."""
        if Flags.DOT in affliction.flags or Flags.HOT in affliction.flags:
            self.add_buff(affliction.get())
        if Flags.MDOT in affliction.flags or Flags.MHOT in affliction.flags:
            self.add_buff_m(affliction.get())
        super().afflict(affliction)

    def modify(self, value: float):
        """Increments or decrements the value of the 
        ressource by a value. Resets to 0 or max should
        the new value overflows or underflows the limits.
        
        Args:
            value (float): Value of the increment.
        """
        self._value += value
        if self._value > self.get_max_value():
            self._value = self.get_max_value()
        elif self._value < 0:
            self._value = 0

    def tick(self):
        """Ticks down all the buffs and debuffs, and
        also replenish the ressource.
        """
        self._value += self._value * self._rate.get_value()
        super().tick()
        for buff in self._buffs:
            self._value += buff[1]
            if buff[2] > 0:
                buff[2] -= 1
            if buff[2] == 0:
                self.remove_buff(buff[0])
        for buff in self._buffs_multi:
            self._value += self._value * buff[1]
            if buff[2] > 0:
                buff[2] -= 1
            if buff[2] == 0:
                self.remove_buff_m(buff[0])
        if self._value > self.get_max_value():
            self._value = self.get_max_value()
        elif self._value < 0:
            self._value = 0
