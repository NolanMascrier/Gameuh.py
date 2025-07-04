"""Class that defines a level.
A level can be of multiple type:
Waves, dungeon ...
Only waves for now."""

import random
import pygame
from data.creature import Creature
from data.constants import ENNEMY_TRACKER, SCREEN_WIDTH, SCREEN_HEIGHT, WAVE_TIMER, SYSTEM, GAME_VICTORY
from data.game.enemy import Enemy
from data.physics.entity import Entity
from data.physics.hitbox import HitBox
from data.image.animation import Animation
from data.image.parallaxe import Parallaxe
from data.tables.enemy_table import *

class Level():
    """A level."""
    def __init__(self, name: str, area_lvl:int, icon: Animation,\
                    wave_timer = 5000,\
                    background: Animation|Parallaxe|None = None,\
        waves: int = 5, \
        flags = None):
        self._name = name
        self._area_level = area_lvl
        self._icon = icon
        self._background = background
        self._started = False
        self._finished = False
        self._current_wave = 0
        self._waves = waves
        if flags is None:
            self._flags = []
        else:
            self._flags = flags
        self._wave_timer = wave_timer
        self._gold = 0
        self._loot = []

    def generate_enemy(self, reference: list, level:int):
        """Creates a single enemy."""
        y_pos = random.randint(0, SCREEN_HEIGHT - 300)
        enemy_type = reference[3]
        img = SYSTEM["images"][reference[0]]
        hb = HitBox(SCREEN_WIDTH - 100, y_pos, img.width, img.height)
        ent = Entity(SCREEN_WIDTH - 100, y_pos, img, hb)
        exp_value = random.randint(int(reference[5]*(level + 1) *0.9),\
                                   int(reference[5]*(level + 1) * 1.1))
        gold_value = random.randint(int(reference[6]*(level + 1) *0.9),\
                                    int(reference[6]*(level + 1) * 1.1))
        crea = Creature(reference[1])
        crea.import_stackblock(reference[2])
        #TODO: append the modifiers from the level to the creature
        crea.scale(level)
        enemy = Enemy(ent, crea, reference[7], behaviours=enemy_type,\
            timer=1, exp_value=exp_value, gold_value=gold_value)
        return enemy

    def summon_wave(self, level:int, wave:int):
        """Summons a wave of monsters."""
        min_monsters = (1 + random.randint(0, 3)) * wave
        max_monsters = (4 + random.randint(0, 3)) * wave
        monsters = max(random.randint(min_monsters, max_monsters + 1), 1)
        for _ in range(monsters):
            #TODO: Actual random choice of monster depending on zone
            monster = VOIDLING if random.randint(0, 1) == 0 else VOIDSNIPER
            mob = self.generate_enemy(monster, level)
            ENNEMY_TRACKER.append(mob)

    def start(self):
        """Starts the level."""
        pygame.time.set_timer(WAVE_TIMER, self._wave_timer)
        self.summon_wave(self._area_level, self._current_wave)
        self._current_wave += 1

    def next_wave(self):
        """Summons the next wave."""
        if not self._started:
            self._started = True
            self.start()
            return
        if self._current_wave > self._waves:
            if len(ENNEMY_TRACKER) <= 0:
                self._finished = True
                SYSTEM["player"].gold += self._gold
                SYSTEM["game_state"] = GAME_VICTORY
            return
        self.summon_wave(self._area_level, self._current_wave)
        self._current_wave += 1

    @property
    def name(self) -> str:
        """Returns the level's name."""
        return self._name

    @name.setter
    def name(self, value):
        self._name = value

    @property
    def area_level(self) -> int:
        """Returns the level's area level."""
        return self._area_level

    @area_level.setter
    def area_level(self, value):
        self._area_level = value

    @property
    def icon(self):
        """Returns the level's icon."""
        return self._icon

    @icon.setter
    def icon(self, value):
        self._icon = value

    @property
    def background(self):
        """Returns the level's background image."""
        return self._background

    @background.setter
    def background(self, value):
        self._background = value

    @property
    def finished(self):
        """Returns whether or not the level is finished."""
        return self._finished

    @finished.setter
    def finished(self, value):
        self._finished = value

    @property
    def current_wave(self):
        """Returns the level's current wave.."""
        return self._current_wave

    @current_wave.setter
    def current_wave(self, value):
        self._current_wave = value

    @property
    def gold(self):
        """Returns the amount of gold gained during this level."""
        return self._gold

    @gold.setter
    def gold(self, value):
        self._gold = value

    @property
    def loot(self):
        """Returns the loot gained during this level."""
        return self._loot

    @loot.setter
    def loot(self, value):
        self._loot = value
