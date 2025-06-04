"""Stores the project's constants."""

from enum import Enum
import json
import pygame
from pygame import *
from pygame.constants import *

ROOT = ""
#ROOT = "Gameuh.py/"
RESSOURCES = f"{ROOT}ressources"

SCREEN_WIDTH = 1920
SCREEN_HEIGHT = 1080
PROJECTILE_TRACKER = []
ENNEMY_TRACKER = []
TEXT_TRACKER = []
POWER_UP_TRACKER = []

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

def change_language(lang):
    """Changes the system's language.
    
    Args:
        lang (str): Name of the language. Must correspond\
        to a file in ressources/locales.
    """
    try:
        with open(f"{ROOT}/locales/{lang}.json", mode = 'r',\
                encoding="utf-8") as file:
            data = file.read()
            langfile = json.loads(data)
    except FileNotFoundError:
        print("File not found, language unchanged.")
        langfile = None
    return langfile

SYSTEM = {
    "font": None,
    "font_crit": None,
    "text_generator": None,
    "options": {
        "screen_width": 1280,
        "screen_height": 720,
        "resolutions": [(1138, 640), (1280, 720), (1600, 900), (1920, 1080)],
        "fullscreen": False,
        "vsync": False,
        "lang_selec": "EN-en",
        "lang": change_language("EN_us")
    },
    "game_state": None,
    "windows": None,
    "images": {
        "fireball": None,
        "energyball": None,
        "character": None
    },
    "spells": {

    }
}

WAVE_TIMER = USEREVENT+4
TICKER_TIMER = USEREVENT+5



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
    HELM = "helm"
    HANDS = "hands"
    ARMOR = "armor"
    BELT = "belt"
    BOOTS = "boots"
    WEAPON = "weapon"
    OFFHAND = "off_hand"
    RELIC = "relic"
    AMULET = "amulet"
    SPEED = "speed"
    CSPEED = "cast_speed"
    RING = "ring"
    ITEM = "items"
    GOLD = "gold"
    #Flags for projectiles
    PROJECTILE = "projectile"
    BOUNCE = "bounce"
    CURVE = "curve"
    ACCELERATE = "accelerate"
    DELAYED = "delayed"
    PIERCING = "piercing"
    #Flags for spells
    BARRAGE = "barrage"
    SPREAD = "spread"
    CHANNELED = "channeled"
    BUFF = "buff"
    DASH = "dash"
    #Flags for ennemies
    SHOOTER = "shooter"
    CHASER = "chaser"
