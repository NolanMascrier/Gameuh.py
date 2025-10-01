from data.constants import *
from data.projectile import Projectile
from data.physics.hitbox import HitBox
from data.tables.spell_table import VOIDBOLT
from math import pi
import numpy

class Generator():
    def __init__(self, x, y, dest, delay, power, duration, gen_img, proj_img, frame_max = 4, evil = True, caster = None):
        self._x = x
        self._y = y
        self._destination = dest
        self._delay = delay
        self._power = power
        self._duration = duration
        self._tock = 0
        self._ready = False
        self._gen_img = gen_img
        self._proj_img = proj_img
        self._frame = 0
        self._frame_max = frame_max
        self._evil = evil
        self._box = HitBox(self._x, self._y, 32, 32)
        self._caster = caster
        self._angle = 0

    def get_pos(self):
        return (self._x, self._y)

    def get_image(self):
        return self._gen_img.get_image()

    def tick(self, player):
        self._frame += 0.1
        if self._ready:
            self._tock += float(SYSTEM["options"]["fps"])
            self._duration -= float(SYSTEM["options"]["fps"])
            while self._tock >= self._delay:
                proj = Projectile(self._x - 16, self._y + 8, 180, self._proj_img,\
                                VOIDBOLT, self._caster, True, clone_image=False)
                PROJECTILE_TRACKER.append(proj)
                self._tock -= self._delay
            if self._tock >= self._duration:
                PROJECTILE_TRACKER.remove(self)
        else:
            if self._x <= self._destination[0] + 5 and self._x >= self._destination[0] - 5 \
                and self._y <= self._destination[1] + 5 and self._y >= self._destination[1] - 5:
                self._angle = 90 - numpy.arctan2(player.x - self._x,\
                           player.y - self._y) * 180 / pi
                self._ready = True
            if self._x < self._destination[0]:
                self._x += 6
            if self._x > self._destination[0]:
                self._x -= 6
            if self._y < self._destination[1]:
                self._y += 6
            if self._y > self._destination[1]:
                self._y -= 6
            self._box.move((self._x, self._y))

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
    def destination(self):
        return self._destination

    @destination.setter
    def destination(self, value):
        self._destination = value

    @property
    def delay(self):
        return self._delay

    @delay.setter
    def delay(self, value):
        self._delay = value

    @property
    def power(self):
        return self._power

    @power.setter
    def power(self, value):
        self._power = value

    @property
    def duration(self):
        return self._duration

    @duration.setter
    def duration(self, value):
        self._duration = value

    @property
    def tock(self):
        return self._tock

    @tock.setter
    def tock(self, value):
        self._tock = value

    @property
    def ready(self):
        return self._ready

    @ready.setter
    def ready(self, value):
        self._ready = value

    @property
    def gen_img(self):
        return self._gen_img

    @gen_img.setter
    def gen_img(self, value):
        self._gen_img = value

    @property
    def proj_img(self):
        return self._proj_img

    @proj_img.setter
    def proj_img(self, value):
        self._proj_img = value

    @property
    def frame(self):
        return self._frame

    @frame.setter
    def frame(self, value):
        self._frame = value

    @property
    def frame_max(self):
        return self._frame_max

    @frame_max.setter
    def frame_max(self, value):
        self._frame_max = value

    @property
    def evil(self):
        return self._evil

    @evil.setter
    def evil(self, value):
        self._evil = value

    @property
    def hitbox(self):
        return self._box

    @hitbox.setter
    def hitbox(self, value):
        self._box = value
