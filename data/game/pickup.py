"""A pick up is something the player can gather by touching it"""

import random
import math
from functools import lru_cache

from data.api.vec2d import Vec2

from data.physics.hitbox import HitBox
from data.image.text import Text
from data.constants import Flags, TEXT_TRACKER, SYSTEM, BLUE_ALT, GREEN_WEAK

COLORS = [
    (128, 128, 128),
    (0, 128, 255),
    (255, 215, 0),
    (128, 0, 255),
    (255, 140, 0),
]

@lru_cache(maxsize=256)
def _fast_sqrt(value):
    """Cached square root for distance calculations."""
    result = value ** 0.5
    return result

class PickUp(HitBox):
    """Creates a pickup"""
    def __init__(self, x, y, value = 0, w = 16, h = 16, speed_mod = 1,\
                flags = None, contained = None):
        super().__init__(x, y, w, h)
        self._value = value
        if flags is None:
            self._flags = []
        else:
            self._flags = flags
        self._to_delete = False
        self._max_speed = 5.0 * speed_mod
        self._max_force = 0.2 * speed_mod
        self._arrival_threshold = 10
        self._arrival_threshold_sq = 100
        self._delay = 30
        angle = random.uniform(0, 2 * math.pi)
        speed = random.uniform(2, 4) * speed_mod
        self._velocity = Vec2(math.cos(angle), math.sin(angle)) * speed
        self._contains = contained
        self._cached_image = None

    def get_image(self):
        """Returns the pickup image - CACHED VERSION."""
        if self._cached_image is not None:
            return self._cached_image
        if Flags.LIFE in self._flags:
            self._cached_image = SYSTEM["images"]["life_orb"].get_image()
        elif Flags.MANA in self._flags:
            self._cached_image = SYSTEM["images"]["mana_orb"].get_image()
        elif Flags.EXPERIENCE in self._flags:
            self._cached_image = SYSTEM["images"]["exp_orb"].get_image()
        elif Flags.GOLD in self._flags:
            if self._value < 5:
                self._cached_image = SYSTEM["images"]["mini_moolah"].image
            elif self._value < 20:
                self._cached_image = SYSTEM["images"]["moolah"].image
            elif self._value < 50:
                self._cached_image = SYSTEM["images"]["big_moolah"].image
            elif self._value < 100:
                self._cached_image = SYSTEM["images"]["super_moolah"].image
            elif self._value < 250:
                self._cached_image = SYSTEM["images"]["mega_moolah"].image
            elif self._value < 500:
                self._cached_image = SYSTEM["images"]["giga_moolah"].image
            elif self._value < 1000:
                self._cached_image = SYSTEM["images"]["terra_moolah"].image
            elif self._value < 2500:
                self._cached_image = SYSTEM["images"]["zeta_moolah"].image
            elif self._value < 5000:
                self._cached_image = SYSTEM["images"]["supra_moolah"].image
            else:
                self._cached_image = SYSTEM["images"]["maxi_moolah"].image
        elif Flags.ITEM in self._flags:
            self._cached_image = SYSTEM["images"]["loot_icon"].image
        elif Flags.RUNE in self._flags:
            self._cached_image = SYSTEM["images"][f"rune_{self._value}_mini"].image
        return self._cached_image

    def move(self, pos):
        """Gravitates toward the player - HIGHLY OPTIMIZED VERSION."""
        if self._delay > 0:
            self._delay -= 1
            self._position.x += self._velocity.x
            self._position.y += self._velocity.y
            return
        player_x = pos.hitbox.x + pos.hitbox.width / 2
        player_y = pos.hitbox.y + pos.hitbox.height / 2
        dx = player_x - self.x
        dy = player_y - self.y
        dist_squared = dx * dx + dy * dy
        if dist_squared < self._arrival_threshold_sq:
            self._velocity.x *= 0.9
            self._velocity.y *= 0.9
            return
        if dist_squared < 1.0:
            distance = 1.0
        else:
            distance = dist_squared ** 0.5
        inv_dist = self._max_speed / distance
        desired_x = dx * inv_dist
        desired_y = dy * inv_dist
        steer_x = desired_x - self._velocity.x
        steer_y = desired_y - self._velocity.y
        steer_mag_squared = steer_x * steer_x + steer_y * steer_y
        max_force_squared = self._max_force * self._max_force
        if steer_mag_squared > max_force_squared:
            steer_mag = steer_mag_squared ** 0.5
            inv_steer = self._max_force / steer_mag
            steer_x *= inv_steer
            steer_y *= inv_steer
        self._velocity.x += steer_x
        self._velocity.y += steer_y
        vel_mag_squared = self._velocity.x * self._velocity.x + self._velocity.y * self._velocity.y
        max_speed_squared = self._max_speed * self._max_speed
        if vel_mag_squared > max_speed_squared:
            vel_mag = vel_mag_squared ** 0.5
            inv_vel = self._max_speed / vel_mag
            self._velocity.x *= inv_vel
            self._velocity.y *= inv_vel
        self._position.x += self._velocity.x
        self._position.y += self._velocity.y

    def generate_text(self, color, value):
        """generates a floating text above the pickup."""
        if self._value > 1:
            SYSTEM["text_generator"].generate_damage_text(self._position[0],\
                self._position[1], color, False, value)

    def generate_item_text(self):
        """Generates the text when picking up an item"""
        rare = self._contains.rarity
        text = Text(f"#c#{COLORS[rare]}{self._contains.base}", font="item_desc")
        TEXT_TRACKER.append([text, self.x, self.y, 255])

    def pickup(self, player):
        """Picks up the pickup."""
        if self._to_delete:
            return
        if Flags.LIFE in self._flags:
            value = round(self._value / 100 * player.creature.stats["life"].get_value())
            player.creature.stats["life"].current_value += value
            self.generate_text(GREEN_WEAK, value)
        elif Flags.MANA in self._flags:
            value = round(self._value / 100 * player.creature.stats["mana"].get_value())
            player.creature.stats["mana"].current_value += value
            self.generate_text(BLUE_ALT, value)
        elif Flags.EXPERIENCE in self._flags:
            player.creature.grant_experience(self._value)
            SYSTEM["level"].exp += self._value
        elif Flags.GOLD in self._flags:
            SYSTEM["level"].gold += self._value
        elif Flags.ITEM in self._flags:
            SYSTEM["player"].inventory.append(self._contains)
            SYSTEM["level"].loot.append(self._contains)
            self.generate_item_text()
        elif Flags.RUNE in self._flags:
            SYSTEM["player"].runes[self._value] += 1
            SYSTEM["level"].runes[self._value] += 1
        self._to_delete = True

    def tick(self, player):
        """Ticks down the pickup"""
        self.move(player)
        super().move((self.x, self.y))
        if self.is_colliding(SYSTEM["player"].hitbox):
            self.pickup(player)

    @property
    def hitbox(self):
        """Returns the pickup's hitbox."""
        return self

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
