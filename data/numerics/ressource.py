"""Class to hold Ressources. A ressource is a stat
that can be used, spent, damaged or replenished.

A ressource can have buffs or debuffs that modify the value 
each tick. It can also have increases and multipliers."""

from data.numerics.stat import Stat
from data.numerics.affliction import Affliction
from data.constants import Flags, trad
from data.image.hoverable import Hoverable

class Ressource(Stat):
    """Defines a ressource. A ressource has a maximum \
    value and can be replenished or spent.
    
    Args:
        val (float, optionnal): Default value of the stat. Defaults \
        to 100.
        name (str, optionnal): Name of the ressource. Defaults to \
        `ressource`.
        refresh (float, optionnal): Refresh rate of the ressource, ie \
        the proportion that is restored each tick. Defaults to 5%.
        cap (float, optionnal): At what value the stat should cap\
        ie what it is its maximum value. Defaults to -1 (no cap).
        scaling_value (float, optionnal): How much level influence\
        this stat. Only for enemies. Defaults to 1.
        mult_scaling (bool, optionnal): Whether or not the stat\
        scales multiplicatively. Defaults to `False` (additive).

    """
    def __init__(self, val = 100.0, name = "ressource", refresh = None,\
            max_cap = None, min_cap = None, scaling_value:float = 1, mult_scaling = False):
        super().__init__(val, name, max_cap, min_cap, scaling_value, mult_scaling)
        self._current_value = val
        if refresh is None:
            self._rate = Stat(0, "refresh")
        else:
            self._rate = refresh
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

    def remove_affliction(self, affliction: Affliction):
        """Removes an affliction.
        
        Args:
            affliction (Afflicton): Affliction to remove.
        """
        super().remove_affliction(affliction)
        for afflic in self._buffs.copy():
            if afflic == affliction:
                self._buffs.remove(afflic)
        for afflic in self._buffs_multi.copy():
            if afflic == affliction:
                self._buffs_multi.remove(afflic)

    def refill(self):
        """Restores the ressource to its maximum value."""
        self._current_value = self.get_value()

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
        self._current_value += self.get_value() * self._rate.get_value()
        for buff in self._buffs:
            self._current_value += buff.value
            if buff.expired:
                self._buffs.remove(buff)
        for buff in self._buffs_multi:
            self._current_value += buff.value * self._current_value
            if buff.expired:
                self._buffs.remove(buff)
        if self._current_value > self.get_value():
            self._current_value = self.get_value()
        elif self._current_value < 0:
            self._current_value = 0

    def gather_afflictions(self) -> list:
        """Gather all buffs and debuffs as a list. \
        Usefull for display purpose.
        
        Returns:
            list: List of afflictions.
        """
        result = super().gather_afflictions()
        result.extend(self._buffs)
        result.extend(self._buffs_multi)
        return result

    def clone(self):
        """Returns a copy of the ressource."""
        copy = Ressource(
            self._value,
            self._name,
            self._rate.clone()
        )
        return copy

    def reset(self):
        """Resets the stat."""
        super().reset()
        self._buffs.clear()
        self._buffs_multi.clear()
        self.refill()

    def describe(self, is_percentage = True):
        """Describe the stat as a surface."""
        name = f"{trad('descripts', self.name)}: "
        name_hover = Hoverable(0, 0, name, trad(self.name))
        refresh = f"{trad('meta_words', 'refresh')}:" +\
            f"{self.get_value() * self._rate.get_value()}/s"
        if is_percentage:
            value = f"{round(self.get_value() * 100)}%, {refresh}"
            desc = f"{trad('meta_words', 'base')}: {self._value * 100}%\n" +\
                f"{trad('meta_words', 'flat')}: {self.get_flats() * 100}%\n" +\
                f"{trad('meta_words', 'increase')}: {self.get_increases() * 100}%\n" +\
                f"{trad('meta_words', 'mult')}: {self.get_multipliers() * 100}%\n"
        else:
            value = f"{round(self.get_value())}, {refresh}"
            desc = f"{trad('meta_words', 'base')}: {self._value}\n" +\
                f"{trad('meta_words', 'flat')}: {self.get_flats()}\n" +\
                f"{trad('meta_words', 'increase')}: {self.get_increases() * 100}%\n" +\
                f"{trad('meta_words', 'mult')}: {self.get_multipliers() * 100}%\n"
        value_hover = Hoverable(0, 0, value, desc)
        return name_hover, value_hover

    @property
    def current_value(self) -> float:
        """Returns the current value of the ressource, ie the one \
        that will be spent or restored."""
        return self._current_value

    @current_value.setter
    def current_value(self, value):
        self._current_value = value

    @property
    def rate(self) -> Stat:
        """Returns the refresh rate of the ressource."""
        return self._rate

    @rate.setter
    def rate(self, value):
        self._rate = value

    @property
    def buffs(self):
        """Returns the current buff list."""
        return self._buffs

    @buffs.setter
    def buffs(self, value):
        self._buffs = value

    @property
    def buffs_multi(self):
        """Returns the current multiplicative buff
        list."""
        return self._buffs_multi

    @buffs_multi.setter
    def buffs_multi(self, value):
        self._buffs_multi = value
