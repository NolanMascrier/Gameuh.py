"""Game launcher."""

import cProfile
import pstats
import random

from data.api.surface import Surface, get_press, get_keys, get_events

from data.image.text import Text
from data.constants import *
from data.interface.gameui import draw_ui
from data.game.level import Level
from data.interface.general import setup_bottom_bar, draw_bottom_bar
from data.interface.inventory import draw_inventory
from data.interface.spellbook import draw_spells
from data.interface.skilltree import draw_skills
from data.interface.options import draw_options
from data.interface.general import logic_tick, draw_game
from data.interface.gear import draw_gear
from data.loading import init_game, init_timers
from data.interface.render import render_all, render, resolution, renders
from data.interface.endlevel import draw_end
from data.projectile import Projectile
from data.slash import Slash
from data.tables.uniques_table import UNIQUES

DAMAGE_COLOR = (255, 30, 30)

def debug_create_items():
    """Creates a bunch of items."""
    base_loot = []
    for _ in range(100):
        base_loot.append(SYSTEM["looter"].generate_item(5, random.randint(2,3)))
    SYSTEM["player"].inventory.extend(base_loot)
    SYSTEM["player"].inventory.extend([f[0] for f in UNIQUES])

def check_collisions():
    """Checks all collisions."""
    for proj in PROJECTILE_TRACKER.copy():
        if proj.ignore_team or proj.evil: #check for player
            if proj.hitbox.is_colliding(SYSTEM["player"].entity.hitbox):
                if proj in SYSTEM["player"].immune:
                    continue
                if isinstance(proj, Projectile):
                    dmg, crit = proj.on_hit(SYSTEM["player"].creature)
                    if dmg is None or crit is None:
                        continue
                    SYSTEM["text_generator"].generate_damage_text(SYSTEM["player"].x,\
                                                                  SYSTEM["player"].y,\
                                                                DAMAGE_COLOR, crit, dmg)
                elif isinstance(proj, Slash):
                    dmg, crit = proj.on_hit(SYSTEM["player"].creature)
                    if dmg is None or crit is None:
                        continue
                    SYSTEM["text_generator"].generate_damage_text(SYSTEM["player"].x,\
                                                                  SYSTEM["player"].y,\
                                                                DAMAGE_COLOR, crit, dmg)
        elif proj.ignore_team or not proj.evil: #Check for each enemy
            for enemy in ENNEMY_TRACKER.copy():
                if proj.hitbox.is_colliding(enemy.entity.hitbox):
                    if proj in enemy.immune:
                        continue
                    if isinstance(proj, Projectile):
                        dmg, crit = proj.on_hit(enemy.creature)
                        if dmg is None or crit is None:
                            continue
                        SYSTEM["text_generator"].generate_damage_text(enemy.x,\
                                                                    enemy.y,\
                                                                    DAMAGE_COLOR, crit, dmg)
                    elif isinstance(proj, Slash):
                        dmg, crit = proj.on_hit(enemy.creature)
                        if dmg is None or crit is None:
                            continue
                        SYSTEM["text_generator"].generate_damage_text(enemy.x,\
                                                                    enemy.y,\
                                                                    DAMAGE_COLOR, crit, dmg)

def game_loop(keys, time_event):
    """Main game loop."""
    #Handle Events
    for event in time_event:
        if event == QUIT:
            SYSTEM["playing"] = False
        if event == WAVE_TIMER:
            SYSTEM["level"].next_wave()
        if event == TICKER_TIMER:
            logic_tick()
    SYSTEM["level"].background.draw()
    draw_game()
    draw_ui()
    #Handle logic
    SYSTEM["player"].action(keys)
    check_collisions()
    if SYSTEM["player"].creature.stats["life"].current_value <= 0:
        SYSTEM["level"].fail_level()

def draw_pause(_):
    """Draws the pause menu."""
    x_offset = SCREEN_WIDTH / 2 - SYSTEM["images"]["menu_bg"].width / 2
    y_offset = SCREEN_HEIGHT / 2 - SYSTEM["images"]["menu_bg"].height / 2
    SYSTEM["level"].background.draw()
    draw_game()
    render(SYSTEM["images"]["menu_bg"].image, (x_offset, y_offset))
    SYSTEM["buttons"]["button_resume"].set(x_offset + 200, y_offset + 100)
    SYSTEM["buttons"]["button_abandon"].set(x_offset + 200, y_offset + 200)
    SYSTEM["buttons"]["button_quit"].set(x_offset + 200, y_offset + 300)
    SYSTEM["buttons"]["button_resume"].draw(SYSTEM["windows"])
    SYSTEM["buttons"]["button_abandon"].draw(SYSTEM["windows"])
    SYSTEM["buttons"]["button_quit"].draw(SYSTEM["windows"])
    for b in ["button_resume", "button_abandon", "button_quit"]:
        SYSTEM["buttons"][b].tick()

def draw_small_card():
    """Draws a small character card."""
    x = SCREEN_WIDTH - SYSTEM["images"]["char_details"].width
    y = 0
    render(SYSTEM["images"]["char_details"].image, (x, y))

def draw_menu(events):
    """Draws the main game menu."""
    renders(SYSTEM["city_back"].as_background)
    sfc = Surface(width=2000, height=2000)
    sfc.blit(SYSTEM["images"]["mission_map"].image, (0, 0))
    SYSTEM["buttons_e"][0].set(350, 680, SYSTEM["images"]["mission_scroller"]).draw(sfc)
    SYSTEM["buttons_e"][1].set(860, 250, SYSTEM["images"]["mission_scroller"]).draw(sfc)
    SYSTEM["buttons_e"][2].set(900, 900, SYSTEM["images"]["mission_scroller"]).draw(sfc)
    SYSTEM["buttons_e"][3].set(478, 420, SYSTEM["images"]["mission_scroller"]).draw(sfc)
    SYSTEM["images"]["mission_scroller"].contains = sfc
    SYSTEM["images"]["mission_scroller"].tick().draw()
    draw_small_card()
    if SYSTEM["selected"] is not None and isinstance(SYSTEM["selected"], Level):
        x = SCREEN_WIDTH - SYSTEM["images"]["char_details"].width / 2
        y = SCREEN_HEIGHT - SYSTEM["images"]["char_details"].height / 2
        name = Text(f'{SYSTEM["selected"].describe()}', True, "item_desc",
                force_x=SYSTEM["images"]["char_details"].width - 20, line_wrap=True)
        #TODO: modifiers ...
        render(name.surface, (x - name.width / 2, 25))
        SYSTEM["buttons"]["button_assault"].set(x - SYSTEM["buttons"]["button_assault"].width / 2,\
                                                930).draw(SYSTEM["windows"])
        render(SYSTEM["selected"].icon.image, (x - SYSTEM["selected"].icon.width / 2, 780))
    draw_bottom_bar()
    for b in [0, 1, 2, 3]:
        SYSTEM["buttons_e"][b].tick()
    SYSTEM["buttons"]["button_assault"].tick()

def loading():
    """Displays the loading screen."""
    if SYSTEM["loading_text"] is not None:
        render(SYSTEM["loading_text"].surface, (200, SCREEN_HEIGHT - 128))
    SYSTEM["images"]["load_orb"].tick()
    render(SYSTEM["images"]["load_orb"].get_image(), (SCREEN_WIDTH - 128, SCREEN_HEIGHT - 128))
    render(SYSTEM["images"]["load_back"].image, (200, SCREEN_HEIGHT - 111))
    width = SYSTEM["images"]["load_jauge"].width * (SYSTEM["progress"] / 100)
    render(SYSTEM["images"]["load_jauge"].image.subsurface((0, 0, width, 30))\
        , (200, SCREEN_HEIGHT - 111))
    render_all()
    resolution()

def main_loop():
    """Main loop. Temporary"""
    while SYSTEM["playing"]:
        SYSTEM["deltatime"].tick()
        if SYSTEM["game_state"] == LOADING:
            loading()
            continue
        if SYSTEM["post_effects"].pause:
            SYSTEM["post_effects"].tick()
            continue
        SYSTEM["pop_up"] = None
        get_mouse_pos()
        SYSTEM["mouse_click"] = get_press()
        if SYSTEM["mouse_click"][0] and not SYSTEM["held"]:
            SYSTEM["held"] = True
            SYSTEM["mouse_previous"] = SYSTEM["mouse"]
        if SYSTEM["held"] and not SYSTEM["mouse_click"][0]:
            SYSTEM["held"] = False
        SYSTEM["mouse_wheel"] = [(0, 0), (0, 0)]
        events = get_events()
        time_event = SYSTEM["deltatime"].get()
        for event in events:
            if event.type == QUIT:
                SYSTEM["playing"] = False
            if event.type == MOUSEWHEEL:
                SYSTEM["mouse_wheel"][0] = SYSTEM["mouse_wheel"][1]
                SYSTEM["mouse_wheel"][1] = (event.x, event.y)
        keys = get_keys()
        SYSTEM["keys"] = keys
        if keys[K_ESCAPE]:
            if SYSTEM["cooldown"] <= 0:
                SYSTEM["cooldown"] = 0.5
                if SYSTEM["game_state"] == GAME_LEVEL:
                    SYSTEM["game_state"] = GAME_PAUSE
                elif SYSTEM["game_state"] == GAME_PAUSE:
                    SYSTEM["game_state"] = GAME_LEVEL
        if SYSTEM["game_state"] == GAME_LEVEL:
            game_loop(keys, time_event)
        if SYSTEM["game_state"] == GAME_PAUSE:
            draw_pause(events)
        if SYSTEM["game_state"] == GAME_VICTORY:
            draw_end(events)
        if SYSTEM["game_state"] == GAME_DEATH:
            draw_end(events)
        if SYSTEM["game_state"] == MENU_MAIN:
            draw_menu(events)
        if SYSTEM["game_state"] == MENU_GEAR:
            draw_gear(events)
        if SYSTEM["game_state"] == MENU_SPELLBOOK:
            draw_spells(events)
        if SYSTEM["game_state"] == MENU_INVENTORY:
            draw_inventory(events)
        if SYSTEM["game_state"] == MENU_TREE:
            draw_skills(events)
        if SYSTEM["game_state"] == MENU_OPTIONS:
            draw_options(events)

        if SYSTEM["pop_up"] is not None:
            x = SYSTEM["mouse"][0] - SYSTEM["pop_up"][1]
            if x < 0:
                x += SYSTEM["pop_up"][1]
            y = SYSTEM["mouse"][1]
            if y + SYSTEM["pop_up"][2] > SCREEN_HEIGHT:
                y -= y + SYSTEM["pop_up"][2] - SCREEN_HEIGHT
            render(SYSTEM["pop_up"][0], (x, y))

        SYSTEM["cooldown"] -= 0.032
        SYSTEM["cooldown"] = max(SYSTEM["cooldown"], 0)
        if SYSTEM["dragged"] is not None:
            SYSTEM["dragged"].tick().draw()
        if not SYSTEM["mouse_click"][0]:
            SYSTEM["dragged"] = None
        if SYSTEM["mouse_click"][0] and SYSTEM["cooldown"] <= 0:
            if SYSTEM["rune"] != -1 and not SYSTEM["keys"][K_LSHIFT]:
                SYSTEM["rune"] = -1
                SYSTEM["rune_display"] = None
                SYSTEM["cooldown"] = 0.8
            if SYSTEM["rune"] != -1 and SYSTEM["player"].runes[SYSTEM["rune"]] <= 0:
                SYSTEM["rune"] = -1
                SYSTEM["rune_display"] = None
                SYSTEM["cooldown"] = 0.8
        render_all()
        SYSTEM["post_effects"].tick()

if __name__ == "__main__":
    init_game()
    init_timers()
    while True:
        if not SYSTEM["loaded"]:
            if SYSTEM["loading_text"] is not None:
                render(SYSTEM["loading_text"].surface, (200, SCREEN_HEIGHT - 128))
            SYSTEM["windows"].fill((0, 0, 0))
            SYSTEM["images"]["load_orb"].tick()
            render(SYSTEM["images"]["load_orb"].get_image(), (SCREEN_WIDTH - 128, SCREEN_HEIGHT - 128))
            render(SYSTEM["images"]["load_back"].image, (200, SCREEN_HEIGHT - 111))
            width = SYSTEM["images"]["load_jauge"].width * (SYSTEM["progress"] / 100)
            render(SYSTEM["images"]["load_jauge"].image.subsurface((0, 0, width, 30))\
                , (200, SCREEN_HEIGHT - 111))
            render_all()
            resolution()
        else:
            break
    profiler = cProfile.Profile()
    debug_create_items()
    setup_bottom_bar()
    profiler.enable()
    try:
        main_loop()
    except KeyboardInterrupt:
        pass
    profiler.disable()
    stats = pstats.Stats(profiler).sort_stats("cumtime")
    stats.print_stats(25)
