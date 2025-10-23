"""For loading and saving data."""

import json

from data.api.surface import set_screen, Surface

from data.constants import SYSTEM, RESSOURCES
from data.character import Character
from data.game.tree import Node
from data.game.spell import Spell

def save(filename = None):
    """Save the character data."""
    if filename is None:
        filename = "default.char"
    with open(filename, "w", encoding="utf-8") as file:
        spells = {}
        for s in SYSTEM["spells"]:
            if SYSTEM["spells"][s] is not None:
                spells[s] = SYSTEM["spells"][s].export()
            else:
                spells[s] = 'null'
        data = {
            "player": SYSTEM["player"].export(),
            "tree": SYSTEM["tree"].export(),
            "spells": spells
        }
        json.dump(data, file)

def load(filename = None):
    """Loads the character data."""
    if filename is None:
        filename = "default.char"
    with open(filename, "r", encoding="utf-8") as file:
        read = json.load(file)
        SYSTEM["player"] = Character.imports(json.loads(read["player"]))
        SYSTEM["tree"] = Node.imports(json.loads(read["tree"]))
        for s in read["spells"]:
            if s != 'null' and SYSTEM["spells"][s] is not None:
                SYSTEM["spells"][s] = Spell.imports(json.loads(read["spells"][s]))

def change_language(lang):
    """Changes the system's language.
    
    Args:
        lang (str): Name of the language. Must correspond\
        to a file in ressources/locales.
    """
    try:
        with open(f"{RESSOURCES}/locales/{lang}.json", mode = 'r',\
                encoding="utf-8") as file:
            data = file.read()
            SYSTEM["lang"] = json.loads(data)
    except FileNotFoundError:
        print("File not found, language unchanged.")
        SYSTEM["lang"] = None

def export_options():
    """Exports the option portion of the SYSTEM as a json file."""
    if SYSTEM["options"]["screen_resolution"] != SYSTEM["options"]["screen_resolution_temp"]:
        SYSTEM["options"]["changed"] = True
    SYSTEM["options"]["screen_resolution"] = SYSTEM["options"]["screen_resolution_temp"]
    SYSTEM["options"]["fps"] = SYSTEM["options"]["fps_temp"]
    if SYSTEM["options"]["lang_selec"] != SYSTEM["options"]["lang_temp"]:
        SYSTEM["options"]["lang_selec"] = SYSTEM["options"]["lang_temp"]
        change_language(SYSTEM["options"]["lang_temp"])
    data = json.dumps(SYSTEM["options"])
    with open("user_config.json", "w", encoding='utf-8') as file:
        file.write(data)

def reload_options():
    """Reloads the options from the SYSTEM."""
    if SYSTEM["options"]["changed"]:
        disp = set_screen(SYSTEM["options"]["fullscreen"], SYSTEM["options"]["screen_resolution"][0],\
                        SYSTEM["options"]["screen_resolution"][1],\
                        SYSTEM["options"]["vsync"])
        SYSTEM["real_windows"] = Surface(SYSTEM["options"]["screen_resolution"][0],\
                                        SYSTEM["options"]["screen_resolution"][1], is_alpha=False)
        SYSTEM["real_windows"].surface = disp
        SYSTEM["options"]["changed"] = False

def export_and_reload():
    """Does what is says on the tincan"""
    export_options()
    reload_options()

def load_options(is_start = False):
    """Attemps to load the options."""
    try:
        with open("user_config.json", "r", encoding='utf-8') as f:
            data = json.loads(f.read())
            for d in data:
                if d in SYSTEM["options"]:
                    SYSTEM["options"][d] = data[d]
    except FileNotFoundError:
        print("No config file exists. Creating one")
        export_options()
    if is_start:
        SYSTEM["options"]["changed"] = True
    reload_options()
