"""Stores the project's constants."""

from enum import Enum

from data.api.surface import mouse_position


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

FONT = None

LANGUAGE = None

BLUE = (3, 188, 255)
GREEN = (0, 143, 0)
ORANGE = (255, 210, 48)
BLACK = (0, 0, 0)
RED = (255, 25, 25)
CLEAN = (0, 0, 0, 0)
BLACK_TRANSP = (0, 0, 0, 0)
RED_TRANSP = (255, 0, 0, 155)
GREEN_TRANSP = (0, 255, 0, 155)
BLUE_TRANSP = (0, 0, 255, 155)
RED_PURE = (255, 0, 0, 255)
GREEN_PURE = (0, 255, 0, 255)
BLUE_PURE = (0, 0, 255, 255)
RED_WARNING = [255, 0, 0, 185]
RED_WEAK = (150, 0, 0)
YELLOW = (255, 196, 0)
LEVEL_COLOR = (252, 161, 3)
WHITE = (255,255,255)
BLUE_ALT = (3, 188, 255)
GREEN_WEAK = (0, 143, 0)
DAMAGE_COLOR = (255, 30, 30)

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
        "changed": True,
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
        "show_fps": False,
        "show_cards": True,
        "show_bars": False,
        "particles_enabled": True,
        "display_hp": True,
        "display_exp": False,
        "display_cd": True,
    },
    "lang": set(),
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

def get_mouse_pos():
    """Updates the mouse position."""
    x_factor = SCREEN_WIDTH / SYSTEM["options"]["screen_resolution"][0]
    y_factor = SCREEN_HEIGHT / SYSTEM["options"]["screen_resolution"][1]
    x, y = mouse_position()
    x *= x_factor
    y *= y_factor
    SYSTEM["mouse"] = (x, y)

def trad(keys, subkey = None) -> str:
    """Returns the translation data for the given key."""
    try:
        if subkey is None:
            return SYSTEM["lang"][keys]
        else:
            return SYSTEM["lang"][keys][subkey]
    except KeyError:
        return "[Unknown text data]"

WAVE_TIMER = "wave"
TICKER_TIMER = "ticker"
UPDATE_TIMER = "updoot"
WAVE_CHECK = "checkcheckcheck"

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
    LIFE_POT = "life_pot"
    MANA_POT = "mana_pot"
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
    DEBUFF_RES = "debuff_res"
    DEBUFF_LEN = "debuff_len"
    DEBUFF_RTE = "debuff_rte"
    DEBUFF_POT = "debuff_pot"
    DEBUFF_CHANCE = "debuff_chance"
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
    ANIMATION_SPEED = "anim_speed"
    PACK_SIZE = "pack_size"
    CANNOT_ACT = "stunned"
    POT_HEAL_FLAT = "potion_healing_flat"
    POT_HEAL_RELAT = "potion_healing_relative"
    POT_HEAL_COUNT = "potion_healing_count"
    POT_MANA_FLAT = "potion_mana_flat"
    POT_MANA_RELAT = "potion_mana_relative"
    POT_MANA_COUNT = "potion_mana_count"
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
    ARC_PARTICLE = "arc_particles"
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
    IMPACT_ANIMATION_RANDOM = "impact_anim_random"
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
    DESC_NO_SIGN = "desc_no_sign"
    DESC_HEAL = "desc_heal"
    DESC_HEAL_FLAT = "desc_heal_flat"
    DESC_LIFE = "desc_life"
    DESC_MANA = "desc_mana"

META_FLAGS = [Flags.DESC_FLAT, Flags.DESC_PERCENT, Flags.DESC_UNIQUE, Flags.DESC_NO_SIGN,\
                Flags.BOON, Flags.HEX, Flags.BLESS, Flags.CURSE, Flags.FLAT]
GEAR_FLAGS = [Flags.HELM, Flags.BOOTS, Flags.ARMOR, Flags.HANDS, Flags.BELT,\
                Flags.RING, Flags.AMULET, Flags.RELIC, Flags.AMULET]
