"""Class for ennemies. Ennemies are the physical entities
the player can fight in the world. They are a creature, 
and also an entity.
They can move toward the player, or fire projectiles."""

import random
from math import atan2, pi, sqrt
from data.physics.entity import Entity
from data.creature import Creature
from data.constants import Flags, PROJECTILE_TRACKER, POWER_UP_TRACKER, SYSTEM, ENNEMY_TRACKER
from data.spell_list import *
from data.projectile import Projectile
from data.game.pickup import PickUp

class Enemy():
    """Defines an enemy, which associates an entity to a creature
    with set behaviours."""
    def __init__(self, entity: Entity, creature: Creature, projectile, power = 1,\
                timer = 2, exp_value = 10, behaviours = None):
        self._entity = entity
        self._creature = creature
        if behaviours is None:
            self._behaviours = []
        else:
            self._behaviours = behaviours
        self._timer = timer
        self._power = power
        self._counter = 0
        self._projectile = projectile
        self._exp_value = exp_value
        self._exploded = False
        self._immune = []
        self._stopped = False
        self._aim_right = False

    def explode(self):
        """Explodes the creature in loot, life and mana orbs,
        and exp."""
        amount = random.randint(0,5)
        for _ in range(amount + 1):
            power_type = True if random.randint(0, 1) == 0 else False
            x = self.x + 30
            y = self.y + 60
            pu = PickUp(x, y, value = 1)
            if power_type:
                pu.flags.append(Flags.MANA)
            else:
                pu.flags.append(Flags.LIFE)
            POWER_UP_TRACKER.append(pu)
        for _ in range(self._exp_value + 1):
            x = self.x + 30
            y = self.y + 60
            pu = PickUp(x, y, 1, flags=[Flags.EXPERIENCE], speed_mod=2.5)
            POWER_UP_TRACKER.append(pu)
        self._exploded = True

    def distance_to_player(self, player):
        """Returns the distance to the player."""
        return sqrt((self.x - player.x) ** 2 + (self.y - player.y) ** 2)

    def tick(self, player):
        """Ticks down the entity."""
        if self._exploded:
            return
        if self._creature.stats["life"].current_value <= 0:
            self.explode()
            return
        self._counter += 0.016
        self._entity.tick(self)
        self._creature.tick()
        if Flags.CHASER in self._behaviours:
            if self._stopped:
                if self._counter >= self._timer:
                    SYSTEM["spells"]["e_charge"].cast(self._creature, self._entity, True,\
                                                    aim_right=self._aim_right)
                    self._stopped = False
            else:
                if not self._entity.flipped and player.x > self.x:
                    self.entity.flip()
                    self._aim_right = True
                if self._entity.flipped and player.x < self.x:
                    self.entity.flip()
                    self._aim_right = False
                if self.distance_to_player(player) < 100:
                    self._stopped = True
                    self._counter = 0
                else:
                    self._entity.move((player.x, player.y))
        if Flags.SHOOTER in self._behaviours:
            if self._counter >= self._timer:
                self.attack(player)
        if self._counter >= self._timer:
            self._counter -= self._timer
        for proj in PROJECTILE_TRACKER.copy():
            if not proj.evil and proj.hitbox.is_colliding(self._entity.hitbox):
                if proj in self._immune:
                    return
                dmg, crit = self.creature.damage(proj.damage)
                SYSTEM["text_generator"].generate_damage_text(self.x, self.y,\
                                                              (255, 30, 30), crit, dmg)
                if Flags.PIERCING not in proj.behaviours:
                    PROJECTILE_TRACKER.remove(proj)
                else:
                    self._immune.append(proj)
        for slash in SLASH_TRACKER:
            if not slash.evil and slash.hitbox.is_colliding(self._entity.hitbox):
                if slash in self._immune:
                    return
                dmg, crit = slash.on_hit(self._creature)
                SYSTEM["text_generator"].generate_damage_text(self.x, self.y,\
                                                              (255, 30, 30), crit, dmg)
                self._immune.append(slash)

    def attack(self, player):
        """Shoots a projectile toward the player."""
        angle = 90 - atan2(player.hitbox.center[0] - self._entity.x,\
                           player.hitbox.center[1] - self._entity.y) * 180 / pi
        proj = Projectile(self._entity.x, self._entity.y, angle, SYSTEM["images"]["energyball"],\
                          DARKBOLT, self._creature, True)
        PROJECTILE_TRACKER.append(proj)

    def get_image(self):
        """Returns the entity's image."""
        return self._entity.get_image()

    @property
    def entity(self):
        """Returns the enemy's entity."""
        return self._entity

    @entity.setter
    def entity(self, value):
        self._entity = value

    @property
    def creature(self):
        """Returns the enemy's creature."""
        return self._creature

    @creature.setter
    def creature(self, value):
        self._creature = value

    @property
    def hitbox(self):
        """Returns the enemy's hitbox. Shorthand for\
        Enemy.entity.hitbox"""
        return self._entity.hitbox

    @property
    def x(self):
        """Returns the enemy's x. Shorthand for\
        Enemy.entity.x"""
        return self._entity.x

    @property
    def y(self):
        """Returns the enemy's y. Shorthand for\
        Enemy.entity.y"""
        return self._entity.y
