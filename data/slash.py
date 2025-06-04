"""A slash is a type of attack that attaches itself to its caster,
plays its animation and disappear. It's used for melee attacks."""

from data.damage import Damage
from data.creature import Creature
from data.physics.entity import Entity
from data.physics.hitbox import HitBox
from data.image.animation import Animation
from data.projectile import Projectile
from data.constants import PROJECTILE_TRACKER, Flags

class Slash():
    def __init__(self, caster: Entity, origin: Creature, animation: Animation,\
                damage:Damage, aim_right = True, evil = False, flags = None):
        self._caster = caster
        self._origin = origin
        self._image = animation.clone()
        self._damage = damage
        self._evil = evil
        self._hitbox = HitBox(caster.x, caster.y, animation.height *2 , animation.width * 2)
        if flags is None or not isinstance(flags, list):
            self._flags = []
        else:
            self._flags = flags
        self._finished = False
        self._aim_right = aim_right
        self._immune = []

    def get_image(self):
        """Returns the slash image."""
        return self._image.get_image()

    def get_pos(self):
        """Returns the slash's position."""
        if self._aim_right:
            return (self._caster.right + 30, self._caster.y)
        return (self._caster.x - 30 - self._image.width, self._caster.y)

    def tick(self):
        """Ticks down the slash."""
        self._image.tick()
        if self._aim_right:
            self._hitbox.move((self._caster.right + 30, self._caster.y))
        else:
            self._hitbox.move((self._caster.x - 30 - self._image.width, self._caster.y))
        if self._image.finished:
            self._finished = True
        if Flags.CUTS_PROJECTILE in self._flags:
            for proj in PROJECTILE_TRACKER.copy():
                if not isinstance(proj, Projectile):
                    return
                if proj.hitbox.is_colliding(self._hitbox) and\
                    proj.evil is not self._evil:
                    PROJECTILE_TRACKER.remove(proj)

    def on_hit(self, target: Creature) -> tuple[float|None,bool|None]:
        """Called when the slash hits a target."""
        if target not in self._immune:
            dmg = self._origin.recalculate_damage(self._damage)
            num, crit = target.damage(dmg)
            self._immune.append(target)
            return num, crit
        return (None, None)

    @property
    def caster(self) -> Entity:
        """Returns the slash's caster."""
        return self._caster

    @caster.setter
    def caster(self, value):
        self._caster = value

    @property
    def origin(self) -> Creature:
        """Returns the slash's origin creature."""
        return self._origin

    @origin.setter
    def origin(self, value):
        self._origin = value

    @property
    def damage(self):
        """Returns the slash's damage."""
        return self._damage

    @damage.setter
    def damage(self, value):
        self._damage = value

    @property
    def evil(self):
        """Returns whether or nto the slash's shot by an enemy."""
        return self._evil

    @evil.setter
    def evil(self, value):
        self._evil = value

    @property
    def hitbox(self):
        """Returns the slash's hitbox."""
        return self._hitbox

    @hitbox.setter
    def hitbox(self, value):
        self._hitbox = value

    @property
    def flags(self) -> list[Flags]:
        """Returns the slash's flags list."""
        return self._flags

    @flags.setter
    def flags(self, value):
        self._flags = value

    @property
    def finished(self):
        """Returns whether or not the slash's animation is finished."""
        return self._finished

    @finished.setter
    def finished(self, value):
        self._finished = value
