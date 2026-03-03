"""Handles the general UI operations such as the bottom bar"""

from functools import lru_cache

from data.api.surface import Surface

from data.constants import SYSTEM, SCREEN_HEIGHT, POWER_UP_TRACKER, ENNEMY_TRACKER,\
    PROJECTILE_TRACKER, TEXT_TRACKER, trad,\
    MENU_MAIN, MENU_GEAR, MENU_SPELLBOOK, MENU_TREE, MENU_INVENTORY, MENU_OPTIONS,\
    ANIMATION_TRACKER, RED_TRANSP, RED_PURE, RED_WARNING, GREEN_PURE, GREEN_TRANSP, BLUE_PURE,\
    BLUE_TRANSP
from data.image.tabs import Tabs
from data.components.projectiles.projectile import Projectile
from data.components.slashes.slash import Slash

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

def draw_warning(polygon, color, _ = 255):
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
    camera_x, camera_y = SYSTEM["level"].map.camera_offset

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
            x, y, w, h = SYSTEM["player"].entity.hitbox.get_rect()
            screen_rect = (x - camera_x, y - camera_y, w, h)
            chars_layer.append(draw_hitbox(screen_rect, GREEN_TRANSP, GREEN_PURE))
        px, py, _, _ = SYSTEM["player"].get_pos()
        chars_layer.append((SYSTEM["player"].get_image(), (px - camera_x, py - camera_y)))
        for buff in SYSTEM["player"].creature.buffs:
            if f"buffanim_{buff.name}" in SYSTEM["images"]:
                buff_anim = SYSTEM["images"][f"buffanim_{buff.name}"]
                buff_anim.tick()
                chars_layer.append((buff_anim.get_image(),\
                    (SYSTEM["player"].entity.center_x - camera_x - buff_anim.width // 2,\
                     SYSTEM["player"].entity.center_y - camera_y - buff_anim.height // 2)))
    if show_loot:
        loot_count = len(POWER_UP_TRACKER)
        if loot_count > 0:
            if show_hitboxes:
                for b in POWER_UP_TRACKER:
                    loot_rect = b.hitbox.get_rect()
                    pickup_layer.append(draw_hitbox((loot_rect[0] - camera_x, loot_rect[1] -
                                                     camera_y, loot_rect[2], loot_rect[3]),
                                                     BLUE_TRANSP, BLUE_PURE))
            loot_blits = [(b.get_image(), (b.x - camera_x, b.y - camera_y)) for b in
                          POWER_UP_TRACKER]
            if loot_blits:
                pickup_layer.extend(loot_blits)

    if show_enemies:
        enemy_count = len(ENNEMY_TRACKER)
        if enemy_count > 0:
            if show_hitboxes:
                for b in ENNEMY_TRACKER:
                    enemy_rect = b.hitbox.get_rect()
                    chars_layer.append(draw_hitbox((enemy_rect[0] - camera_x, enemy_rect[1] -
                                                    camera_y, enemy_rect[2], enemy_rect[3]),
                                                    RED_TRANSP, RED_PURE))
            enemy_blits = []
            if show_bars:
                enemy_jauge_back = SYSTEM["images"]["enemy_jauge_mini_back"].image
                for b in ENNEMY_TRACKER:
                    bar_x = b.entity.center_x - camera_x - 50
                    bar_y = b.y - camera_y - 25
                    enemy_blits.append((enemy_jauge_back, (bar_x, bar_y)))
                    life_pct = b.creature.stats["life"].current_value / \
                        b.creature.stats["life"].c_value
                    life_width = max(int(life_pct * 100), 0)
                    if life_width > 0:
                        life_bar = SYSTEM["images"]["enemy_jauge_mini"].image\
                            .subsurface((0, 0, life_width, 20))
                        enemy_blits.append((life_bar, (bar_x, bar_y)))
                    enemy_pos = b.get_pos()
                    enemy_blits.append((b.get_image(), (enemy_pos[0] - camera_x,
                                                        enemy_pos[1] - camera_y)))
                    for buff in b.creature.buffs:
                        if f"buffanim_{buff.name}" in SYSTEM["images"]:
                            buff_anim = SYSTEM["images"][f"buffanim_{buff.name}"]
                            buff_anim.tick()
                            enemy_blits.append((buff_anim.get_image(),\
                                (b.entity.center_x - camera_x - buff_anim.width // 2,\
                                 b.entity.center_y - camera_y - buff_anim.height // 2)))
            else:
                for b in ENNEMY_TRACKER:
                    enemy_pos = b.get_pos()
                    enemy_blits.append((b.get_image(), (enemy_pos[0] - camera_x,
                                                        enemy_pos[1] - camera_y)))
                    for buff in b.creature.buffs:
                        if f"buffanim_{buff.name}" in SYSTEM["images"]:
                            buff_anim = SYSTEM["images"][f"buffanim_{buff.name}"]
                            buff_anim.tick()
                            enemy_blits.append((buff_anim.get_image(),\
                                (b.entity.center_x - camera_x - buff_anim.width // 2,\
                                 b.entity.center_y - camera_y - buff_anim.height // 2)))
            if enemy_blits:
                chars_layer.extend(enemy_blits)

    if show_animations:
        anim_count = len(ANIMATION_TRACKER)
        if anim_count > 0:
            anim_blits = [(p[0].get_image(), (p[1] - camera_x, p[2] - camera_y))
                          for p in ANIMATION_TRACKER]
            if anim_blits:
                chars_layer.extend(anim_blits)

    if show_projectiles:
        proj_count = len(PROJECTILE_TRACKER)
        if proj_count > 0:
            for p in PROJECTILE_TRACKER:
                if show_hitboxes:
                    if p.effective:
                        proj_rect = p.hitbox.get_rect()
                        bullets_layer.append(draw_hitbox((proj_rect[0] - camera_x, proj_rect[1] -
                                                          camera_y, proj_rect[2], proj_rect[3]),
                                                          BLUE_TRANSP, BLUE_PURE))
                if p.warning is not None:
                    warning_points = [(pt[0] - camera_x, pt[1] - camera_y) for pt in p.warning[0]]
                    draw_warning(warning_points, RED_WARNING, p.warning[1])
            proj_blits = [(p.get_image(), (p.x - camera_x, p.y - camera_y))
                          for p in PROJECTILE_TRACKER if \
                          hasattr(p, 'get_image')]
            if proj_blits:
                bullets_layer.extend(proj_blits)

    if show_text:
        text_count = len(TEXT_TRACKER)
        if text_count > 0:
            text_blits = [(t[0].image, (t[1] - camera_x, t[2] - camera_y)) for t in TEXT_TRACKER]
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
            baddie.entity.real_image = None
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
            del p
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
