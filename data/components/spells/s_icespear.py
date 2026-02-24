"""Ice spear which breaks upon hitting an enemy."""

from data.constants import PROJECTILE_TRACKER
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
