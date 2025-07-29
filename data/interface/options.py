"""Handles the options tab rendering."""

from data.constants import SYSTEM, MENU_OPTIONS, export_and_reload
from data.interface.general import draw_bottom_bar, setup_bottom_bar
from data.image.checkbox import Checkbox
from data.image.button import Button

def reload():
    """Resets the button to their default values."""

def open_option_screen():
    """Sets up the option screen menu."""
    SYSTEM["game_state"] = MENU_OPTIONS
    setup_bottom_bar()
    #Boutton accepter -> export + reload options
    SYSTEM["ui"]["button_validate"] = Button(SYSTEM["images"]["btn"],\
        SYSTEM["images"]["btn_p"], export_and_reload, "Ok")
    #Boutton annuler -> Remets le reste en fonction du SYSTEM
    #Selecteur FPS
    #Selecteur résolution
    #Selecteur de langage
    #Case fullscreen
    SYSTEM["ui"]["box_fullscreen"] = Checkbox("fullscreen", SYSTEM["images"]["checkbox"],\
        SYSTEM["images"]["checkbox_ok"], "fullscreen")
    SYSTEM["ui"]["box_vsync"] = Checkbox("vsync", SYSTEM["images"]["checkbox"],\
        SYSTEM["images"]["checkbox_ok"], "vsync")
    SYSTEM["ui"]["box_hitboxes"] = Checkbox("hitboxes", SYSTEM["images"]["checkbox"],\
        SYSTEM["images"]["checkbox_ok"], "show_hitboxes")

def unloader():
    """Unloads all option-specific data."""

def draw_options(events):
    """Draws the optino tree menu."""
    SYSTEM["windows"].blit(SYSTEM["city_back"].draw(), (0, 0))
    SYSTEM["ui"]["button_validate"].set(1000, 250).tick().draw()
    SYSTEM["ui"]["box_fullscreen"].set(10, 10).tick().draw()
    SYSTEM["ui"]["box_vsync"].set(10, 100).tick().draw()
    SYSTEM["ui"]["box_hitboxes"].set(10, 190).tick().draw()
    draw_bottom_bar(events)
