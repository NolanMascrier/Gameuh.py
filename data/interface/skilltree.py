"""Handles the skill tree rendering."""

from data.constants import SYSTEM, MENU_TREE
from data.image.text import Text
from data.interface.general import draw_bottom_bar, setup_bottom_bar

def open_skill_screen():
    """Sets up the skill tree screen menu."""
    SYSTEM["game_state"] = MENU_TREE
    setup_bottom_bar()

def unloader():
    """Unloads all skill tree-specific data."""

def draw_skills(events):
    """Draws the skill tree menu."""
    SYSTEM["windows"].blit(SYSTEM["city_back"].draw(), (0, 0))
    draw_bottom_bar(events)
    SYSTEM["images"]["tree_surface"].fill((0,0,0,0))
    SYSTEM["tree"].tick()
    SYSTEM["tree"].draw(SYSTEM["images"]["tree_surface"])
    SYSTEM["images"]["tree_scroller"].tick().draw()
    SYSTEM["windows"].blit(SYSTEM["images"]["skillpoints"].image, (10, 10))
    txt = Text(f"{SYSTEM['player'].creature.ap}", size=60, default_color=(255,255,255))
    SYSTEM["windows"].blit(txt.surface, (140, 74))
