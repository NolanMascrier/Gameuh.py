"""Class for player characters."""

import json
import numpy
from data.constants import SCREEN_HEIGHT, SYSTEM, Flags, BLUE, GREEN, Classes
from data.physics.hitbox import HitBox
from data.physics.entity import Entity
from data.game.creature import Creature
from data.game.item import Item

KEY_TYPE = {
    0: "spell_1",
    1: "spell_2",
    2: "spell_3",
    3: "spell_4",
    4: "spell_5",
    5: "dash",
    6: "potion_life",
    7: "potion_mana",
    8: "up",
    9: "down",
    10: "left",
    11: "right",
    12: "pause"
}

class Character():
    """Defines a character. A character is a creature/entity
    specifically made to be used by players."""
    def __init__(self, x = 10, y = SCREEN_HEIGHT / 2, imagefile:str = None, speed = 12):
        if imagefile is None:
            box = None
        else:
            box = HitBox(x, y, SYSTEM["images"][imagefile].width / 3,\
                        SYSTEM["images"][imagefile].height / 2)
        self._entity = Entity(x, y, imagefile, box, speed)
        self._creature = Creature("hero", self)
        self._cooldown = 0
        self._max_cooldown = 2
        self._class = Classes.SORCERESS
        self._base_speed = speed
        self._potions = [3, 3]
        self._equipped_spells = {
            "spell_L": "firebolt",
            "spell_R": None,
            "spell_M": None,
            "spell_1": "voidbolt",
            "spell_2": "arc",
            "spell_3": "icebolt",
            "spell_4": "elefury",
            "spell_5": "furyslash",
            "spell_6": None,
            "spell_7": None,
            "dash": "winddash"
        }
        self._immune = []
        self._spellbook = [
            "firebolt",
            "fireball",
            "voidbolt",
            "arc",
            "icebolt",
            "masterstrike",
            "rip",
            "exult",
            "magicmissile",
            "elefury",
            "furyslash",
            "winddash",
        ]
        self._inventory = []
        self._runes = [
            0, 0, 0, 0, 0, 0, 0, 0, 0, 0
        ]
        self._gold = 0
        self._input = [0, 0]

    def get_pos(self):
        """Returns the position of the character as a
        rect tuple."""
        x, y, w, h = self._entity.get_rect()
        x -= 20
        y -= 10
        return (x, y, w, h)

    def get_image(self):
        """Returns the character current image."""
        return self._entity.get_image()

    def reset(self):
        """Resets the character."""
        self._creature.reset()
        self._entity.reset()
        self._potions = [
            self._creature.stats["potion_healing_count"].c_value,
            self._creature.stats["potion_mana_count"].c_value
        ]
        self._cooldown = 0
        for spell in self._equipped_spells:
            if self.equipped_spells[spell] is not None:
                SYSTEM["spells"][self._equipped_spells[spell]].reset()

    def tick(self):
        """Ticks down the character."""
        self._creature.tick()
        self._entity.tick(self, self._base_speed)
        if self._cooldown > 0:
            self._cooldown -= float(0.016)
        already_ticked = []
        for spell, skill in self._equipped_spells.items():
            if skill is not None and skill not in already_ticked:
                SYSTEM["spells"][self._equipped_spells[spell]].tick(self)
                already_ticked.append(skill)
        SYSTEM["player.x"] = self.hitbox.center[0]
        SYSTEM["player.y"] = self.hitbox.center[1]
        desired_flip = SYSTEM["mouse"][0] < self.entity.center_x
        if desired_flip != self.entity.flipped:
            self.entity.flip(desired_flip)
        if self._creature.stats["life"].current_value <= 0:
            SYSTEM["level"].fail_level()

    def __cast(self, keys):
        """Cast a spell from the corresponding keys."""
        if self._equipped_spells[keys] is not None:
            SYSTEM["spells"][self._equipped_spells[keys]]\
                .cast(self._creature, self._entity, False, not self._entity.flipped)

    def on_hit(self, value):
        """Called when the creature is hit."""

    def on_crit(self):
        """Called when the creature crits."""
        for keys in self._equipped_spells:
            if self._equipped_spells[keys] is not None:
                SYSTEM["spells"][self._equipped_spells[keys]]\
                    .on_crit(self._creature, self._entity, False, self._entity.flipped)

    def on_dodge(self):
        """Called when the creature dodges."""

    def on_block(self):
        """Called when the creature blocks."""

    def on_damage(self, value):
        """Called when the creature inflicts damage."""

    def gain_exp(self, amount):
        """Grants exp to the equipped skills."""
        for _, s in self._equipped_spells.items():
            if s is not None:
                SYSTEM["spells"][s].gain_exp(amount)

    def __move(self, dx, dy):
        """Moves the character by dx, dy."""
        new_x = self._entity.x + dx
        new_y = self._entity.y + dy
        self._entity.angle = numpy.arctan2(new_y - self._entity.y,\
            new_x - self._entity.x)
        self._entity.displace((new_x, new_y))

    def __set_movement(self, dx, dy):
        """Prepares the movement."""
        self._input[0] += dx
        self._input[1] += dy

    def action(self, keys):
        """Acts depending on the input."""
        actions = {
            "spell_L": lambda: self.__cast("spell_L"),
            "spell_R": lambda: self.__cast("spell_R"),
            "spell_M": lambda: self.__cast("spell_M"),
            "spell_1": lambda: self.__cast("spell_1"),
            "spell_2": lambda: self.__cast("spell_2"),
            "spell_3": lambda: self.__cast("spell_3"),
            "spell_4": lambda: self.__cast("spell_4"),
            "spell_5": lambda: self.__cast("spell_5"),
            "spell_6": lambda: self.__cast("spell_6"),
            "spell_7": lambda: self.__cast("spell_7"),
            "dash": lambda: self.__cast("dash"),
            "potion_life": self.use_life_potion,
            "potion_mana": self.use_mana_potion,
            "left": lambda: self.__set_movement(-1, 0),
            "right": lambda: self.__set_movement(1, 0),
            "up": lambda: self.__set_movement(0, -1),
            "down": lambda: self.__set_movement(0, 1),
        }
        if Flags.CANNOT_ACT in self.creature.gather_flags():
            return
        for k in keys:
            if k in actions:
                actions[k]()
        dx = self._input[0] * self._entity.move_speed
        dy = self._input[1] * self._entity.move_speed
        self.__move(dx, dy)
        self._input = [0, 0]

    def use_life_potion(self):
        """Uses a life potion, which heals for 20% of the user's life."""
        if self._creature.stats["life"].current_value >= \
            self._creature.stats["life"].get_free_ressource():
            return
        if self._potions[0] > 0 and self._cooldown <= 0.0:
            self._potions[0]-= 1
            self._cooldown = 0.5
            flat_heal = self._creature.stats["potion_healing_flat"].c_value
            rel_heal = self._creature.stats["potion_healing_relative"].c_value * \
                       self._creature.stats["life"].get_value()
            self._creature.stats["life"].current_value += flat_heal + rel_heal
            SYSTEM["text_generator"].generate_damage_text(self.x, self.y, GREEN,
                                                                    False, rel_heal + flat_heal)

    def use_mana_potion(self):
        """Uses a mana potion, which heals for 40% of the user's mana."""
        if self._creature.stats["mana"].current_value >= \
            self._creature.stats["mana"].get_free_ressource():
            return
        if self._potions[1] > 0 and self._cooldown <= 0.0:
            self._potions[1]-= 1
            self._cooldown = 0.5
            flat_heal = self._creature.stats["potion_mana_flat"].c_value
            rel_heal = self._creature.stats["potion_mana_relative"].c_value * \
                       self._creature.stats["mana"].get_value()
            self._creature.stats["mana"].current_value += flat_heal + rel_heal
            SYSTEM["text_generator"].generate_damage_text(self.x, self.y, BLUE,
                                                                    False, rel_heal + flat_heal)

    def export(self) -> str:
        """Serializes the character as JSON."""
        inventory = []
        for i in self._inventory:
            if isinstance(i, Item):
                inventory.append(i.export())
        data = {
            "type": "character",
            "creature": self._creature.export(),
            "entity": self._entity.export(),
            "speed": self._base_speed,
            "equiped_spells": self._equipped_spells,
            "known_spells": self._spellbook,
            "inventory": inventory,
            "gold": self._gold,
            "runes": self._runes
        }
        return json.dumps(data)

    @staticmethod
    def imports(data):
        """Creates a character from a json data array."""
        char = Character(
            0, 0, None, int(data["speed"])
        )
        char.entity = Entity.imports(json.loads(data["entity"]))
        char.creature = Creature.imports(json.loads(data["creature"]))
        char.equipped_spells = data["equiped_spells"]
        char.spellbook = data["known_spells"]
        char.gold = int(data["gold"])
        char.runes = data["runes"]
        for i in data["inventory"]:
            char.inventory.append(Item.imports(json.loads(i)))
        return char

    @property
    def current_class(self):
        """Returns the character's current class."""
        return self._class

    @property
    def x(self):
        """Returns the character's x value."""
        return self._entity.x

    @property
    def y(self):
        """Returns the character's y value."""
        return self._entity.y

    @property
    def right(self):
        """Returns the character's right value."""
        return self._entity.right

    @property
    def bottom(self):
        """Returns the character's bottom value."""
        return self._entity.bottom

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

    @property
    def immune(self):
        """Returns the character's immunity."""
        return self._immune

    @immune.setter
    def immune(self, value):
        self._immune = value

    @property
    def gold(self):
        """Returns the character's gold."""
        return self._gold

    @gold.setter
    def gold(self, value):
        self._gold = value

    @property
    def runes(self):
        """Return's the character's runes."""
        return self._runes

    @runes.setter
    def runes(self, value):
        self._runes = value
