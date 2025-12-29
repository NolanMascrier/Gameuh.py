"""A slash is a type of attack that attaches itself to its caster or a position,
plays its animation and disappear. It's used for melee attacks or explosions."""

import json

from data.numerics.damage import Damage
from data.game.creature import Creature
from data.game.projectile import DummyEntity
from data.physics.entity import Entity
from data.physics.hitbox import HitBox
from data.game.projectile import Projectile
from data.numerics.affliction import Affliction
from data.constants import PROJECTILE_TRACKER, Flags, SYSTEM, ANIMATION_TRACKER

from data.image.controller import AnimationController

class Slash(HitBox):
    """Defines a slash."""
    __slots__ = '_caster', '_origin', '_image', '_real_image', '_damage', '_evil', '_area', \
                '_center', '_anim_on_hit', '_effective_frames', '_flags', '_finished', \
                '_aim_right', '_immune', '_animation_state', '_debuffs', '_ignore_team', \
                '_tick_time', '_anim_speed', '_debuff_chance', '_animation_controller'
    def __init__(self, caster: Entity, origin: Creature, animation: str,\
                damage:Damage, aim_right = True, evil = False, flags = None,\
                offset_x = 0, offset_y = 0, debuffs = None, area = 1, center = False,\
                ignore_team = False, effective_frames = None, anim_on_hit = None,
                anim_speed = 1, debuff_chance = 1.0):
        self._caster = caster
        self._origin = origin
        self._image = animation

        cached = SYSTEM["trans_cache"].get(animation, 0, area, not aim_right)
        if cached is not None:
            self._real_image = cached
            self._animation_controller = AnimationController(cached)
        else:
            base_image = SYSTEM["images"][animation]
            self._real_image = base_image.clone().scale(area, area, False)\
                .flip(False, not aim_right)
            SYSTEM["trans_cache"].put(animation, self._real_image, 0, area, not aim_right)
            self._animation_controller = None
        self._damage = damage
        self._evil = evil
        self._area = area
        self._center = center
        self._anim_on_hit = anim_on_hit
        self._effective_frames = effective_frames
        super().__init__(caster.x, caster.y, self._real_image.w,\
            self._real_image.h)
        if flags is None or not isinstance(flags, list):
            self._flags = []
        else:
            self._flags = flags
        self._finished = False
        self._aim_right = aim_right
        if not aim_right:
            offset_y *= -1
        self._immune = []
        self._animation_state = [0, False]
        self._offset = (offset_x, offset_y)
        if debuffs is None or not isinstance(debuffs, list):
            self._debuffs = []
        else:
            self._debuffs = debuffs
        self._ignore_team = ignore_team
        self._tick_time = 0
        self._anim_speed = anim_speed
        self._debuff_chance = debuff_chance

    def clone(self, entity, origin, area = None, center=False):
        """Returns a deep copy of the slash."""
        return Slash(
            entity,
            origin,
            self._image,
            self._damage,
            self._aim_right,
            self._evil,
            self._flags.copy(),
            self._offset[0],
            self._offset[1],
            self._debuffs.copy(),
            self._area if area is None else area,
            center,
            effective_frames=self._effective_frames
        )

    def get_image(self):
        """Returns the slash image."""
        if self._animation_controller:
            return self._animation_controller.get_image()
        return self._real_image.get_image()

    def get_pos(self):
        """Returns the slash's position."""
        x, y = self._caster.hitbox.center
        anim_x, anim_y = self.width / 2, self.height / 2
        offset_x, offset_y = self._offset[0] * (-1 if self._aim_right else 1),\
            self._offset[1] * (-1 if self._aim_right else 1)
        if self._center:
            center_x, center_y = self._real_image.width / 2, self._real_image.height / 2
        else:
            center_x, center_y = 0, 0
        return (x - anim_x - center_x + offset_x, y - anim_y - center_y + offset_y)

    def tick(self):
        """Ticks down the slash."""
        if self._animation_controller:
            self._animation_controller.tick(self._anim_speed)
        else:
            self._real_image.tick(self._anim_speed)
        super().move(self.get_pos())
        if Flags.CAN_TICK in self._flags:
            self._tick_time += 0.016
            if self._tick_time >= 0.1:
                self._tick_time = 0
                self._immune.clear()
        if self._animation_controller:
            if self._animation_controller.finished:
                self._finished = True
        else:
            if self._real_image.finished:
                self._finished = True
        if Flags.CUTS_PROJECTILE in self._flags:
            for proj in PROJECTILE_TRACKER:
                if not isinstance(proj, Projectile):
                    return
                if proj.hitbox.is_colliding(self) and\
                    proj.evil is not self._evil:
                    proj.flag()

    def on_hit(self, target: Creature, _ = None) -> tuple[float|None,bool|None]:
        """Called when the slash hits a target."""
        if target not in self._immune:
            dmg = self._origin.recalculate_damage(self._damage)
            num, crit = target.damage(dmg)
            if num != "Dodged !":
                if self._anim_on_hit is not None:
                    ANIMATION_TRACKER.append((self._anim_on_hit.clone(), self.x, self.y))
                for debuff in self._debuffs:
                    if debuff.damage is not None:
                        debuff.damage.origin = self._origin
                    target.afflict(debuff.clone(), True, self._debuff_chance)
            self._immune.append(target)
            return num, crit
        return (None, None)

    def export(self) -> str:
        """Serializes the slash as JSON data."""
        debuffs = []
        for d in self._debuffs:
            debuffs.append(d.export())
        data = {
            "type": "slash",
            "anim": self._image,
            "damage": self._damage.export(),
            "flags": self._flags,
            "offset": self._offset,
            "debuffs": debuffs,
            "area": self._area,
            "effective": self._effective_frames
        }
        return json.dumps(data)

    @staticmethod
    def imports(data):
        """Reads JSON data and returns a slash."""
        dt = DummyEntity(0,0,0)
        return Slash(
            dt,
            None,
            data["anim"],
            Damage.imports(json.loads(data["damage"])),
            flags = data["flags"],
            offset_x=int(data["offset"][0]),
            offset_y=int(data["offset"][1]),
            debuffs=[Affliction.imports(json.loads(d)) for d in data["debuffs"]],
            area=float(data["area"]),
            effective_frames=data["effective"]
        )

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
        return self

    @property
    def area(self):
        """Returns the slash's area."""
        return self._area

    @area.setter
    def area(self, value):
        self._area = value

    @property
    def debuffs(self):
        """Returns the slash's debuffs."""
        return self._debuffs

    @debuffs.setter
    def debuffs(self, value):
        self._debuffs = value

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

    @property
    def ignore_team(self) -> bool:
        """Returns wether or not the slash's ignore the evil flag."""
        return self._ignore_team

    @property
    def warning(self):
        """Dummy"""
        return None

    @property
    def effective(self):
        """Returns whether or not the slash is still in effect, or if it's just the end
        of its animation."""
        if self._effective_frames is None:
            return True
        if self._animation_controller:
            return self._animation_controller.frame < self._effective_frames
        return self._real_image.frame < self._effective_frames
