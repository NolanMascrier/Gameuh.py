"""Projectile definition for meteor."""

from data.constants import PROJECTILE_TRACKER, SCREEN_HEIGHT, SYSTEM
from data.components.projectiles.projectile import Projectile, DummyEntity

class MeteorProjectile(Projectile):
    """Special projectile"""
    def __init__(self, x, y, imagefile, damage, origin, evil=False, caster=None,
                 delay=0, behaviours=None, debuffs=None,
                 explosion=None, area=1, ignore_team=False, debuff_chance=1,
                 reset_rate=0, dest_y = SCREEN_HEIGHT):
        speed_factor = 6 * (SYSTEM["mouse"][1] / SCREEN_HEIGHT) + 4
        super().__init__(x, y, 0, imagefile, damage, origin, evil, speed_factor, caster, 0,
                         delay, 0, behaviours, debuffs, explosion, area, ignore_team,
                         0, 0, None, 1, debuff_chance, None, None)
        self._reset_rate = reset_rate
        self._reset_timer = reset_rate
        self._dest_y = dest_y

    def tick(self):
        super().tick()
        if self._reset_timer <= 0:
            self._reset_timer = self._reset_rate
            self._immune.clear()
        self._reset_timer -= 0.016
        self._speed *= 1.0001

    def explode_meteor(self):
        """Explode the meteor, creating the explosion and applying the damage."""
        sl = self._explosion.clone(DummyEntity(self.x, self.y, self),\
                    self._origin, self._area, True)
        PROJECTILE_TRACKER.append(sl)
        self._flagged = True
