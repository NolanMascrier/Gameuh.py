"""Projectile are the most common type of attacks."""

from math import pi
import random
import numpy

from data.api.vec2d import Vec2

from data.constants import Flags, SCREEN_HEIGHT, SCREEN_WIDTH, SYSTEM,\
    PROJECTILE_TRACKER, ENNEMY_TRACKER, ANIMATION_TRACKER
from data.numerics.damage import Damage
from data.creature import Creature
from data.physics.hitbox import HitBox
from data.image.animation import Animation
from data.image.controller import AnimationController

class DummyEntity():
    """Emulates an entity of the projectile."""
    def __init__(self, x, y, hitbox):
        self.x = x
        self.y = y
        self.hitbox = hitbox

class Projectile(HitBox):
    """Defines a projectile."""
    __slots__ = '_speed', '_angle', '_wander_angle', '_target', '_image', '_area', '_ignore_team', \
                '_offset_barrage', '_anim_on_hit', '_real_image', '_velocity', '_caster',\
                '_acceleration', '_origin', '_damage', '_evil', '_bounces', '_delay', \
                '_initial_delay', '_explosion', '_behaviours', '_debuffs', '_flagged', \
                '_wandering', '_immune', '_bounced', '_chains', '_warning', '_anim_speed', \
                '_debuff_chance', '_animation_controller'
    def __init__(self, x, y, angle, imagefile: str, damage: Damage, origin:Creature,\
                evil = False, speed = 20, caster = None,\
                bounces = 0, delay = 0, chains = 0,\
                behaviours = None, debuffs = None, explosion = None, area = 1,\
                ignore_team = False, offset_x = 0, offset_y = 0, anim_on_hit = None,
                anim_speed = 1, debuff_chance = 1.0):
        if Flags.RANDOM_POSITION in behaviours:
            if numpy.random.random() > 0.5: #Horizontal
                y = int(numpy.random.choice([0, SCREEN_HEIGHT]))
                x = numpy.random.randint(0, SCREEN_WIDTH + 1)
            else: #Vertical
                x = int(numpy.random.choice([0, SCREEN_WIDTH]))
                y = numpy.random.randint(0, SCREEN_HEIGHT)
        self._speed = speed
        self._angle = angle
        self._wander_angle = angle
        self._target = None
        self._image = imagefile
        self._area = area
        self._ignore_team = ignore_team
        self._offset_barrage = (offset_x, offset_y)
        self._anim_on_hit = anim_on_hit
        if Flags.AIMED_AT_PLAYER in behaviours:
            self._angle = 90 - numpy.arctan2(SYSTEM["player.x"] - x,\
                    SYSTEM["player.y"] - y) * 180 / pi
        if Flags.AIMED_AT_MOUSE in behaviours:
            self._angle = 90 - numpy.arctan2(SYSTEM["mouse"][0] - x,\
                    SYSTEM["mouse"][1] - y) * 180 / pi
        if Flags.AIMED_AT_CLOSEST in behaviours:
            closest = SYSTEM["level"].closest_enemy()
            if closest is None:
                self._angle = 0
            else:
                self._angle = 90 - numpy.arctan2(closest.entity.hitbox.center_x - x,\
                    closest.entity.hitbox.center_y - y) * 180 / pi
                self._target = closest
        cached = SYSTEM["trans_cache"].get(imagefile, -self._angle, area, False)
        if cached is not None:
            self._real_image = cached
            self._animation_controller = AnimationController(cached)
        else:
            base_image = SYSTEM["images"][imagefile]
            self._real_image = base_image.clone().rotate(-self._angle).scale(area, area, False)
            SYSTEM["trans_cache"].put(imagefile, self._real_image, -self._angle, area, False)
            self._animation_controller = None

        self._width = self._real_image.w
        self._height = self._real_image.h
        super().__init__(x, y, self._width, self._height)
        self._velocity = Vec2(numpy.cos(angle), numpy.sin(angle)) * speed
        self._acceleration = Vec2(0, 0)
        self._origin = origin
        self._damage = damage
        self._evil = evil
        self._bounces = bounces
        self._delay = delay
        self._initial_delay = delay
        self._explosion = explosion
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
        self._immune = []
        self._bounced = False
        self._chains = chains
        self._warning = None
        self._anim_speed = anim_speed
        self._debuff_chance = debuff_chance

    def get_image(self):
        """Returns the projectile image."""
        if self._animation_controller:
            return self._animation_controller.get_image()
        return self._real_image.get_image()

    def can_be_destroyed(self):
        """Checks whether or not the projectile is out of the screen
        and can be garbage collected."""
        if self._flagged:
            return True
        if self.y < 0 - self.height:
            return True
        if self.y > SCREEN_HEIGHT + self.height:
            return True
        if self.x < 0 - self.width:
            return True
        if self.x > SCREEN_WIDTH + self.width:
            return True
        return False

    def on_hit(self, target: Creature, entity = None) -> tuple[float|None,bool|None]:
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
                if self._anim_on_hit is not None:
                    if Flags.IMPACT_ANIMATION_RANDOM in self._behaviours:
                        x = numpy.random.randint(entity.left, entity.right)
                        y = numpy.random.randint(entity.top, entity.bottom)
                    else:
                        x = self.center_x - self._anim_on_hit.width / 2
                        y = self.center_y - self._anim_on_hit.height / 2
                    ANIMATION_TRACKER.append((self._anim_on_hit.clone(), x, y))
                for debuff in self._debuffs:
                    if debuff.damage is not None:
                        debuff.damage.origin = self._origin
                    target.afflict(debuff.clone(), True, self._debuff_chance)
            if self._explosion is not None:
                sl = self._explosion.clone(DummyEntity(self.x, self.y, self),\
                    self._origin, self._area, True)
                PROJECTILE_TRACKER.append(sl)
            return num, crit
        return (None, None)

    def _distance_to_edge(self):
        """Return how far this projectile can go before leaving the screen."""
        dx, dy = numpy.cos(numpy.radians(self._angle)), numpy.sin(numpy.deg2rad(self._angle))
        candidates = []
        if dx > 0:
            candidates.append((1920 - self.x) / dx)
        elif dx < 0:
            candidates.append((0 - self.x) / dx)
        if dy > 0:
            candidates.append((1080 - self.y) / dy)
        elif dy < 0:
            candidates.append((0 - self.y) / dy)
        return min(c for c in candidates if c > 0)

    def move(self, _ = None):
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
                self._angle = 90 - numpy.arctan2(self._target.entity.hitbox.x - SYSTEM["player.x"],\
                    self._target.entity.hitbox.y - SYSTEM["player.y"]) * 180 / pi
        angle = numpy.radians(self._angle)
        if Flags.ACCELERATE in self._behaviours:
            self._speed *= 1.1
        if Flags.WANDER in self._behaviours and self._wandering:
            self.x = self.x + (self._speed / 3) * numpy.cos(self._wander_angle)
            self.y = self.y + (self._speed / 3) * numpy.sin(self._wander_angle)
            self._delay -= 0.016
            if self._delay <= 0:
                self._wandering = False
        elif Flags.WANDER in self._behaviours:
            position = Vec2(self.x, self.y)
            desired = Vec2(self._target.hitbox.center) - position
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
            self.x = position[0]
            self.y = position[1]
            self._acceleration *= 0
        else:
            self.x = self.x + self._speed * numpy.cos(angle)
            self.y = self.y + self._speed * numpy.sin(angle)
        super().move((self.x, self.y))

    def tick(self):
        """Ticks down the projectile."""
        if self._animation_controller:
            self._animation_controller.tick(self._anim_speed)
        else:
            self._real_image.tick(self._anim_speed)
        if Flags.DELAYED in self._behaviours:
            if self._delay > 0:
                if self._caster is not None and Flags.UNNATACH not in self._behaviours:
                    self.x = self._caster.x + self._offset[0]
                    self.y = self._caster.y + self._offset[1]
                    self.move((self.x, self.y))
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
                    half_h = self.height / 2
                    perp_x, perp_y = -dy * half_h, dx * half_h
                    start_x, start_y = self.x, self.y
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
            closest = SYSTEM["level"].closest_from(self, self._target)
            if closest is None:
                self._flagged = True
            else:
                self._angle = 90 - numpy.arctan2(closest.entity.hitbox.center_x - self.center_x,\
                    closest.entity.hitbox.center_y - self.center_y) * 180 / pi
                self._target = closest
        elif self.can_be_destroyed() and Flags.BOUNCE not in self._behaviours:
            self._flagged = True
        elif self.can_be_destroyed():
            self._bounces -= 1
            self._damage.coeff = round(self._damage.coeff * 0.7, 2)
            self._speed *= 1.4
            if self.x <= 0:
                self.x += self._width
                self._angle = random.randint(45, 135)
            if self.x >= SCREEN_WIDTH:
                self.x -= self._width * 2
                self._angle = random.randint(135, 225)
            if self.y <= 0:
                self.y += self._height
                self._angle = random.randint(-45, 45)
            if self.y >= SCREEN_HEIGHT:
                self.y -= self._height * 2
                self._angle = random.randint(225, 315)
            self.move((self.x, self.y))
        if self._bounces <= 0 and Flags.BOUNCE in self._behaviours:
            self._flagged = True

    def flag(self):
        """Flags the projectile for destruction."""
        self._flagged = True

    def get_pos(self):
        """Returns the projectile's position."""
        return (self.x, self.y)

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
        return self._real_image

    @image.setter
    def image(self, value):
        self._image = value

    @property
    def hitbox(self):
        """Returns the projectile's hitbox."""
        return self

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

    @property
    def effective(self):
        """Dummy"""
        return True

    @property
    def finished(self):
        """Returns whether or not the projectile is finished."""
        return self.can_be_destroyed()
