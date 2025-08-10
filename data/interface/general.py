"""Handles the general UI operations such as the bottom bar."""

from data.generator import Generator
from data.constants import SYSTEM, SCREEN_HEIGHT, POWER_UP_TRACKER, ENNEMY_TRACKER,\
    PROJECTILE_TRACKER, SLASH_TRACKER, TEXT_TRACKER, generate_grids, clean_grids, trad,\
    MENU_MAIN, MENU_GEAR, MENU_SPELLBOOK, MENU_TREE, MENU_INVENTORY, MENU_OPTIONS
from data.image.tabs import Tabs

def setup_bottom_bar():
    """Sets up the bottom bar."""
    values = [
        trad('buttons', 'map'),
        trad('buttons', 'gear'),
        trad('buttons', 'spells'),
        trad('buttons', 'tree'),
        trad('buttons', 'inventory'),
        trad('buttons', 'options')
    ]
    states = [
        MENU_MAIN,
        MENU_GEAR,
        MENU_SPELLBOOK,
        MENU_TREE,
        MENU_INVENTORY,
        MENU_OPTIONS
    ]
    SYSTEM["ui"]["bottom_bar"] = Tabs(10, SCREEN_HEIGHT - 64, values,\
                states, "game_state",\
                SYSTEM["images"]["btn"], SYSTEM["images"]["btn_p"], True,\
                SYSTEM["buttons"]["menu_states"])

def draw_bottom_bar(events):
    """Draws the bottom bar, quick access to the menus."""
    SYSTEM["ui"]["bottom_bar"].tick()

def draw_game(show_player = True, show_enemies = True,\
    show_loot = True, show_projectiles = True, show_slashes = True,\
    show_text = True):
    """Draws the main game component."""
    if show_player:
        SYSTEM["windows"].blit(SYSTEM["player"].get_image(), SYSTEM["player"].get_pos())
    if show_loot:
        SYSTEM["windows"].blits([b.get_image(), (b.x, b.y)] for b in POWER_UP_TRACKER)
    if show_enemies:
        SYSTEM["windows"].blits([b.get_image(), (b.x, b.y)] for b in ENNEMY_TRACKER)
    if show_projectiles:
        SYSTEM["windows"].blits([p.get_image(), p.get_pos()] for p in PROJECTILE_TRACKER)
    if show_slashes:
        SYSTEM["windows"].blits([s.get_image(), s.get_pos()] for s in SLASH_TRACKER)
    if show_text:
        SYSTEM["windows"].blits([t[0].image, (t[1], t[2])] for t in TEXT_TRACKER)

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
