from numerics.Ressource import Ressource
from numerics.Stat import Stat
from Damage import Damage

class Creature:
    def __init__(self, name):
        self._name = name
        self._life = Ressource(100, "Life", 0)
        self._mana = Ressource(50, "Mana", 5)
        self._exp = 0
        self._exp_to_next = 100
        self._stats = {
            "str": Stat(10, "Strength"),
            "dex": Stat(10, "Dexterity"),
            "int": Stat(10, "Intelligence"),
            "def": Stat(0, "Endurance"),
            "mdef": Stat(0, "Spirit")
        }
        self._substats = {
            "exp_mult": Stat(1, "Exp Multiplier"),
            "abs_def": Stat(0, "Absolute Defense"),
            "heal_factor": Stat(1, "Healing Effectivness"),
            "crit_rate": Stat(0.05, "Crit rate"),
            "crit_dmg": Stat(1.5, "Crit Damage"),
            "dodge": Stat(0, "Evasion"),
            "precision": Stat(0, "Precision")
        }
        self._defenses = {
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
        for dmg in damage_source.get_damage():
            damage += damage_source.get_damage()[dmg] * self._defenses[dmg]
        self._life._value -= damage
        
    def heal(self, amount: float):
        """Restores a certain amount of life to
        the creature.
        
        Args:
            amount (float): amount to restore that will be \
            multiplied by the heal factor.
        """