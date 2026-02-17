"""Table for spells levels effects."""

from data.constants import Flags
from data.numerics.affliction import Affliction

FIREBALL_LEVELS = {
    1: [],
    2: [
        Affliction("frb_lvl_dmg", 1.1, -1, [Flags.DAMAGE_MOD, Flags.BOON]),
        Affliction("frb_lvl_cost", 1.05, -1, [Flags.MANA_COST, Flags.BOON])
    ],
    3: [
        Affliction("frb_lvl_dmg", 1.2, -1, [Flags.DAMAGE_MOD, Flags.BOON]),
        Affliction("frb_lvl_cost", 1.1, -1, [Flags.MANA_COST, Flags.BOON])
    ],
    4: [
        Affliction("frb_lvl_dmg", 1.3, -1, [Flags.DAMAGE_MOD, Flags.BOON]),
        Affliction("frb_lvl_cost", 1.15, -1, [Flags.MANA_COST, Flags.BOON])
    ],
    5: [
        Affliction("frb_lvl_dmg", 1.5, -1, [Flags.DAMAGE_MOD, Flags.BOON]),
        Affliction("frb_lvl_cost", 1.25, -1, [Flags.MANA_COST, Flags.BOON])
    ],
    6: [
        Affliction("frb_lvl_dmg", 1.6, -1, [Flags.DAMAGE_MOD, Flags.BOON]),
        Affliction("frb_lvl_cost", 1.3, -1, [Flags.MANA_COST, Flags.BOON])
    ],
    7: [
        Affliction("frb_lvl_dmg", 1.7, -1, [Flags.DAMAGE_MOD, Flags.BOON]),
        Affliction("frb_lvl_cost", 1.35, -1, [Flags.MANA_COST, Flags.BOON])
    ],
    8: [
        Affliction("frb_lvl_dmg", 1.8, -1, [Flags.DAMAGE_MOD, Flags.BOON]),
        Affliction("frb_lvl_cost", 1.4, -1, [Flags.MANA_COST, Flags.BOON])
    ],
    9: [
        Affliction("frb_lvl_dmg", 2, -1, [Flags.DAMAGE_MOD, Flags.BOON]),
        Affliction("frb_lvl_cost", 1.5, -1, [Flags.MANA_COST, Flags.BOON])
    ],
    10: [
        Affliction("frb_lvl_dmg", 2.1, -1, [Flags.DAMAGE_MOD, Flags.BOON]),
        Affliction("frb_lvl_cost", 1.6, -1, [Flags.MANA_COST, Flags.BOON])
    ],
    11: [
        Affliction("frb_lvl_dmg", 2.2, -1, [Flags.DAMAGE_MOD, Flags.BOON]),
        Affliction("frb_lvl_cost", 1.7, -1, [Flags.MANA_COST, Flags.BOON])
    ],
    12: [
        Affliction("frb_lvl_dmg", 2.3, -1, [Flags.DAMAGE_MOD, Flags.BOON]),
        Affliction("frb_lvl_cost", 1.8, -1, [Flags.MANA_COST, Flags.BOON])
    ],
    13: [
        Affliction("frb_lvl_dmg", 2.4, -1, [Flags.DAMAGE_MOD, Flags.BOON]),
        Affliction("frb_lvl_cost", 1.9, -1, [Flags.MANA_COST, Flags.BOON])
    ],
    14: [
        Affliction("frb_lvl_dmg", 2.5, -1, [Flags.DAMAGE_MOD, Flags.BOON]),
        Affliction("frb_lvl_cost", 2, -1, [Flags.MANA_COST, Flags.BOON])
    ],
    15: [
        Affliction("frb_lvl_dmg", 2.6, -1, [Flags.DAMAGE_MOD, Flags.BOON]),
        Affliction("frb_lvl_cost", 2.05, -1, [Flags.MANA_COST, Flags.BOON])
    ],
    16: [
        Affliction("frb_lvl_dmg", 2.7, -1, [Flags.DAMAGE_MOD, Flags.BOON]),
        Affliction("frb_lvl_cost", 2.1, -1, [Flags.MANA_COST, Flags.BOON])
    ],
    17: [
        Affliction("frb_lvl_dmg", 2.8, -1, [Flags.DAMAGE_MOD, Flags.BOON]),
        Affliction("frb_lvl_cost", 2.15, -1, [Flags.MANA_COST, Flags.BOON])
    ],
    18: [
        Affliction("frb_lvl_dmg", 2.9, -1, [Flags.DAMAGE_MOD, Flags.BOON]),
        Affliction("frb_lvl_cost", 2.2, -1, [Flags.MANA_COST, Flags.BOON])
    ],
    19: [
        Affliction("frb_lvl_dmg", 3, -1, [Flags.DAMAGE_MOD, Flags.BOON]),
        Affliction("frb_lvl_cost", 2.25, -1, [Flags.MANA_COST, Flags.BOON])
    ],
    20: [
        Affliction("frb_lvl_dmg", 3.5, -1, [Flags.DAMAGE_MOD, Flags.BOON]),
        Affliction("frb_lvl_cost", 2.3, -1, [Flags.MANA_COST, Flags.BOON])
    ]
}

TEMPLATE = {
    1: [],
    2: [],
    3: [],
    4: [],
    5: [],
    6: [],
    7: [],
    8: [],
    9: [],
    10: [],
    11: [],
    12: [],
    13: [],
    14: [],
    15: [],
    16: [],
    17: [],
    18: [],
    19: [],
    20: []
}