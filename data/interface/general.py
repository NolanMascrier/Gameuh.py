"""Handles the general UI operations such as the bottom bar."""

import pygame
from data.generator import Generator
from data.constants import SYSTEM, SCREEN_HEIGHT, POWER_UP_TRACKER, ENNEMY_TRACKER,\
    PROJECTILE_TRACKER, SLASH_TRACKER, TEXT_TRACKER, generate_grids, clean_grids

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

def draw_game(show_player = True, show_enemies = True,\
    show_loot = True, show_projectiles = True, show_slashes = True,\
    show_text = True):
    """Draws the main game component."""
    if show_player:
        SYSTEM["windows"].blit(SYSTEM["player"].get_image(), SYSTEM["player"].get_pos())
    if show_loot:
        for bubble in POWER_UP_TRACKER:
            SYSTEM["windows"].blit(bubble.get_image(), (bubble.x, bubble.y))
    if show_enemies:
        for baddie in ENNEMY_TRACKER:
            SYSTEM["windows"].blit(baddie.get_image(), (baddie.x, baddie.y))
    if show_projectiles:
        for p in PROJECTILE_TRACKER:
            SYSTEM["windows"].blit(p.get_image(), p.get_pos())
    if show_slashes:
        for s in SLASH_TRACKER:
            SYSTEM["windows"].blit(s.get_image(), s.get_pos())
    if show_text:
        for txt in TEXT_TRACKER:
            SYSTEM["windows"].blit(txt[0].image, (txt[1], txt[2]))

def tick():
    """Ticks all there is to tick."""
    generate_grids()
    SYSTEM["player"].tick()
    for bubble in POWER_UP_TRACKER.copy():
        bubble.tick(SYSTEM["player"])
        if bubble.flagged_for_deletion:
            POWER_UP_TRACKER.remove(bubble)
    for baddie in ENNEMY_TRACKER.copy():
        baddie.tick(SYSTEM["player"])
        if baddie.destroyed:
            ENNEMY_TRACKER.remove(baddie)
    for p in PROJECTILE_TRACKER.copy():
        if isinstance(p, Generator):
            p.tick(SYSTEM["player"])
            continue
        p.tick()
        if p.can_be_destroyed():
            PROJECTILE_TRACKER.remove(p)
    for s in SLASH_TRACKER.copy():
        s.tick()
        if s.finished:
            SLASH_TRACKER.remove(s)
    for txt in TEXT_TRACKER.copy():
        sfc = txt[0]
        sfc.opacity(txt[3])
        txt[3] -= 5
        txt[2] -= 3
        if txt[3] < 10:
            TEXT_TRACKER.remove(txt)
    clean_grids()
