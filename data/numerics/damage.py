"""Defines a damage source. A damage source is a 
collection of various multipliers, one for each damage
type, and one for the initial power of the ability. A
damage source also has a flat damage.

P stands for penetration, ie how much of the
resistance the damage source shall ignore."""

import json
import random
from data.constants import trad

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
        crit_rate (float, optional): Default critical chance of the damage\
        source. Defaults to 5%.
    """
    def __init__(self, multiplier, phys = 0, fire = 0, ice = 0,\
                elec = 0, energ = 0, light = 0, dark = 0, pp = 0, fp = 0, \
                ip = 0, ep = 0, enp = 0, lp = 0, dp = 0, is_crit = False, \
                crit_mult = 1.5, flags = None, ignore_dodge = False,\
                ignore_block = False, origin = None, lower_bound = 0.9,\
                upper_bound = 1.1, crit_rate = 0.05):
        self._coeff = multiplier
        self._mod = 1
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
        self._crit_rate = crit_rate
        if flags is None or not isinstance(flags, list):
            self._flags = []
        else:
            self._flags = flags
        self._ignore_block = ignore_block
        self._ignore_dodge = ignore_dodge
        self._origin = origin
        self._bounds = (lower_bound, upper_bound)

    def get_damage(self):
        """Returns the rolled flat damage.
        
        Returns:
            tuple(dict(str, float), dict(str, float)): 
            List of damages and list of \
            penetration values.
        """
        damages = {
            "phys": self._types["phys"] * random.uniform(self._bounds[0], self._bounds[1]),
            "fire": self._types["fire"] * random.uniform(self._bounds[0], self._bounds[1]),
            "ice": self._types["ice"] * random.uniform(self._bounds[0], self._bounds[1]),
            "elec": self._types["elec"] * random.uniform(self._bounds[0], self._bounds[1]),
            "energy": self._types["energy"] * random.uniform(self._bounds[0], self._bounds[1]),
            "light": self._types["light"] * random.uniform(self._bounds[0], self._bounds[1]),
            "dark": self._types["dark"] * random.uniform(self._bounds[0], self._bounds[1])
        }
        return damages, self._penetration

    def describe(self, caster, is_melee = False, is_ranged = False, is_spell = False):
        """Returns a text description of the damage.
        Simulates the damage from a caster."""
        types = ["phys", "fire", "ice", "elec", "energy", "light", "dark"]
        txt = ""
        mult = 1
        total = [0, 0]
        if is_melee:
            mult *= caster.stats["melee_dmg"].c_value
        if is_ranged:
            mult *= caster.stats["ranged_dmg"].c_value
        if is_spell:
            mult *= caster.stats["spell_dmg"].c_value
        for typ in types:
            type_mult = caster.stats[f"{typ}_dmg"].c_value * mult
            low_roll = self._types[typ] * self._bounds[0] * type_mult
            hig_roll = self._types[typ] * self._bounds[1] * type_mult
            added_low = caster.stats[f"{typ}_flat"].lower.c_value * type_mult * self._coeff
            added_high = caster.stats[f"{typ}_flat"].upper.c_value * type_mult * self._coeff
            low = (low_roll + added_low) * self._mod
            up = (hig_roll + added_high) * self._mod
            if low == 0 and up == 0:
                continue
            total[0] += round(low)
            total[1] += round(up)
            txt += f"{trad('meta_words', 'deal')} {round(low)}-{round(up)} " +\
                f"{trad('meta_words', typ)} {trad('meta_words', 'damage')}\n"
        return txt + f"{trad('meta_words', 'total')}: {total[0]}-{total[1]}\n"

    def clone(self):
        """Creates a deep copy of the damage source."""
        dmg = Damage(self._coeff, is_crit=self._is_crit, crit_mult=self._crit_mult,
            flags=self._flags.copy(), ignore_block=self._ignore_block,
            ignore_dodge=self._ignore_dodge, origin=self._origin,
            lower_bound=self._bounds[0], upper_bound=self._bounds[1])
        dmg.types = self._types.copy()
        dmg.penetration = self._penetration.copy()
        return dmg

    def export(self) -> str:
        """Serialize the damage as JSON data."""
        data = {
            "type": "damage",
            "coeff": self._coeff,
            "types": self._types,
            "pen": self._penetration,
            "min_bound": self._bounds[0],
            "max_bound": self._bounds[1],
            "ignore_block": self._ignore_block,
            "ignore_dodge": self._ignore_dodge,
            "flags": self._flags,
            "crit": self._crit_mult
        }
        return json.dumps(data)

    @staticmethod
    def imports(data):
        """Reads JSON data and creates a damage instance."""
        dmg = Damage(
            float(data["coeff"]),
            crit_mult=float(data["crit"]),
            flags=data["flags"],
            ignore_block=bool(data["ignore_block"]),
            ignore_dodge=bool(data["ignore_dodge"]),
            lower_bound=float(data["min_bound"]),
            upper_bound=float(data["max_bound"]),
        )
        dmg.types = data["types"]
        dmg.penetration = data["pen"]
        return dmg

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

    @crit_mult.setter
    def crit_mult(self, value):
        self._crit_mult = value

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

    @property
    def crit_rate(self):
        """Returns the damage source's crit rate."""
        return self._crit_rate

    @crit_rate.setter
    def crit_rate(self, value):
        self._crit_rate = value

    @property
    def mod(self):
        """Returns the damage source's final damage modifier."""
        return self._mod

    @mod.setter
    def mod(self, value):
        self._mod = value
