"""Table for level affixes."""

from data.constants import Flags
from data.numerics.affix import Affix

MODIFIERS = {
    "life": ([
        (Affix("AREA_LIFE_1", 0.1, [Flags.BOON, Flags.LIFE], level_modifier=True), 1, 0, 60),
        (Affix("AREA_LIFE_2", 0.3, [Flags.BOON, Flags.LIFE], level_modifier=True), 0.8, 0, 60),
        (Affix("AREA_LIFE_3", 0.5, [Flags.BOON, Flags.LIFE], level_modifier=True), 0.6, 10, 80),
        (Affix("AREA_LIFE_4", 0.7, [Flags.BOON, Flags.LIFE], level_modifier=True), 0.5, 10, 80),
        (Affix("AREA_LIFE_5", 0.9, [Flags.BOON, Flags.LIFE], level_modifier=True), 0.4, 20, 90),
        (Affix("AREA_LIFE_6", 1.25, [Flags.BOON, Flags.LIFE], level_modifier=True), 0.4, 25, 999),
        (Affix("AREA_LIFE_7", 1.6, [Flags.BOON, Flags.LIFE], level_modifier=True), 0.3, 40, 999),
        (Affix("AREA_LIFE_8", 2, [Flags.BOON, Flags.LIFE], level_modifier=True), 0.3, 50, 999),
        (Affix("AREA_LIFE_9", 3, [Flags.BOON, Flags.LIFE], level_modifier=True), 0.2, 50, 999),
    ], 1, 1),
    "damage": ([
        (Affix("AREA_DMG_1", 0.1, [Flags.BOON, Flags.ALL_DAMAGE], level_modifier=True), 1, 0, 60),
        (Affix("AREA_DMG_2", 0.3, [Flags.BOON, Flags.ALL_DAMAGE], level_modifier=True), 0.8, 0, 60),
        (Affix("AREA_DMG_3", 0.5, [Flags.BOON, Flags.ALL_DAMAGE], level_modifier=True), 0.6, 10, 80),
        (Affix("AREA_DMG_4", 0.7, [Flags.BOON, Flags.ALL_DAMAGE], level_modifier=True), 0.5, 10, 80),
        (Affix("AREA_DMG_5", 1.1, [Flags.BOON, Flags.ALL_DAMAGE], level_modifier=True), 0.4, 20, 90),
        (Affix("AREA_DMG_6", 1.5, [Flags.BOON, Flags.ALL_DAMAGE], level_modifier=True), 0.4, 25, 999),
        (Affix("AREA_DMG_7", 2, [Flags.BOON, Flags.ALL_DAMAGE], level_modifier=True), 0.3, 40, 999),
    ], 0.7, 1.2),
    "res": ([
        (Affix("AREA_RES_1", 0.02, [Flags.BOON, Flags.ALL_RESISTANCES], level_modifier=True), 1, 0, 60),
        (Affix("AREA_RES_2", 0.1, [Flags.BOON, Flags.ALL_RESISTANCES], level_modifier=True), 0.8, 0, 60),
        (Affix("AREA_RES_3", 0.15, [Flags.BOON, Flags.ALL_RESISTANCES], level_modifier=True), 0.6, 10, 80),
        (Affix("AREA_RES_4", 0.2, [Flags.BOON, Flags.ALL_RESISTANCES], level_modifier=True), 0.5, 10, 80),
        (Affix("AREA_RES_5", 0.3, [Flags.BOON, Flags.ALL_RESISTANCES], level_modifier=True), 0.4, 20, 90),
        (Affix("AREA_RES_6", 0.4, [Flags.BOON, Flags.ALL_RESISTANCES], level_modifier=True), 0.4, 25, 999),
        (Affix("AREA_RES_7", 0.6, [Flags.BOON, Flags.ALL_RESISTANCES], level_modifier=True), 0.3, 40, 999),
    ], 0.2, 2.2),
    "dodge": ([
        (Affix("AREA_DODGE_1", 0.05, [Flags.FLAT, Flags.DODGE], level_modifier=True), 1, 0, 60),
        (Affix("AREA_DODGE_2", 0.08, [Flags.FLAT, Flags.DODGE], level_modifier=True), 0.8, 0, 60),
        (Affix("AREA_DODGE_3", 0.1, [Flags.FLAT, Flags.DODGE], level_modifier=True), 0.6, 10, 80),
        (Affix("AREA_DODGE_4", 0.12, [Flags.FLAT, Flags.DODGE], level_modifier=True), 0.5, 10, 80),
        (Affix("AREA_DODGE_5", 0.2, [Flags.FLAT, Flags.DODGE], level_modifier=True), 0.4, 20, 90),
        (Affix("AREA_DODGE_6", 0.25, [Flags.FLAT, Flags.DODGE], level_modifier=True), 0.4, 25, 999),
        (Affix("AREA_DODGE_7", 0.33, [Flags.FLAT, Flags.DODGE], level_modifier=True), 0.3, 40, 999),
    ], 0.25, 5),
    "block": ([
        (Affix("AREA_BLOCK_1", 0.05, [Flags.FLAT, Flags.BLOCK], level_modifier=True), 1, 0, 60),
        (Affix("AREA_BLOCK_2", 0.08, [Flags.FLAT, Flags.BLOCK], level_modifier=True), 0.8, 0, 60),
        (Affix("AREA_BLOCK_3", 0.1, [Flags.FLAT, Flags.BLOCK], level_modifier=True), 0.6, 10, 80),
        (Affix("AREA_BLOCK_4", 0.12, [Flags.FLAT, Flags.BLOCK], level_modifier=True), 0.5, 10, 80),
        (Affix("AREA_BLOCK_5", 0.2, [Flags.FLAT, Flags.BLOCK], level_modifier=True), 0.4, 20, 90),
        (Affix("AREA_BLOCK_6", 0.25, [Flags.FLAT, Flags.BLOCK], level_modifier=True), 0.4, 25, 999),
        (Affix("AREA_BLOCK_7", 0.33, [Flags.FLAT, Flags.BLOCK], level_modifier=True), 0.3, 40, 999),
    ], 0.25, 5),
    "move_speed": ([
        (Affix("AREA_MSPEED_1", 0.1, [Flags.BOON, Flags.SPEED], level_modifier=True), 1, 0, 60),
        (Affix("AREA_MSPEED_2", 0.3, [Flags.BOON, Flags.SPEED], level_modifier=True), 0.8, 0, 60),
        (Affix("AREA_MSPEED_3", 0.5, [Flags.BOON, Flags.SPEED], level_modifier=True), 0.6, 10, 80),
        (Affix("AREA_MSPEED_4", 0.7, [Flags.BOON, Flags.SPEED], level_modifier=True), 0.5, 10, 80),
        (Affix("AREA_MSPEED_5", 1.1, [Flags.BOON, Flags.SPEED], level_modifier=True), 0.4, 20, 90),
        (Affix("AREA_MSPEED_6", 1.5, [Flags.BOON, Flags.SPEED], level_modifier=True), 0.4, 25, 999),
        (Affix("AREA_MSPEED_7", 2, [Flags.BOON, Flags.SPEED], level_modifier=True), 0.3, 40, 999),
    ], 1, 1),
    "cast_speed": ([
        (Affix("AREA_CSPEED_1", 0.1, [Flags.BOON, Flags.CSPEED], level_modifier=True), 1, 0, 60),
        (Affix("AREA_CSPEED_2", 0.3, [Flags.BOON, Flags.CSPEED], level_modifier=True), 0.8, 0, 60),
        (Affix("AREA_CSPEED_3", 0.5, [Flags.BOON, Flags.CSPEED], level_modifier=True), 0.6, 10, 80),
        (Affix("AREA_CSPEED_4", 0.7, [Flags.BOON, Flags.CSPEED], level_modifier=True), 0.5, 10, 80),
        (Affix("AREA_CSPEED_5", 1.1, [Flags.BOON, Flags.CSPEED], level_modifier=True), 0.4, 20, 90),
        (Affix("AREA_CSPEED_6", 1.5, [Flags.BOON, Flags.CSPEED], level_modifier=True), 0.4, 25, 999),
        (Affix("AREA_CSPEED_7", 2, [Flags.BOON, Flags.CSPEED], level_modifier=True), 0.3, 40, 999),
    ], 0.7, 1.2),
}

AREA_WEIGHTS = sum(t[1][1] for t in MODIFIERS.items())
