"""Class for ennemies. Ennemies are the physical entities
the player can fight in the world. They are a creature, 
and also an entity.
They can move toward the player, or fire projectiles."""

import random
from data.physics.entity import Entity
from data.creature import Creature
from data.constants import Flags, PROJECTILE_GRID, POWER_UP_TRACKER, SYSTEM
from data.game.pickup import PickUp
from data.game.spell import Spell
from data.projectile import Projectile
from data.slash import Slash

DAMAGE_COLOR = (255, 30, 30)

class Enemy():
    """Defines an enemy, which associates an entity to a creature
    with set behaviours."""
    def __init__(self, entity: Entity, creature: Creature, abilities, power = 1,\
                timer = 2, exp_value = 10, gold_value = 10, behaviours = None):
        self._entity = entity
        self._creature = creature
        if behaviours is None:
            self._behaviours = []
        else:
            self._behaviours = behaviours
        self._timer = timer
        self._power = power
        self._counter = 0
        self._abilities = abilities
        self._gold_value = gold_value
        self._exp_value = exp_value
        self._exploded = False
        self._immune = {}
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
        denominations = [5000, 2500, 1000, 500, 250, 100, 50, 20, 5, 1]
        exp = self._exp_value
        for value in denominations:
            while exp >+ value:
                x = self.x + 30
                y = self.y + 60
                pu = PickUp(x, y, value, flags=[Flags.EXPERIENCE], speed_mod=2.5)
                POWER_UP_TRACKER.append(pu)
                exp -= value
        gold_left = self._gold_value
        for value in denominations:
            while gold_left >= value:
                x = self.x + random.randint(-20, 20)
                y = self.y + random.randint(-20, 20)
                pu = PickUp(x, y, value, flags=[Flags.GOLD], speed_mod=2.5)
                POWER_UP_TRACKER.append(pu)
                gold_left -= value
        loot = SYSTEM["looter"].roll(1, self._creature.level)
        for l in loot:
            x = self.x + random.randint(-20, 20)
            y = self.y + random.randint(-20, 20)
            pu = PickUp(x, y, 1, flags=[Flags.ITEM], contained=l)
            POWER_UP_TRACKER.append(pu)
        self._exploded = True

    def distance_to_player(self, player):
        """Returns the distance to the player."""
        dx = player.x - self.x
        dy = player.y - self.y
        return dx*dx + dy*dy

    def tick(self, player):
        """Ticks down the entity."""
        if self._exploded:
            return
        if self._creature.stats["life"].current_value <= 0:
            self.explode()
            return
        self._counter += float(SYSTEM["options"]["fps"])
        self._entity.tick(self)
        self._creature.tick()
        if Flags.CHASER in self._behaviours:
            if self._stopped:
                if self._counter >= self._timer:
                    self.attack()
                    self._stopped = False
            else:
                if not self._entity.flipped and player.x > self.x:
                    self.entity.flip()
                    self._aim_right = True
                if self._entity.flipped and player.x < self.x:
                    self.entity.flip()
                    self._aim_right = False
                if self.distance_to_player(player) < 1000:
                    self._stopped = True
                    self._counter = 0
                else:
                    self._entity.move((player.x, player.y))
        if Flags.SHOOTER in self._behaviours:
            if self._counter >= self._timer:
                self.attack()
        if self._counter >= self._timer:
            self._counter -= self._timer
        for proj in PROJECTILE_GRID.query(self.hitbox):
            if not proj.evil and proj.hitbox.is_colliding(self._entity.hitbox):
                if proj in self._immune:
                    return
                if isinstance(proj, Projectile):
                    dmg, crit = self.creature.damage(proj.damage)
                    SYSTEM["text_generator"].generate_damage_text(self.x, self.y,\
                                                                DAMAGE_COLOR, crit, dmg)
                    if Flags.PIERCING not in proj.behaviours:
                        proj.flag()
                    else:
                        self._immune[proj] = True
                elif isinstance(proj, Slash):
                    dmg, crit = proj.on_hit(self._creature)
                    SYSTEM["text_generator"].generate_damage_text(self.x, self.y,\
                                                                DAMAGE_COLOR, crit, dmg)
                    self._immune[proj] = True

    def attack(self):
        """Launches a random attack from the enemy's arsenal."""
        choice = random.uniform(0, 1)
        cumulative = 0.0
        for ability, weight in self._abilities:
            cumulative += weight
            if cumulative >= choice:
                if ability not in SYSTEM["spells"] or \
                    not isinstance(SYSTEM["spells"][ability], Spell):
                    return
                SYSTEM["spells"][ability].cast(self._creature, self._entity,\
                                               True, self._aim_right, True)

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

    @property
    def destroyed(self) -> bool:
        """Returns whether or not the enemy can be\
        removed."""
        return self._exploded
