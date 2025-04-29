"""Stores the project's constants."""

from enum import Enum
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
    BELT = "belt"
    BOOTS = "boots"
    WEAPON = "weapon"
    OFFHAND = "off_hand"
    RELIC = "relic"
    AMULET = "amulet"
    RING = "ring"
