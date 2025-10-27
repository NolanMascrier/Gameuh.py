""""Renders the screen."""

from data.constants import SYSTEM, SCREEN_HEIGHT, SCREEN_WIDTH, GAME_LEVEL, MENU_INVENTORY, LOADING\
    , BLACK_TRANSP

RENDER_LIST = []

def render(image, pos):
    """Prepares the image to be rendered at position pos."""
    x, y = pos
    if x < -200 or x > SCREEN_WIDTH + 200:
        return
    if y < -200 or y > SCREEN_HEIGHT + 200:
        return
    RENDER_LIST.append((image, pos))

def renders(lst):
    """Prepares a list of tuple (image:pos) to be rendered."""
    RENDER_LIST.extend(lst)

def render_all():
    """Renders the screen - OPTIMIZED."""
    game_state = SYSTEM["game_state"]
    if game_state == LOADING:
        SYSTEM["windows"].fill(BLACK_TRANSP)
        if RENDER_LIST:
            SYSTEM["windows"].blits(RENDER_LIST)
            RENDER_LIST.clear()
    else:
        all_blits = []
        shake = SYSTEM["post_effects"].shake_factor
        all_blits.append((SYSTEM["gm_background"], shake))
        all_blits.append((SYSTEM["gm_parallaxe"], shake))
        if RENDER_LIST:
            all_blits.extend(RENDER_LIST)
            RENDER_LIST.clear()
        if game_state == GAME_LEVEL:
            SYSTEM["images"]["life_orb"].tick()
            SYSTEM["images"]["mana_orb"].tick()
            SYSTEM["images"]["exp_orb"].tick()
            all_blits.append((SYSTEM["warnings"], shake))
            for layer in SYSTEM["layers"].values():
                all_blits.extend(layer)
        elif game_state == MENU_INVENTORY:
            all_blits.extend(SYSTEM["layers"]["pickup"])
        if SYSTEM["post_effects"].flash_timer > 0:
            all_blits.append((SYSTEM["post_effects"].flash_surface, shake))
        if SYSTEM["fps_counter"] is not None and SYSTEM["options"]["show_fps"]:
            all_blits.append((SYSTEM["fps_counter"].surface,\
                                (SCREEN_WIDTH - SYSTEM["fps_counter"].width, 0)))
        if all_blits:
            SYSTEM["windows"].blits(all_blits)
    if game_state == GAME_LEVEL:
        SYSTEM["warnings"].fill(BLACK_TRANSP)
