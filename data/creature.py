"""A creature is the game's main entity, and represents
both the player and the ennemies alike."""

import random
import math
from data.numerics.ressource import Ressource
from data.numerics.rangestat import RangeStat
from data.numerics.stat import Stat
from data.numerics.affliction import Affliction
from data.numerics.damage import Damage
from data.constants import Flags, SYSTEM, trad
from data.item import Item
from data.image.hoverable import Hoverable

class Creature:
    """Defines a creature. A creature can be interacted with\
    and attacked.
    
    Args:
        name (str): Name of the creature."""
    def __init__(self, name):
        self._name = name
        self._level = 1
        self._exp = 0
        self._exp_to_next = 1000
        life_regen = Stat(0, "life_regen")
        mana_regen = Stat(0.001, "life_regen", precision=4)
        self._stats = {
            "life": Ressource(90, "Life", life_regen),
            "mana": Ressource(40, "Mana", mana_regen),

            "life_regen": life_regen,
            "mana_regen": mana_regen,

            "str": Stat(10, "Strength"),
            "dex": Stat(10, "Dexterity"),
            "int": Stat(10, "Intelligence"),
            "def": Stat(0, "Endurance"),
            "add_def": Stat(0, "add_def"),

            "exp_mult": Stat(1, "Exp Multiplier"),
            "abs_def": Stat(0, "Absolute Defense", scaling_value=0.001),
            "heal_factor": Stat(1, "Healing Effectivness"),
            "mana_efficiency": Stat(1, "Mana Efficiency", 1.95, 0.05, 0),
            "crit_rate": Stat(0.05, "Crit rate", 1, 0, scaling_value=0.001),
            "crit_dmg": Stat(1.5, "Crit Damage", scaling_value=0.02),
            "item_quant": Stat(0, "Item Quantity"),
            "item_qual": Stat(0, "Item Rarity"),
            "speed": Stat(1, "Move Speed", scaling_value=0.001),
            "cast_speed": Stat(1, "Cast Speed", scaling_value=0.001),

            "proj_quant": Stat(1, "proj_quant", scaling_value=0),
            "proj_speed": Stat(1, "proj_speed", scaling_value=0.001),
            "chains": Stat(0, "chains", scaling_value=0),

            "melee_dmg": Stat(1, "Melee Damage", scaling_value=0.01),
            "spell_dmg": Stat(1, "Spell Damage", scaling_value=0.01),
            "ranged_dmg": Stat(1, "Ranged Damage", scaling_value=0.01),

            "precision": Stat(1, "precision", scaling_value=0.01, min_cap=0),
            "block": Stat(0, "block", scaling_value=0, min_cap=0, max_cap=0.9),
            "dodge_rating": Stat(0, "dodge_rating", scaling_value=0, min_cap=0),
            "dodge": Stat(0, "dodge", scaling_value=0, min_cap=0, max_cap=0.95),

            "phys": Stat(0, "Physical resistance", 0.9, -2, scaling_value=0.005),
            "fire": Stat(0, "Fire resistance", 0.9, -2, scaling_value=0.005),
            "ice": Stat(0, "Ice resistance", 0.9, -2, scaling_value=0.005),
            "elec": Stat(0, "Electric resistance", 0.9, -2, scaling_value=0.005),
            "energy": Stat(0, "Energy resistance", 0.9, -2, scaling_value=0.005),
            "light": Stat(0, "Light resistance", 0.9, -2, scaling_value=0.005),
            "dark": Stat(0, "Dark resistance", 0.9, -2, scaling_value=0.005),
            "crit_res": Stat(0, "Crit res", 1, 0, scaling_value=0),

            "phys_flat": RangeStat(0, 0, "Physical damage", scaling_value=0.05),
            "fire_flat": RangeStat(0, 0, "Fire damage", scaling_value=0.05),
            "ice_flat": RangeStat(0, 0, "Ice damage", scaling_value=0.05),
            "elec_flat": RangeStat(0, 0, "Electric damage", scaling_value=0.05),
            "energy_flat": RangeStat(0, 0, "Energy damage", scaling_value=0.05),
            "light_flat": RangeStat(0, 0, "Light damage", scaling_value=0.05),
            "dark_flat": RangeStat(0, 0, "Dark damage", scaling_value=0.05),

            "phys_dmg": Stat(1, "Physical damage", scaling_value=0.05),
            "fire_dmg": Stat(1, "Fire damage", scaling_value=0.05),
            "ice_dmg": Stat(1, "Ice damage", scaling_value=0.05),
            "elec_dmg": Stat(1, "Electric damage", scaling_value=0.05),
            "energy_dmg": Stat(1, "Energy damage", scaling_value=0.05),
            "light_dmg": Stat(1, "Light damage", scaling_value=0.05),
            "dark_dmg": Stat(1, "Dark damage", scaling_value=0.05),

            "phys_pen": Stat(0, "Physical resistance penetration", 2, 0, scaling_value=0.01),
            "fire_pen": Stat(0, "Fire resistance penetration", 2, 0, scaling_value=0.01),
            "ice_pen": Stat(0, "Ice resistance penetration", 2, 0, scaling_value=0.01),
            "elec_pen": Stat(0, "Electric resistance penetration", 2, 0, scaling_value=0.01),
            "energy_pen": Stat(0, "Energy resistance penetration", 2, 0, scaling_value=0.01),
            "light_pen": Stat(0, "Light resistance penetration", 2, 0, scaling_value=0.01),
            "dark_pen": Stat(0, "Dark resistance penetration", 2, 0, scaling_value=0.01)
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
        self._ap = 0
        self.__get_bonuses_from_stat()
        self._stats["life"].refill()
        self._stats["mana"].refill()

    def recalculate_damage(self, damage_source: Damage) -> Damage:
        """Takes a raw damage source (ie from a spell) and applies the creature's
        own multipliers to it."""
        crit_roll = random.uniform(0, 1)
        crit = bool(crit_roll <= self._stats["crit_rate"].get_value())
        multi = damage_source.coeff
        flags = damage_source.flags
        if Flags.MELEE in flags:
            multi *= self._stats["melee_dmg"].get_value()
        if Flags.RANGED in flags:
            multi *= self._stats["ranged_dmg"].get_value()
        if Flags.SPELL in flags:
            multi *= self._stats["spell_dmg"].get_value()
        dmg = damage_source.types
        pen = damage_source.penetration

        phys = (dmg["phys"] + self._stats["phys_flat"].roll())\
                    * self._stats["phys_dmg"].get_value()
        fire = (dmg["fire"] + self._stats["fire_flat"].roll())\
                    * self._stats['fire_dmg'].get_value()
        ice = (dmg["ice"] + self._stats["ice_flat"].roll())\
                    * self._stats["ice_dmg"].get_value()
        elec = (dmg["elec"] + self._stats["elec_flat"].roll())\
                    * self._stats["elec_dmg"].get_value()
        energ = (dmg["energy"] + self._stats["energy_flat"].roll())\
                    * self._stats["energy_dmg"].get_value()
        light = (dmg["light"] + self._stats["light_flat"].roll())\
                    * self._stats["light_dmg"].get_value()
        dark = (dmg["dark"] + self._stats["dark_flat"].roll())\
                    * self._stats["dark_dmg"].get_value()

        pp = pen["phys"] + self._stats["phys_pen"].get_value()
        fp = pen["fire"] + self._stats["fire_pen"].get_value()
        ip = pen["ice"] + self._stats["ice_pen"].get_value()
        ep = pen["elec"] + self._stats["elec_pen"].get_value()
        enp = pen["energy"] + self._stats["energy_pen"].get_value()
        lp = pen["light"] + self._stats["light_pen"].get_value()
        dp = pen["dark"] + self._stats["dark_pen"].get_value()

        return Damage(multi, phys, fire, ice, elec, energ, light, dark, \
                      pp, fp, ip, ep, enp, lp, dp, crit,\
                      self._stats["crit_dmg"].get_value(), flags,\
                      damage_source.ignore_dodge, damage_source.ignore_block, self)

    def __get_bonuses_from_stat(self):
        """Generates the bonuses from the bases stats.\
        
        STR gives HP and melee damage. \
        INT gives MP and spell damage. \
        DEX gives crit chance and ranged damage.
        """
        hp = round(self._stats["str"].get_value())
        mp = round(self._stats["int"].get_value())
        crit = (self._stats["dex"].get_value() - 10) * 0.001
        melee = (self._stats["str"].get_value() - 10) * 0.01
        spell = (self._stats["int"].get_value() - 10) * 0.01
        ranged = (self._stats["dex"].get_value() - 10) * 0.01
        self.afflict(Affliction("str_to_hp", hp, -1, [Flags.LIFE, Flags.FLAT], False))
        self.afflict(Affliction("int_to_mp", mp, -1, [Flags.MANA, Flags.FLAT], False))
        self.afflict(Affliction("str_to_hp", crit, -1, [Flags.CRIT_CHANCE, Flags.BOON], False))
        self.afflict(Affliction("str_to_melee", melee, -1, [Flags.MELEE, Flags.BOON], False))
        self.afflict(Affliction("int_to_spell", spell, -1, [Flags.SPELL, Flags.BOON], False))
        self.afflict(Affliction("dex_to_ranged", ranged, -1, [Flags.RANGED, Flags.BOON], False))

    def __gather_flags(self) -> list:
        """Gathers all flags from all debuffs and buffs. Used to
        do special effects from unique affixes."""
        lst = []
        for afflic in self._buffs:
            if isinstance(afflic, Affliction):
                lst.extend(afflic.flags)
        return lst

    def __get_armor_mitigation(self) -> float:
        """Calculate and returns the mitigation from the endurance
        values.
        Thank you chatGPT for pulling that formula out of nowhere"""
        k = 0.0004
        a = 7000
        x = self.stats["def"].get_value()
        offset = 90 / (1 + math.exp(k * a))
        value = round((90 / (1 + math.exp(-k * (abs(x) - a))) - offset) / 100, 2)
        value += self._stats["add_def"].get_value()
        value = min(value, 0.9)
        return value

    def __get_dodge_chance(self, precision) -> float:
        """Calculate and returns the mitigation from the endurance
        values.
        Thank you chatGPT for pulling that formula out of nowhere"""
        k = 0.0004
        a = 7000
        x = self.stats["dodge_rating"].get_value() - precision
        offset = 90 / (1 + math.exp(k * a))
        value = round((90 / (1 + math.exp(-k * (abs(x) - a))) - offset) / 100, 2)
        value += self._stats["dodge"].get_value()
        value = min(value, 0.95)
        return value

    def damage(self, damage_source: Damage) -> tuple[float, bool]:
        """Deals damage to a creature. Adapts each source
        of damage from the damage to the creature's resistance.
        Returns the final damage as a float for display purpose.
        
        Args:
            damage (Damage): Source of damage.
        """
        unique_flags = self.__gather_flags()
        damage = 0
        dmg, pen = damage_source.get_damage()
        mitig = 1 - self.__get_armor_mitigation()
        if not damage_source.ignore_dodge:
            roll = random.uniform(0, 1)
            if roll <= self.__get_dodge_chance(damage_source.origin.stats["precision"].get_value()):
                return "Dodged !", False
        if not damage_source.ignore_block:
            roll = random.uniform(0, 1)
            if roll <= self._stats["block"].get_value():
                return "Blocked !", False
        for dmg_type in dmg:
            dmga = float(dmg[dmg_type]) * mitig
            res = self._stats[dmg_type].get_value() - pen[dmg_type]
            damage += dmga * (1 - res)
        if damage_source.is_crit:
            crit = damage_source.crit_mult * (1 - self._stats["crit_res"].get_value())
            if crit > 0:
                damage *= crit
        damage -= self._stats["abs_def"].get_value()
        damage = max(damage, 0)
        if Flags.ARMOR_MOM in unique_flags:
            life_dmg = damage * 0.65
            mana_dmg = damage * 0.35
            if self._stats["mana"].current_value < mana_dmg:
                mana = mana_dmg - self._stats["mana"].current_value
                life_dmg += mana
            self._stats["life"].modify(-life_dmg)
            self._stats["mana"].modify(-mana_dmg)
        else:
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
        value = max(value, 0)
        self._stats["mana"].modify(value)

    def get_efficient_value(self, base:float):
        """Returns the input value modified by the mana
        efficiency. """
        value = base * self._stats["mana_efficiency"].get_value()
        return value

    def afflict(self, affliction: Affliction):
        """Afflicts the creature with an affliction.
        
        Args:
            affliction (Affliction): Affliction to afflict.
        """
        for flag in affliction.flags:
            stat_key = flag.value
            if stat_key in self._stats:
                self._stats[stat_key].afflict(affliction)
            elif stat_key == "all_resistances":
                self._stats["phys"].afflict(affliction)
                self._stats["fire"].afflict(affliction)
                self._stats["ice"].afflict(affliction)
                self._stats["elec"].afflict(affliction)
                self._stats["energy"].afflict(affliction)
                self._stats["light"].afflict(affliction)
                self._stats["dark"].afflict(affliction)
            elif stat_key == "all_damage":
                self._stats["phys_dmg"].afflict(affliction)
                self._stats["fire_dmg"].afflict(affliction)
                self._stats["ice_dmg"].afflict(affliction)
                self._stats["elec_dmg"].afflict(affliction)
                self._stats["energy_dmg"].afflict(affliction)
                self._stats["light_dmg"].afflict(affliction)
                self._stats["dark_dmg"].afflict(affliction)
            elif stat_key == "elemental_resistances":
                self._stats["fire"].afflict(affliction)
                self._stats["ice"].afflict(affliction)
                self._stats["elec"].afflict(affliction)
            elif stat_key == "elemental_damage":
                self._stats["fire_dmg"].afflict(affliction)
                self._stats["ice_dmg"].afflict(affliction)
                self._stats["elec_dmg"].afflict(affliction)
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
            if buff.expired:
                self._buffs.remove(buff)
        for stat in self._stats:
            self._stats[stat].tick()

    def on_level_up(self):
        """Grants the creature a level, one ap (up to
        150), and refill its life and mana."""
        self._stats["life"].refill()
        self._stats["mana"].refill()
        if self._level <= 150:
            self._ap += 1
        SYSTEM["text_generator"].generate_level_up()

    def grant_experience(self, amount:int):
        """Grants a creature experience, leveling it up if needed.
        
        Args:
            amount (int): amount of experience won.
        """
        final_amount = self._stats["exp_mult"].value * amount
        self._exp += final_amount
        self._exp = round(self._exp)
        while self._exp >= self._exp_to_next:
            self._exp -= self._exp_to_next
            self._exp_to_next *= 1.35
            self._exp_to_next = round(self._exp_to_next)
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
        for affix in item.implicits:
            self.afflict(affix.as_affliction())
        self.__get_bonuses_from_stat()
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
        else:
            item = self._gear[slot.value]
            self._gear[slot.value] = None
        if item is not None:
            for affix in item.affixes :
                self.remove_affliction(affix.as_affliction())
            for affix in item.implicits :
                self.remove_affliction(affix.as_affliction())
        self.__get_bonuses_from_stat()
        return item

    def import_stackblock(self, statblock: dict):
        """Import a statblock and replace current
        stats with the block's."""
        for val in statblock:

            if val in self._stats:
                self.stats[val] = statblock[val].clone()

    def scale(self, level: int):
        """Scales the creature to the given level."""
        for stat in self._stats:
            self._stats[stat].scale(level)
        self._level = level
        self._stats["life"].refill()
        self._stats["mana"].refill()

    def generate_stat_simple(self, x, y):
        """Generates a simple report of the creature's data."""
        lines = []
        name = SYSTEM["font_detail"].render(f'{self._name}', False, (255, 255, 255))
        SYSTEM["windows"].blit(name, (x, y))
        life = Hoverable(x, y + 20, f"{self._stats['life'].get_value()}", SYSTEM["lang"]["life"])
        mana = Hoverable(x + 150, y + 20, f"{self._stats['mana'].get_value()}",\
                         SYSTEM["lang"]["mana"])
        exp1 = Hoverable(x + 90, y + 45, f"Level : {self._level}", SYSTEM["lang"]["exp"])
        exp2 = Hoverable(x + 70, y + 65, f"{self._exp}/{self._exp_to_next}", SYSTEM["lang"]["exp"])
        lines.append(life)
        lines.append(mana)
        lines.extend([exp1, exp2])
        return lines

    def generate_stat_details(self, x, y):
        """Generates a detailed report of the creature's data."""
        lines = []
        name = SYSTEM["font_detail"].render(f'{self._name}', False, (255, 255, 255))
        SYSTEM["windows"].blit(name, (x, y))
        life = Hoverable(x, y + 20, f"{self._stats['life'].get_value()}", trad("life"))
        mana = Hoverable(x + 150, y + 20, f"{self._stats['mana'].get_value()}",\
                         trad("mana"))
        exp1 = Hoverable(x + 90, y + 45, f"Level : {self._level}", trad("exp"))
        exp2 = Hoverable(x + 70, y + 65, f"{self._exp}/{self._exp_to_next}", trad("exp"))
        str = Hoverable(x, y + 90, f"{self._stats['str'].get_value()}", trad("str"), (255, 0, 0))
        int = Hoverable(x + 80, y + 90, f"{self._stats['int'].get_value()}",\
            trad("int"), (0, 0, 255))
        dex = Hoverable(x + 160, y + 90, f"{self._stats['dex'].get_value()}",\
            trad("dex"), (0, 255, 0))
        expb = Hoverable(x, y + 120, f"Exp Multiplier: {self._stats['exp_mult'].get_value()*100}%",\
             trad("exp_mult"))
        end = Hoverable(x, y + 135, f"Endurance: {self._stats['def'].get_value()}"\
            + f"(Estimated mitigation : {self.__get_armor_mitigation()*100}%)",\
            trad("def"))
        absdef = Hoverable(x, y + 150, f"Absolute defense: {self._stats['abs_def'].get_value()}",\
            trad("abs_def"))
        cr = Hoverable(x, y + 165, f"Crit chance: {self._stats['crit_rate'].get_value()*100}%",\
             trad("crit_rate"))
        cd = Hoverable(x, y + 180, f"Crit damage: {self._stats['crit_dmg'].get_value()*100}%",\
             trad("crit_dmg"))
        hf = Hoverable(x, y + 195,\
            f"Mana Efficiency: {self._stats['mana_efficiency'].get_value()*100}%",\
            trad("mana_efficiency"))
        me = Hoverable(x, y + 210, f"Heal Factor: {self._stats['heal_factor'].get_value()*100}%",\
             trad("heal_factor"))
        iir = Hoverable(x, y + 225, f"Item quantity: {self._stats['item_quant'].get_value()*100}%",\
             trad("item_quant"))
        iiq = Hoverable(x, y + 240, f"Item quality : {self._stats['item_qual'].get_value()*100}%",\
             trad("item_qual"))
        sp = Hoverable(x, y + 255, f"Move speed: {self._stats['speed'].get_value()*100}%",\
             trad("speed"))
        cs = Hoverable(x, y + 270, f"Cast speed: {self._stats['cast_speed'].get_value()*100}%",\
             trad("cast_speed"))
        md = Hoverable(x, y + 285, f"Melee damage: {self._stats['melee_dmg'].get_value()*100}%",\
             trad("melee_dmg"))
        sp = Hoverable(x, y + 300, f"Spell damage: {self._stats['spell_dmg'].get_value()*100}%",\
             trad("spell_dmg"))
        rd = Hoverable(x, y + 315, f"Ranged damage: {self._stats['ranged_dmg'].get_value()*100}%",\
             trad("ranged_dmg"))
        res = Hoverable(x, y + 350, "Resistances :", trad("res"))
        rp = Hoverable(x, y + 370, f"{self._stats['phys'].get_value()*100}%", trad("phys"),\
            (168, 168, 168))
        rf = Hoverable(x, y + 385, f"{self._stats['fire'].get_value()*100}%", trad("fire"),\
            (255, 119, 0))
        ri = Hoverable(x, y + 400, f"{self._stats['ice'].get_value()*100}%", trad("ice"),\
            (89, 219, 255))
        rt = Hoverable(x, y + 415, f"{self._stats['elec'].get_value()*100}%", trad("elec"),\
            (250, 233, 0))
        re = Hoverable(x, y + 430, f"{self._stats['energy'].get_value()*100}%", trad("energy"),\
            (156, 0, 5))
        rl = Hoverable(x, y + 445, f"{self._stats['light'].get_value()*100}%", trad("light"),\
            (255, 254, 219))
        rda = Hoverable(x, y + 460, f"{self._stats['dark'].get_value()*100}%", trad("dark"),\
            (71, 0, 125))
        dmg = Hoverable(x, y + 500, "Damages :", trad("dmg"))
        dp = Hoverable(x, y + 520, f"{self._stats['phys_dmg'].get_value()*100}%", trad("phys"),\
            (168, 168, 168))
        df = Hoverable(x, y + 535, f"{self._stats['fire_dmg'].get_value()*100}%", trad("fire"),\
            (255, 119, 0))
        di = Hoverable(x, y + 550, f"{self._stats['ice_dmg'].get_value()*100}%", trad("ice"),\
            (89, 219, 255))
        dt = Hoverable(x, y + 565, f"{self._stats['elec_dmg'].get_value()*100}%", trad("elec"),\
            (250, 233, 0))
        de = Hoverable(x, y + 580, f"{self._stats['energy_dmg'].get_value()*100}%", trad("energy"),\
            (156, 0, 5))
        dl = Hoverable(x, y + 595, f"{self._stats['light_dmg'].get_value()*100}%", trad("light"),\
            (255, 254, 219))
        dda = Hoverable(x, y + 610, f"{self._stats['dark_dmg'].get_value()*100}%", trad("dark"),\
            (71, 0, 125))
        pen = Hoverable(x, y + 650, "Penetration :", trad("pen"))
        pp = Hoverable(x, y + 670, f"{self._stats['phys_pen'].get_value()*100}%", trad("phys"),\
            (168, 168, 168))
        pf = Hoverable(x, y + 685, f"{self._stats['fire_pen'].get_value()*100}%", trad("fire"),\
            (255, 119, 0))
        pi = Hoverable(x, y + 700, f"{self._stats['ice_pen'].get_value()*100}%", trad("ice"),\
            (89, 219, 255))
        pt = Hoverable(x, y + 715, f"{self._stats['elec_pen'].get_value()*100}%", trad("elec"),\
            (250, 233, 0))
        pe = Hoverable(x, y + 730, f"{self._stats['energy_pen'].get_value()*100}%", trad("energy"),\
            (156, 0, 5))
        pl = Hoverable(x, y + 745, f"{self._stats['light_pen'].get_value()*100}%", trad("light"),\
            (255, 254, 219))
        pda = Hoverable(x, y + 760, f"{self._stats['dark_pen'].get_value()*100}%", trad("dark"),\
            (71, 0, 125))
        lines.append(life)
        lines.append(mana)
        lines.extend([exp1, exp2, str, int, dex, expb, absdef, cr, cd,\
                hf, me, iir, iiq, sp, cs, md, sp, rd, res, dmg, pen,\
                rp, rf, ri, rt, re, rl, rda, dp, df, di, dt, de, dl, dda,\
                pp, pf, pi, pt, pe, pl, pda, end])
        return lines

    def reset(self):
        """Resets the creature data."""
        for stat in self._stats:
            self._stats[stat].reset()
        self._buffs.clear()
        for gear in self._gear:
            if isinstance(self._gear[gear], dict):
                for gearr in self._gear[gear]:
                    if self._gear[gear][gearr] is not None:
                        for affix in self._gear[gear][gearr].affixes:
                            self.afflict(affix.as_affliction())
                        for affix in self._gear[gear][gearr].implicits:
                            self.afflict(affix.as_affliction())
            else:
                if self._gear[gear] is not None:
                    for affix in self._gear[gear].affixes:
                        self.afflict(affix.as_affliction())
                    for affix in self._gear[gear].implicits:
                        self.afflict(affix.as_affliction())
        self.__get_bonuses_from_stat()
        self._stats["life"].refill()
        self._stats["mana"].refill()

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

    @property
    def ap(self):
        """Returns the creatures's ability points.
        Only used for player characters."""
        return self._ap

    @ap.setter
    def ap(self, value):
        self._ap = value
