"""Class for ennemies. Ennemies are the physical entities
the player can fight in the world. They are a creature, 
and also an entity.
They can move toward the player, or fire projectiles."""

from math import atan2, pi
from data.physics.entity import Entity
from data.creature import Creature
from data.constants import Flags, PROJECTILE_TRACKER, TEXT_TRACKER, SYSTEM
#TODO: Replace with real projectile code
from data.Fireball import Fireball

class Enemy():
    """Defines an enemy, which associates an entity to a creature
    with set behaviours."""
    def __init__(self, entity: Entity, creature: Creature, projectile, power = 1,\
                timer = 2, behaviours = None):
        self._entity = entity
        self._creature = creature
        if behaviours is None:
            self._behaviours = []
        else:
            self._behaviours = behaviours
        self._timer = timer
        #TODO: Replace enemy damage with actual damage sources
        self._power = power
        self._counter = 0
        self._projectile = projectile

    def tick(self, player):
        """Ticks down the entity."""
        if self._creature.stats["life"].current_value <= 0:
            return
        self._counter += 0.016
        self._entity.tick(player)
        self._creature.tick()
        if Flags.CHASER in self._behaviours:
            self._entity.move((player.x, player.y))
        if Flags.SHOOTER in self._behaviours:
            if self._counter >= self._timer:
                self.attack(player)
        if self._counter >= self._timer:
            self._counter -= self._timer
        for proj in PROJECTILE_TRACKER.copy():
            if not proj.evil and proj.box.is_colliding(self._entity.hitbox):
                #self._creature.damage() ...
                self._creature.stats["life"].current_value -= proj.power
                text = SYSTEM["font"].render(f'{proj.power}', False, (255, 30, 30))
                TEXT_TRACKER.append([text, proj.x, proj.y, 255])
                PROJECTILE_TRACKER.remove(proj)

    def attack(self, player):
        """Shoots a projectile toward the player."""
        angle = 90 - atan2(player._box.center[0] - self._entity.x, player._box.center[1] - self._entity.y) * 180 / pi
        proj = Fireball(self._entity.x, self._entity.y, angle, True, self._power, image=self._projectile, animated=True, max_frame=4)
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
