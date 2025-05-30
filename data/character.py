from data.constants import *
from data.spell_list import *
from data.projectile import Projectile
from data.physics.hitbox import HitBox
from data.physics.entity import Entity
from data.creature import Creature
from data.image.animation import Animation

class Character():
    def __init__(self, x = 10, y = SCREEN_HEIGHT / 2, imagefile:Animation = None, speed = 12):
        box = HitBox(x, y, imagefile.width / 3, imagefile.height / 1.3)
        self._entity = Entity(x, y, imagefile, box, speed)
        self._creature = Creature("hero")
        self._cooldown = 0
        self._max_cooldown = 2
        self._base_speed = speed
        self._equipped_spells = {
            K_q: SYSTEM["spells"]["firebolt"],
            K_e: SYSTEM["spells"]["voidbolt"],
            K_f: SYSTEM["spells"]["icebolt"],
            K_t: SYSTEM["spells"]["elefury"],
            K_r: None,
            K_LSHIFT: SYSTEM["spells"]["winddash"]
        }

    def get_pos(self):
        """Returns the position of the character as a
        rect tuple."""
        return self._entity.hitbox.get_rect()

    def get_image(self):
        """Returns the character current image."""
        return self._entity.get_image()

    def tick(self):
        """Ticks down the character."""
        self._creature.tick()
        self._entity.tick(self, self._base_speed)
        if self._cooldown > 0:
            self._cooldown -= 0.016
        for _, skill in self._equipped_spells.items():
            if skill is not None:
                skill.tick()

    def shoot_fireball(self):
        orig_x, orig_y = self._entity.hitbox.center
        if self._cooldown <= 0 and self._creature.stats["mana"].current_value >= 2:
            fire = Projectile(orig_x, orig_y, 0, SYSTEM["images"]["fireball"], FIREBOLT,\
                              self._creature, len=32, height=32)
            PROJECTILE_TRACKER.append(fire)
            self._cooldown = 0.5
            self._max_cooldown = 0.5
            self._creature.stats["mana"].current_value -= 2

    def action(self, keys):
        """Acts depending on the input."""
        if keys[K_LEFT] or keys[K_a]:
            if self._entity.hitbox.left >= 0:
                x = self._entity.x - self._entity.move_speed
                y = self._entity.y
                self._entity.displace((x, y), keys)
        if keys[K_RIGHT] or keys[K_d]:
            if self._entity.hitbox.right <= SCREEN_WIDTH:
                x = self._entity.x + self._entity.move_speed
                y = self._entity.y
                self._entity.displace((x, y), keys)
        if keys[K_UP] or keys[K_w]:
            if self._entity.hitbox.top >= 0:
                x = self._entity.x
                y = self._entity.y - self._entity.move_speed
                self._entity.displace((x, y), keys)
        if keys[K_DOWN] or keys[K_s]:
            if self._entity.hitbox.bottom <= SCREEN_HEIGHT:
                x = self._entity.x
                y = self._entity.y + self._entity.move_speed
                self._entity.displace((x, y), keys)
        #TODO: Check if None
        if keys[K_q]:
            self._equipped_spells[K_q].cast(self._creature, self._entity, False)
        if keys[K_e]:
            self._equipped_spells[K_e].cast(self._creature, self._entity, False)
        if keys[K_f]:
            self._equipped_spells[K_f].cast(self._creature, self._entity, False)
        if keys[K_t]:
            self._equipped_spells[K_t].cast(self._creature, self._entity, False)
        if keys[K_LSHIFT]:
            self._equipped_spells[K_LSHIFT].cast(self._creature, self._entity, False)

    @property
    def x(self):
        """Returns the character's x value."""
        return self._entity.x

    @property
    def y(self):
        """Returns the character's y value."""
        return self._entity.y

    @property
    def hitbox(self):
        """Returns the character's hitbox."""
        return self._entity.hitbox

    @property
    def entity(self) -> Entity:
        """Returns the character's entity."""
        return self._entity

    @entity.setter
    def entity(self, value):
        self._entity = value

    @property
    def creature(self) -> Creature:
        """Returns the character's creature."""
        return self._creature

    @creature.setter
    def creature(self, value):
        self._creature = value

    @property
    def cooldown(self) -> float:
        """Returns the character's cooldown."""
        return self._cooldown

    @cooldown.setter
    def cooldown(self, value):
        self._cooldown = value

    @property
    def max_cooldown(self) -> float:
        """Returns the character's max cooldown."""
        return self._max_cooldown

    @max_cooldown.setter
    def max_cooldown(self, value):
        self._max_cooldown = value
