"""A pick up is something the player can gather by touching it.
It can be added to their inventory, or immediately consumed."""

import random
import math
import pygame
from data.physics.hitbox import HitBox
from data.constants import Flags, TEXT_TRACKER, SYSTEM

class PickUp():
    """Creates a pickup."""
    def __init__(self, x, y, value = 0, w = 16, h = 16, speed_mod = 1, flags = None):
        self._position = pygame.math.Vector2(x, y)
        self._value = value
        if flags is None:
            self._flags = []
        else:
            self._flags = flags
        self._hitbox = HitBox(x, y, w, h)
        self._to_delete = False
        #maths stuff
        self._acceleration = pygame.math.Vector2(0, 0)
        self._max_speed = 5.0 * speed_mod
        self._max_force = 0.2 * speed_mod
        self._arrival_threshold = 10
        self._delay = 30
        angle = random.uniform(0, 2 * math.pi)
        speed = random.uniform(2, 4) * speed_mod
        self._velocity = pygame.math.Vector2(math.cos(angle), math.sin(angle)) * speed

    def get_image(self):
        """Returns the pickup image."""
        if Flags.LIFE in self._flags:
            return SYSTEM["images"]["life_orb"].get_image()
        if Flags.MANA in self._flags:
            return SYSTEM["images"]["mana_orb"].get_image()
        if Flags.EXPERIENCE in self._flags:
            return SYSTEM["images"]["exp_orb"].get_image()
        if Flags.GOLD in self._flags:
            return None
        if Flags.ITEM in self._flags:
            return None
        return None

    def move(self, player):
        """Gravitates toward the player."""
        if self._delay > 0:
            self._delay -= 1
            self._position += self._velocity
            return
        desired = pygame.math.Vector2(player.hitbox.center) - self._position
        distance = desired.length()
        if distance < self._arrival_threshold:
            self._velocity *= 0.9
            return
        desired = desired.normalize() * self._max_speed
        steer = desired - self._velocity
        if steer.length() > self._max_force:
            steer = steer.normalize() * self._max_force
        self._acceleration += steer
        self._velocity += self._acceleration
        if self._velocity.length() > self._max_speed:
            self._velocity = self._velocity.normalize() * self._max_speed
        self._position += self._velocity
        self._acceleration *= 0

    def generate_text(self, color):
        """generates a floating text above the pickup."""
        if self._value > 1:
            text = SYSTEM["font"].render(f'{self._value}', False, color)
            TEXT_TRACKER.append([text, self.x, self.y, 255])

    def pickup(self, player):
        """Picks up the pickup."""
        if Flags.LIFE in self._flags:
            player.creature.stats["life"].current_value += self._value
            self.generate_text(0xFF0000)
        if Flags.MANA in self._flags:
            player.creature.stats["mana"].current_value += self._value
            self.generate_text(0x00FF00)
        if Flags.EXPERIENCE in self._flags:
            player.creature.grant_experience(self._value)
        if Flags.GOLD in self._flags:
            pass #TODO
            self.generate_text(0xFCA400)
        if Flags.ITEM in self._flags:
            pass #TODO
        self._to_delete = True

    def tick(self, player):
        """Ticks down the pickup"""
        self.move(player)
        self._hitbox.move((self.x, self.y))
        SYSTEM["images"]["life_orb"].tick()
        SYSTEM["images"]["mana_orb"].tick()
        SYSTEM["images"]["exp_orb"].tick()

    @property
    def x(self):
        """Returns the pickup x position"""
        return self._position[0]

    @property
    def y(self):
        """Returns the pickup x position"""
        return self._position[1]

    @property
    def hitbox(self):
        """Returns the pickup's hitbox."""
        return self._hitbox

    @hitbox.setter
    def hitbox(self, value):
        self._hitbox = value

    @property
    def flags(self) -> list:
        """Returns the pickup's flags."""
        return self._flags

    @flags.setter
    def flags(self, value):
        self._flags = value

    @property
    def flagged_for_deletion(self):
        """Return wether or not this pickup needs to be deleted."""
        return self._to_delete
