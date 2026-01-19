"""Handles the skill tree rendering."""

from data.constants import SYSTEM, MENU_TREE
from data.image.text import Text
from data.interface.general import draw_bottom_bar, setup_bottom_bar
from data.interface.render import render, renders
from data.interface.gear import STAT_LIST, draw_stat_panel, STATES, Tabs

UPDATED = [False]

def open_skill_screen():
    """Sets up the skill tree screen menu."""
    SYSTEM["game_state"] = MENU_TREE
    setup_bottom_bar()
    lst = SYSTEM["player"].creature.generate_stat_details()
    for f in lst:
        STAT_LIST[f] = lst[f]
    SYSTEM["gear_tab"] = STATES[0]
    SYSTEM["gear_tabs"] = Tabs(15, 200, STATES, STATES, "gear_tab")

def unloader():
    """Unloads all skill tree-specific data."""

def draw_skills(_):
    """Draws the skill tree menu."""
    current_class = SYSTEM["player"].current_class
    if UPDATED[0]:
        lst = SYSTEM["player"].creature.generate_stat_details()
        UPDATED[0] = False
        for f in lst:
            STAT_LIST[f] = lst[f]
    renders(SYSTEM["city_back"].as_background)
    SYSTEM["images"]["tree_surface"].fill((0,0,0,0))
    SYSTEM["tree"][current_class].tick()
    SYSTEM["tree"][current_class].draw(SYSTEM["images"]["tree_surface"])
    SYSTEM["images"]["tree_scroller"].tick().draw()
    txt = Text(f"SP: {SYSTEM['player'].creature.ap}", size=50,
               default_color=(255,255,255), font="item_desc")
    draw_stat_panel()
    draw_bottom_bar()
    render(txt.surface, (450, 60))
