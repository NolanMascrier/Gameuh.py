"""Handles the general UI operations such as the bottom bar."""

import pygame
from data.constants import SYSTEM, SCREEN_HEIGHT

def draw_bottom_bar(events):
    """Draws the bottom bar, quick access to the menus."""
    SYSTEM["images"]["button_map"].set(10, SCREEN_HEIGHT - 64)
    SYSTEM["images"]["button_map"].draw(SYSTEM["windows"])
    SYSTEM["images"]["button_gear"].set(300, SCREEN_HEIGHT - 64)
    SYSTEM["images"]["button_gear"].draw(SYSTEM["windows"])
    SYSTEM["images"]["button_spells"].set(590, SCREEN_HEIGHT - 64)
    SYSTEM["images"]["button_spells"].draw(SYSTEM["windows"])
    SYSTEM["images"]["button_tree"].set(880, SCREEN_HEIGHT - 64)
    SYSTEM["images"]["button_tree"].draw(SYSTEM["windows"])
    SYSTEM["images"]["button_inventory"].set(1170, SCREEN_HEIGHT - 64)
    SYSTEM["images"]["button_inventory"].draw(SYSTEM["windows"])
    SYSTEM["images"]["button_options"].set(1460, SCREEN_HEIGHT - 64)
    SYSTEM["images"]["button_options"].draw(SYSTEM["windows"])
    for event in events:
        if event.type == pygame.MOUSEBUTTONDOWN:
            SYSTEM["images"]["button_map"].press()
            SYSTEM["images"]["button_gear"].press()
            SYSTEM["images"]["button_tree"].press()
            SYSTEM["images"]["button_inventory"].press()
            SYSTEM["images"]["button_options"].press()
            SYSTEM["images"]["button_spells"].press()