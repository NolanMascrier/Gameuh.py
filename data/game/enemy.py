"""Class for ennemies. Ennemies are the physical entities
the player can fight in the world. They are a creature, 
and also an entity.
They can move toward the player, or fire projectiles."""

import random
import numpy

from data.physics.entity import Entity
from data.creature import Creature
from data.constants import Flags, POWER_UP_TRACKER, SYSTEM, SCREEN_HEIGHT, SCREEN_WIDTH
from data.game.pickup import PickUp
from data.game.spell import Spell

DAMAGE_COLOR = (255, 30, 30)
VALUE_GROUPS = [5000, 2500, 1000, 500, 250, 100, 50, 20, 5, 1]

ALREADY = []

class Enemy():
    """Defines an enemy, which associates an entity to a creature
    with set behaviours."""
    def __init__(self, entity: Entity, creature: Creature, abilities, power = 1,\
                timer = 2, exp_value = 10, gold_value = 10, behaviours = None,\
                tier = 1, delay = 0, destination = None):
        self._entity = entity
        self._creature = creature
        self._creature.origin = self
        if behaviours is None:
            self._behaviours = []
        else:
            self._behaviours = behaviours
        self._timer = timer / self.creature.stats["cast_speed"].c_value
        self._power = power
        self._counter = 0
        self._destination = destination
        self._started = False if destination is not None else True
        if not self._started:
            self._entity.play("dash")
        self._abilities = abilities
        self._gold_value = gold_value
        self._exp_value = exp_value
        self._exploded = False
        self._immune = []
        self._stopped = False
        self._aim_right = False
        self._tier = tier
        self._delay = delay
        self._attacking = False
        self._attack_delay = 0

    def explode(self):
        """Explodes the creature in loot, life and mana orbs,
        and exp."""
        loot = SYSTEM["looter"].enemy_drop(self)
        pickups = []
        pickups.extend([(d, "rune") for d in loot["runes"]])
        pickups.extend([(d, "life") for d in loot["life"]])
        pickups.extend([(d, "mana") for d in loot["mana"]])
        for pickup, types in pickups:
            x = self.x + numpy.random.randint(-20, 20)
            y = self.y + numpy.random.randint(-20, 20)
            match types:
                case "rune":
                    pu = PickUp(x, y, pickup, flags=[Flags.RUNE])
                case "life":
                    pu = PickUp(x, y, pickup, flags=[Flags.LIFE])
                case "mana":
                    pu = PickUp(x, y, pickup, flags=[Flags.MANA])
            POWER_UP_TRACKER.append(pu)
        exp = self._exp_value
        for value in VALUE_GROUPS:
            while exp >+ value:
                x = self.x + 30
                y = self.y + 60
                pu = PickUp(x, y, value, flags=[Flags.EXPERIENCE], speed_mod=2.5)
                POWER_UP_TRACKER.append(pu)
                exp -= value
        gold_left = int(loot["gold"])
        for value in VALUE_GROUPS:
            while gold_left >= value:
                x = self.x + numpy.random.randint(-20, 20)
                y = self.y + numpy.random.randint(-20, 20)
                pu = PickUp(x, y, value, flags=[Flags.GOLD], speed_mod=2.5)
                POWER_UP_TRACKER.append(pu)
                gold_left -= value
        for l in loot["items"]:
            x = self.x + numpy.random.randint(-20, 20)
            y = self.y + numpy.random.randint(-20, 20)
            pu = PickUp(x, y, 1, flags=[Flags.ITEM], contained=l)
            POWER_UP_TRACKER.append(pu)
            if l in ALREADY:
                print("DUPLICATE")
            else:
                ALREADY.append(l)
        self._exploded = True

    def distance_to_player(self, player):
        """Returns the distance to the player."""
        dx = player.entity.center_x - self.entity.center_x
        dy = player.entity.center_y - self.entity.center_y
        return dx*dx + dy*dy

    def distance_to_destination(self):
        """Returns the distance to the destination."""
        dx = self._destination[0] - self.x
        dy = self._destination[1] - self.y
        return dx*dx + dy*dy

    def on_hit(self, value):
        """Called when the creature is hit."""
        self._entity.play("hit")
        if Flags.SUICIDER in self._behaviours:
            self.attack()
            self.explode()

    def on_crit(self):
        """Called when the creature crits."""

    def on_dodge(self):
        """Called when the creature dodges."""

    def on_block(self):
        """Called when the creature blocks."""

    def on_damage(self, value):
        """Called when the creature inflicts damage."""

    def on_heal(self, value):
        """Called when the creature heals."""

    def tick(self, player):
        """Ticks down the entity."""
        if self._exploded:
            return
        if self._creature.stats["life"].current_value <= 0:
            if Flags.SUICIDER in self._behaviours:
                self._entity.play("attack")
                self.attack()
            self._entity.detach("die", True)
            self.explode()
            return
        if self._entity.is_inside(SYSTEM["mouse"]):
            SYSTEM["mouse_target"] = self
        self._entity.tick(self)
        self._creature.tick()
        if self._attacking and self._attack_delay >= self._delay:
            self.attack()
            self._attacking = False
            self._stopped = False
        elif self._attacking:
            self._attack_delay += 0.016
            return
        self._counter += 0.016
        if not self._started:
            self._entity.move(self._destination)
            if self.distance_to_destination() < 1000 or self._counter >= 3:
                self._started = True
                self._entity.play("idle")
                self._counter = 0
            return
        if Flags.CHASER in self._behaviours or Flags.SUICIDER in self._behaviours:
            if self._stopped:
                if self._counter >= self._timer:
                    self._entity.play("attack")
                    self._attack_delay = 0
                    self._attacking = True
            else:
                desired_flip = player.entity.center_x > self.entity.center_x
                if desired_flip != self.entity.flipped:
                    self.entity.flip(desired_flip)
                    self._aim_right = not desired_flip
                if self.distance_to_player(player) < 10000:
                    self._stopped = True
                    self._counter = 0
                else:
                    self._entity.move((player.x, player.y))
        if Flags.SHOOTER in self._behaviours:
            if self._counter >= self._timer:
                self._entity.play("attack")
                self._attack_delay = 0
                self._attacking = True
        if Flags.RANDOM_MOVE in self._behaviours:
            if self._counter >= self._timer:
                self.attack()
                self._destination = [numpy.random.randint(SCREEN_WIDTH - 400, SCREEN_WIDTH),\
                                     numpy.random.randint(100, SCREEN_HEIGHT - 400)]
            else:
                self._entity.move(self._destination)
        if self._counter >= self._timer:
            self._counter -= self._timer

    def attack(self):
        """Launches a random attack from the enemy's arsenal."""
        choice = random.uniform(0, sum(weight for _, weight in self._abilities))
        cumulative = 0.0
        for ability, weight in self._abilities:
            cumulative += weight
            if cumulative >= choice:
                if ability not in SYSTEM["spells"] or \
                    not isinstance(SYSTEM["spells"][ability], Spell):
                    return
                if Flags.SUICIDER in self._behaviours:
                    ignore = True
                else:
                    ignore = False
                SYSTEM["spells"][ability].cast(self._creature, self._entity,\
                                               True, self._aim_right, True, ignore)
                break
        if Flags.SUICIDER in self._behaviours:
            self.creature.stats["life"].value = 0
            self._exploded = True

    def get_image(self):
        """Returns the entity's image."""
        return self._entity.get_image()

    def get_pos(self) -> tuple:
        """Returns the position for the image."""
        return self._entity.hitbox.center_offset

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

    @property
    def destroyed(self) -> bool:
        """Returns whether or not the enemy can be\
        removed."""
        return self._exploded

    @property
    def immune(self):
        """Returns the enemy's immunity."""
        return self._immune

    @immune.setter
    def immune(self, value):
        self._immune = value

    @property
    def tier(self):
        """Returns the enemy's tier."""
        return self._tier

    @property
    def gold_value(self):
        """Returns the enemy's gold value."""
        return self._gold_value
