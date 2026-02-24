"""Special spell component for ice orb."""

from data.constants import PROJECTILE_TRACKER
from data.components.spells.spell import Spell
from data.components.projectiles.p_darkorb import DarkOrbProjectile

class DarkOrb(Spell):
    """Unique spell component for ice orbs."""
    def __init__(self, name, icon, attack_anim, base_damage, mana_cost=0, life_cost=0,
                 delay=0, explosion=None, cooldown=8, flags=None, debuffs=None,
                 effective_frames=None, alterations=None, debuff_chance=1, level_list=None,
                 reset_rate=1, proj_damage=None, subprojectile=None):
        super().__init__(name, icon, attack_anim, base_damage, mana_cost, life_cost,
                         0, delay, 0, 0, 0, explosion, None, cooldown,
                         1, flags, None, debuffs, 0, 0, 0,
                         effective_frames, None, alterations, debuff_chance, None, None,
                         level_list, reset_rate)
        self._proj_damage = proj_damage if proj_damage is not None else base_damage
        self._subprojectile = subprojectile if subprojectile is not None else attack_anim

    def spawn_projectile(self, entity, caster, evil=False, x_diff=0, y_diff=0, delay=1,
                         angle=0, ignore_team=False):
        area = self._stats["area"].c_value + caster.stats["area"].c_value
        debuffs, debuff_chance = self.generate_debuff_list(caster)
        x = entity.center[0] + x_diff
        y = entity.center[1] + y_diff
        proj = DarkOrbProjectile(x, y,\
                        self._attack_anim,\
                        self._real_damage, caster, evil,\
                        delay=self._stats["delay"].c_value * delay,\
                        behaviours=self._flags, caster=entity, debuffs=debuffs,
                        explosion=self._explosion, area=area,\
                        ignore_team=ignore_team,
                        debuff_chance=debuff_chance,
                        reset_rate=self._stats["reset_rate"].c_value,
                        proj_damage=self._proj_damage,
                        subprojectile=self._subprojectile)
        PROJECTILE_TRACKER.append(proj)
