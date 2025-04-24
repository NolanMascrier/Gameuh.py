"""Defines a damage source. A damage source is a 
collection of various multipliers, one for each damage
type, and one for the initial power of the ability. A
damage source also has a flat damage.

P stands for penetration, ie how much of the
resistance the damage source shall ignore."""

class Damage():
    """A source of damage is a group of numbers that will \
    be substracted from a creature's life. While all arguments \
    are optionnal aside from damage and base, a damage \
    source will need at least one resistance modifier to \
    work, or the resulting damage will be 0.
    
    Args:
        damage (float): Base damage of the source.
        multiplier (float): Multiplier of the source.
        phys (float, optionnal): Physical damage multiplier.\
        Defaults to 0.
        phys (float, optionnal): Physical damage multiplier.\
        Defaults to 0.
        fire (float, optionnal): Fire damage multiplier.\
        Defaults to 0.
        ice (float, optionnal): Ice damage multiplier.\
        Defaults to 0.
        elec (float, optionnal): Electric damage multiplier.\
        Defaults to 0.
        energ (float, optionnal): Energy damage multiplier.\
        Defaults to 0.
        light (float, optionnal): Light damage multiplier.\
        Defaults to 0.
        dark (float, optionnal): Darkness damage multiplier.\
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
    """
    def __init__(self, damage, multiplier, phys = 0, fire = 0, ice = 0,\
                elec = 0, energ = 0, light = 0, dark = 0, pp = 0, fp = 0, \
                ip = 0, ep = 0, enp = 0, lp = 0, dp = 0):
        self._base = damage
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

    def get_damage(self):
        """Returns the computed damage.
        
        Returns:
            tuple(dict(str, float), dict(str, float)): 
            List of damages and list of \
            penetration values.
        """
        init_damage = self._base * self._coeff
        damages = {
            "phys": init_damage * self._types["phys"],
            "fire": init_damage * self._types["fire"],
            "ice": init_damage * self._types["ice"],
            "elec": init_damage * self._types["elec"],
            "energy": init_damage * self._types["energy"],
            "light": init_damage * self._types["light"],
            "dark": init_damage * self._types["dark"]
        }
        return damages, self._penetration

    @property
    def base(self):
        """Returns the base damage of the source."""
        return self._base

    @base.setter
    def base(self, value):
        self._base = value

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
