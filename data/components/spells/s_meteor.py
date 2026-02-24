"""Special spell component for meteor."""

import numpy

from data.constants import SYSTEM, PROJECTILE_TRACKER, SCREEN_WIDTH, trad
from data.components.spells.spell import Spell
from data.components.projectiles.p_meteor import MeteorProjectile
from data.game.creature import Creature
from data.physics.entity import Entity

class Meteor(Spell):
    """Unique spell component for meteor."""
    def __init__(self, name, icon, attack_anim, base_damage, mana_cost=0, life_cost=0,
                 delay=0, explosion=None, cooldown=8, flags=None, debuffs=None,
                 effective_frames=None, alterations=None, debuff_chance=1, level_list=None,
                 reset_rate = 1, alt_icon = None):
        super().__init__(name, icon, attack_anim, base_damage, mana_cost, life_cost,
                         0, delay, 0, 0, 0, explosion, None, cooldown,
                         1, flags, None, debuffs, 0, 0, 0,
                         effective_frames, None, alterations, debuff_chance, None, None,
                         level_list, reset_rate)
        self._active_meteor = []
        self._clicked = False
        self._safety_timer = 0.5
        self._alt_icon = alt_icon if alt_icon is not None else icon

    def spawn_projectile(self, entity, caster, evil=False, x_diff=0, y_diff=0, delay=1,
                         angle=90, ignore_team=False):
        area = self._stats["area"].c_value + caster.stats["area"].c_value
        debuffs, debuff_chance = self.generate_debuff_list(caster)
        x = int(numpy.random.randint(0, SCREEN_WIDTH)) - 64
        y = SYSTEM["mouse"][1]
        proj = MeteorProjectile(x, -64,\
                        self._attack_anim,\
                        self._real_damage, caster, evil,\
                        delay=self._stats["delay"].c_value * delay,\
                        behaviours=self._flags, caster=entity, debuffs=debuffs,
                        explosion=self._explosion, area=area,\
                        ignore_team=ignore_team,
                        debuff_chance=debuff_chance,
                        reset_rate=self._stats["reset_rate"].c_value, dest_y=y)
        self._active_meteor.append(proj)
        PROJECTILE_TRACKER.append(proj)

    def on_cast(self, caster: Creature, entity: Entity, evil: bool,\
            aim_right = True, force = False, ignore_team = False,
            victim: Creature = None, victim_entity: Entity = None):
        if len(self._active_meteor) > 0:
            if self._safety_timer > 0:
                return
            self.detonate()
        else:
            super().on_cast(caster, entity, evil, aim_right, force, ignore_team)
            self._safety_timer = 0.5

    def detonate(self):
        """Meteor goes BRRRR"""
        for meteor in self._active_meteor:
            meteor.explode_meteor()
        self._active_meteor.clear()

    def tick(self, caster = None):
        super().tick()
        self._safety_timer -= 0.016
        if len(self._active_meteor) > 0 and self._cooldown <= 0:
            self.detonate()

    def describe(self):
        desc = super().describe()
        desc["explosion_tab"] = trad('buttons', 'detonates')
        return desc

    @property
    def icon(self):
        """Returns the spell's icon."""
        if len(self._active_meteor) > 0:
            return self._alt_icon
        return self._icon
