"""Class to hold Ressources. A ressource is a numerical value
that can be used, spent, damaged or replenished.

A ressource can have buffs or debuffs that modify the value 
each tick. It can also have increases and multipliers."""

from numerics.Stat import Stat

class Ressource:
    def __init__(self, val = 100, name = "ressource", refresh = 0.05):
        self._max_value = val
        self._value = val
        self._name = name
        self._rate = Stat(refresh, "refresh_rate")
        self._flats = []
        self._mults = []
        self._incr = []
        self._buffs = []
        self._buffs_multi = []

    def tick(self):
        """Ticks down all the buffs and debuffs, and
        also replenish the ressource.
        """
        self._value += self._value * self._rate.get_value()
        if self._value >= self._max_value:
            self._value = self._max_value
