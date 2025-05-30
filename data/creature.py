"""A creature is the game's main entity, and represents
both the player and the ennemies alike."""

import random
from data.numerics.ressource import Ressource
from data.numerics.stat import Stat
from data.numerics.affliction import Affliction
from data.damage import Damage
from data.constants import Flags, SYSTEM
from data.item import Item

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
            "mana": Ressource(50, "Mana", 0.001),

            "str": Stat(10, "Strength"),
            "dex": Stat(10, "Dexterity"),
            "int": Stat(10, "Intelligence"),
            "def": Stat(0, "Endurance"),
            "mdef": Stat(0, "Spirit"),

            "exp_mult": Stat(1, "Exp Multiplier"),
            "abs_def": Stat(0, "Absolute Defense"),
            "heal_factor": Stat(1, "Healing Effectivness"),
            "mana_efficiency": Stat(1, "Mana Efficiency"),
            "crit_rate": Stat(0.05, "Crit rate"),
            "crit_dmg": Stat(1.5, "Crit Damage"),
            "dodge": Stat(0, "Evasion"),
            "precision": Stat(0, "Precision"),
            "item_quant": Stat(0, "Item Quantity"),
            "item_qual": Stat(0, "Item Rarity"),
            "speed": Stat(1, "Move Speed"),
            "cast_speed": Stat(1, "Cast Speed"),

            "melee_dmg": Stat(1, "Melee Damage"),
            "spell_dmg": Stat(1, "Spell Damage"),
            "ranged_dmg": Stat(1, "Ranged Damage"),

            "phys": Stat(0, "Physical resistance"),
            "fire": Stat(0, "Fire resistance"),
            "ice": Stat(0, "Ice resistance"),
            "elec": Stat(0, "Electric resistance"),
            "energy": Stat(0, "Energy resistance"),
            "light": Stat(0, "Light resistance"),
            "dark": Stat(0, "Dark resistance"),

            "phys_dmg": Stat(1, "Physical damage"),
            "fire_dmg": Stat(1, "Fire damage"),
            "ice_dmg": Stat(1, "Ice damage"),
            "elec_dmg": Stat(1, "Electric damage"),
            "energy_dmg": Stat(1, "Energy damage"),
            "light_dmg": Stat(1, "Light damage"),
            "dark_dmg": Stat(1, "Dark damage"),

            "phys_pen": Stat(0, "Physical resistance penetration"),
            "fire_pen": Stat(0, "Fire resistance penetration"),
            "ice_pen": Stat(0, "Ice resistance penetration"),
            "elec_pen": Stat(0, "Electric resistance penetration"),
            "energy_pen": Stat(0, "Energy resistance penetration"),
            "light_pen": Stat(0, "Light resistance penetration"),
            "dark_pen": Stat(0, "Dark resistance penetration")
        }
        self._gear = {
            "helm": None,
            "hands": None,
            "armor": None,
            "belt": None,
            "boots": None,
            "weapon": None,
            "off_hand": None,
            "relic": None,
            "amulet": None,
            "ring": {
                "left": None,
                "right": None
            }
        }
        self._buffs = []
        self._abilities = []

    def recalculate_damage(self, damage_source: Damage) -> Damage:
        """Takes a raw damage source (ie from a spell) and applies the creature's
        own multipliers to it."""
        crit_roll = random.uniform(0, 1)
        crit = bool(crit_roll <= self._stats["crit_rate"].get_value())
        flat = damage_source.base
        flags = damage_source.flags
        if Flags.MELEE in flags:
            flat *= self._stats["melee_dmg"].get_value()
        if Flags.RANGED in flags:
            flat *= self._stats["ranged_dmg"].get_value()
        if Flags.SPELL in flags:
            flat *= self._stats["spell_dmg"].get_value()
        multi = damage_source.coeff
        dmg = damage_source.types
        pen = damage_source.penetration
        phys = dmg["phys"] * self._stats["phys_dmg"].get_value()
        fire = dmg["fire"] * self._stats["fire_dmg"].get_value()
        ice = dmg["ice"] * self._stats["ice_dmg"].get_value()
        elec = dmg["elec"] * self._stats["elec_dmg"].get_value()
        energ = dmg["energy"] * self._stats["energy_dmg"].get_value()
        light = dmg["light"] * self._stats["light_dmg"].get_value()
        dark = dmg["dark"] * self._stats["dark_dmg"].get_value()

        pp = pen["phys"] + self._stats["phys_pen"].get_value()
        fp = pen["fire"] + self._stats["fire_pen"].get_value()
        ip = pen["ice"] + self._stats["ice_pen"].get_value()
        ep = pen["elec"] + self._stats["elec_pen"].get_value()
        enp = pen["energy"] + self._stats["energy_pen"].get_value()
        lp = pen["light"] + self._stats["light_pen"].get_value()
        dp = pen["dark"] + self._stats["dark_pen"].get_value()

        return Damage(flat, multi, phys, fire, ice, elec, energ, light, dark, \
                      pp, fp, ip, ep, enp, lp, dp, crit,\
                      self._stats["crit_dmg"].get_value(), flags)


    def damage(self, damage_source: Damage) -> float:
        """Deals damage to a creature. Adapts each source
        of damage from the damage to the creature's resistance.
        Returns the final damage as a float for display purpose.
        
        Args:
            damage (Damage): Source of damage.
        """
        damage = 0
        dmg, pen = damage_source.get_damage()
        for dmg_type in dmg:
            dmga = float(dmg[dmg_type])
            res = self._stats[dmg_type].get_value() - pen[dmg_type]
            damage += dmga * (1 - res)
        if damage_source.is_crit:
            damage *= damage_source.crit_mult
        self._stats["life"].modify(-damage)
        return round(damage, 2), damage_source.is_crit

    def heal(self, amount: float):
        """Restores a certain amount of life to
        the creature.
        
        Args:
            amount (float): amount to restore that will be \
            multiplied by the heal factor.
        """
        value = amount * self._stats["heal_factor"].get_value()
        self._stats["life"].modify(value)

    def consume_mana(self, cost: float):
        """Comsumes mana from a creature. Consumed mana is\
        reduced by the creature's mana efficiency.
        
        Args:
            cost (float): Amount to consume.
        """
        value = cost * self._stats["mana_efficiency"].get_value()
        self._stats["mana"].modify(-value)

    def restore_mana(self, amount: float):
        """Restores a certain amount of mana to
        the creature.
        
        Args:
            amount (float): amount to restore that will be \
            multiplied by the mana efficiency.
        """
        mod = self._stats["mana_efficiency"].get_value()
        value = amount * (1 + (1 - mod))
        if value <= 0:
            value = 0
        self._stats["mana"].modify(value)

    def afflict(self, affliction: Affliction):
        """Afflicts the creature with an affliction.
        
        Args:
            affliction (Affliction): Affliction to afflict.
        """
        for flag in affliction.flags:
            stat_key = flag.value
            if stat_key in self._stats:
                self._stats[stat_key].afflict(affliction)
        if affliction.stackable:
            self._buffs.append(affliction)
        else:
            for i, existing_aff in enumerate(self._buffs):
                if existing_aff.name == affliction.name:
                    self._buffs[i] = affliction
                    return
            self._buffs.append(affliction)

    def remove_affliction(self, affliction: Affliction):
        """Removes an affliction from the character.
        
        Args:
            affliction (Affliction): Affliction to remove.
        """
        for d in self._buffs.copy():
            if d == affliction:
                self._buffs.remove(d)
        for st in self._stats:
            self._stats[st].remove_affliction(affliction)

    def tick(self):
        """Ticks down all buffs and debuffs."""
        for buff in self._buffs.copy():
            buff.tick()
            if buff.duration <= 0:
                self._buffs.remove(buff)
        for stat in self._stats:
            self._stats[stat].tick()

    def on_level_up(self):
        """Does an action on level up. Empty by
        default, function to overide for player
        characters."""

    def grant_experience(self, amount:int):
        """Grants a creature experience, leveling it up if needed.
        
        Args:
            amount (int): amount of experience won.
        """
        final_amount = self._stats["exp_mult"].value * amount
        self._exp += final_amount
        while self._exp >= self._exp_to_next:
            self._exp -= self._exp_to_next
            self._exp_to_next *= 1.2
            self._level += 1
            self.on_level_up()

    def equip(self, slot: Flags, item: Item, left_hand = False) -> Item | None:
        """Equips an item in the slot. Returns the
        equipped item if the slot is already occupied.
        
        Args:
            slot (Flags):Flag of the slot to equip.
            item (Item): Item to equip. The item needs the GEAR flag !
            left_hand (bool, optionnal): If the slot is\
            a ring, `True` will indicate the left ring\
            and `False` the right ring. Defaults to `False`.
        """
        if item is None or Flags.GEAR not in item.flags:
            return None
        if slot.value not in self._gear:
            return None
        old = self.unequip(slot, left_hand)
        if slot == Flags.RING:
            if left_hand:
                self._gear["ring"]["left"] = item
            else:
                self._gear["ring"]["right"] = item
        else:
            self._gear[slot.value] = item
        for affix in item.affixes:
            self.afflict(affix.as_affliction())
        return old

    def unequip(self, slot: Flags, left_hand = False) -> Item | None:
        """Removes an item from the user's gear, and returns it.
        
        Args:
            slot (Flags): Flag of the slot to empty.
            left_hand (bool, optionnal): If the slot is\
            a ring, `True` will indicate the left ring\
            and `False` the right ring. Defaults to `False`.
        
        Returns:
            item: Item removed. `None` if the slot was\
            empty.
        """
        if slot.value not in self._gear:
            return None
        if slot == Flags.RING:
            if left_hand:
                item = self._gear["ring"]["left"]
                self._gear["ring"]["left"] = None
            else:
                item = self._gear["ring"]["right"]
                self._gear["ring"]["right"] = None
        item = self._gear[slot.value]
        self._gear[slot.value] = None
        if item is not None:
            for affix in item.affixes :
                self.remove_affliction(affix.as_affliction())
        return item

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

    @property
    def gear(self):
        """Returns the creature's gear."""
        return self._gear

    @gear.setter
    def gear(self, value):
        self._gear = value

    @property
    def abilities(self):
        """Returns the creature's abilities."""
        return self._abilities

    @abilities.setter
    def abilities(self, value):
        self._abilities = value
