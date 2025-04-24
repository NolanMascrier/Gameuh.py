"""Class to hold Ressources. A ressource is a stat
that can be used, spent, damaged or replenished.

A ressource can have buffs or debuffs that modify the value 
each tick. It can also have increases and multipliers."""

from data.numerics.Stat import Stat
from data.numerics.Affliction import Affliction
from data.constants import Flags

class Ressource(Stat):
    def __init__(self, val = 100, name = "ressource", refresh = 0.05):
        super().__init__(val, name)
        self._current_value = val
        self._rate = Stat(refresh, "refresh_rate")
        self._buffs = []
        self._buffs_multi = []

    def afflict(self, affliction: Affliction):
        """Adds the debuff to the stat according to its
        flag.
        
        Args:
            affliction (Affliction): affliction to afflict."""
        super().afflict(affliction)
        if Flags.DOT in affliction.flags or Flags.HOT in affliction.flags:
            self._handle_affliction_list("_buffs", affliction)
        if Flags.MDOT in affliction.flags or Flags.MHOT in affliction.flags:
            self._handle_affliction_list("_buffs_multi", affliction)

    def modify(self, value: float):
        """Increments or decrements the value of the 
        ressource by a value. Resets to 0 or max should
        the new value overflows or underflows the limits.
        
        Args:
            value (float): Value of the increment.
        """
        self._current_value += value
        if self._current_value > self.get_value():
            self._current_value = self.get_value()
        elif self._current_value < 0:
            self._current_value = 0

    def tick(self):
        """Ticks down all the buffs and debuffs, and
        also replenish the ressource.
        """
        self._current_value += self._current_value * self._rate.get_value()
        super().tick()
        for buff in self._buffs:
            self._current_value += buff.value
            if buff.duration == 0:
                self._buffs.remove(buff)
        for buff in self._buffs_multi:
            self._current_value += buff.value * self._current_value
            if buff.duration == 0:
                self._buffs.remove(buff)
        if self._current_value > self.get_value():
            self._current_value = self.get_value()
        elif self._current_value < 0:
            self._current_value = 0
    
    @property
    def current_value(self):
        return self._current_value

    @current_value.setter
    def current_value(self, value):
        self._current_value = value

    @property
    def rate(self):
        return self._rate

    @rate.setter
    def rate(self, value):
        self._rate = value

    @property
    def buffs(self):
        return self._buffs

    @buffs.setter
    def buffs(self, value):
        self._buffs = value

    @property
    def buffs_multi(self):
        return self._buffs_multi

    @buffs_multi.setter
    def buffs_multi(self, value):
        self._buffs_multi = value
