""""A bunch of template for enemies."""

from data.numerics.ressource import Ressource, Stat
from data.constants import Flags

#TEMPLATE = [
#  0: image
#  1: name
#  2: statblock
#  3: flags
#  4: cooldown
#  5: exp modifier
#  6: gold modifier
#  7: Abilities (Spell, weight)
#  8: Animation delay (in second)
#  9: Hitbox adjustment (w, h, offset x, offset_y)
# ]

VOIDLING = {
    "image": "badguy",
    "name": "voidling",
    "stats": {
            "life": Ressource(20, "Life"),
            "mana": Ressource(10, "Mana"),
            "life_regen": Stat(0, "life_regen"),
            "mana_regen": Stat(0, "mana_regen"),
            "str": Stat(2, "Strength"),
            "dex": Stat(2, "Dexterity"),
            "int": Stat(2, "Intelligence"),
            "def": Stat(1, "Endurance"),
            "light": Stat(-0.5, "Light resistance", 0.9, scaling_value=0.005),
            "dark": Stat(0.2, "Dark resistance", 0.9, scaling_value=0.005),
            "dark_dmg": Stat(1.2, "Dark damage", scaling_value=0.05),
    },
    "flags": [Flags.CHASER],
    "cooldown": 0.34,
    "exp": 10,
    "gold": 10,
    "spelllist": [("e_charge", 1)],
    "delay": 0,
    "hitbox": (0.3, 0.5, 100, 10)
}

VOIDSNIPER = {
    "image": "necromancer",
    "name": "voidsniper",
    "stats": {
            "life": Ressource(10, "Life"),
            "mana": Ressource(10, "Mana"),
            "life_regen": Stat(0, "life_regen"),
            "mana_regen": Stat(0, "mana_regen"),
            "str": Stat(2, "Strength"),
            "dex": Stat(2, "Dexterity"),
            "int": Stat(2, "Intelligence"),
            "def": Stat(1, "Endurance"),
            "light": Stat(-0.5, "Light resistance", 0.9, scaling_value=0.005),
            "dark": Stat(0.2, "Dark resistance", 0.9, scaling_value=0.005),
            "dark_dmg": Stat(1.2, "Dark damage", scaling_value=0.05),
    },
    "flags": [Flags.SHOOTER],
    "cooldown": 1,
    "exp": 8,
    "gold": 8,
    "spelllist": [("e_voidbolt", 1)],
    "delay": 0.8,
    "hitbox": (0.2, 0.4, -60, -60)
}

VOIDBOMBER = {
    "image": "badguy",
    "name": "voidbomber",
    "stats": {
            "life": Ressource(1, "Life"),
            "mana": Ressource(1, "Mana"),
            "life_regen": Stat(0, "life_regen"),
            "mana_regen": Stat(0, "mana_regen"),
            "str": Stat(2, "Strength"),
            "dex": Stat(2, "Dexterity"),
            "int": Stat(2, "Intelligence"),
            "def": Stat(1, "Endurance"),
            "light": Stat(-0.5, "Light resistance", 0.9, scaling_value=0.005),
            "fire_dmg": Stat(2, "Dark damage", scaling_value=0.05),
            "speed": Stat(3, "speed", scaling_value=0),
    },
    "flags": [Flags.SUICIDER],
    "cooldown": 0.25,
    "exp": 6,
    "gold": 6,
    "spelllist": [("e_kamikaze", 1)],
    "delay": 0,
    "hitbox": None
}

VOIDBOSS = {
    "image": "boss_a",
    "name": "voidboss",
    "stats": {
            "life": Ressource(150, "Life"),
            "mana": Ressource(1, "Mana"),
            "life_regen": Stat(0, "life_regen"),
            "mana_regen": Stat(0, "mana_regen"),
            "str": Stat(10, "Strength"),
            "dex": Stat(10, "Dexterity"),
            "int": Stat(10, "Intelligence"),
            "def": Stat(10, "Endurance"),
            "light": Stat(-0.5, "Light resistance", 0.9, scaling_value=0.005),
            "fire_dmg": Stat(2, "Dark damage", scaling_value=0.05),
            "speed": Stat(1, "speed", scaling_value=0),
    },
    "flags": [Flags.BOSS, Flags.RANDOM_MOVE],
    "cooldown": 0.25,
    "exp": 15,
    "gold": 25,
    "spelllist": [("e_voidflurry", 1), ("e_voidspear", 0.7)],
    "delay": 0,
    "hitbox": None
}

MONOLITH = {
    "image": "monolith",
    "name": "monolith",
    "stats": {
            "life": Ressource(1500, "Life"),
            "mana": Ressource(1, "Mana"),
            "life_regen": Stat(0, "life_regen"),
            "mana_regen": Stat(0, "mana_regen"),
            "str": Stat(10, "Strength"),
            "dex": Stat(10, "Dexterity"),
            "int": Stat(10, "Intelligence"),
            "def": Stat(10, "Endurance"),
            "light": Stat(0.5, "Light resistance", 0.9, scaling_value=0),
            "dark": Stat(0.5, "Light resistance", 0.9, scaling_value=0),
            "fire": Stat(0.5, "Light resistance", 0.9, scaling_value=0),
            "ice": Stat(0.5, "Light resistance", 0.9, scaling_value=0),
            "elec": Stat(0.5, "Light resistance", 0.9, scaling_value=0),
            "energy": Stat(0.5, "Light resistance", 0.9, scaling_value=0),
            "speed": Stat(0.3, "speed", scaling_value=0),
    },
    "flags": [Flags.BOSS, Flags.PINNACLE, Flags.MONOLITH],
    "cooldown": 0.25,
    "exp": 15,
    "gold": 25,
    "spelllist": [("e_voidflurry", 1), ("e_voidspear", 0.7)],
    "delay": 0,
    "hitbox": None
}
