"""Stores the project's constants."""

from enum import Enum
import json
import pygame
from pygame import *
from pygame.constants import *
from data.physics.spatialgrid import SpatialGrid

ROOT = ""
#ROOT = "Gameuh.py/"
RESSOURCES = f"{ROOT}ressources"

SCREEN_WIDTH = 1920
SCREEN_HEIGHT = 1080

PROJECTILE_TRACKER = []
ENNEMY_TRACKER = []
SLASH_TRACKER = []
POWER_UP_TRACKER = []
TEXT_TRACKER = []
IMAGE_TRACKER = []

PROJECTILE_GRID = SpatialGrid()
ENNEMY_GRID = SpatialGrid()
SLASH_GRID = SpatialGrid()
POWER_UP_GRID = SpatialGrid()

def clean_grids():
    """Cleans up all the grids."""
    PROJECTILE_GRID.clear()
    ENNEMY_GRID.clear()
    SLASH_GRID.clear()
    POWER_UP_GRID.clear()

def generate_grids():
    """Fills up the grids."""
    for p in PROJECTILE_TRACKER:
        PROJECTILE_GRID.add(p, p.hitbox)
    for e in ENNEMY_TRACKER:
        ENNEMY_GRID.add(e, e.hitbox)
    for s in SLASH_TRACKER:
        SLASH_GRID.add(s, s.hitbox)
    for p in POWER_UP_TRACKER:
        POWER_UP_GRID.add(p, p.hitbox)

FIREBALL_IMAGE = "ressources/fire.png"
UI_JAUGE = "ressources/ui_main.png"
UI_JAUGE_L = "ressources/ui_life.png"
UI_JAUGE_M = "ressources/ui_mana.png"
UI_JAUGE_C = "ressources/ui_cd.png"
JAUGE_L = "ressources/life_jauge.png"
JAUGE_M = "ressources/mana_jauge.png"
JAUGE_C = "ressources/cd_jauge.png"
JAUGE_BOSS_BACK = "ressources/life_boss_back.png"
JAUGE_BOSS = "ressources/life_boss.png"

FONT = None

LANGUAGE = None

#Game states
MENU_MAIN = 0
MENU_OPTIONS = 1
MENU_START = 2
MENU_LOAD = 3
MENU_SAVE = 4
GAME_LEVEL = 5
GAME_MAP = 6
GAME_SHOP = 7
GAME_INVENTORY = 8
GAME_EQUIP = 9
GAME_PAUSE = 10
GAME_VICTORY = 11
GAME_DEATH = 111
MENU_GEAR = 12
MENU_INVENTORY = 13
MENU_SPELLBOOK = 131
MENU_SPELLBOOK_Q = 1311
MENU_SPELLBOOK_E = 1312
MENU_SPELLBOOK_F = 1313
MENU_SPELLBOOK_R = 1314
MENU_SPELLBOOK_T = 1315
MENU_SPELLBOOK_SHIFT = 1316
MENU_OPTIONS_GAME = 14
MENU_TREE = 15
LOADING = 999

SYSTEM = {
    "loaded": False,
    "progress": 0,
    "playing": True,
    "font": None,
    "font_crit": None,
    "text_generator": None,
    "options": {
        "screen_width": 1920,
        "screen_height": 1080,
        "fps": 0.016,
        "fps_selector": (0, 0.008, 0.016, 0.032),
        "resolutions": [(1138, 640), (1280, 720), (1366, 768), (1600, 900), (1920, 1080)],
        "fullscreen": True,
        "vsync": 1,
        "lang_selec": "EN_us",
        "langs": ["EN_us", "FR_fr"],
        "show_hitboxes": False
    },
    "lang": [],
    "game_state": None,
    "windows": None,
    "images": {
        "fireball": None,
        "energyball": None,
        "character": None
    },
    "spells": {

    },
    "buttons": {
        "tab_e": None,
        "tab_r": None,
    },
    "ui": {},
    "player": None,
    "level": None,
    "selected": None,
    "dragged": None,
    "pop-up": None
}

def factor() -> int:
    """Returns the resolution factor"""
    x = SYSTEM["options"]["screen_width"] / SCREEN_WIDTH
    y = SYSTEM["options"]["screen_height"] / SCREEN_HEIGHT
    return x, y

def get_mouse_pos():
    """Updates the mouse position."""
    x_factor = SCREEN_WIDTH / SYSTEM["options"]["screen_width"]
    y_factor = SCREEN_HEIGHT / SYSTEM["options"]["screen_height"]
    x, y = pygame.mouse.get_pos()
    x *= x_factor
    y *= y_factor
    SYSTEM["mouse"] = (x, y)

def trad(keys, subkey = None):
    """Returns the translation data for the given key."""
    try:
        if subkey is None:
            return SYSTEM["lang"][keys]
        else:
            return SYSTEM["lang"][keys][subkey]
    except KeyError:
        return ["Unknown text data."]

WAVE_TIMER = USEREVENT+4
TICKER_TIMER = USEREVENT+5
UPDATE_TIMER = USEREVENT+6

def change_language(lang):
    """Changes the system's language.
    
    Args:
        lang (str): Name of the language. Must correspond\
        to a file in ressources/locales.
    """
    try:
        with open(f"{RESSOURCES}/locales/{lang}.json", mode = 'r',\
                encoding="utf-8") as file:
            data = file.read()
            SYSTEM["lang"] = json.loads(data)
    except FileNotFoundError:
        print("File not found, language unchanged.")
        SYSTEM["lang"] = None

change_language("EN_us")

class Flags(Enum):
    """Flags to use for skills and damage sources."""
    HOT = "heal_over_time"
    DOT = "damage_over_time"
    MHOT = "multiplicative_heal_over_time"
    MDOT = "multiplicative_damage_over_time"
    MANA = "mana"
    LIFE = "life"
    STUN = "stun"
    GEAR = "gear"
    CONSUMABLE = "consumable"
    FLAT = "flat" #flat stat bonus
    HEX = "hex" #additive malus
    BOON = "boon" #additive bonus
    CURSE = "curse" #multiplictive malus
    BLESS = "blessing" #multiplicative bonus
    STR = "str"
    DEX = "dex"
    INT = "int"
    DEF = "def"
    PHYS = "phys"
    FIRE = "fire"
    ICE = "ice"
    ELEC = "elec"
    ENERG = "energy"
    LIGHT = "light"
    DARK = "dark"
    CRIT_CHANCE = "crit_rate"
    CRIT_DAMAGE = "crit_dmg"
    PHYS_FLAT = "phys_flat"
    FIRE_FLAT = "fire_flat"
    ICE_FLAT = "ice_flat"
    ELEC_FLAT = "elec_flat"
    ENERG_FLAT = "energy_flat"
    LIGHT_FLAT = "light_flat"
    DARK_FLAT = "dark_flat"
    PHYS_DMG = "phys_dmg"
    FIRE_DMG = "fire_dmg"
    ICE_DMG = "ice_dmg"
    ELEC_DMG = "elec_dmg"
    ENERG_DMG = "energy_dmg"
    LIGHT_DMG = "light_dmg"
    DARK_DMG = "dark_dmg"
    PHYS_PEN = "phys_pen"
    FIRE_PEN = "fire_pen"
    ICE_PEN = "ice_pen"
    ELEC_PEN = "elec_pen"
    ENERG_PEN = "energy_pen"
    LIGHT_PEN = "light_pen"
    DARK_PEN = "dark_pen"
    SPELL = "spell_dmg"
    MELEE = "melee_dmg"
    RANGED = "ranged_dmg"
    PRECISION = "precision"
    BLOCK = "block"
    DODGE_RATING = "dodge_rating"
    DODGE = "dodge"
    ABS_DEF = "abs_def"
    PIERCE_BLOCK = "cant_be_blocked"
    PIERCE_DODGE = "cant_be_dodged"
    ALL_DAMAGE = "all_damage"
    ALL_RESISTANCES = "all_resistances"
    ELEMENTAL_DAMAGE = "elemental_damage"
    ELEMENTAL_RESISTANCES = "elemental_resistances"
    MANA_REGEN = "mana_regen"
    LIFE_REGEN = "life_regen"
    ARMOR_MOM = "armor_mind_over_matter"
    HEAL_EFFICIENCY = "heal_factor"
    MANAL_EFFICIENCY = "mana_efficiency"
    CRIT_RES = "crit_res"
    HELM = "helms"
    HANDS = "gloves"
    ARMOR = "armors"
    BELT = "belts"
    BOOTS = "boots"
    WEAPON = "weapons"
    OFFHAND = "offhands"
    RELIC = "relics"
    AMULET = "amulets"
    SPEED = "speed"
    CSPEED = "cast_speed"
    RING = "rings"
    ITEM = "items"
    GOLD = "gold"
    EXPERIENCE = "exp"
    #Flags for projectiles
    PROJECTILE = "projectile"
    BOUNCE = "bounce"
    CURVE = "curve"
    ACCELERATE = "accelerate"
    DELAYED = "delayed"
    PIERCING = "piercing"
    TRACK_STRICT = "tracking_strict"
    TRACK_LOOSE = "tracking_loose"
    AIMED_AT_PLAYER = "aimed_at_player"
    AIMED_AT_MOUSE = "aimed_at_mouse"
    #Flags for spells
    BARRAGE = "barrage"
    SPREAD = "spread"
    CHANNELED = "channeled"
    BUFF = "buff"
    DEBUFF = "debuff"
    DASH = "dash"
    #Flags for slashes
    CUTS_PROJECTILE = "cuts_proj"
    #Flags for ennemies
    SHOOTER = "shooter"
    CHASER = "chaser"
    #Flags for levels
    WAVES = "waves"
    DUNGEON = "dungeon"
    RAID = "raid"
    HAS_BOSS = "has_boss"
    #Flags for description
    DESC_FLAT = "description_flat_attribute"
    DESC_PERCENT = "force_percentage_in_desc"
    DESC_UNIQUE = "desc_unique_effect"

META_FLAGS = [Flags.DESC_FLAT, Flags.DESC_PERCENT, Flags.DESC_UNIQUE,\
                Flags.BOON, Flags.HEX, Flags.BLESS, Flags.CURSE, Flags.FLAT]
GEAR_FLAGS = [Flags.HELM, Flags.BOOTS, Flags.ARMOR, Flags.HANDS, Flags.BELT,\
                Flags.RING, Flags.AMULET, Flags.RELIC, Flags.AMULET]
