"""Class that defines a level.
A level can be of multiple type:
Waves, dungeon ...
Only waves for now."""

import random
from data.creature import Creature
from data.constants import ENNEMY_TRACKER, SCREEN_WIDTH, SCREEN_HEIGHT
from data.game.enemy import Enemy
from data.physics.entity import Entity
from data.physics.hitbox import HitBox
from data.image.animation import Animation
from data.image.parallaxe import Parallaxe
from data.game.statblocks import *

class Level():
    """A level."""
    def __init__(self, name: str, area_lvl:int, icon: Animation,\
        background: Animation|Parallaxe|None = None,\
        waves: int = 5, \
        flags = None):
        self._name = name
        self._area_level = area_lvl
        self._icon = icon
        self._background = background
        self._waves = waves
        self._current_wave = 0
        if flags is None:
            self._flags = []
        else:
            self._flags = flags

    def generate_enemy(self, reference: list, level:int):
        """Creates a single enemy."""
        y_pos = random.randint(0, SCREEN_HEIGHT - 300)
        enemy_type = reference[3].copy()
        img = reference[0]
        hb = HitBox(SCREEN_WIDTH - 100, y_pos, img.width, img.height)
        ent = Entity(SCREEN_WIDTH - 100, y_pos, img, hb)
        crea = Creature(reference[1])
        crea.import_stackblock(reference[2])
        #TODO: append the modifiers from the level to the creature
        crea.scale(level)
        enemy = Enemy(ent, crea, reference[7], behaviours=[enemy_type],\
            timer=1, exp_value=reference[3]*level)
        return enemy

    def summon_wave(self, level:int, wave:int):
        """Summons a wave of monsters."""
        min_monsters = 3 + random.randint(0, 5) * wave
        max_monsters = 10 + random.randint(0, 5) * wave
        monsters = random.randint(min_monsters, max_monsters) + 1
        for i in range(monsters):
            #TODO: Actual random choice of monster depending on zone
            monster = VOIDLING if random.randint(0, 1) == 0 else VOIDSNIPER
            mob = self.generate_enemy(monster, level)
            ENNEMY_TRACKER.append(mob)
