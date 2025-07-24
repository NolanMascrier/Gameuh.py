"""Handles the skill tree rendering."""

from data.constants import SYSTEM, MENU_TREE
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
    SYSTEM["images"]["tree_scroller"].tick().draw()
