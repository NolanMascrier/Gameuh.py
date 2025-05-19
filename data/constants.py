"""Stores the project's constants."""

from enum import Enum
import json
import pygame
from pygame import *
from pygame.constants import *

SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 960
PROJECTILE_TRACKER = []
TEXT_TRACKER = []

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

def change_language(lang):
    """Changes the system's language.
    
    Args:
        lang (str): Name of the language. Must correspond\
        to a file in ressources/locales.
    """
    try:
        with open(f"{lang}.json", mode = 'r',\
                encoding="utf-8") as file:
            data = file.read()
            langfile = json.loads(data)
    except FileNotFoundError:
        print("File not found, language unchanged.")
        langfile = None
    return langfile

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
    MDEF = "mdef"
    PHYS = "phys"
    FIRE = "fire"
    ICE = "ice"
    ELEC = "elec"
    ENERG = "energy"
    LIGHT = "light"
    DARK = "dark"
    HELM = "helm"
    HANDS = "hands"
    ARMOR = "armor"
    BELT = "belt"
    BOOTS = "boots"
    WEAPON = "weapon"
    OFFHAND = "off_hand"
    RELIC = "relic"
    AMULET = "amulet"
    RING = "ring"
    #Flags for projectiles
    BOUNCE = "bounce"
    CURVE = "curve"
