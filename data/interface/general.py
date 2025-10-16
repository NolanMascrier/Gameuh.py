"""Handles the general UI operations such as the bottom bar."""

from functools import lru_cache

from data.constants import SYSTEM, SCREEN_HEIGHT, POWER_UP_TRACKER, ENNEMY_TRACKER,\
    PROJECTILE_TRACKER, TEXT_TRACKER, trad,\
    MENU_MAIN, MENU_GEAR, MENU_SPELLBOOK, MENU_TREE, MENU_INVENTORY, MENU_OPTIONS,\
    ANIMATION_TRACKER
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
    
    # PLAYER RENDERING
    if show_player:
        if SYSTEM["options"]["show_hitboxes"]:
            draw_hitbox(SYSTEM["player"].entity.hitbox, GRE, GRE_B, SYSTEM["layers"]["characters"])
        SYSTEM["layers"]["characters"].blit(SYSTEM["player"].get_image(),\
            SYSTEM["player"].get_pos())
    
    # LOOT RENDERING - BATCH
    if show_loot:
        loot_count = len(POWER_UP_TRACKER)
        if loot_count > 0:
            if SYSTEM["options"]["show_hitboxes"]:
                for b in POWER_UP_TRACKER:
                    draw_hitbox(b.hitbox, BLU, BLU_B, SYSTEM["layers"]["pickup"])
            
            # CRITICAL: Pre-allocate list with exact size (faster than list comp)
            loot_blits = []
            for b in POWER_UP_TRACKER:
                loot_blits.append((b.get_image(), (b.x, b.y)))
            
            if loot_blits:
                SYSTEM["layers"]["pickup"].blits(loot_blits)
    
    # ENEMY RENDERING - BATCH
    if show_enemies:
        enemy_count = len(ENNEMY_TRACKER)
        if enemy_count > 0:
            if SYSTEM["options"]["show_hitboxes"]:
                for b in ENNEMY_TRACKER:
                    draw_hitbox(b.hitbox, RED, RED_B, SYSTEM["layers"]["characters"])
            
            if SYSTEM["options"]["show_bars"]:
                # Pre-allocate with estimated size
                enemy_bars = []
                for b in ENNEMY_TRACKER:
                    bar_x = b.entity.center_x - SYSTEM["images"]["enemy_jauge_mini_back"].width / 2
                    bar_y = b.y - 25
                    enemy_bars.append((SYSTEM["images"]["enemy_jauge_mini_back"].image, (bar_x, bar_y)))
                    
                    life = max(b.creature.stats["life"].current_value /\
                        b.creature.stats["life"].c_value * 100, 0)
                    enemy_bars.append((SYSTEM["images"]["enemy_jauge_mini"].image\
                        .subsurface((0, 0, int(life), 20)), (bar_x, bar_y)))
                
                if enemy_bars:
                    SYSTEM["layers"]["characters"].blits(enemy_bars)
            
            # Build enemy blit list
            enemy_blits = []
            for b in ENNEMY_TRACKER:
                enemy_blits.append((b.get_image(), b.get_pos()))
            
            if enemy_blits:
                SYSTEM["layers"]["characters"].blits(enemy_blits)
    
    # ANIMATIONS - BATCH
    if show_animations:
        anim_count = len(ANIMATION_TRACKER)
        if anim_count > 0:
            anim_blits = []
            for p in ANIMATION_TRACKER:
                anim_blits.append((p[0].get_image(), (p[1], p[2])))
            
            if anim_blits:
                SYSTEM["layers"]["characters"].blits(anim_blits)
    
    # PROJECTILES - BATCH
    if show_projectiles:
        proj_count = len(PROJECTILE_TRACKER)
        if proj_count > 0:
            if SYSTEM["options"]["show_hitboxes"]:
                for b in PROJECTILE_TRACKER:
                    if b.effective:
                        draw_hitbox(b.hitbox, BLU, BLU_B, SYSTEM["layers"]["bullets"])
            
            # Draw warnings first (can't batch these easily)
            for p in PROJECTILE_TRACKER:
                if p.warning is not None:
                    SYSTEM["layers"]["warnings"].draw_polygon(RED_WARNING, p.warning[0])
            
            # Batch projectile sprites
            proj_blits = []
            for p in PROJECTILE_TRACKER:
                proj_blits.append((p.get_image(), p.get_pos()))
            
            if proj_blits:
                SYSTEM["layers"]["bullets"].blits(proj_blits)
    
    # TEXT - BATCH
    if show_text:
        text_count = len(TEXT_TRACKER)
        if text_count > 0:
            text_blits = []
            for t in TEXT_TRACKER:
                text_blits.append((t[0].image, (t[1], t[2])))
            
            if text_blits:
                SYSTEM["layers"]["texts"].blits(text_blits)

def logic_tick():
    """Ticks all there is to tick."""
    SYSTEM["player"].tick()
    i = 0
    while i < len(POWER_UP_TRACKER):
        bubble = POWER_UP_TRACKER[i]
        bubble.tick(SYSTEM["player"])
        if bubble.flagged_for_deletion:
            POWER_UP_TRACKER.pop(i)
        else:
            i += 1
    i = 0
    while i < len(ENNEMY_TRACKER):
        baddie = ENNEMY_TRACKER[i]
        baddie.tick(SYSTEM["player"])
        if baddie.destroyed:
            ENNEMY_TRACKER.pop(i)
        else:
            i += 1
    i = 0
    while i < len(ANIMATION_TRACKER):
        p = ANIMATION_TRACKER[i]
        p[0].tick()
        if p[0].finished:
            ANIMATION_TRACKER.pop(i)
        else:
            i += 1
    i = 0
    while i < len(PROJECTILE_TRACKER):
        p = PROJECTILE_TRACKER[i]
        p.tick()
        if (isinstance(p, Projectile) and p.can_be_destroyed()) or \
            (isinstance(p, Slash) and p.finished):
            PROJECTILE_TRACKER.pop(i)
        else:
            i += 1
    i = 0
    while i < len(TEXT_TRACKER):
        txt = TEXT_TRACKER[i]
        sfc = txt[0]
        sfc.opacity(txt[3])
        txt[3] -= 5
        txt[2] -= 3
        if txt[3] < 10:
            TEXT_TRACKER.pop(i)
        else:
            i += 1
