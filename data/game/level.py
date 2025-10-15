"""Class that defines a level.
A level can be of multiple type:
Waves, dungeon ...
Only waves for now."""

import time
import threading
import random

import numpy as np

from data.api.surface import Surface

from data.creature import Creature
from data.constants import ENNEMY_TRACKER, SCREEN_WIDTH, SCREEN_HEIGHT, WAVE_TIMER, SYSTEM,\
    trad, LOADING, GAME_LEVEL, USEREVENT, TICKER_TIMER, UPDATE_TIMER,\
    PROJECTILE_TRACKER, POWER_UP_TRACKER, ANIMATION_TRACKER
from data.game.enemy import Enemy
from data.game.enemy_monolith import Monolith
from data.physics.entity import Entity
from data.physics.hitbox import HitBox
from data.image.animation import Animation, Image
from data.image.parallaxe import Parallaxe
from data.numerics.affix import Affix
from data.image.text import Text
from data.item import Item
from data.tables.area_table import MODIFIERS
from data.tables.enemy_table import *
from data.interface.endlevel import generate_victory, generate_defeat

RUNE_ORDER = [0, 7, 9, 8, 6, 1, 2, 3, 5, 4]

RED = (255,0,0)

RUNES = {
    0: "blank",
    1: "thurisaz",
    2: "ansuz",
    3: "ingwaz",
    4: "othalan",
    5: "uruz",
    6: "raido",
    7: "tiwaz",
    8: "eihwaz",
    9: "algiz",
}

def init_timers():
    """Inits Pygame's timers."""
    SYSTEM["deltatime"].start(WAVE_TIMER, 1500)
    SYSTEM["deltatime"].start(USEREVENT+1, 2000)
    SYSTEM["deltatime"].start(USEREVENT+2, 100)
    SYSTEM["deltatime"].start(TICKER_TIMER, int(0.016 * 1000))
    SYSTEM["deltatime"].start(UPDATE_TIMER, int(SYSTEM["options"]["fps"]))

class DummyItems(Item):
    """Fake items to show in the showcase at the end of a level."""
    def __init__(self, name, image = None, quantity = 1, stolen = 0, rarity = 0):
        self._amount = quantity
        self._stolen = stolen
        super().__init__(name, "", 0, image=image, rarity=rarity)
        if stolen == 0:
            self._quantity = Text(f"{quantity}" if quantity <= 999 else "999+", font="item_desc")
        else:
            self._quantity = Text(f"{quantity - stolen}" if quantity <= 999 else "999+",\
                                  font="item_desc", default_color=RED)
        self._img = Surface(64, 64)
        self._img.blit(self._image.image, (0, 0), True)
        if quantity > 1:
            self._img.blit(self._quantity.image, (0, 0), True)
        self._img = Image(self._img)
        self._image = self._img

    def create_popup(self, _ = False):
        """Creates the detailed popup surface."""
        if self._image is None:
            return None
        if self._stolen == 0:
            txt = "\n".join(trad('runes', self._name)) + "\n"\
                + trad('descripts', 'amount') + f"{self._amount}"
        else:
            txt = "\n".join(trad('runes', self._name)) + "\n"\
                + trad('descripts', 'amount') + f"{self._amount - self._stolen}"\
                + f"({trad('descripts', 'stolen')}: #c#(255,0,0){self._stolen}#c#(255,255,255))"
        desc = Text(txt.format(rarity=trad('rarities', self._rarity)), font="item_desc")
        title_card = SYSTEM["images"]["item_desc"]\
                    .duplicate(desc.width, desc.height)
        sfc = Surface(title_card.get_width(), title_card.get_height())
        title_pos = (title_card.get_width() / 2 - desc.width / 2,
                     title_card.get_height() / 2 - desc.height / 2)
        sfc.blit(title_card, (0, 0), True)
        sfc.blit(desc.surface, title_pos, True)
        return sfc

    def get_image(self):
        """returns the item's image."""
        return self._img

class Level():
    """A level."""
    def __init__(self, name: str, area_lvl:int, icon: Animation,\
                    wave_timer = 5000,\
                    background: Animation|Parallaxe|None = None,\
                    waves: int = 5, difficulty = 0,\
                    flags = None, boss = None):
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
        self._exp = 0
        self._boss = boss
        self._loot = []
        self._wave_tracker = []
        self._runes = [
            0, 0, 0, 0, 0, 0, 0, 0, 0, 0
        ]
        self._modifiers = self.generate_modifiers()
        self._t = time.time()
        self._boss_stat = None

    def generate_modifiers(self):
        """Generates a list of modifiers for the level."""
        mods_by_diff = {1: 2, 2: 3, 3: 4, 0: 0, 4:6}
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
        monsters = max(random.randint(min_monsters, max_monsters + 1), 1) + 4
        choice = [VOIDBOMBER, DEMONBAT, NECROMANCER]
        chance = [0.1, 0.4, 0.5]
        wave = []
        for _ in range(monsters):
            monster = np.random.choice(choice, p=chance)
            mob = self.generate_enemy(monster, level)
            wave.append(mob)
        self._wave_tracker.append(wave)

    def summon_boss(self, level:int, _):
        """Summons the boss."""
        if self._boss is None:
            return []
        boss = self.generate_enemy(self._boss, level)
        wave = [boss]
        self._boss_stat = boss.creature
        self._wave_tracker.append(wave)
        return wave

    def summon_pinnacle(self, level: int, _):
        """Summons a pinnacle boss."""
        wave = []
        if Flags.MONOLITH in self._flags:
            y_pos = 340
            x_pos = SCREEN_WIDTH
            enemy_type = self._boss["flags"]
            img = self._boss["image"]
            ent = Entity(SCREEN_WIDTH + 200, y_pos, img, hitbox_mod=self._boss["hitbox"])
            exp_value = random.randint(int(self._boss["exp"]*(level + 1) *0.9),\
                                    int(self._boss["exp"]*(level + 1) * 1.1))
            gold_value = random.randint(int(self._boss["gold"]*(level + 1) *0.9),\
                                        int(self._boss["gold"]*(level + 1) * 1.1))
            attack_delay = self._boss["delay"]
            crea = Creature(self._boss["name"])
            crea.import_stackblock(self._boss["stats"])
            for mod in self._modifiers:
                crea.afflict(mod.as_affliction())
            crea.scale(level)
            crea.reset()
            dest = (SCREEN_WIDTH - x_pos, y_pos)
            enemy = Monolith(ent, crea, self._boss["spelllist"], behaviours=enemy_type,\
                timer=2, exp_value=exp_value, gold_value=gold_value, delay=attack_delay,\
                destination=dest)
            wave = [enemy]
        self._wave_tracker.append(wave)
        return wave

    def load_simple_level(self):
        """Loads a basic level."""
        tasks = [(self.summon_wave, i, 1) for i in range(self._waves)]
        if self._boss is not None:
            self._waves += 1
            tasks.append((self.summon_boss, 1, 1))
        total = sum(weight for _, _, weight in tasks)
        SYSTEM["progress"] = 0
        return total, tasks

    def load_pinnacle(self):
        """Loads a basic level."""
        tasks = [(self.summon_pinnacle, 1, 1)]
        total = sum(weight for _, _, weight in tasks)
        SYSTEM["progress"] = 0
        return total, tasks

    def load_level(self):
        """Loading function of the level."""
        SYSTEM["game_state"] = LOADING
        progress = 0
        if Flags.PINNACLE in self._flags:
            total, tasks = self.load_pinnacle()
        else:
            total, tasks = self.load_simple_level()
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
        SYSTEM["deltatime"].clear()
        SYSTEM["deltatime"].start(WAVE_TIMER, self._wave_timer)
        for e in self._wave_tracker[self._current_wave]:
            ENNEMY_TRACKER.append(e)
        if Flags.MONOLITH in self._flags:
            SYSTEM["post_effects"].shake(50, 0, 500)
        self._wave_tracker[self._current_wave].clear()
        self._current_wave += 1

    def end_level(self):
        """End level sequence. Sets the needed flag and creates the dummy items."""
        for pick in POWER_UP_TRACKER:
            pick.pickup(SYSTEM["player"])
        self._finished = True
        SYSTEM["player"].gold += self._gold
        gold = DummyItems("gold", SYSTEM["images"]["gold_icon"], self._gold)
        self._loot.insert(0, gold)
        exp = DummyItems("exp", SYSTEM["images"]["exp_orb_big"], self._exp)
        self._loot.insert(1, exp)
        pos = 2
        for i in RUNE_ORDER:
            if self._runes[i] > 0:
                rune = DummyItems(RUNES[i], SYSTEM["images"][f"rune_{i}"], self._runes[i])
                self._loot.insert(pos, rune)
                pos += 1
        generate_victory()
        SYSTEM["deltatime"].stop(WAVE_TIMER)

    def fail_level(self):
        """Game over sequence. Removes half the gold gained, 10% of the player's current exp,
        and a random amount of items."""
        self._finished = True
        failure = int(len(self._loot) * np.random.random())
        loss = np.random.choice(len(self._loot), size=failure, replace=False).tolist()
        for i in loss:
            it = self._loot[i]
            if it in SYSTEM["player"].inventory:
                SYSTEM["player"].inventory.remove(it)
            fake = DummyItems("stolen", SYSTEM["images"]["loss"], rarity=it.rarity)
            self._loot[i] = fake
        gold = DummyItems("gold", SYSTEM["images"]["gold_icon"], self._gold, int(self._gold / 2))
        self._loot.insert(0, gold)
        exp_loss = int(SYSTEM["player"].creature.exp_to_next / 10)
        SYSTEM["player"].creature.exp -= exp_loss
        exp = DummyItems("exp", SYSTEM["images"]["exp_orb_big"], self._exp, exp_loss)
        self._loot.insert(1, exp)
        pos = 2
        runes_loss = [
            0, 0, 0, 0, 0, 0, 0, 0, 0, 0
        ]
        for i in RUNE_ORDER:
            if self._runes[i] > 0:
                runes_loss[i] = np.random.randint(0, self._runes[i] + 1)
                SYSTEM["player"].runes[i] -= runes_loss[i]
                if runes_loss[i] == self._runes[i]:
                    rune = DummyItems("stolen_rune", SYSTEM["images"]["loss"])
                else:
                    rune = DummyItems(RUNES[i], SYSTEM["images"][f"rune_{i}"],\
                                        self._runes[i], runes_loss[i])
                self._loot.insert(pos, rune)
                pos += 1
        SYSTEM["player"].gold += self._gold / 2
        generate_defeat()
        SYSTEM["deltatime"].stop(WAVE_TIMER)

    def next_wave(self):
        """Summons the next wave."""
        if not self._started:
            self._started = True
            self.start()
            return
        if self._current_wave >= self._waves:
            if len(ENNEMY_TRACKER) <= 0:
                self.end_level()
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
        if self._boss is not None:
            text += f"#s#(17){trad('meta_words', 'boss')}\n"
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
        """Returns the level's current wave."""
        return self._current_wave

    @current_wave.setter
    def current_wave(self, value):
        self._current_wave = value

    @property
    def waves(self):
        """Returns the level's amount of wave."""
        return self._waves

    @waves.setter
    def waves(self, value):
        self._waves = value

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

    @property
    def exp(self):
        """Returns the exp gained during this level."""
        return self._exp

    @exp.setter
    def exp(self, value):
        self._exp = value

    @property
    def runes(self):
        """Returns the runes gained during this level."""
        return self._runes

    @runes.setter
    def runes(self, value):
        self._runes = value

    @property
    def boss(self):
        """Returns the boss' stats."""
        return self._boss_stat

    @boss.setter
    def boss(self, value):
        self._boss_stat = value
