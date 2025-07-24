"""Handles the options tab rendering."""

from data.constants import SYSTEM, MENU_OPTIONS
from data.interface.general import draw_bottom_bar, setup_bottom_bar

def open_option_screen():
    """Sets up the option screen menu."""
    SYSTEM["game_state"] = MENU_OPTIONS
    setup_bottom_bar()

def unloader():
    """Unloads all option-specific data."""

def draw_options(events):
    """Draws the optino tree menu."""
    SYSTEM["windows"].blit(SYSTEM["city_back"].draw(), (0, 0))
    draw_bottom_bar(events)
