""""Renders the screen."""

from data.constants import SYSTEM, SCREEN_HEIGHT, SCREEN_WIDTH, GAME_LEVEL, MENU_INVENTORY, LOADING


RENDER_LIST = []
CLEAN = (0, 0, 0, 0)
BLACK_TRANSP = (0, 0, 0, 255)

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
    """Renders the screen."""
    game_state = SYSTEM["game_state"]
    
    if game_state == LOADING:
        SYSTEM["windows"].fill(BLACK_TRANSP)
    else:
        shake = SYSTEM["post_effects"].shake_factor
        SYSTEM["windows"].blit(SYSTEM["gm_background"], shake, True)
        SYSTEM["windows"].blit(SYSTEM["gm_parallaxe"], shake, True)
    if RENDER_LIST:
        SYSTEM["windows"].blits(RENDER_LIST)
        RENDER_LIST.clear()
    if game_state == GAME_LEVEL or game_state == MENU_INVENTORY:
        shake = SYSTEM["post_effects"].shake_factor
        layer_list = [(layer, shake) for _, layer in SYSTEM["layers"].items()]
        if layer_list:
            SYSTEM["windows"].blits(layer_list)
        SYSTEM["windows"].blit(SYSTEM["ui_surface"], (0, 0))

