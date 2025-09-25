"""Projectile are the most common type of attacks."""

from math import atan2, pi
import random
import numpy

import pygame

from data.constants import Flags, SCREEN_HEIGHT, SCREEN_WIDTH, SYSTEM, PROJECTILE_TRACKER, ENNEMY_TRACKER
from data.numerics.damage import Damage
from data.creature import Creature
from data.physics.hitbox import HitBox
from data.image.animation import Animation
from data.interface.render import render

class DummyEntity():
    """Emulates an entity of the projectile."""
    def __init__(self, x, y, hitbox):
        self.x = x
        self.y = y
        self.hitbox = hitbox

class Projectile():
    """Defines a projectile."""
    def __init__(self, x, y, angle, imagefile: str, damage: Damage, origin:Creature,\
                evil = False, speed = 20, caster = None,\
                bounces = 0, delay = 0, chains = 0,\
                behaviours = None, debuffs = None, explosion = None, area = 1,\
                ignore_team = False, offset_x = 0, offset_y = 0):
        if Flags.RANDOM_POSITION in behaviours:
            if numpy.random.random() > 0.5: #Horizontal
                y = int(numpy.random.choice([0, SCREEN_HEIGHT]))
                x = numpy.random.randint(0, SCREEN_WIDTH + 1)
            else: #Vertical
                x = int(numpy.random.choice([0, SCREEN_WIDTH]))
                y = numpy.random.randint(0, SCREEN_HEIGHT)
        self._x = x
        self._y = y
        self._speed = speed
        self._angle = angle
        self._wander_angle = angle
        self._target = None
        self._image = imagefile
        self._area = area
        self._ignore_team = ignore_team
        self._offset_barrage = (offset_x, offset_y)
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
        self._real_image = SYSTEM["images"][self._image].clone()\
            .rotate(-self._angle).scale(area, area, False)
        self._width = self._real_image.w
        self._velocity = pygame.math.Vector2(numpy.cos(angle), numpy.sin(angle)) * speed
        self._acceleration = pygame.math.Vector2(0, 0)
        self._height = self._real_image.h
        self._origin = origin
        self._damage = damage
        self._evil = evil
        self._bounces = bounces
        self._delay = delay
        self._initial_delay = delay
        self._explosion = explosion
        hitbox_len = self._width
        hitbox_height = self._height
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
        self._wandering = True if Flags.WANDER in self._behaviours else False
        self._animation_state = [0, False]
        self._immune = []
        self._bounced = False
        self._chains = chains
        self._warning = None

    def get_image(self):
        """Returns the projectile image."""
        return self._real_image.get_image()

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
        if self._wandering:
            return (None, None)
        if target not in self._immune:
            if Flags.CHAINS in self.behaviours:
                self._immune.clear()
            dmg = self._origin.recalculate_damage(self._damage)
            num, crit = target.damage(dmg)
            self._immune.append(target)
            self._bounced = True
            if self._bounces <= 0 and self._chains <= 0 and Flags.PIERCING not in self._behaviours:
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

    def _distance_to_edge(self):
        """Return how far this projectile can go before leaving the screen."""
        dx, dy = numpy.cos(numpy.radians(self._angle)), numpy.sin(numpy.deg2rad(self._angle))
        candidates = []
        if dx > 0:
            candidates.append((1920 - self._x) / dx)
        elif dx < 0:
            candidates.append((0 - self._x) / dx)
        if dy > 0:
            candidates.append((1080 - self._y) / dy)
        elif dy < 0:
            candidates.append((0 - self._y) / dy)
        return min(c for c in candidates if c > 0)

    def move(self):
        """Handles the movement of the projectile."""
        if Flags.HARD_TRACKING in self._behaviours:
            if self._target is None:
                self._wandering = True
                self._wander_angle = self._angle
            elif self._target not in ENNEMY_TRACKER:
                self._target = SYSTEM["level"].closest_enemy()
                if self._target is None:
                    return
            else:
                self._angle = 90 - atan2(self._target.entity.hitbox.x - SYSTEM["player.x"],\
                    self._target.entity.hitbox.y - SYSTEM["player.y"]) * 180 / pi
        angle = numpy.radians(self._angle)
        if Flags.ACCELERATE in self._behaviours:
            self._speed *= 1.1
        if Flags.WANDER in self._behaviours and self._wandering:
            self._x = self._x + (self._speed / 3) * numpy.cos(self._wander_angle)
            self._y = self._y + (self._speed / 3) * numpy.sin(self._wander_angle)
            self._delay -= 0.016
            if self._delay <= 0:
                self._wandering = False
        elif Flags.WANDER in self._behaviours:
            position = pygame.math.Vector2((self.x, self.y))
            desired = pygame.math.Vector2(self._target.hitbox.center) - position
            distance = desired.length()
            if distance < 10:
                self._velocity *= 0.9
                return
            desired = desired.normalize() * 10
            steer = desired - self._velocity
            if steer.length() > 1:
                steer = steer.normalize() * 1
            self._acceleration += steer
            self._velocity += self._acceleration
            if self._velocity.length() > 10:
                self._velocity = self._velocity.normalize() * 10
            position += self._velocity
            self._x = position[0]
            self._y = position[1]
            self._acceleration *= 0
        else:
            self._x = self._x + self._speed * numpy.cos(angle)
            self._y = self._y + self._speed * numpy.sin(angle)
        self._box.move((self._x, self._y))

    def tick(self):
        """Ticks down the projectile."""
        self._real_image.tick()
        if Flags.DELAYED in self._behaviours:
            if self._delay > 0:
                if self._caster is not None and Flags.UNNATACH not in self._behaviours:
                    self.x = self._caster.x + self._offset[0]
                    self.y = self._caster.y + self._offset[1]
                    self._box.move((self._x, self._y))
                if Flags.WARN in self._behaviours:
                    progress = 1 - (self._delay / self._initial_delay)
                    if progress < 0.3:
                        alpha = int((progress / 0.3) * 185)
                    else:
                        alpha = 185
                    max_len = self._distance_to_edge()
                    if progress < 0.7:
                        length = max_len
                    else:
                        shrink_p = (progress - 0.7) / 0.3
                        length = int(max_len * (1 - shrink_p))
                        if length <= 0:
                            return
                    angle_rad = numpy.radians(self._angle)
                    dx, dy = numpy.cos(angle_rad), numpy.sin(angle_rad)
                    half_h = self._box.height / 2
                    perp_x, perp_y = -dy * half_h, dx * half_h
                    start_x, start_y = self._x, self._y
                    end_x, end_y = start_x + dx * length, start_y + dy * length
                    if length > 0:
                        points = [
                            (int(start_x + perp_x), int(start_y + perp_y)),
                            (int(start_x - perp_x), int(start_y - perp_y)),
                            (int(end_x - perp_x), int(end_y - perp_y)),
                            (int(end_x + perp_x), int(end_y + perp_y)),
                        ]
                        self._warning = (points, alpha)
                    else:
                        self._warning = None
                self._delay -= float(0.016)
                return
        self.move()
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
                self._x += self._width
                self._angle = random.randint(45, 135)
            if self._x >= SCREEN_WIDTH:
                self._x -= self._width * 2
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

    @property
    def ignore_team(self) -> bool:
        """Returns wether or not the slash's ignore the evil flag."""
        return self._ignore_team

    @property
    def warning(self) -> bool:
        """Returns the aoe warning surface."""
        return self._warning
