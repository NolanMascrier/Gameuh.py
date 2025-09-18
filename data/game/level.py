"""Class that defines a level.
A level can be of multiple type:
Waves, dungeon ...
Only waves for now."""

import threading
import random
from data.creature import Creature
from data.constants import ENNEMY_TRACKER, SCREEN_WIDTH, SCREEN_HEIGHT, WAVE_TIMER, SYSTEM,\
    GAME_VICTORY, trad, LOADING, GAME_LEVEL, USEREVENT, TICKER_TIMER, UPDATE_TIMER,\
    PROJECTILE_TRACKER, POWER_UP_TRACKER, ANIMATION_TRACKER
from data.game.enemy import Enemy
from data.physics.entity import Entity
from data.physics.hitbox import HitBox
from data.image.animation import Animation
from data.image.parallaxe import Parallaxe
from data.numerics.affix import Affix
from data.image.text import Text
from data.tables.area_table import MODIFIERS
from data.tables.enemy_table import *

def init_timers():
    """Inits Pygame's timers."""
    SYSTEM["deltatime"].start(WAVE_TIMER, 500)
    SYSTEM["deltatime"].start(USEREVENT+1, 2000)
    SYSTEM["deltatime"].start(USEREVENT+2, 100)
    SYSTEM["deltatime"].start(TICKER_TIMER, int(0.016 * 1000))
    SYSTEM["deltatime"].start(UPDATE_TIMER, int(SYSTEM["options"]["fps"]))

class Level():
    """A level."""
    def __init__(self, name: str, area_lvl:int, icon: Animation,\
                    wave_timer = 5000,\
                    background: Animation|Parallaxe|None = None,\
                    waves: int = 5, difficulty = 0,\
                    flags = None):
        self._name = name
        self._area_level = area_lvl
        self._difficulty = difficulty
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
        self._wave_tracker = []
        self._modifiers = self.generate_modifiers()

    def generate_modifiers(self):
        """Generates a list of modifiers for the level."""
        mods_by_diff = {1: 2, 2: 3, 3: 4, 0: 0}
        target_mods = mods_by_diff[self._difficulty]
        modifiers = []
        total_risk = 0.0
        available = []
        for name, (tiers, type_weight, type_risk) in MODIFIERS.items():
            eligible_tiers = [t for t in tiers
                            if self._area_level >= t[2] and self._area_level <= t[3]]
            if eligible_tiers:
                available.append((name, eligible_tiers, type_weight, type_risk))
        to_pick = min(target_mods, len(available))
        options = available[:]
        for _ in range(to_pick):
            total_type_weight = sum(opt[2] for opt in options)
            r = random.uniform(0, total_type_weight)
            cum = 0.0
            picked_index = None
            for idx, opt in enumerate(options):
                cum += opt[2]
                if r <= cum:
                    picked_index = idx
                    break
            if picked_index is None:
                break
            name, eligible_tiers, type_weight, type_risk = options.pop(picked_index)
            tier_total = sum(t[1] for t in eligible_tiers)
            tr = random.uniform(0, tier_total)
            tcum = 0.0
            picked_tier = None
            for t in eligible_tiers:
                tcum += t[1]
                if tr <= tcum:
                    picked_tier = t
                    break
            if picked_tier is None:
                continue
            aff_obj = picked_tier[0]
            mod = aff_obj.roll()
            modifiers.append(mod)
            mod_value = mod.value
            total_risk += type_risk * mod_value
        if total_risk > 0:
            iiq = Affix("IIQ_RISK_REWARD", total_risk, [Flags.BOON, Flags.IIQ]).roll()
            iir = Affix("IIR_RISK_REWARD", total_risk / 7, [Flags.BOON, Flags.IIR]).roll()
            modifiers.extend([iiq, iir])
        return modifiers

    def generate_enemy(self, reference: list, level:int):
        """Creates a single enemy."""
        y_pos = random.randint(0, SCREEN_HEIGHT - 300)
        x_pos = random.randint(100, 300)
        enemy_type = reference["flags"]
        img = reference["image"]
        ent = Entity(SCREEN_WIDTH + 200, y_pos, img, hitbox_mod=reference["hitbox"])
        exp_value = random.randint(int(reference["exp"]*(level + 1) *0.9),\
                                   int(reference["exp"]*(level + 1) * 1.1))
        gold_value = random.randint(int(reference["gold"]*(level + 1) *0.9),\
                                    int(reference["gold"]*(level + 1) * 1.1))
        attack_delay = reference["delay"]
        crea = Creature(reference["name"])
        crea.import_stackblock(reference["stats"])
        for mod in self._modifiers:
            crea.afflict(mod.as_affliction())
        crea.scale(level)
        crea.reset()
        dest = (SCREEN_WIDTH - x_pos, y_pos)
        enemy = Enemy(ent, crea, reference["spelllist"], behaviours=enemy_type,\
            timer=2, exp_value=exp_value, gold_value=gold_value, delay=attack_delay,\
            destination=dest)
        return enemy

    def summon_wave(self, level:int, wave:int):
        """Summons a wave of monsters."""
        min_monsters = (1 + random.randint(0, 3)) * wave
        max_monsters = (4 + random.randint(0, 3)) * wave
        monsters = max(random.randint(min_monsters, max_monsters + 1), 1)
        wave = []
        for _ in range(monsters):
            #TODO: Actual random choice of monster depending on zone
            monster = VOIDSNIPER if random.randint(0, 1) == 0 else VOIDSNIPER
            mob = self.generate_enemy(monster, level)
            wave.append(mob)
        self._wave_tracker.append(wave)

    def load_level(self):
        """Loading function of the level."""
        SYSTEM["game_state"] = LOADING
        tasks = [(self.summon_wave, i, 1) for i in range(self._waves)]
        total = sum(weight for _, _, weight in tasks)
        SYSTEM["progress"] = 0
        progress = 0
        for t, i, w in tasks:
            SYSTEM["loading_text"] = Text(trad('loading', 'level'), font="item_titles", size=30)
            t(self._area_level, i)
            progress += w
            SYSTEM["progress"] = progress / total * 100
        SYSTEM["loaded"] = True
        SYSTEM["game_state"] = GAME_LEVEL
        init_timers()
        SYSTEM["deltatime"].clear()

    def init(self):
        """Sets up the background of the level."""
        SYSTEM["gm_background"].fill((0,0,0,0))
        SYSTEM["gm_background"].blit(self._background.background, (0,0))
        ENNEMY_TRACKER.clear()
        PROJECTILE_TRACKER.clear()
        POWER_UP_TRACKER.clear()
        ANIMATION_TRACKER.clear()
        loading_thread = threading.Thread(target=self.load_level)
        loading_thread.start()

    def start(self):
        """Starts the level."""
        SYSTEM["deltatime"].start(WAVE_TIMER, self._wave_timer)
        self.summon_wave(self._area_level, self._current_wave)
        self._current_wave += 1
        SYSTEM["deltatime"].clear()

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
                SYSTEM["deltatime"].stop(WAVE_TIMER)
            return
        for e in self._wave_tracker[self._current_wave]:
            ENNEMY_TRACKER.append(e)
        self._wave_tracker[self._current_wave].clear()
        self._current_wave += 1

    def distance_to_player(self, player, hitbox):
        """Returns the distance from the hitbox to the player."""
        dx = player.center_x - hitbox.center_x
        dy = player.center_y - hitbox.center_y
        return dx*dx + dy*dy

    def closest_enemy(self, exclude: Enemy = None):
        """Returns the closests enemy to the player."""
        dist = 99999999999999
        enemy = None
        for e in ENNEMY_TRACKER:
            if exclude is not None and e == exclude:
                continue
            dist_tmp = self.distance_to_player(SYSTEM["player"].entity.hitbox, e.entity.hitbox)
            if dist_tmp < dist:
                dist = dist_tmp
                enemy = e
        return enemy

    def closest_from(self, origin: HitBox, exclude: Enemy = None):
        """Returns the closest enemy from the origin."""
        dist = 99999999999999
        enemy = None
        for e in ENNEMY_TRACKER:
            if exclude is not None and e == exclude:
                continue
            dist_tmp = self.distance_to_player(origin, e.entity.hitbox)
            if dist_tmp < dist:
                dist = dist_tmp
                enemy = e
        return enemy

    def describe(self) -> str:
        """Returns a text description of the level."""
        text = f"#s#(30)#f#(item_titles_alt){self._name}\n"
        text += f"#s#(20)#c#(180,180,180)Area level: {self._area_level}\n\t\n\t\n"
        text += f"#s#(15){trad('descripts', 'difficulty')}:" +\
                f"{trad('difficulties', str(self._difficulty))}\n\t\n\t\n"
        for aff in self._modifiers:
            if aff is not None:
                text += f"#s#(17){aff.describe()}\n"
        return text

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
