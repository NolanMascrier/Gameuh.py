import pygame
from pygame import *
from time import sleep
from math import cos, sin, radians
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