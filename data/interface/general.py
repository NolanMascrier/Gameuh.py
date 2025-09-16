"""Handles the general UI operations such as the bottom bar."""

from data.generator import Generator
from data.constants import SYSTEM, SCREEN_HEIGHT, POWER_UP_TRACKER, ENNEMY_TRACKER,\
    PROJECTILE_TRACKER, TEXT_TRACKER, generate_grids, clean_grids, trad,\
    MENU_MAIN, MENU_GEAR, MENU_SPELLBOOK, MENU_TREE, MENU_INVENTORY, MENU_OPTIONS,\
    ANIMATION_TRACKER
from data.image.tabs import Tabs
from data.projectile import Projectile
from data.slash import Slash

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

def draw_bottom_bar():
    """Draws the bottom bar, quick access to the menus."""
    SYSTEM["ui"]["bottom_bar"].tick()

def draw_game(show_player = True, show_enemies = True,\
    show_loot = True, show_projectiles = True,\
    show_text = True, show_animations = True):
    """Draws the main game component."""
    for _, layer in SYSTEM["layers"].items():
        layer.fill((0,0,0,0))
    if show_player:
        SYSTEM["layers"]["characters"].blit(SYSTEM["player"].get_image(),\
            SYSTEM["player"].get_pos())
    if show_loot:
        SYSTEM["layers"]["pickup"].blits([b.get_image(), (b.x, b.y)] for b in POWER_UP_TRACKER)
    if show_enemies:
        SYSTEM["layers"]["characters"].blits([b.get_image(), (b.x, b.y)] for b in ENNEMY_TRACKER)
    if show_animations:
        SYSTEM["layers"]["characters"].blits([p[0].get_image(), (p[1], p[2])]\
                                             for p in ANIMATION_TRACKER)
    if show_projectiles:
        SYSTEM["layers"]["bullets"].blits([p.get_image(), p.get_pos()] for p in PROJECTILE_TRACKER)
    if show_text:
        SYSTEM["layers"]["pickup"].blits([t[0].image, (t[1], t[2])] for t in TEXT_TRACKER)

def logic_tick():
    """Ticks all there is to tick."""
    generate_grids()
    SYSTEM["player"].tick()
    for bubble in POWER_UP_TRACKER:
        bubble.tick(SYSTEM["player"])
        if bubble.flagged_for_deletion:
            POWER_UP_TRACKER.remove(bubble)
    for baddie in ENNEMY_TRACKER:
        baddie.tick(SYSTEM["player"])
        if baddie.destroyed:
            ENNEMY_TRACKER.remove(baddie)
    for p in ANIMATION_TRACKER:
        p[0].tick()
        if p[0].finished:
            ANIMATION_TRACKER.remove(p)
    for p in PROJECTILE_TRACKER:
        if isinstance(p, Generator):
            p.tick(SYSTEM["player"])
            continue
        p.tick()
        if (isinstance(p, Projectile) and p.can_be_destroyed()) or \
            (isinstance(p, Slash) and p.finished):
            PROJECTILE_TRACKER.remove(p)
    for txt in TEXT_TRACKER:
        sfc = txt[0]
        sfc.opacity(txt[3])
        txt[3] -= 5
        txt[2] -= 3
        if txt[3] < 10:
            TEXT_TRACKER.remove(txt)
    clean_grids()
