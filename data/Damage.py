"""Defines a damage source. A damage source is a 
collection of various multipliers, one for each damage
type, and one for the initial power of the ability. A
damage source also has a flat damage."""

class Damage():
    def __init__(self, damage, multiplier, phys = 0, fire = 0, ice = 0,\
                elec = 0, energ = 0, light = 0, dark = 0):
        self._base = damage
        self._coeff = multiplier
        self._types = {
            "phys": phys,
            "fire": fire,
            "ice": ice,
            "elec": elec,
            "energ": energ,
            "light": light,
            "dark": dark
        }
        
    def get_damage(self):
        """Returns the computed damage.
        
        Returns:
            dict(str, float): List of damages."""
        init_damage = self._base * self._coeff
        damages = {
            "phys": init_damage * self._types["phys"],
            "fire": init_damage * self._types["fire"],
            "ice": init_damage * self._types["ice"],
            "elec": init_damage * self._types["elec"],
            "energ": init_damage * self._types["energ"],
            "light": init_damage * self._types["light"],
            "dark": init_damage * self._types["dark"]
        }
        return damages