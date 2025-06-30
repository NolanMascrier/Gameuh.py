"""Class for player characters."""

from data.constants import *
from data.tables.spell_table import *
from data.generator import Generator
from data.physics.hitbox import HitBox
from data.physics.entity import Entity
from data.creature import Creature
from data.image.animation import Animation

class Character():
    """Defines a character. A character is a creature/entity
    specifically made to be used by players."""
    def __init__(self, x = 10, y = SCREEN_HEIGHT / 2, imagefile:Animation = None, speed = 12):
        box = HitBox(x, y, imagefile.width / 3, imagefile.height / 1.3)
        self._entity = Entity(x, y, imagefile, box, speed)
        self._creature = Creature("hero")
        self._cooldown = 0
        self._max_cooldown = 2
        self._base_speed = speed
        self._potions = [3, 3]
        self._equipped_spells = {
            K_q: SYSTEM["spells"]["firebolt"],
            K_e: SYSTEM["spells"]["voidbolt"],
            K_f: SYSTEM["spells"]["icebolt"],
            K_t: SYSTEM["spells"]["elefury"],
            K_r: SYSTEM["spells"]["furyslash"],
            K_LSHIFT: SYSTEM["spells"]["winddash"]
        }
        self._immune = []
        self._spellbook = [
            SYSTEM["spells"]["firebolt"],
            SYSTEM["spells"]["voidbolt"],
            SYSTEM["spells"]["icebolt"],
            SYSTEM["spells"]["elefury"],
            SYSTEM["spells"]["furyslash"],
            SYSTEM["spells"]["winddash"],
        ]
        self._inventory = []

    def get_pos(self):
        """Returns the position of the character as a
        rect tuple."""
        return self._entity.hitbox.get_rect()

    def get_image(self):
        """Returns the character current image."""
        return self._entity.get_image()

    def reset(self):
        """Resets the character."""
        self._creature.reset()
        self._entity.reset()
        self._potions = [3, 3]
        self._cooldown = 0
        for spell in self._equipped_spells:
            self._equipped_spells[spell].reset()

    def tick(self):
        """Ticks down the character."""
        self._creature.tick()
        self._entity.tick(self, self._base_speed)
        if self._cooldown > 0:
            self._cooldown -= float(SYSTEM["options"]["fps"])
        for _, skill in self._equipped_spells.items():
            if skill is not None:
                skill.tick()
        SYSTEM["player.x"] = self.hitbox.center[0]
        SYSTEM["player.y"] = self.hitbox.center[1]
        for proj in PROJECTILE_GRID.query(self.hitbox):
            if isinstance(proj, Generator):
                continue
            if proj.evil and proj.hitbox.is_colliding(self._entity.hitbox):
                if proj in self._immune:
                    return
                dmg, crit = self.creature.damage(proj.damage)
                SYSTEM["text_generator"].generate_damage_text(self.x, self.y,\
                                                              (255, 30, 30), crit, dmg)
                if Flags.PIERCING not in proj.behaviours:
                    proj.flag()
                else:
                    self._immune.append(proj)
        for slash in SLASH_GRID.query(self.hitbox):
            if slash.evil and slash.hitbox.is_colliding(self._entity.hitbox):
                if slash in self._immune:
                    return
                dmg, crit = slash.on_hit(self._creature)
                SYSTEM["text_generator"].generate_damage_text(self.x, self.y,\
                                                              (255, 30, 30), crit, dmg)
                self._immune.append(slash)
        for pickup in POWER_UP_GRID.query(self.hitbox):
            if self.hitbox.is_colliding(pickup.hitbox):
                pickup.pickup(self)

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
        if keys[K_q]:
            if self._equipped_spells[K_q] is not None:
                self._equipped_spells[K_q].cast(self._creature, self._entity, False)
        if keys[K_e]:
            if self._equipped_spells[K_e] is not None:
                self._equipped_spells[K_e].cast(self._creature, self._entity, False)
        if keys[K_f]:
            if self._equipped_spells[K_f] is not None:
                self._equipped_spells[K_f].cast(self._creature, self._entity, False)
        if keys[K_t]:
            if self._equipped_spells[K_t] is not None:
                self._equipped_spells[K_t].cast(self._creature, self._entity, False)
        if keys[K_r]:
            if self._equipped_spells[K_r] is not None:
                self._equipped_spells[K_r].cast(self._creature, self._entity, False)
        if keys[K_LSHIFT]:
            if self._equipped_spells[K_LSHIFT] is not None:
                self._equipped_spells[K_LSHIFT].cast(self._creature, self._entity, False)
        if keys[K_1]:
            self.use_life_potion()
        if keys[K_2]:
            self.use_mana_potion()

    def use_life_potion(self):
        """Uses a life potion, which heals for 20% of the user's life."""
        #TODO: Maybe add stats to them ?
        if self._potions[0] > 0 and self._cooldown <= 0.0:
            self._potions[0]-= 1
            self._cooldown = 0.5
            self._creature.stats["life"].current_value +=\
                self._creature.stats["life"].get_value() / 5

    def use_mana_potion(self):
        """Uses a mana potion, which heals for 40% of the user's mana."""
        #TODO: Maybe add stats to them ?
        if self._potions[1] > 0 and self._cooldown <= 0.0:
            self._potions[1]-= 1
            self._cooldown = 0.5
            self._creature.stats["mana"].current_value +=\
                self._creature.stats["mana"].get_value() * 0.4

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

    @property
    def potions(self):
        """Returns the user's potions."""
        return self._potions

    @potions.setter
    def potions(self, value):
        self._potions = value

    @property
    def equipped_spells(self):
        """Returns the character equipped spells."""
        return self._equipped_spells

    @equipped_spells.setter
    def equipped_spells(self, value):
        self._equipped_spells = value

    @property
    def spellbook(self):
        """Returns the character's known spells."""
        return self._spellbook

    @spellbook.setter
    def spellbook(self, value):
        self._spellbook = value

    @property
    def inventory(self):
        """Returns the character's inventory."""
        return self._inventory

    @inventory.setter
    def inventory(self, value):
        self._inventory = value
