"""Handles the options tab rendering."""

from data.constants import SYSTEM, MENU_OPTIONS, export_and_reload, trad, save, load
from data.interface.general import draw_bottom_bar, setup_bottom_bar
from data.image.checkbox import Checkbox
from data.image.button import Button
from data.image.dropdown import DropDown
from data.interface.render import renders

def reload():
    """Resets the button to their default values."""

def open_option_screen():
    """Sets up the option screen menu."""
    SYSTEM["game_state"] = MENU_OPTIONS
    setup_bottom_bar()
    SYSTEM["ui"]["button_validate"] = Button(SYSTEM["images"]["btn"],\
        SYSTEM["images"]["btn_p"], export_and_reload, trad('buttons', 'accept'))
    SYSTEM["ui"]["button_cancel"] = Button(SYSTEM["images"]["btn"],\
        SYSTEM["images"]["btn_p"], open_option_screen, trad('buttons', 'cancel'))
    SYSTEM["ui"]["button_save"] = Button(SYSTEM["images"]["btn"],\
        SYSTEM["images"]["btn_p"], save, "Save")
    SYSTEM["ui"]["button_load"] = Button(SYSTEM["images"]["btn"],\
        SYSTEM["images"]["btn_p"], load, "Load")
    SYSTEM["ui"]["button_quit"] = Button(SYSTEM["images"]["btn"],\
        SYSTEM["images"]["btn_p"],lambda: SYSTEM.__setitem__("playing", False), "Quit")
    default_res = 0
    for k in SYSTEM["options"]["resolutions"]:
        if k == SYSTEM["options"]["screen_resolution"]:
            break
        default_res += 1
    default_lang = 0
    for k in SYSTEM["options"]["langs"]:
        if k == SYSTEM["options"]["lang_selec"]:
            break
        default_lang += 1
    default_fps = 0
    for k in SYSTEM["options"]["fps_selector"]:
        if k == SYSTEM["options"]["fps"]:
            break
        default_fps += 1
    SYSTEM["ui"]["drop_resolution"] = DropDown("resolution",\
        [f"{w}x{h}" for w, h in SYSTEM["options"]["resolutions"]],\
        SYSTEM["options"]["resolutions"], "screen_resolution_temp", default_res)
    SYSTEM["ui"]["drop_lang"] = DropDown("lang",\
        [f"{trad('langs', l)}" for l in SYSTEM["options"]["langs"]],\
        SYSTEM["options"]["langs"], "lang_temp", default_lang)
    SYSTEM["ui"]["drop_fps"] = DropDown("fps",\
        [f"{str(fps)}" for fps in SYSTEM["options"]["fps_display"]],\
        SYSTEM["options"]["fps_selector"], "fps_temp", default_fps)
    SYSTEM["ui"]["box_fullscreen"] = Checkbox("fullscreen", SYSTEM["images"]["checkbox"],\
        SYSTEM["images"]["checkbox_ok"], "fullscreen")
    SYSTEM["ui"]["box_vsync"] = Checkbox("vsync", SYSTEM["images"]["checkbox"],\
        SYSTEM["images"]["checkbox_ok"], "vsync")
    SYSTEM["ui"]["box_hitboxes"] = Checkbox("hitboxes", SYSTEM["images"]["checkbox"],\
        SYSTEM["images"]["checkbox_ok"], "show_hitboxes")
    SYSTEM["ui"]["box_fps"] = Checkbox("show_fps", SYSTEM["images"]["checkbox"],\
        SYSTEM["images"]["checkbox_ok"], "show_fps")
    SYSTEM["ui"]["box_bars"] = Checkbox("show_bars", SYSTEM["images"]["checkbox"],\
        SYSTEM["images"]["checkbox_ok"], "show_bars")
    SYSTEM["ui"]["box_cards"] = Checkbox("show_cards", SYSTEM["images"]["checkbox"],\
        SYSTEM["images"]["checkbox_ok"], "show_cards")

#SYSTEM["playing"]

def unloader():
    """Unloads all option-specific data."""

def draw_options(_):
    """Draws the optino tree menu."""
    renders(SYSTEM["city_back"].as_background)
    SYSTEM["ui"]["box_fullscreen"].set(10, 10).tick().draw()
    SYSTEM["ui"]["box_vsync"].set(10, 100).tick().draw()
    SYSTEM["ui"]["box_hitboxes"].set(10, 190).tick().draw()
    SYSTEM["ui"]["box_fps"].set(10, 280).tick().draw()
    SYSTEM["ui"]["box_cards"].set(10, 370).tick().draw()
    SYSTEM["ui"]["box_bars"].set(10, 460).tick().draw()
    SYSTEM["ui"]["drop_resolution"].set(450, 10).tick().draw()
    SYSTEM["ui"]["drop_fps"].set(750, 10).tick().draw()
    SYSTEM["ui"]["drop_lang"].set(1050, 10).tick().draw()
    SYSTEM["ui"]["button_validate"].set(10, 650).tick().draw()
    SYSTEM["ui"]["button_cancel"].set(10, 700).tick().draw()
    SYSTEM["ui"]["button_save"].set(10, 850).tick().draw()
    SYSTEM["ui"]["button_load"].set(10, 900).tick().draw()
    SYSTEM["ui"]["button_quit"].set(10, 950).tick().draw()
    draw_bottom_bar()
