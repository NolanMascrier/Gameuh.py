""""Renders the screen."""

from data.api.surface import flip

from data.constants import SYSTEM, SCREEN_HEIGHT, SCREEN_WIDTH, GAME_LEVEL, MENU_INVENTORY, LOADING


RENDER_LIST = []
CLEAN = (0, 0, 0, 0)

def render(image, pos):
    """Prepares the image to be rendered at position pos."""
    if pos[0] < -image.get_width() or pos[0] > SCREEN_WIDTH + image.get_width():
        return
    if pos[1] < -image.get_height() or pos[1] > SCREEN_HEIGHT + image.get_height():
        return
    RENDER_LIST.append((image, pos))

def renders(lst):
    """Prepares a list of tuple (image:pos) to be rendered."""
    for l in lst:
        render(l[0], l[1])

def render_all():
    """Renders the screen."""
    SYSTEM["windows"].fill((0,0,0, 255))
    shake = SYSTEM["post_effects"].shake_factor
    if SYSTEM["game_state"] != LOADING:
        SYSTEM["windows"].blit(SYSTEM["gm_background"], shake)
        SYSTEM["windows"].blit(SYSTEM["gm_parallaxe"], shake)
    SYSTEM["windows"].blits(RENDER_LIST)
    RENDER_LIST.clear()
    if SYSTEM["game_state"] == GAME_LEVEL:
        for name in ["pickup", "warnings", "bullets", "characters", "texts"]:
            SYSTEM["windows"].blit(SYSTEM["layers"][name], shake)
        SYSTEM["windows"].blit(SYSTEM["ui_surface"], (0, 0))
    elif SYSTEM["game_state"] in [MENU_INVENTORY]:
        SYSTEM["windows"].blit(SYSTEM["layers"]["pickup"], shake)
