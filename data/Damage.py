"""Defines a damage source. A damage source is a 
collection of various multipliers, one for each damage
type, and one for the initial power of the ability. A
damage source also has a flat damage.

P stands for penetration, ie how much of the
resistance the damage source shall ignore."""

class Damage():
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