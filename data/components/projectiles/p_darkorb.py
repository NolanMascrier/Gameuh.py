"""Projectile definition for ice orbs."""

from data.constants import PROJECTILE_TRACKER, Flags
from data.components.projectiles.projectile import Projectile

class DarkOrbProjectile(Projectile):
    """Special projectile"""
    def __init__(self, x, y, imagefile, damage, origin, evil=False, caster=None,
                 delay=0, behaviours=None, debuffs=None,
                 explosion=None, area=1, ignore_team=False, debuff_chance=1,
                 reset_rate=0, proj_damage=None, subprojectile = "", counter = 0.1):
        super().__init__(x, y, 0, imagefile, damage, origin, evil, 5, caster, 0,
                         delay, 0, behaviours, debuffs, explosion, area, ignore_team,
                         0, 0, None, 1, debuff_chance, None, None)
        self._subprojectile = subprojectile
        self._reset_rate = reset_rate
        self._reset_timer = reset_rate
        self._proj_damage = proj_damage
        self._subangle = 0
        self._timer = counter
        self._counter = counter

    def tick(self):
        super().tick()
        if self._reset_timer <= 0:
            self._reset_timer = self._reset_rate
            self._immune.clear()
        if self._timer <= 0:
            proj1 = Projectile(
                self.center_x, self.center_y, self._subangle,
                self._subprojectile, self._proj_damage, self._origin, self._evil, 15,
                caster=self._caster,
                behaviours=[Flags.PROJECTILE, Flags.SPREAD]
            )
            proj2 = Projectile(
                self.center_x, self.center_y, self._subangle + 180,
                self._subprojectile, self._proj_damage, self._origin, self._evil, 15,
                caster=self._caster,
                behaviours=[Flags.PROJECTILE, Flags.SPREAD]
            )
            PROJECTILE_TRACKER.append(proj1)
            PROJECTILE_TRACKER.append(proj2)
            self._subangle = (self._subangle + 15) % 360
            self._timer = self._counter
        self._reset_timer -= 0.016
        self._timer -= 0.016
