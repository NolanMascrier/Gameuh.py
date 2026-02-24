"""Projectile definition for ice spears."""

from data.constants import Flags, PROJECTILE_TRACKER
from data.components.projectiles.projectile import Projectile

class IceSpearProjectile(Projectile):
    """Special projectile"""
    def __init__(self, x, y, imagefile, damage, origin, evil=False, caster=None,
                 delay=0, behaviours=None, debuffs=None,
                 explosion=None, area=1, ignore_team=False, debuff_chance=1,
                 secondary_damage=None, secondary_anim=None):
        super().__init__(x, y, 0, imagefile, damage, origin, evil, 18, caster, 0,
                         delay, 0, behaviours, debuffs, explosion, area, ignore_team,
                         0, 0, None, 1, debuff_chance, None, None)
        self._secondary_damage = secondary_damage if secondary_damage is not None else damage
        self._secondary_anim = secondary_anim if secondary_anim is not None else damage

    def on_hit(self, target, entity=None):
        values = super().on_hit(target, entity)
        angle = self._angle - 15
        for _ in range(3):
            pr = Projectile(self.x, self.y, angle, self._secondary_anim, self._secondary_damage,
                            self._origin, self._evil, self._speed * 0.9, self._caster,
                            behaviours=[Flags.PROJECTILE, Flags.PIERCING])
            angle += 15
            pr.immune = self._immune
            PROJECTILE_TRACKER.append(pr)
        return values
