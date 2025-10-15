"""Handles the general UI operations such as the bottom bar."""

from functools import lru_cache

from data.constants import SYSTEM, SCREEN_HEIGHT, POWER_UP_TRACKER, ENNEMY_TRACKER,\
    PROJECTILE_TRACKER, TEXT_TRACKER, trad,\
    MENU_MAIN, MENU_GEAR, MENU_SPELLBOOK, MENU_TREE, MENU_INVENTORY, MENU_OPTIONS,\
    ANIMATION_TRACKER
from data.image.tabs import Tabs
from data.physics.hitbox import HitBox

RED = (255, 0, 0, 155)
GRE = (0, 255, 0, 155)
BLU = (0, 0, 255, 155)
RED_B = (255, 0, 0, 255)
GRE_B = (0, 255, 0, 255)
BLU_B = (0, 0, 255, 255)
RED_WARNING = [255, 0, 0, 185]

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

def draw_hitbox(hitbox: HitBox, color, color_border, layer):
    """Draws the hitbox."""
    layer.draw_rect(color, (hitbox.x, hitbox.y, hitbox.width, hitbox.height))
    layer.draw_rect(color_border, (hitbox.x, hitbox.y, hitbox.width, hitbox.height), 2)
    layer.draw_rect(color_border, (hitbox.x + hitbox.width / 2 - 2,
                    hitbox.y + hitbox.height /2 - 2 , 4, 4), 2)

@lru_cache(maxsize=64)
def enemy_life(life):
    """Returns the enemy life bar (cached)"""
    return SYSTEM["images"]["enemy_jauge_mini"].image.subsurface((0, 0, life, 20))

def draw_game(show_player = True, show_enemies = True,\
    show_loot = True, show_projectiles = True,\
    show_text = True, show_animations = True):
    """Draws the main game component - OPTIMIZED VERSION."""
    if show_player or show_enemies or show_animations:
        SYSTEM["layers"]["characters"].fill((0,0,0,0))
    if show_loot:
        SYSTEM["layers"]["pickup"].fill((0,0,0,0))
    if show_projectiles:
        SYSTEM["layers"]["bullets"].fill((0,0,0,0))
        SYSTEM["layers"]["warnings"].fill((0,0,0,0))
    if show_text:
        SYSTEM["layers"]["texts"].fill((0,0,0,0))
    if show_player:
        if SYSTEM["options"]["show_hitboxes"]:
            draw_hitbox(SYSTEM["player"].entity.hitbox, GRE, GRE_B, SYSTEM["layers"]["characters"])
        SYSTEM["layers"]["characters"].blit(SYSTEM["player"].get_image(),\
            SYSTEM["player"].get_pos())
    if show_loot:
        if SYSTEM["options"]["show_hitboxes"]:
            for b in POWER_UP_TRACKER:
                draw_hitbox(b.hitbox, BLU, BLU_B, SYSTEM["layers"]["pickup"])
        loot_blits = [(b.get_image(), (b.x, b.y)) for b in POWER_UP_TRACKER]
        if loot_blits:
            SYSTEM["layers"]["pickup"].blits(loot_blits)
    if show_enemies:
        if SYSTEM["options"]["show_hitboxes"]:
            for b in ENNEMY_TRACKER:
                draw_hitbox(b.hitbox, RED, RED_B, SYSTEM["layers"]["characters"])
        if SYSTEM["options"]["show_bars"]:
            enemy_bars = []
            for b in ENNEMY_TRACKER:
                bar_x = b.entity.center_x - SYSTEM["images"]["enemy_jauge_mini_back"].width / 2
                bar_y = b.y - 25
                enemy_bars.append((SYSTEM["images"]["enemy_jauge_mini_back"].image, (bar_x, bar_y)))
                life = max(b.creature.stats["life"].current_value /\
                    b.creature.stats["life"].c_value * 100, 0)
                enemy_bars.append((enemy_life(life), (bar_x, bar_y)))
            if enemy_bars:
                SYSTEM["layers"]["characters"].blits(enemy_bars)
        enemy_blits = [(b.get_image(), b.get_pos()) for b in ENNEMY_TRACKER]
        if enemy_blits:
            SYSTEM["layers"]["characters"].blits(enemy_blits)
    if show_animations:
        anim_blits = [(p[0].get_image(), (p[1], p[2])) for p in ANIMATION_TRACKER]
        if anim_blits:
            SYSTEM["layers"]["characters"].blits(anim_blits)
    if show_projectiles:
        if SYSTEM["options"]["show_hitboxes"]:
            for b in PROJECTILE_TRACKER:
                if b.effective:
                    draw_hitbox(b.hitbox, BLU, BLU_B, SYSTEM["layers"]["bullets"])
        for p in PROJECTILE_TRACKER:
            if p.warning is not None:
                SYSTEM["layers"]["warnings"].draw_polygon(RED_WARNING, p.warning[0])
        proj_blits = [(p.get_image(), p.get_pos()) for p in PROJECTILE_TRACKER]
        if proj_blits:
            SYSTEM["layers"]["bullets"].blits(proj_blits)
    if show_text:
        text_blits = [(t[0].image, (t[1], t[2])) for t in TEXT_TRACKER]
        if text_blits:
            SYSTEM["layers"]["texts"].blits(text_blits)

def logic_tick():
    """Ticks all there is to tick."""
    SYSTEM["player"].tick()
    POWER_UP_TRACKER[:] = [b for b in POWER_UP_TRACKER if b.tick(SYSTEM["player"]) is None and
                           not b.flagged_for_deletion]
    ENNEMY_TRACKER[:] = [e for e in ENNEMY_TRACKER 
                         if e.tick(SYSTEM["player"]) is None and not e.destroyed]
    ANIMATION_TRACKER[:] = [a for a in ANIMATION_TRACKER if a[0].tick() is None
                            and not a[0].finished]
    PROJECTILE_TRACKER[:] = [p for p in PROJECTILE_TRACKER if p.tick() is None and not p.finished]
    for txt in TEXT_TRACKER:
        sfc = txt[0]
        sfc.opacity(txt[3])
        txt[3] -= 5
        txt[2] -= 3
    TEXT_TRACKER[:] = [txt for txt in TEXT_TRACKER if txt[3] >= 10
                       and txt[0].opacity(txt[3]) is None]
