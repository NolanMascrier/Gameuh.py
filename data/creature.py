"""A creature is the game's main entity, and represents
both the player and the ennemies alike."""

from data.numerics.ressource import Ressource
from data.numerics.stat import Stat
from data.numerics.affliction import Affliction
from data.damage import Damage

class Creature:
    """Defines a creature. A creature can be interacted with\
    and attacked.
    
    Args:
        name (str): Name of the creature."""
    def __init__(self, name):
        self._name = name
        self._level = 1
        self._exp = 0
        self._exp_to_next = 100
        self._stats = {
            "life": Ressource(100, "Life", 0),
            "mana": Ressource(50, "Mana", 5),

            "str": Stat(10, "Strength"),
            "dex": Stat(10, "Dexterity"),
            "int": Stat(10, "Intelligence"),
            "def": Stat(0, "Endurance"),
            "mdef": Stat(0, "Spirit"),

            "exp_mult": Stat(1, "Exp Multiplier"),
            "abs_def": Stat(0, "Absolute Defense"),
            "heal_factor": Stat(1, "Healing Effectivness"),
            "crit_rate": Stat(0.05, "Crit rate"),
            "crit_dmg": Stat(1.5, "Crit Damage"),
            "dodge": Stat(0, "Evasion"),
            "precision": Stat(0, "Precision"),
            "item_quant": Stat(0, "Item Quantity"),
            "item_qual": Stat(0, "Item Rarity"),

            "speed": Stat(1, "Move Speed"),
            "phys": Stat(0, "Physical resistance"),
            "fire": Stat(0, "Fire resistance"),
            "ice": Stat(0, "Ice resistance"),
            "elec": Stat(0, "Electric resistance"),
            "energy": Stat(0, "Energy resistance"),
            "light": Stat(0, "Light resistance"),
            "dark": Stat(0, "Dark resistance")
        }
        self._buffs = []

    def damage(self, damage_source: Damage):
        """Deals damage to a creature. Adapts each source
        of damage from the damage to the creature's resistance.
        
        Args:
            damage (Damage): Source of damage.
        """
        damage = 0
        dmg, pen = damage_source.get_damage()
        for dmg_type in dmg:
            dmga = float(dmg[dmg_type])
            res = self._stats[dmg_type].get_value() - pen[dmg_type]
            damage += dmga * (1 - res)
        self._stats["life"].modify(-damage)

    def heal(self, amount: float):
        """Restores a certain amount of life to
        the creature.
        
        Args:
            amount (float): amount to restore that will be \
            multiplied by the heal factor.
        """
        value = amount * self._stats["heal_factor"].get_value()
        self._stats["life"].modify(value)

    def afflict(self, affliction: Affliction):
        """Afflicts the creature with an affliction.
        
        Args:
            affliction (Affliction): Affliction to afflict.
        """
        self._buffs.append(affliction)
        for flag in affliction.flags:
            stat_key = flag.value
            if stat_key in self._stats:
                self._stats[stat_key].afflict(affliction)

    def tick(self):
        """Ticks down all buffs and debuffs."""
        for buff in self._buffs.copy():
            buff.tick()
            if buff.duration == 0:
                self._buffs.remove(buff)
        for stat in self._stats:
            self._stats[stat].tick()

    @property
    def name(self) -> str:
        """Returns the creature's name."""
        return self._name

    @name.setter
    def name(self, value):
        self._name = value

    @property
    def level(self) -> int:
        """Return's the creature's level."""
        return self._level

    @level.setter
    def level(self, value):
        self._level = value

    @property
    def exp(self) -> int:
        """Return's the creature's experience."""
        return self._exp

    @exp.setter
    def exp(self, value):
        self._exp = value

    @property
    def exp_to_next(self) -> int:
        """Return's the creature's needed experience \
        to level up."""
        return self._exp_to_next

    @exp_to_next.setter
    def exp_to_next(self, value):
        self._exp_to_next = value

    @property
    def stats(self):
        """Return the creature's stat block."""
        return self._stats

    @stats.setter
    def stats(self, value):
        self._stats = value

    @property
    def buffs(self):
        """Returns the creature's buffs and debuffs
        list."""
        return self._buffs

    @buffs.setter
    def buffs(self, value):
        self._buffs = value
