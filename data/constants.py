import pygame
from pygame import *
from time import sleep
from math import cos, sin, radians
from pygame.constants import *
from enum import Enum

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

def Flags(Enum):
    HOT = "heal_over_time",
    DOT = "damage_over_time",
    MHOT = "multiplicative_heal_over_time",
    MDOT = "multiplicative_damage_over_time",
    MANA = "mana",
    LIFE = "life",
    STUN = "stun",
    GEAR = "gear",
    HEX = "hex", #additive malus
    BOON = "boon", #additive bonus
    CURSE = "curse", #multiplictive malus
    BLESS = "blessing", #multiplicative bonus
    STR = "strength",
    DEX = "dexterity",
    INT = "intelligence",
    DEF = "defense",
    MDEF = "magic_defense",
    PHYS = "physic_damage",
    FIRE = "fire_damage",
    ICE = "ice_damage",
    ELEC = "elec_damage",
    ENERG = "energ_damage",
    LIGHT = "light_damage",
    DARK = "dark_damage",