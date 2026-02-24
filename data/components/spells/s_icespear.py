"""Ice spear which breaks upon hitting an enemy."""

from data.constants import PROJECTILE_TRACKER, trad, SYSTEM, BLACK, Flags
from data.image.hoverable import Hoverable
from data.components.spells.spell import Spell
from data.components.projectiles.p_icespear import IceSpearProjectile

class IceSpear(Spell):
    """Unique spell component for ice spears."""
    def __init__(self, name, icon, attack_anim, base_damage, mana_cost=0, life_cost=0,
                 delay=0, explosion=None, cooldown=8, flags=None, debuffs=None,
                 effective_frames=None, alterations=None, debuff_chance=1, level_list=None,
                 secondary_damage=None, secondary_anim=None):
        super().__init__(name, icon, attack_anim, base_damage, mana_cost, life_cost,
                         0, delay, 0, 0, 0, explosion, None, cooldown,
                         1, flags, None, debuffs, 0, 0, 0,
                         effective_frames, None, alterations, debuff_chance, None, None,
                         level_list, 1)
        self._secondary_damage = secondary_damage
        self._secondary_anim = secondary_anim

    def spawn_projectile(self, entity, caster, evil=False, x_diff=0, y_diff=0, delay=1,
                         angle=0, ignore_team=False):
        area = self._stats["area"].c_value + caster.stats["area"].c_value
        debuffs, debuff_chance = self.generate_debuff_list(caster)
        x = entity.center[0] + x_diff
        y = entity.center[1] + y_diff
        proj = IceSpearProjectile(x, y,\
                        self._attack_anim,\
                        self._real_damage, caster, evil,\
                        delay=self._stats["delay"].c_value * delay,\
                        behaviours=self._flags, caster=entity, debuffs=debuffs,
                        explosion=self._explosion, area=area,\
                        ignore_team=ignore_team,
                        debuff_chance=debuff_chance,
                        secondary_damage=self._secondary_damage,
                        secondary_anim=self._secondary_anim)
        PROJECTILE_TRACKER.append(proj)

    def __shard_describe(self, caster):
        """Describes the damage and buffs components."""
        if self._secondary_damage is None:
            return None
        descript = ""
        if self._secondary_damage is not None:
            descript += self._secondary_damage.describe(caster,\
                Flags.MELEE in self._secondary_damage.flags,\
                Flags.RANGED in self._secondary_damage.flags, Flags.SPELL
                in self._secondary_damage.flags)
        return descript

    def __damage_describe(self, caster):
        """Describes the damage and buffs components."""
        descript = ""
        if self._real_damage is not None:
            descript += self._real_damage.describe(caster, Flags.MELEE in self.all_flags,\
                Flags.RANGED in self.all_flags, Flags.SPELL in self.all_flags)
        if Flags.DASH in self.all_flags:
            descript += f"{trad('meta_words', 'dash')} {self._stats['distance'].c_value}" +\
                f" {trad('meta_words', 'meters')}\n"
        return descript

    def __describe_afflictions(self):
        """Describe the spell's buff and debuff components."""
        debuff_chance = self._stats["debuff_chance"].c_value * \
            SYSTEM["player"].creature.stats["debuff_chance"].c_value
        buffs = []
        if Flags.BUFF in self.all_flags:
            for afflic in self._buffs:
                if Flags.TOGGLEABLE in self.all_flags:
                    buffs.append(afflic.aura_describe())
                else:
                    buffs.append(afflic.describe(True))
        if Flags.DEBUFF in self.all_flags:
            for afflic in self._debuffs:
                buffs.append(afflic.describe(False, debuff_chance))
        if Flags.CUTS_PROJECTILE in self.all_flags:
            buffs.append(Hoverable(0, 0, trad('meta_words', 'cut_proj'), None, BLACK))
        if Flags.TRIGGER in self.all_flags:
            buffs.append(Hoverable(0, 0, trad('meta_words', 'trigger'), None, BLACK))
        if Flags.TRIGGER_ON_CRIT in self.all_flags:
            buffs.append(Hoverable(0, 0, trad('meta_words', 'trigger_on_crit'), None, BLACK))
        return buffs

    def describe(self):
        """Returns a description of the spell."""
        sequence = None if len(self._sequence) == 0 else self._sequence
        explosion = {
            "damage": self.__shard_describe(SYSTEM["player"].creature),
            "buffs": [],
            "name": trad('spells_name', f"{self._name}_explosion"),
            "desc": trad('spells_desc', f"{self._name}_explosion"),
            "level": str(self._level),
            "cooldown": None,
            "projectiles": None,
            "area": self._stats['area'].c_value,
            "costs": (0, 0),
            "crit_rate": 1 + self._secondary_damage.crit_rate,
            "crit_dmg": 1 + self._secondary_damage.crit_mult,
            "dmg_effic": Hoverable(0, 0, f"{trad('descripts', 'dmg_effic')}:" +\
                f"{round(self._secondary_damage.coeff * 100, 2)}%",\
                trad('dmg_effic'), BLACK) if self._secondary_damage is not None else None,
            "sequence": None,
            "explosion": None
        }
        data = {
            "name": trad('spells_name', self._name),
            "desc": trad('spells_desc', self._name),
            "level": str(self._level),
            "damage": self.__damage_describe(SYSTEM["player"].creature),
            "buffs": self.__describe_afflictions(),
            "cooldown": str(self._stats["cooldown"].get_value() *\
                            SYSTEM["player"].creature.stats["cast_speed"].c_value),
            "costs": (self._stats["life_cost"].c_value, self._stats["mana_cost"].c_value),
            "projectiles": self._stats["projectiles"].c_value\
                if Flags.PROJECTILE in self.all_flags else None,
            "dmg_effic": Hoverable(0, 0, f"{trad('descripts', 'dmg_effic')}:" +\
                f"{round(self._base_damage.coeff * 100, 2)}%",\
                trad('dmg_effic'), BLACK) if self._base_damage is not None else None,
            "area": self._stats['area'].c_value,
            "crit_rate": self._stats['crit_rate'].c_value if\
                (self._real_damage is not None and not self._real_damage.is_crit) else True,
            "crit_dmg": self._stats['crit_dmg'].c_value,
            "sequence": sequence,
            "explosion_tab": trad('buttons', 'shards'),
            "explosion": explosion
        }
        return data
