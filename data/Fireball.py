import random
from math import cos, sin, radians
from data.constants import *

"""Stealth py update for the workflow, this file will be deleted
anyway."""

from data.physics.hitbox import HitBox

class Fireball():
    def __init__(self, x, y, angle, evil = False, power = 5, len = 64, height = 32, speed = 20, image = None, \
                hitbox_len = None, hitbox_height = None, animated = False, max_frame = 1, bounces = 0, \
                frame_delay = 1,behaviours = None):
        self._x = x
        self._y = y
        self._speed = speed
        self._angle = angle
        self._length = len
        self._height = height
        self._power = power
        if hitbox_len is None:
            hitbox_len = len
        if hitbox_height is None:
            hitbox_height = height
        self._box = HitBox(x, y, hitbox_len, hitbox_height)
        self._evil = evil
        self._animated = animated
        self._frame = 0
        self._frame_max = max_frame
        self._bounces = bounces
        if behaviours is None or not isinstance(behaviours, list):
            self._behaviours = []
        else:
            self._behaviours = behaviours
        if image is None:
            self._image = pygame.transform.rotate(pygame.transform.scale(pygame.image.load(FIREBALL_IMAGE).convert_alpha(), (self._length, self._height)), angle)
        else:
            self._image = image
        self._frame_delay = frame_delay

    def get_image(self):
        if not self._animated:
            return self._image
        else:
            return self._image[int(self._frame) % self._frame_max]

    def can_be_destroyed(self):
        if self._box.y < 0 - self._box.height:
            return True
        if self._box.y > SCREEN_HEIGHT + self._box.height:
            return True
        if self._box.x < 0 - self._box.width:
            return True
        if self._box.x > SCREEN_WIDTH + self._box.width:
            return True
        return False

    def tick(self, player):
        angle = radians(self._angle)
        self._box.move((self._x, self._y))
        self._x = round(self._x + self._speed * cos(angle))
        self._y = round(self._y + self._speed * sin(angle))
        self._frame += self._frame_delay
        if self._frame > self._frame_max:
            self._frame -= self._frame_max
        if self.can_be_destroyed() and Flags.BOUNCE not in self._behaviours:
            PROJECTILE_TRACKER.remove(self)
        elif self.can_be_destroyed():
            self._bounces -= 1
            self._power = round(self._power * 0.7, 2)
            if self._power < 1:
                self._power = 1
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
            PROJECTILE_TRACKER.remove(self)

    def get_pos(self):
        return (self._x, self._y)

    @property
    def x(self):
        return self._x

    @x.setter
    def x(self, value):
        self._x = value

    @property
    def y(self):
        return self._y

    @y.setter
    def y(self, value):
        self._y = value

    @property
    def power(self):
        return self._power

    @power.setter
    def power(self, value):
        self._power = value

    @property
    def evil(self):
        return self._evil

    @evil.setter
    def evil(self, value):
        self._evil = value
    
    @property
    def box(self):
        return self._box

    @box.setter
    def box(self, value):
        self._box = value
