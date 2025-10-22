"""Handles the general UI operations such as the bottom bar"""

from functools import lru_cache

from data.api.surface import Surface

from data.constants import SYSTEM, SCREEN_HEIGHT, POWER_UP_TRACKER, ENNEMY_TRACKER,\
    PROJECTILE_TRACKER, TEXT_TRACKER, trad,\
    MENU_MAIN, MENU_GEAR, MENU_SPELLBOOK, MENU_TREE, MENU_INVENTORY, MENU_OPTIONS,\
    ANIMATION_TRACKER, SCREEN_WIDTH
from data.image.tabs import Tabs
from data.physics.hitbox import HitBox
from data.projectile import Projectile
from data.slash import Slash

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

@lru_cache(maxsize=256)
def draw_hitbox(hitbox, color, color_border):
    """Draws the hitbox."""
    sfc = Surface(hitbox[2], hitbox[3])
    sfc.draw_rect(color, (0, 0, hitbox[2], hitbox[3]))
    sfc.draw_rect(color_border, (0, 0, hitbox[2], hitbox[3]), 2)
    sfc.draw_rect(color_border, (0 + hitbox[2] / 2 - 2,
                    0 + hitbox[3] /2 - 2 , 4, 4), 2)
    return (sfc, (hitbox[0], hitbox[1]))

def draw_warning(polygon, color, alpha = 255):
    """Draws the hitbox."""
    SYSTEM["warnings"].draw_polygon(color, polygon)

@lru_cache(maxsize=64)
def enemy_life(life):
    """Returns the enemy life bar (cached)"""
    return SYSTEM["images"]["enemy_jauge_mini"].image.subsurface((0, 0, life, 20))

def draw_game(show_player = True, show_enemies = True,\
    show_loot = True, show_projectiles = True,\
    show_text = True, show_animations = True):
    """Draws the main game component - HIGHLY OPTIMIZED VERSION."""
    show_hitboxes = SYSTEM["options"]["show_hitboxes"]
    show_bars = SYSTEM["options"]["show_bars"]
    if show_player or show_enemies or show_animations:
        chars_layer = SYSTEM["layers"]["characters"]
        chars_layer.clear()
    if show_loot:
        pickup_layer = SYSTEM["layers"]["pickup"]
        pickup_layer.clear()
    if show_projectiles:
        bullets_layer = SYSTEM["layers"]["bullets"]
        warnings_layer = SYSTEM["layers"]["warnings"]
        bullets_layer.clear()
        warnings_layer.clear()
    if show_text:
        texts_layer = SYSTEM["layers"]["texts"]
        texts_layer.clear()
    if show_player:
        if show_hitboxes:
            chars_layer.append(draw_hitbox(SYSTEM["player"].entity.hitbox.get_rect(), GRE, GRE_B))
        chars_layer.append((SYSTEM["player"].get_image(), SYSTEM["player"].get_pos()))
    if show_loot:
        loot_count = len(POWER_UP_TRACKER)
        if loot_count > 0:
            if show_hitboxes:
                for b in POWER_UP_TRACKER:
                    pickup_layer.append(draw_hitbox(b.hitbox.get_rect(), BLU, BLU_B))
            loot_blits = [(b.get_image(), (b.x, b.y)) for b in POWER_UP_TRACKER]
            if loot_blits:
                pickup_layer.extend(loot_blits)
    if show_enemies:
        enemy_count = len(ENNEMY_TRACKER)
        if enemy_count > 0:
            if show_hitboxes:
                for b in ENNEMY_TRACKER:
                    chars_layer.append(draw_hitbox(b.hitbox.get_rect(), RED, RED_B))
            enemy_blits = []
            if show_bars:
                enemy_jauge_back = SYSTEM["images"]["enemy_jauge_mini_back"].image
                for b in ENNEMY_TRACKER:
                    bar_x = b.entity.center_x - 50
                    bar_y = b.y - 25
                    enemy_blits.append((enemy_jauge_back, (bar_x, bar_y)))
                    life_pct = b.creature.stats["life"].current_value / \
                        b.creature.stats["life"].c_value
                    life_width = max(int(life_pct * 100), 0)
                    if life_width > 0:
                        life_bar = SYSTEM["images"]["enemy_jauge_mini"].image\
                            .subsurface((0, 0, life_width, 20))
                        enemy_blits.append((life_bar, (bar_x, bar_y)))
                    enemy_blits.append((b.get_image(), b.get_pos()))
            else:
                for b in ENNEMY_TRACKER:
                    enemy_blits.append((b.get_image(), b.get_pos()))
            if enemy_blits:
                chars_layer.extend(enemy_blits)
    if show_animations:
        anim_count = len(ANIMATION_TRACKER)
        if anim_count > 0:
            anim_blits = [(p[0].get_image(), (p[1], p[2])) for p in ANIMATION_TRACKER]
            if anim_blits:
                chars_layer.extend(anim_blits)
    if show_projectiles:
        proj_count = len(PROJECTILE_TRACKER)
        if proj_count > 0:
            for p in PROJECTILE_TRACKER:
                if show_hitboxes:
                    if b.effective:
                        bullets_layer.append(draw_hitbox(b.hitbox.get_rect(), BLU, BLU_B))
                if p.warning is not None:
                    draw_warning(p.warning[0], RED_WARNING, p.warning[1])
            proj_blits = [(p.get_image(), p.get_pos()) for p in PROJECTILE_TRACKER]
            if proj_blits:
                bullets_layer.extend(proj_blits)
    if show_text:
        text_count = len(TEXT_TRACKER)
        if text_count > 0:
            text_blits = [(t[0].image, (t[1], t[2])) for t in TEXT_TRACKER]
            if text_blits:
                texts_layer.extend(text_blits)

def logic_tick():
    """Ticks all there is to tick"""
    SYSTEM["player"].tick()
    i = len(POWER_UP_TRACKER) - 1
    while i >= 0:
        bubble = POWER_UP_TRACKER[i]
        bubble.tick(SYSTEM["player"])
        if bubble.flagged_for_deletion:
            POWER_UP_TRACKER.pop(i)
        i -= 1
    i = len(ENNEMY_TRACKER) - 1
    while i >= 0:
        baddie = ENNEMY_TRACKER[i]
        baddie.tick(SYSTEM["player"])
        if baddie.destroyed:
            ENNEMY_TRACKER.pop(i)
        i -= 1
    i = len(ANIMATION_TRACKER) - 1
    while i >= 0:
        p = ANIMATION_TRACKER[i]
        p[0].tick()
        if p[0].finished:
            ANIMATION_TRACKER.pop(i)
        i -= 1
    i = len(PROJECTILE_TRACKER) - 1
    while i >= 0:
        p = PROJECTILE_TRACKER[i]
        p.tick()
        if (isinstance(p, Projectile) and p.can_be_destroyed()) or \
            (isinstance(p, Slash) and p.finished):
            PROJECTILE_TRACKER.pop(i)
        i -= 1
    i = len(TEXT_TRACKER) - 1
    while i >= 0:
        txt = TEXT_TRACKER[i]
        sfc = txt[0]
        sfc.opacity(txt[3])
        txt[3] -= 5
        txt[2] -= 3
        if txt[3] < 10:
            TEXT_TRACKER.pop(i)
        i -= 1
