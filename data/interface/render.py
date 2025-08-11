""""Renders the screen."""

import pygame
from data.constants import SYSTEM, SCREEN_HEIGHT, SCREEN_WIDTH, GAME_LEVEL

RENDER_LIST = []

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
    SYSTEM["windows"].blits(RENDER_LIST)
    RENDER_LIST.clear()
    if SYSTEM["game_state"] == GAME_LEVEL:
        SYSTEM["windows"].blit(SYSTEM["ui_surface"], (0, 0))
    window = pygame.transform.scale(SYSTEM["windows"],\
            (SYSTEM["options"]["screen_resolution"][0], SYSTEM["options"]["screen_resolution"][1]))
    SYSTEM["real_windows"].blit(window, (0, 0))
    pygame.display.update()
