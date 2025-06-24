"""Projectile are the most common type of attacks."""

import random
from math import atan2, pi
from math import cos, sin, radians
from data.constants import Flags, SCREEN_HEIGHT, SCREEN_WIDTH, SYSTEM
from data.damage import Damage
from data.creature import Creature
from data.physics.hitbox import HitBox
from data.image.animation import Animation

class Projectile():
    """Defines a projectile."""
    def __init__(self, x, y, angle, imagefile: Animation, damage: Damage, origin:Creature,\
                evil = False, len = 64, height = 32, speed = 20, \
                hitbox_len = None, hitbox_height = None, caster = None,\
                bounces = 0, delay = 0,\
                clone_image = True,\
                behaviours = None):
        self._x = x
        self._y = y
        self._speed = speed
        self._angle = angle
        if Flags.AIMED_AT_PLAYER in behaviours:
            self._angle = 90 - atan2(SYSTEM["player.x"] - x,\
                    SYSTEM["player.y"] - y) * 180 / pi
        if Flags.AIMED_AT_MOUSE in behaviours:
            self._angle = 90 - atan2(SYSTEM["mouse"][0] - x,\
                    SYSTEM["mouse"][1] - y) * 180 / pi
        self._length = len
        self._height = height
        self._damage = origin.recalculate_damage(damage)
        self._evil = evil
        self._bounces = bounces
        if clone_image:
            self._image = imagefile.clone().rotate(-self._angle)
        else:
            self._image = imagefile
        self._delay = delay
        if hitbox_len is None:
            hitbox_len = len
        if hitbox_height is None:
            hitbox_height = height
        self._box = HitBox(x, y, hitbox_len, hitbox_height)
        if behaviours is None or not isinstance(behaviours, list):
            self._behaviours = []
        else:
            self._behaviours = behaviours
        #for delayed casts
        self._caster = caster
        if caster is not None:
            self._offset = (self.x - caster.x, self.y - caster.y)
        self._flagged = False

    def get_image(self):
        """Returns the projectile image."""
        return self._image.get_image()

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

    def tick(self):
        """Ticks down the projectile."""
        self._image.tick()
        if Flags.DELAYED in self._behaviours:
            if self._delay > 0:
                if self._caster is not None:
                    self.x = self._caster.x + self._offset[0]
                    self.y = self._caster.y + self._offset[1]
                self._delay -= float(SYSTEM["options"]["fps"])
                return
        angle = radians(self._angle)
        self._box.move((self._x, self._y))
        if Flags.ACCELERATE in self._behaviours:
            self._speed *= 1.1
        self._x = round(self._x + self._speed * cos(angle))
        self._y = round(self._y + self._speed * sin(angle))
        if self.can_be_destroyed() and Flags.BOUNCE not in self._behaviours:
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
        return self._image

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
