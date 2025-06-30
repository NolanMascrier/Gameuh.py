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
# ]

VOIDLING = [
    "badguy",
    "Voidling",
    {
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
    [
        Flags.CHASER
    ],
    0.34,
    10,
    10,
    [
        ("e_charge", 1)
    ]
]

VOIDSNIPER = [
    "badguy",
    "Void Sniper",
    {
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
    [
        Flags.SHOOTER
    ],
    1,
    8,
    8,
    [
        ("e_voidbolt", 1)
    ]
]
