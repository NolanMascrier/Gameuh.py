"""Projectile are the most common type of attacks."""

from math import atan2, pi
import random
import numpy
from data.constants import Flags, SCREEN_HEIGHT, SCREEN_WIDTH, SYSTEM, PROJECTILE_TRACKER
from data.numerics.damage import Damage
from data.creature import Creature
from data.physics.hitbox import HitBox
from data.image.animation import Animation

class DummyEntity():
    """Emulates an entity of the projectile."""
    def __init__(self, x, y, hitbox):
        self.x = x
        self.y = y
        self.hitbox = hitbox

class Projectile():
    """Defines a projectile."""
    def __init__(self, x, y, angle, imagefile: str, damage: Damage, origin:Creature,\
                evil = False, width = 64, height = 32, speed = 20, \
                hitbox_len = None, hitbox_height = None, caster = None,\
                bounces = 0, delay = 0, chains = 0,\
                behaviours = None, debuffs = None, explosion = None, area = 1):
        self._x = x
        self._y = y
        self._speed = speed
        self._angle = angle
        self._target = None
        self._area = area
        if Flags.AIMED_AT_PLAYER in behaviours:
            self._angle = 90 - numpy.atan2(SYSTEM["player.x"] - x,\
                    SYSTEM["player.y"] - y) * 180 / pi
        if Flags.AIMED_AT_MOUSE in behaviours:
            self._angle = 90 - numpy.atan2(SYSTEM["mouse"][0] - x,\
                    SYSTEM["mouse"][1] - y) * 180 / pi
        if Flags.AIMED_AT_CLOSEST in behaviours:
            closest = SYSTEM["level"].closest_enemy()
            if closest is None:
                self._angle = 0
            else:
                self._angle = 90 - numpy.atan2(closest.entity.hitbox.center_x - x,\
                    closest.entity.hitbox.center_y - y) * 180 / pi
                self._target = closest
        self._length = width
        self._height = height
        self._origin = origin
        self._damage = damage
        self._evil = evil
        self._bounces = bounces
        self._image = imagefile
        self._delay = delay
        self._explosion = explosion
        if hitbox_len is None:
            hitbox_len = width
        if hitbox_height is None:
            hitbox_height = height
        self._box = HitBox(x, y, hitbox_len, hitbox_height)
        if behaviours is None or not isinstance(behaviours, list):
            self._behaviours = []
        else:
            self._behaviours = behaviours
        if debuffs is None or not isinstance(debuffs, list):
            self._debuffs = []
        else:
            self._debuffs = debuffs
        #for delayed casts
        self._caster = caster
        if caster is not None:
            self._offset = (self.x - caster.x, self.y - caster.y)
        self._flagged = False
        self._animation_state = [0, False]
        self._immune = []
        self._bounced = False
        self._chains = chains

    def get_image(self):
        """Returns the projectile image."""
        return SYSTEM["images"][self._image].get_image(self._animation_state)

    def can_be_destroyed(self):
        """Checks whether or not the projectile is out of the screen
        and can be garbage collected."""
        if self._flagged:
            return True
        if self._box.y < 0 - self._box.height:
            return True
        if self._box.y > SCREEN_HEIGHT + self._box.height:
            return True
        if self._box.x < 0 - self._box.width:
            return True
        if self._box.x > SCREEN_WIDTH + self._box.width:
            return True
        return False

    def on_hit(self, target: Creature) -> tuple[float|None,bool|None]:
        """Called when the projectile hits a target."""
        if target not in self._immune:
            if Flags.CHAINS in self.behaviours:
                self._immune.clear()
            dmg = self._origin.recalculate_damage(self._damage)
            num, crit = target.damage(dmg)
            self._immune.append(target)
            self._bounced = True
            if self._bounces <= 0 and self._chains <= 0:
                self._flagged = True
            if num != "Dodged !":
                for debuff in self._debuffs:
                    if debuff.damage is not None:
                        debuff.damage.origin = self._origin
                    target.afflict(debuff.clone(), True)
            if self._explosion is not None:
                sl = self._explosion.clone(DummyEntity(self._x, self._y, self._box),\
                    self._origin, self._area, True)
                PROJECTILE_TRACKER.append(sl)
            return num, crit
        return (None, None)

    def tick(self):
        """Ticks down the projectile."""
        SYSTEM["images"][self._image].tick(self._animation_state)
        if Flags.HARD_TRACKING in self._behaviours:
            self._angle = 90 - atan2(SYSTEM["player.x"] - self._target.entity.hitbox.x,\
                    SYSTEM["player.y"] - self._target.entity.hitbox.y) * 180 / pi
        if Flags.DELAYED in self._behaviours:
            if self._delay > 0:
                if self._caster is not None:
                    self.x = self._caster.x + self._offset[0]
                    self.y = self._caster.y + self._offset[1]
                self._delay -= float(0.016)
                return
        angle = numpy.radians(self._angle)
        if Flags.ACCELERATE in self._behaviours:
            self._speed *= 1.1
        self._x = self._x + self._speed * numpy.cos(angle)
        self._y = self._y + self._speed * numpy.sin(angle)
        self._box.move((self._x, self._y))
        if Flags.CHAINS in self._behaviours and self._bounced and self._chains > 0:
            self._bounced = False
            self._chains -= 1
            closest = SYSTEM["level"].closest_from(self._box, self._target)
            if closest is None:
                self._flagged = True
            else:
                self._angle = 90 - atan2(closest.entity.hitbox.center_x - self._box.center_x,\
                    closest.entity.hitbox.center_y - self._box.center_y) * 180 / pi
                self._target = closest
        elif self.can_be_destroyed() and Flags.BOUNCE not in self._behaviours:
            self._flagged = True
        elif self.can_be_destroyed():
            self._bounces -= 1
            self._damage.coeff = round(self._damage.coeff * 0.7, 2)
            self._speed *= 1.4
            if self._x <= 0:
                self._x += self._length
                self._angle = random.randint(45, 135)
            if self._x >= SCREEN_WIDTH:
                self._x -= self._length * 2
                self._angle = random.randint(135, 225)
            if self._y <= 0:
                self._y += self._height
                self._angle = random.randint(-45, 45)
            if self._y >= SCREEN_HEIGHT:
                self._y -= self._height * 2
                self._angle = random.randint(225, 315)
            self._box.move((self._x, self._y))
        if self._bounces <= 0 and Flags.BOUNCE in self._behaviours:
            self._flagged = True

    def flag(self):
        """Flags the projectile for destruction."""
        self._flagged = True

    def get_pos(self):
        """Returns the projectile's position."""
        return (self._x, self._y)

    @property
    def x(self):
        """Returns the projectile's x value."""
        return self._x

    @x.setter
    def x(self, value):
        self._x = value

    @property
    def y(self):
        """Returns the projectile's y value."""
        return self._y

    @y.setter
    def y(self, value):
        self._y = value

    @property
    def speed(self):
        """Returns the projectile's speed."""
        return self._speed

    @speed.setter
    def speed(self, value):
        self._speed = value

    @property
    def angle(self):
        """Returns the projectile's angle."""
        return self._angle

    @angle.setter
    def angle(self, value):
        self._angle = value

    @property
    def damage(self) -> Damage:
        """Returns the projectile's damage."""
        return self._damage

    @damage.setter
    def damage(self, value):
        self._damage = value

    @property
    def evil(self):
        """Returns whether the projectile hurts the players or
        the enemies."""
        return self._evil

    @evil.setter
    def evil(self, value):
        self._evil = value

    @property
    def bounces(self):
        """Returns how many bounces left for the projectile."""
        return self._bounces

    @bounces.setter
    def bounces(self, value):
        self._bounces = value

    @property
    def image(self) -> Animation:
        """Returns the projectile's image."""
        return SYSTEM["images"][self._image]

    @image.setter
    def image(self, value):
        self._image = value

    @property
    def hitbox(self):
        """Returns the projectile's hitbox."""
        return self._box

    @property
    def behaviours(self):
        """Returns the projectile's flags."""
        return self._behaviours

    @behaviours.setter
    def behaviours(self, value):
        self._behaviours = value
