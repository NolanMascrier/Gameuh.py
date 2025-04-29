"""Stores the project's constants."""

from enum import Enum
import json
import pygame
from pygame import *
from pygame.constants import *

SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 860
PROJECTILE_TRACKER = []

FIREBALL_IMAGE = "Gameuh.py/ressources/fire.png"
UI_JAUGE = "Gameuh.py/ressources/ui_main.png"
UI_JAUGE_L = "Gameuh.py/ressources/ui_life.png"
UI_JAUGE_M = "Gameuh.py/ressources/ui_mana.png"
UI_JAUGE_C = "Gameuh.py/ressources/ui_cd.png"
JAUGE_L = "Gameuh.py/ressources/life_jauge.png"
JAUGE_M = "Gameuh.py/ressources/mana_jauge.png"
JAUGE_C = "Gameuh.py/ressources/cd_jauge.png"

FONT = None

LANGUAGE_SELECTOR = "EN_us"
LANGUAGE = None

def change_language(lang):
    """Changes the system's language.
    
    Args:
        lang (str): Name of the language. Must correspond\
        to a file in ressources/locales.
    """
    global LANGUAGE
    try:
        with open(f"Gameuh.py/ressources/locales/{lang}.json", mode = 'r',\
                encoding="utf-8") as file:
            data = file.read()
            LANGUAGE = json.loads(data)
    except FileNotFoundError:
        print("File not found, language unchanged.")

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
