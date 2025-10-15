"""A pick up is something the player can gather by touching it.
It can be added to their inventory, or immediately consumed."""

import random
import math

from data.api.vec2d import Vec2

from data.physics.hitbox import HitBox
from data.image.text import Text
from data.constants import Flags, TEXT_TRACKER, SYSTEM

COLORS = [
    (128, 128, 128),   # Common - Gray shimmer
    (0, 128, 255),     # Uncommon - Blue shimmer
    (255, 215, 0),     # Legendary - Gold shimmer
    (128, 0, 255),     # Rare - Purple shimmer
    (255, 140, 0),     # Epic - Orange shimmer
]

BLUE = (3, 188, 255)
GREEN = (0, 143, 0)

class PickupManager:
    """Spatial partitioning for pickups to reduce collision checks."""
    def __init__(self, cell_size=200):
        self.cell_size = cell_size
        self.grid = {}
        self.pickups = []
    
    def _get_cell(self, x, y):
        """Get grid cell for position."""
        return (int(x // self.cell_size), int(y // self.cell_size))
    
    def add_pickup(self, pickup):
        """Add pickup to spatial grid."""
        cell = self._get_cell(pickup.x, pickup.y)
        if cell not in self.grid:
            self.grid[cell] = []
        self.grid[cell].append(pickup)
        self.pickups.append(pickup)
    
    def get_nearby_pickups(self, x, y, radius):
        """Get pickups near a position (much faster than checking all)."""
        nearby = []
        cell_x, cell_y = self._get_cell(x, y)
        
        # Check adjacent cells
        for dx in range(-1, 2):
            for dy in range(-1, 2):
                cell = (cell_x + dx, cell_y + dy)
                if cell in self.grid:
                    nearby.extend(self.grid[cell])
        
        return nearby
    
    def update_pickup_position(self, pickup, old_x, old_y):
        """Update pickup position in grid."""
        old_cell = self._get_cell(old_x, old_y)
        new_cell = self._get_cell(pickup.x, pickup.y)
        
        if old_cell != new_cell:
            # Remove from old cell
            if old_cell in self.grid:
                self.grid[old_cell].remove(pickup)
                if not self.grid[old_cell]:
                    del self.grid[old_cell]
            
            # Add to new cell
            if new_cell not in self.grid:
                self.grid[new_cell] = []
            self.grid[new_cell].append(pickup)
    
    def remove_pickup(self, pickup):
        """Remove pickup from grid."""
        cell = self._get_cell(pickup.x, pickup.y)
        if cell in self.grid and pickup in self.grid[cell]:
            self.grid[cell].remove(pickup)
            if not self.grid[cell]:
                del self.grid[cell]
        if pickup in self.pickups:
            self.pickups.remove(pickup)

class PickUp(HitBox):
    """Creates a pickup."""
    def __init__(self, x, y, value = 0, w = 16, h = 16, speed_mod = 1,\
                flags = None, contained = None):
        super().__init__(x, y, w, h)
        self._value = value
        if flags is None:
            self._flags = []
        else:
            self._flags = flags
        self._to_delete = False
        #maths stuff
        self._acceleration = Vec2(0, 0)
        self._max_speed = 5.0 * speed_mod
        self._max_force = 0.2 * speed_mod
        self._arrival_threshold = 10
        self._delay = 30
        angle = random.uniform(0, 2 * math.pi)
        speed = random.uniform(2, 4) * speed_mod
        self._velocity = Vec2(math.cos(angle), math.sin(angle)) * speed
        self._contains = contained

    def get_image(self):
        """Returns the pickup image."""
        if Flags.LIFE in self._flags:
            return SYSTEM["images"]["life_orb"].get_image()
        if Flags.MANA in self._flags:
            return SYSTEM["images"]["mana_orb"].get_image()
        if Flags.EXPERIENCE in self._flags:
            return SYSTEM["images"]["exp_orb"].get_image()
        if Flags.GOLD in self._flags:
            if self._value < 5:
                return SYSTEM["images"]["mini_moolah"].image
            if self._value < 20:
                return SYSTEM["images"]["moolah"].image
            if self._value < 50:
                return SYSTEM["images"]["big_moolah"].image
            if self._value < 100:
                return SYSTEM["images"]["super_moolah"].image
            if self._value < 250:
                return SYSTEM["images"]["mega_moolah"].image
            if self._value < 500:
                return SYSTEM["images"]["giga_moolah"].image
            if self._value < 1000:
                return SYSTEM["images"]["terra_moolah"].image
            if self._value < 2500:
                return SYSTEM["images"]["zeta_moolah"].image
            if self._value < 5000:
                return SYSTEM["images"]["supra_moolah"].image
            return SYSTEM["images"]["maxi_moolah"].image
        if Flags.ITEM in self._flags:
            return SYSTEM["images"]["loot_icon"].image
        if Flags.RUNE in self._flags:
            return SYSTEM["images"][f"rune_{self._value}_mini"].image
        return None

    def move(self, pos):
        """Gravitates toward the player."""
        if self._delay > 0:
            self._delay -= 1
            # OPTIMIZATION: In-place vector addition (faster than creating new Vec2)
            self._position.x += self._velocity.x
            self._position.y += self._velocity.y
            return
        
        # OPTIMIZATION: Direct attribute access instead of Vec2 creation
        player_x, player_y = pos.hitbox.center
        
        # Calculate distance components
        dx = player_x - self._position.x
        dy = player_y - self._position.y
        
        # OPTIMIZATION: Fast distance check using squared distance
        # Avoid sqrt for threshold check (distance^2 vs threshold^2)
        dist_squared = dx * dx + dy * dy
        threshold_squared = self._arrival_threshold * self._arrival_threshold
        
        if dist_squared < threshold_squared:
            # Close enough - just slow down
            self._velocity.x *= 0.9
            self._velocity.y *= 0.9
            return
        
        # OPTIMIZATION: Only calculate sqrt when we need normalized direction
        distance = (dist_squared) ** 0.5  # Faster than math.sqrt
        
        # Normalize and scale to max speed
        inv_dist = self._max_speed / distance  # Single division instead of two
        desired_x = dx * inv_dist
        desired_y = dy * inv_dist
        
        # Calculate steering force
        steer_x = desired_x - self._velocity.x
        steer_y = desired_y - self._velocity.y
        
        # OPTIMIZATION: Fast magnitude check without sqrt
        steer_mag_squared = steer_x * steer_x + steer_y * steer_y
        max_force_squared = self._max_force * self._max_force
        
        if steer_mag_squared > max_force_squared:
            # Clamp to max force
            steer_mag = steer_mag_squared ** 0.5
            inv_steer = self._max_force / steer_mag
            steer_x *= inv_steer
            steer_y *= inv_steer
        
        # Apply acceleration (in-place)
        self._velocity.x += steer_x
        self._velocity.y += steer_y
        
        # OPTIMIZATION: Clamp velocity without creating new Vec2
        vel_mag_squared = self._velocity.x * self._velocity.x + self._velocity.y * self._velocity.y
        max_speed_squared = self._max_speed * self._max_speed
        
        if vel_mag_squared > max_speed_squared:
            vel_mag = vel_mag_squared ** 0.5
            inv_vel = self._max_speed / vel_mag
            self._velocity.x *= inv_vel
            self._velocity.y *= inv_vel
        
        # Update position (in-place)
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
            self.generate_text(GREEN, value)
        if Flags.MANA in self._flags:
            value = round(self._value / 100 * player.creature.stats["mana"].get_value())
            player.creature.stats["mana"].current_value += value
            self.generate_text(BLUE, value)
        if Flags.EXPERIENCE in self._flags:
            player.creature.grant_experience(self._value)
            SYSTEM["level"].exp += self._value
        if Flags.GOLD in self._flags:
            SYSTEM["level"].gold += self._value
        if Flags.ITEM in self._flags:
            SYSTEM["player"].inventory.append(self._contains)
            SYSTEM["level"].loot.append(self._contains)
            self.generate_item_text()
        if Flags.RUNE in self._flags:
            SYSTEM["player"].runes[self._value] += 1
            SYSTEM["level"].runes[self._value] += 1
        self._to_delete = True

    def tick(self, player):
        """Ticks down the pickup"""
        self.move(player)
        super().move((self.x, self.y))
        SYSTEM["images"]["life_orb"].tick()
        SYSTEM["images"]["mana_orb"].tick()
        SYSTEM["images"]["exp_orb"].tick()
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
