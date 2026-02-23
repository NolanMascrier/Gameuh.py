"""Special spell component for meteor."""

from data.constants import SYSTEM, PROJECTILE_TRACKER
from data.components.spells.spell import Spell
from data.components.projectiles.p_meteor import MeteorProjectile
from data.game.creature import Creature
from data.physics.entity import Entity

class Meteor(Spell):
    """Unique spell component for meteor."""
    def __init__(self, name, icon, attack_anim, base_damage, mana_cost=0, life_cost=0,
                 delay=0, explosion=None, cooldown=8, flags=None, debuffs=None,
                 effective_frames=None, alterations=None, debuff_chance=1, level_list=None,
                 reset_rate = 1):
        super().__init__(name, icon, attack_anim, base_damage, mana_cost, life_cost,
                         0, delay, 0, 0, 0, explosion, None, cooldown,
                         1, flags, None, debuffs, 0, 0, 0,
                         effective_frames, None, alterations, debuff_chance, None, None,
                         level_list, reset_rate)
        self._active_meteor = None
        self._clicked = False
        self._safety_timer = 0.5

    def spawn_projectile(self, entity, caster, evil=False, x_diff=0, y_diff=0, delay=1,
                         angle=90, ignore_team=False, at_mouse=False):
        area = self._stats["area"].c_value + caster.stats["area"].c_value
        debuffs = []
        debuff_chance = self._stats["debuff_chance"].c_value * caster.stats["debuff_chance"].c_value
        for d in self._debuffs:
            dbf = d.clone()
            dbf.duration *= caster.stats["debuff_len"].c_value
            dbf.tick_rate *= caster.stats["debuff_rte"].c_value
            dbf.value *= caster.stats["debuff_pot"].c_value
            if dbf.damage is not None:
                dbf.damage = caster.recalculate_damage(dbf.damage, True)
                dbf.damage.mod *= caster.stats["debuff_pot"].c_value
            debuffs.append(dbf)
        x = SYSTEM["mouse"][0]
        y = 0

        proj = MeteorProjectile(x, y,\
                        self._attack_anim,\
                        self._real_damage, caster, evil,\
                        delay=self._stats["delay"].c_value * delay,\
                        behaviours=self._flags, caster=entity, debuffs=debuffs,
                        explosion=self._explosion, area=area,\
                        ignore_team=ignore_team,
                        debuff_chance=debuff_chance,
                        reset_rate=self._stats["reset_rate"].c_value)
        self._active_meteor = proj
        PROJECTILE_TRACKER.append(proj)

    def on_cast(self, caster: Creature, entity: Entity, evil: bool,\
            aim_right = True, force = False, ignore_team = False):
        print(self._safety_timer)
        if self._active_meteor is not None:
            if self._safety_timer > 0:
                return
            self._active_meteor.explode_meteor()
            self._active_meteor = None
        else:
            super().on_cast(caster, entity, evil, aim_right, force, ignore_team)
            self._safety_timer = 0.5

    def tick(self, caster = None):
        super().tick()
        self._safety_timer -= 0.016
        