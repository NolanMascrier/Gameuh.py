from time import sleep

from data.image.text import Text
from data.constants import *
from data.interface.gameui import draw_ui
from data.game.level import Level
from data.game.lootgenerator import LootGenerator
from data.interface.general import setup_bottom_bar, draw_bottom_bar
from data.interface.inventory import draw_inventory
from data.interface.spellbook import draw_spells
from data.interface.skilltree import draw_skills
from data.interface.options import draw_options
from data.interface.general import tick, draw_game
from data.interface.gear import draw_gear
from data.loading import init_game, init_timers

PLAYING = True

def debug_create_items():
    """Creates a bunch of items."""
    lg = LootGenerator()
    base_loot = lg.roll(40, 5)
    SYSTEM["player"].inventory.extend(base_loot)

def game_loop(keys, events):
    """Main game loop."""
    #Handle Events
    for event in events:
        if event.type == QUIT:
            SYSTEM["playing"] = False
        if event.type == WAVE_TIMER:
            SYSTEM["level"].next_wave()
        if event.type == TICKER_TIMER:
            tick()
    SYSTEM["windows"].blit(SYSTEM["level"].background.draw(), (0, 0))
    #Handle logic
    SYSTEM["player"].action(keys)
    #Handle printing on screen
    draw_game()
    #Draw the UI
    draw_ui()
    if SYSTEM["player"].creature.stats["life"].current_value <= 0:
        SYSTEM["game_state"] = GAME_DEATH
    SYSTEM["latest_frame"] = SYSTEM["windows"].copy()

def draw_victory(events):
    """Draws the victory screen."""
    for event in events:
        if event.type == TICKER_TIMER:
            tick()
    SYSTEM["windows"].blit(SYSTEM["level"].background.draw(), (0, 0))
    draw_game()
    x_offset = SCREEN_WIDTH / 2 - SYSTEM["images"]["menu_bg"].width / 2
    y_offset = SCREEN_HEIGHT / 2 - SYSTEM["images"]["menu_bg"].height / 2
    SYSTEM["windows"].blit(SYSTEM["images"]["menu_bg"].image, (x_offset, y_offset))
    SYSTEM["buttons"]["button_continue"].set(x_offset + 200, y_offset + 300)
    SYSTEM["buttons"]["button_continue"].draw(SYSTEM["windows"])
    gold = SYSTEM["level"].gold
    text = Text(f"#c#{(255, 179, 0)}{gold}")
    SYSTEM["windows"].blit(SYSTEM["images"]["gold_icon"].image, (x_offset, y_offset))
    SYSTEM["windows"].blit(text.surface, (x_offset + 80, y_offset + 32))
    for event in events:
        if event.type == pygame.MOUSEBUTTONDOWN:
            SYSTEM["buttons"]["button_continue"].press()

def draw_game_over(events):
    """Draws the defeat screen."""
    for event in events:
        if event.type == TICKER_TIMER:
            tick()
    SYSTEM["windows"].blit(SYSTEM["level"].background.draw(), (0, 0))
    draw_game(False)
    x_offset = SCREEN_WIDTH / 2 - SYSTEM["images"]["menu_bg"].width / 2
    y_offset = SCREEN_HEIGHT / 2 - SYSTEM["images"]["menu_bg"].height / 2
    SYSTEM["windows"].blit(SYSTEM["images"]["menu_bg"].image, (x_offset, y_offset))
    SYSTEM["buttons"]["button_continue"].set(x_offset + 200, y_offset + 300)
    SYSTEM["buttons"]["button_continue"].draw(SYSTEM["windows"])
    gold = SYSTEM["level"].gold
    text = Text(f"#c#{(255, 179, 0)}{gold}")
    SYSTEM["windows"].blit(SYSTEM["images"]["gold_icon"].image, (x_offset, y_offset))
    SYSTEM["windows"].blit(text.surface, (x_offset + 80, y_offset + 32))
    for event in events:
        if event.type == pygame.MOUSEBUTTONDOWN:
            SYSTEM["buttons"]["button_continue"].press()

def draw_pause(events):
    """Draws the pause menu."""
    x_offset = SCREEN_WIDTH / 2 - SYSTEM["images"]["menu_bg"].width / 2
    y_offset = SCREEN_HEIGHT / 2 - SYSTEM["images"]["menu_bg"].height / 2
    SYSTEM["windows"].blit(SYSTEM["latest_frame"], (0, 0))
    SYSTEM["windows"].blit(SYSTEM["images"]["menu_bg"].image, (x_offset, y_offset))
    SYSTEM["buttons"]["button_resume"].set(x_offset + 200, y_offset + 100)
    SYSTEM["buttons"]["button_abandon"].set(x_offset + 200, y_offset + 200)
    SYSTEM["buttons"]["button_quit"].set(x_offset + 200, y_offset + 300)
    SYSTEM["buttons"]["button_resume"].draw(SYSTEM["windows"])
    SYSTEM["buttons"]["button_abandon"].draw(SYSTEM["windows"])
    SYSTEM["buttons"]["button_quit"].draw(SYSTEM["windows"])
    for event in events:
        if event.type == pygame.MOUSEBUTTONDOWN:
            SYSTEM["buttons"]["button_resume"].press()
            SYSTEM["buttons"]["button_abandon"].press()
            SYSTEM["buttons"]["button_quit"].press()

def draw_small_card():
    """Draws a small character card."""
    x = SCREEN_WIDTH - SYSTEM["images"]["char_details"].width
    y = 0
    SYSTEM["windows"].blit(SYSTEM["images"]["char_details"].image, (x, y))
    li = SYSTEM["player"].creature.generate_stat_simple(x + 10, y + 10)
    for l in li:
        l.draw(SYSTEM["windows"])
        l.tick()

def draw_menu(events):
    """Draws the main game menu."""
    SYSTEM["windows"].blit(SYSTEM["city_back"].draw(), (0, 0))
    sfc = pygame.Surface((2000, 2000), pygame.SRCALPHA)
    sfc.blit(SYSTEM["images"]["mission_map"].image, (0, 0))
    SYSTEM["buttons_e"][0].set(350, 680, SYSTEM["images"]["mission_scroller"]).draw(sfc)
    SYSTEM["buttons_e"][1].set(860, 250, SYSTEM["images"]["mission_scroller"]).draw(sfc)
    SYSTEM["buttons_e"][2].set(900, 900, SYSTEM["images"]["mission_scroller"]).draw(sfc)
    SYSTEM["buttons_e"][3].set(478, 420, SYSTEM["images"]["mission_scroller"]).draw(sfc)
    SYSTEM["images"]["mission_scroller"].contains = sfc
    SYSTEM["images"]["mission_scroller"].tick().draw()
    draw_small_card()
    if SYSTEM["selected"] is not None and isinstance(SYSTEM["selected"], Level):
        name = Text(f'{SYSTEM["selected"].name}', True)
        lvl = Text(f'Area level: {SYSTEM["selected"].area_level}', True)
        #TODO: modifiers ...
        SYSTEM["windows"].blit(name.surface, (1500, 750))
        SYSTEM["windows"].blit(lvl.surface, (1500, 775))
        SYSTEM["buttons"]["button_assault"].set(1500, 1000).draw(SYSTEM["windows"])
        SYSTEM["windows"].blit(SYSTEM["selected"].icon.image, (1500, 800))
    draw_bottom_bar(events)
    for event in events:
        if event.type == pygame.MOUSEBUTTONDOWN:
            SYSTEM["buttons_e"][0].press()
            SYSTEM["buttons_e"][1].press()
            SYSTEM["buttons_e"][2].press()
            SYSTEM["buttons_e"][3].press()
            SYSTEM["buttons"]["button_assault"].press()

if __name__ == "__main__":
    init_game()
    init_timers()
    while True:
        if not SYSTEM["loaded"]:
            SYSTEM["windows"].fill((0, 0, 0))
            SYSTEM["images"]["load_orb"].tick()
            SYSTEM["windows"].blit(SYSTEM["images"]["load_orb"].get_image(), (SCREEN_WIDTH - 128, SCREEN_HEIGHT - 128))
            SYSTEM["windows"].blit(SYSTEM["images"]["load_back"].image, (200, SCREEN_HEIGHT - 111))
            width = SYSTEM["images"]["load_jauge"].width * (SYSTEM["progress"] / 100)
            SYSTEM["windows"].blit(SYSTEM["images"]["load_jauge"].image.subsurface(0, 0, width, 30)\
                , (200, SCREEN_HEIGHT - 111))
            window = pygame.transform.smoothscale(SYSTEM["windows"],\
                (SYSTEM["options"]["screen_resolution"][0], SYSTEM["options"]["screen_resolution"][1]))
            SYSTEM["real_windows"].blit(window, (0, 0))
            pygame.display.update()
            sleep(float(SYSTEM["options"]["fps"]))
        else:
            break
    held = False
    debug_create_items()
    ###
    setup_bottom_bar()
    while SYSTEM["playing"]:
        SYSTEM["pop_up"] = None
        get_mouse_pos()
        SYSTEM["mouse_click"] = pygame.mouse.get_pressed()
        if SYSTEM["mouse_click"][0] and not held:
            held = True
            SYSTEM["mouse_previous"] = SYSTEM["mouse"]
        if held and not SYSTEM["mouse_click"][0]:
            held = False
        SYSTEM["mouse_wheel"] = [(0, 0), (0, 0)]
        events = pygame.event.get()
        for event in events:
            if event.type == QUIT:
                PLAYING = False
            if event.type == MOUSEWHEEL:
                SYSTEM["mouse_wheel"][0] = SYSTEM["mouse_wheel"][1]
                SYSTEM["mouse_wheel"][1] = (event.x, event.y)
        keys = pygame.key.get_pressed()
        SYSTEM["keys"] = keys
        if keys[K_ESCAPE]:
            if SYSTEM["cooldown"] <= 0:
                SYSTEM["cooldown"] = 0.5
                if SYSTEM["game_state"] == GAME_LEVEL:
                    SYSTEM["game_state"] = GAME_PAUSE
                elif SYSTEM["game_state"] == GAME_PAUSE:
                    SYSTEM["game_state"] = GAME_LEVEL
        if SYSTEM["game_state"] == GAME_LEVEL:
            game_loop(keys, events)
        if SYSTEM["game_state"] == GAME_PAUSE:
            draw_pause(events)
        if SYSTEM["game_state"] == GAME_VICTORY:
            draw_victory(events)
        if SYSTEM["game_state"] == GAME_DEATH:
            draw_game_over(events)
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
            SYSTEM["windows"].blit(SYSTEM["pop_up"][0], (x, y))

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
        window = pygame.transform.smoothscale(SYSTEM["windows"],\
            (SYSTEM["options"]["screen_resolution"][0], SYSTEM["options"]["screen_resolution"][1]))
        SYSTEM["real_windows"].blit(window, (0, 0))
        pygame.display.update()
        sleep(float(SYSTEM["options"]["fps"]))
