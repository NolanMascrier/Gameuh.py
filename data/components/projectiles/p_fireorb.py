"""Projectile definition for ice orbs."""

from data.components.projectiles.projectile import Projectile

class FireOrbProjectile(Projectile):
    """Special projectile"""
    def __init__(self, x, y, imagefile, damage, origin, evil=False, caster=None,
                 delay=0, behaviours=None, debuffs=None,
                 explosion=None, area=1, ignore_team=False, debuff_chance=1,
                 reset_rate=0):
        super().__init__(x, y, 0, imagefile, damage, origin, evil, 5, caster, 0,
                         delay, 0, behaviours, debuffs, explosion, area, ignore_team,
                         0, 0, None, 1, debuff_chance, None, None)
        self._reset_rate = reset_rate
        self._reset_timer = reset_rate

    def tick(self):
        super().tick()
        if self._reset_timer <= 0:
            self._reset_timer = self._reset_rate
            self._immune.clear()
        self._reset_timer -= 0.016
