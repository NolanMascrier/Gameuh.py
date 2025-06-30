"""Defines a damage source. A damage source is a 
collection of various multipliers, one for each damage
type, and one for the initial power of the ability. A
damage source also has a flat damage.

P stands for penetration, ie how much of the
resistance the damage source shall ignore."""

import random

class Damage():
    """A source of damage is a group of numbers that will \
    be substracted from a creature's life. While all arguments \
    are optionnal aside from damage and base, a damage \
    source will need at least one resistance modifier to \
    work, or the resulting damage will be 0.
    
    Args:
        multiplier (float): Multiplier of the source,\
        aka "Efficiency of added damage"
        phys (float, optionnal): Physical damage.\
        Defaults to 0.
        phys (float, optionnal): Physical damage.\
        Defaults to 0.
        fire (float, optionnal): Fire damage.\
        Defaults to 0.
        ice (float, optionnal): Ice damage.\
        Defaults to 0.
        elec (float, optionnal): Electric damage.\
        Defaults to 0.
        energ (float, optionnal): Energy damage.\
        Defaults to 0.
        light (float, optionnal): Light damage.\
        Defaults to 0.
        dark (float, optionnal): Darkness damage.\
        Defaults to 0.
        pp (float, optionnal): Physical penetration factor.\
        Defaults to 0.
        fp (float, optionnal): Fire penetration factor.\
        Defaults to 0.
        ip (float, optionnal): Ice penetration factor.\
        Defaults to 0.
        ep (float, optionnal): Electric penetration factor.\
        Defaults to 0.
        enp (float, optionnal): Energy penetration factor.\
        Defaults to 0.
        lp (float, optionnal): Light penetration factor.\
        Defaults to 0.
        dp (float, optionnal): Darkness penetration factor.\
        Defaults to 0.
        is_crit (bool, optionnal): Whether or not the hit is \
        critical. Defaults to False.
        crit_mult (float, optionnal): Critical multiplier of the\
        damage source. Defaults to 1.5.
        Flags (list, optionnal): List of the damage source flags\
        ie Melee, Ranged or Spell. Defaults to None.
        ignore_dodge (bool, optional): Whether or not this damage\
        should ignore chances to dodge. Defaults to False.
        ignore_block (bool, optional): Whether or not this damage\
        should ignore chances to block. Defaults to False.
        origin (creature, optional): Tracker to the damage's\
        creator. Defaults to None.
        lower_bound (float, optionnal): Minimal value for the damage\
        roll. Defaults to 0.9.
        upper_bound (float, optionnal): Maximal value for the damage\
        roll. Defaults to 1.1.
    """
    def __init__(self, multiplier, phys = 0, fire = 0, ice = 0,\
                elec = 0, energ = 0, light = 0, dark = 0, pp = 0, fp = 0, \
                ip = 0, ep = 0, enp = 0, lp = 0, dp = 0, is_crit = False, \
                crit_mult = 1.5, flags = None, ignore_dodge = False,\
                ignore_block = False, origin = None, lower_bound = 0.9,\
                upper_bound = 1.1):
        self._coeff = multiplier
        self._types = {
            "phys": phys,
            "fire": fire,
            "ice": ice,
            "elec": elec,
            "energy": energ,
            "light": light,
            "dark": dark
        }
        self._penetration = {
            "phys": pp,
            "fire": fp,
            "ice": ip,
            "elec": ep,
            "energy": enp,
            "light": lp,
            "dark": dp
        }
        self._is_crit = is_crit
        self._crit_mult = crit_mult
        if flags is None or not isinstance(flags, list):
            self._flags = []
        else:
            self._flags = flags
        self._ignore_block = ignore_block
        self._ignore_dodge = ignore_dodge
        self._origin = origin
        self._bounds = (lower_bound, upper_bound)

    def get_damage(self):
        """Returns the computed damage.
        
        Returns:
            tuple(dict(str, float), dict(str, float)): 
            List of damages and list of \
            penetration values.
        """
        damages = {
            "phys": self._types["phys"] * random.uniform(self._bounds[0], self._bounds[1])\
                                        * self._coeff,
            "fire": self._types["fire"] * random.uniform(self._bounds[0], self._bounds[1])\
                                        * self._coeff,
            "ice": self._types["ice"] * random.uniform(self._bounds[0], self._bounds[1])\
                                        * self._coeff,
            "elec": self._types["elec"] * random.uniform(self._bounds[0], self._bounds[1])\
                                        * self._coeff,
            "energy": self._types["energy"] * random.uniform(self._bounds[0], self._bounds[1])\
                                        * self._coeff,
            "light": self._types["light"] * random.uniform(self._bounds[0], self._bounds[1])\
                                        * self._coeff,
            "dark": self._types["dark"] * random.uniform(self._bounds[0], self._bounds[1])\
                                        * self._coeff
        }
        return damages, self._penetration

    @property
    def coeff(self):
        """Returns the damage multiplier of the source."""
        return self._coeff

    @coeff.setter
    def coeff(self, value):
        self._coeff = value

    @property
    def types(self):
        """Returns the damage type multipliers."""
        return self._types

    @types.setter
    def types(self, value):
        self._types = value

    @property
    def penetration(self):
        """Returns the penetrations factor"""
        return self._penetration

    @penetration.setter
    def penetration(self, value):
        self._penetration = value

    @property
    def flags(self):
        """Returns the damage source's flags."""
        return self._flags

    @flags.setter
    def flags(self, value):
        self._flags = value

    @property
    def is_crit(self):
        """Returns whether or not the damage is critical."""
        return self._is_crit

    @property
    def crit_mult(self):
        """Returns the critical multiplier of the damage."""
        return self._crit_mult

    @property
    def ignore_block(self):
        """Returns whether or not the damage can be blocked."""
        return self._ignore_block

    @ignore_block.setter
    def ignore_block(self, value):
        self._ignore_block = value

    @property
    def ignore_dodge(self):
        """Returns whether or not the damage can be dodged."""
        return self._ignore_dodge

    @ignore_dodge.setter
    def ignore_dodge(self, value):
        self._ignore_dodge = value

    @property
    def origin(self):
        """Returns the creature at the origin of the damage."""
        return self._origin

    @origin.setter
    def origin(self, value):
        self._origin = value
