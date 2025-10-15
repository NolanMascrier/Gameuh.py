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
    """Renders the screen - OPTIMIZED VERSION."""
    # OPTIMIZATION: Only clear window if needed
    # For most game states, the background covers everything
    game_state = SYSTEM["game_state"]
    
    if game_state == LOADING:
        # Loading screen needs full clear
        SYSTEM["windows"].fill(BLACK_TRANSP)
    else:
        # CRITICAL OPTIMIZATION: Background covers entire screen
        # No need to clear if we're going to blit over it anyway
        shake = SYSTEM["post_effects"].shake_factor
        
        # Blit backgrounds (these cover the full screen, so no clear needed)
        SYSTEM["windows"].blit(SYSTEM["gm_background"], shake, True)
        SYSTEM["windows"].blit(SYSTEM["gm_parallaxe"], shake, True)
    
    # Batch render all queued items
    if RENDER_LIST:
        SYSTEM["windows"].blits(RENDER_LIST)
        RENDER_LIST.clear()
    
    # Render game layers
    if game_state == GAME_LEVEL:
        shake = SYSTEM["post_effects"].shake_factor
        
        # CRITICAL: Use blits for batch rendering layers
        layer_list = [(layer, shake) for _, layer in SYSTEM["layers"].items()]
        if layer_list:
            SYSTEM["windows"].blits(layer_list)
        
        # UI surface always last
        SYSTEM["windows"].blit(SYSTEM["ui_surface"], (0, 0))
    
    elif game_state == MENU_INVENTORY:
        shake = SYSTEM["post_effects"].shake_factor
        SYSTEM["windows"].blit(SYSTEM["layers"]["pickup"], shake)
