"""Handles the general UI operations such as the bottom bar."""

from data.constants import SYSTEM, SCREEN_HEIGHT, POWER_UP_TRACKER, ENNEMY_TRACKER,\
    PROJECTILE_TRACKER, TEXT_TRACKER, trad,\
    MENU_MAIN, MENU_GEAR, MENU_SPELLBOOK, MENU_TREE, MENU_INVENTORY, MENU_OPTIONS,\
    ANIMATION_TRACKER
from data.interface.render import renders, render
from data.image.tabs import Tabs
from data.projectile import Projectile
from data.slash import Slash
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

def draw_game(show_player = True, show_enemies = True,\
    show_loot = True, show_projectiles = True,\
    show_text = True, show_animations = True):
    """Draws the main game component."""
    for _, layer in SYSTEM["layers"].items():
        layer.fill((0,0,0,0))
    if show_player:
        if SYSTEM["options"]["show_hitboxes"]:
            draw_hitbox(SYSTEM["player"].entity.hitbox, GRE, GRE_B, SYSTEM["layers"]["characters"])
        SYSTEM["layers"]["characters"].blit(SYSTEM["player"].get_image(),\
            SYSTEM["player"].get_pos())
    if show_loot:
        if SYSTEM["options"]["show_hitboxes"]:
            for b in POWER_UP_TRACKER:
                draw_hitbox(b.hitbox, BLU, BLU_B, SYSTEM["layers"]["pickup"])
        SYSTEM["layers"]["pickup"].blits([b.get_image(), (b.x, b.y)] for b in POWER_UP_TRACKER)
    if show_enemies:
        if SYSTEM["options"]["show_hitboxes"]:
            for b in ENNEMY_TRACKER:
                draw_hitbox(b.hitbox, RED, RED_B, SYSTEM["layers"]["characters"])
        if SYSTEM["options"]["show_bars"]:
            for b in ENNEMY_TRACKER:
                SYSTEM["layers"]["characters"].blit(SYSTEM["images"]["enemy_jauge_mini_back"]\
                    .image, (b.entity.center_x - SYSTEM["images"]["enemy_jauge_mini_back"].width / 2, b.y - 25))
                life = max(b.creature.stats["life"].current_value /\
                    b.creature.stats["life"].c_value * 100, 0)
                SYSTEM["layers"]["characters"].blit(SYSTEM["images"]["enemy_jauge_mini"].image\
                    .subsurface((0,0, life, 20)), (b.entity.center_x - SYSTEM["images"]["enemy_jauge_mini_back"]\
                                               .width / 2, b.y - 25))
        SYSTEM["layers"]["characters"].blits([b.get_image(), b.get_pos()] for b in ENNEMY_TRACKER)
    if show_animations:
        SYSTEM["layers"]["characters"].blits([p[0].get_image(), (p[1], p[2])]\
                                             for p in ANIMATION_TRACKER)
    if show_projectiles:
        if SYSTEM["options"]["show_hitboxes"]:
            for b in PROJECTILE_TRACKER:
                if b.effective:
                    draw_hitbox(b.hitbox, BLU, BLU_B, SYSTEM["layers"]["bullets"])
        for p in PROJECTILE_TRACKER:
            if p.warning is not None:
                SYSTEM["layers"]["warnings"].draw_polygon(RED_WARNING, p.warning[0])
        SYSTEM["layers"]["bullets"].blits([p.get_image(), p.get_pos()] for p in PROJECTILE_TRACKER)
    if show_text:
        SYSTEM["layers"]["texts"].blits([t[0].image, (t[1], t[2])] for t in TEXT_TRACKER)

def logic_tick():
    """Ticks all there is to tick."""
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
