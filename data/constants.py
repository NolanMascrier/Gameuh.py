"""Stores the project's constants."""

from enum import Enum
import json
from pygame.constants import *
from data.physics.spatialgrid import SpatialGrid
from data.api.surface import Surface, mouse_position, set_screen


ROOT = ""
RESSOURCES = f"{ROOT}ressources"

SCREEN_WIDTH = 1920
SCREEN_HEIGHT = 1080

PROJECTILE_TRACKER = []
ENNEMY_TRACKER = []
POWER_UP_TRACKER = []
TEXT_TRACKER = []
IMAGE_TRACKER = []
ANIMATION_TRACKER = []
ANIMATION_TICK_TRACKER = []

PROJECTILE_GRID = SpatialGrid()
ENNEMY_GRID = SpatialGrid()
POWER_UP_GRID = SpatialGrid()

def clean_grids():
    """Cleans up all the grids."""
    PROJECTILE_GRID.clear()
    ENNEMY_GRID.clear()
    POWER_UP_GRID.clear()

def generate_grids():
    """Fills up the grids."""
    for p in PROJECTILE_TRACKER:
        PROJECTILE_GRID.add(p, p.hitbox)
    for e in ENNEMY_TRACKER:
        ENNEMY_GRID.add(e, e.hitbox)
    for p in POWER_UP_TRACKER:
        POWER_UP_GRID.add(p, p.hitbox)

FIREBALL_IMAGE = "ressources/fire.png"
UI_JAUGE = "ressources/ui_main.png"
UI_JAUGE_L = "ressources/ui_life.png"
UI_JAUGE_M = "ressources/ui_mana.png"
UI_JAUGE_C = "ressources/ui_cd.png"
JAUGE_L = "ressources/life_jauge.png"
JAUGE_M = "ressources/mana_jauge.png"
JAUGE_C = "ressources/cd_jauge.png"
JAUGE_BOSS_BACK = "ressources/life_boss_back.png"
JAUGE_BOSS = "ressources/life_boss.png"

FONT = None

LANGUAGE = None

#Game states
MENU_MAIN = 0
MENU_OPTIONS = 1
MENU_START = 2
MENU_LOAD = 3
MENU_SAVE = 4
GAME_LEVEL = 5
GAME_MAP = 6
GAME_SHOP = 7
GAME_INVENTORY = 8
GAME_EQUIP = 9
GAME_PAUSE = 10
GAME_VICTORY = 11
GAME_DEATH = 111
MENU_GEAR = 12
MENU_INVENTORY = 13
MENU_SPELLBOOK = 131
MENU_SPELLBOOK_1 = 1311
MENU_SPELLBOOK_2 = 1312
MENU_SPELLBOOK_3 = 1313
MENU_SPELLBOOK_5 = 1314
MENU_SPELLBOOK_4 = 1315
MENU_SPELLBOOK_DASH = 1316
MENU_OPTIONS_GAME = 14
MENU_TREE = 15
LOADING = 999


SYSTEM = {
    "loaded": False,
    "progress": 0,
    "playing": True,
    "font": None,
    "font_crit": None,
    "text_generator": None,
    "options": {
        "screen_resolution": (1920, 1080),
        "screen_resolution_temp": (1920, 1080),
        "fps": 60,
        "fps_temp": 60,
        "fps_selector": [120, 60, 30],
        "fps_display": [120, 60, 30],
        "resolutions": [(1138, 640), (1280, 720), (1366, 768), (1600, 900), (1920, 1080)],
        "fullscreen": True,
        "vsync": True,
        "lang_selec": "EN_us",
        "lang_temp": "EN_us",
        "langs": ["EN_us", "FR_fr"],
        "show_hitboxes": False,
        "show_fps": False
    },
    "key_chart": {
      "spell_1": (K_q, None),
      "spell_2": (K_e, None),
      "spell_3": (K_f, None),
      "spell_4": (K_t, None),
      "spell_5": (K_r, None),
      "dash": (K_LSHIFT, None),
      "potion_life": (K_1, None),
      "potion_mana": (K_2, None),
      "up": (K_UP, K_z),
      "down": (K_DOWN, K_s),
      "left": (K_LEFT, K_a),
      "right": (K_RIGHT, K_d),
      "pause": (K_ESCAPE, None)
    },
    "lang": [],
    "game_state": None,
    "windows": None,
    "images": {
        "fireball": None,
        "energyball": None,
        "character": None
    },
    "spells": {

    },
    "buttons": {
        "tab_e": None,
        "tab_r": None,
    },
    "ui": {},
    "ui_surface": None,
    "player": None,
    "level": None,
    "selected": None,
    "dragged": None,
    "pop-up": None,
    "mouse": (0,0)
}

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
    disp = set_screen(SYSTEM["options"]["fullscreen"], SCREEN_WIDTH, SCREEN_HEIGHT,\
                      SYSTEM["options"]["vsync"])
    SYSTEM["real_windows"] = Surface(SCREEN_WIDTH, SCREEN_HEIGHT)
    SYSTEM["real_windows"].surface = disp

def export_and_reload():
    """Does what is says on the tincan"""
    export_options()
    reload_options()

def load_options():
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
    reload_options()

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
    from data.character import Character
    from data.game.tree import Node
    from data.game.spell import Spell
    if filename is None:
        filename = "default.char"
    with open(filename, "r", encoding="utf-8") as file:
        read = json.load(file)
        SYSTEM["player"] = Character.imports(json.loads(read["player"]))
        SYSTEM["tree"] = Node.imports(json.loads(read["tree"]))
        for s in read["spells"]:
            if s != 'null' and SYSTEM["spells"][s] is not None:
                SYSTEM["spells"][s] = Spell.imports(json.loads(read["spells"][s]))

def get_mouse_pos():
    """Updates the mouse position."""
    x_factor = SCREEN_WIDTH / SYSTEM["options"]["screen_resolution"][0]
    y_factor = SCREEN_HEIGHT / SYSTEM["options"]["screen_resolution"][1]
    x, y = mouse_position()
    x *= x_factor
    y *= y_factor
    SYSTEM["mouse"] = (x, y)

def trad(keys, subkey = None):
    """Returns the translation data for the given key."""
    try:
        if subkey is None:
            return SYSTEM["lang"][keys]
        else:
            return SYSTEM["lang"][keys][subkey]
    except KeyError:
        return ["Unknown text data."]

WAVE_TIMER = "wave"
TICKER_TIMER = "ticker"
UPDATE_TIMER = USEREVENT+6

class Flags(str, Enum):
    """Flags to use for skills and damage sources."""
    HOT = "heal_over_time"
    DOT = "damage_over_time"
    MHOT = "multiplicative_heal_over_time"
    MDOT = "multiplicative_damage_over_time"
    MANA = "mana"
    LIFE = "life"
    STUN = "stun"
    GEAR = "gear"
    RUNE = "rune"
    CONSUMABLE = "consumable"
    FLAT = "flat" #flat stat bonus
    HEX = "hex" #additive malus
    BOON = "boon" #additive bonus
    CURSE = "curse" #multiplictive malus
    BLESS = "blessing" #multiplicative bonus
    STR = "str"
    DEX = "dex"
    INT = "int"
    DEF = "def"
    PHYS = "phys"
    FIRE = "fire"
    ICE = "ice"
    ELEC = "elec"
    ENERG = "energy"
    LIGHT = "light"
    DARK = "dark"
    CRIT_CHANCE = "crit_rate"
    CRIT_DAMAGE = "crit_dmg"
    PHYS_FLAT = "phys_flat"
    FIRE_FLAT = "fire_flat"
    ICE_FLAT = "ice_flat"
    ELEC_FLAT = "elec_flat"
    ENERG_FLAT = "energy_flat"
    LIGHT_FLAT = "light_flat"
    DARK_FLAT = "dark_flat"
    PHYS_DMG = "phys_dmg"
    FIRE_DMG = "fire_dmg"
    ICE_DMG = "ice_dmg"
    ELEC_DMG = "elec_dmg"
    ENERG_DMG = "energy_dmg"
    LIGHT_DMG = "light_dmg"
    DARK_DMG = "dark_dmg"
    PHYS_PEN = "phys_pen"
    FIRE_PEN = "fire_pen"
    ICE_PEN = "ice_pen"
    ELEC_PEN = "elec_pen"
    ENERG_PEN = "energy_pen"
    LIGHT_PEN = "light_pen"
    DARK_PEN = "dark_pen"
    SPELL = "spell_dmg"
    MELEE = "melee_dmg"
    RANGED = "ranged_dmg"
    PRECISION = "precision"
    BLOCK = "block"
    DODGE_RATING = "dodge_rating"
    DODGE = "dodge"
    ABS_DEF = "abs_def"
    PIERCE_BLOCK = "cant_be_blocked"
    PIERCE_DODGE = "cant_be_dodged"
    ALL_DAMAGE = "all_damage"
    ALL_RESISTANCES = "all_resistances"
    ELEMENTAL_DAMAGE = "elemental_damage"
    ELEMENTAL_RESISTANCES = "elemental_resistances"
    MANA_REGEN = "mana_regen"
    LIFE_REGEN = "life_regen"
    ARMOR_MOM = "armor_mind_over_matter"
    HEAL_EFFICIENCY = "heal_factor"
    MANAL_EFFICIENCY = "mana_efficiency"
    CRIT_RES = "crit_res"
    IIQ = "item_quant"
    IIR = "item_qual"
    HELM = "helms"
    HANDS = "gloves"
    ARMOR = "armors"
    BELT = "belts"
    BOOTS = "boots"
    WEAPON = "weapons"
    OFFHAND = "offhand"
    RELIC = "relics"
    AMULET = "amulets"
    SPEED = "speed"
    CSPEED = "cast_speed"
    RING = "rings"
    ITEM = "items"
    GOLD = "gold"
    EXPERIENCE = "exp"
    JEWEL = "jewel"
    DAMAGE_MOD = "damage_mod"
    LIFE_COST = "life_cost"
    MANA_COST = "mana_cost"
    COOLDOWN = "cooldown"
    PROJECTILES = "projectiles"
    AREA = "area"
    #Flags for projectiles
    PROJECTILE = "projectile"
    BOUNCE = "bounce"
    CURVE = "curve"
    CHAINS = "chains"
    ACCELERATE = "accelerate"
    DELAYED = "delayed"
    WANDER = "delayed_with_wandering"
    FLURRY_RELEASE = "released_flurry"
    PIERCING = "piercing"
    TRACK_STRICT = "tracking_strict"
    TRACK_LOOSE = "tracking_loose"
    AIMED_AT_PLAYER = "aimed_at_player"
    AIMED_AT_MOUSE = "aimed_at_mouse"
    AIMED_AT_CLOSEST = "aimed_at_closest"
    HARD_TRACKING = "hard_tracking"
    EXPLODES = "explodes"
    UNNATACH = "unnatached_barrage"
    WARN = "warning"
    #Flags for spells
    BARRAGE = "barrage"
    SPREAD = "spread"
    CHANNELED = "channeled"
    RANDOM_POSITION = "spawns_at_random_position"
    BUFF = "buff"
    DEBUFF = "debuff"
    DASH = "dash"
    AURA = "aura"
    CIRCULAR_BLAST = "spread_all_around"
    TRIGGER = "triggered"
    TRIGGER_ON_CRIT = "trigger_on_crit"
    #Flags for slashes
    CUTS_PROJECTILE = "cuts_proj"
    COMBO_SPELL = "combo_spell"
    CAN_TICK = "can_tick"
    #Flags for ennemies
    BOSS = "boss"
    RANDOM_MOVE = "move_randomly"
    SHOOTER = "shooter"
    CHASER = "chaser"
    SUICIDER = "suicider"
    PINNACLE = "unique_boss"
    MONOLITH = "monolith_boss"
    #Flags for levels
    WAVES = "waves"
    DUNGEON = "dungeon"
    RAID = "raid"
    HAS_BOSS = "has_boss"
    #Flags for description
    DESC_FLAT = "description_flat_attribute"
    DESC_PERCENT = "force_percentage_in_desc"
    DESC_UNIQUE = "desc_unique_effect"

META_FLAGS = [Flags.DESC_FLAT, Flags.DESC_PERCENT, Flags.DESC_UNIQUE,\
                Flags.BOON, Flags.HEX, Flags.BLESS, Flags.CURSE, Flags.FLAT]
GEAR_FLAGS = [Flags.HELM, Flags.BOOTS, Flags.ARMOR, Flags.HANDS, Flags.BELT,\
                Flags.RING, Flags.AMULET, Flags.RELIC, Flags.AMULET]
