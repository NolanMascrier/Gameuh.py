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

    def add_flat(self, flat):
        """Adds a flat increase to the max value. Increases must \
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
        """Adds an increase to the max value. Increases must \
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
        """Adds a multiplier to the max value. Multipliers must \
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
