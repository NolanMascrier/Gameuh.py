"""Generates random loot."""

import random
from data.item import Item
from data.constants import SYSTEM, Flags
from data.numerics.affix import Affix

#Affix format : ARMOR TYPE > AFFIX > TIER, WEIGHT, MIN LEVEL TO SHOW, MAX LEVEL TO SHOW
IMPLICITS = {
    "rusted_armor": Affix("IMPLICIT_ARMOR", 250, [Flags.FLAT, Flags.DEF, Flags.DESC_FLAT]),
    "iron_armor": Affix("IMPLICIT_ARMOR", 500, [Flags.FLAT, Flags.DEF, Flags.DESC_FLAT]),
    "chain_armor": Affix("IMPLICIT_ARMOR", 5, [Flags.FLAT, Flags.DEX, Flags.DESC_FLAT]),
    "chain_armor2": Affix("IMPLICIT_ARMOR2", 5, [Flags.FLAT, Flags.STR, Flags.DESC_FLAT]),
    "plate_armor": Affix("IMPLICIT_ARMOR", 1000, [Flags.FLAT, Flags.DEF, Flags.DESC_FLAT]),
    "dragon_armor": Affix("IMPLICIT_ARMOR", 2000, [Flags.FLAT, Flags.DEF, Flags.DESC_FLAT]),
    "bushi_armor": Affix("IMPLICIT_ARMOR", 0.02, [Flags.FLAT, Flags.CRIT_CHANCE]),
    "diamond_armor": Affix("IMPLICIT_ARMOR", 0.05, [Flags.FLAT, Flags.ALL_RESISTANCES]),

    "worker_clothes": Affix("IMPLICIT_ARMOR", 250, [Flags.FLAT, Flags.DODGE_RATING, Flags.DESC_FLAT]),
    "gambeson": Affix("IMPLICIT_ARMOR", 500, [Flags.FLAT, Flags.DODGE_RATING, Flags.DESC_FLAT]),
    "leather_armor": Affix("IMPLICIT_ARMOR", 1000, [Flags.FLAT, Flags.DODGE_RATING, Flags.DESC_FLAT]),
    "brigandine": Affix("IMPLICIT_ARMOR", 1500, [Flags.FLAT, Flags.DODGE_RATING, Flags.DESC_FLAT]),
    "vagabond": Affix("IMPLICIT_ARMOR", 0.03, [Flags.FLAT, Flags.DODGE]),
    "heroic": Affix("IMPLICIT_ARMOR", 0.05, [Flags.BLESS, Flags.LIFE]),
    "dark": Affix("IMPLICIT_ARMOR", 3500, [Flags.FLAT, Flags.DODGE_RATING, Flags.DESC_FLAT]),

    "armor_mom": Affix("armor_mind_over_matter", 1, [Flags.ARMOR_MOM, Flags.DESC_UNIQUE]),
    "robes": Affix("IMPLICIT_ARMOR", 50, [Flags.FLAT, Flags.MANA, Flags.DESC_FLAT]),
    "gown": Affix("IMPLICIT_ARMOR", 75, [Flags.FLAT, Flags.MANA, Flags.DESC_FLAT]),
    "mage_coat": Affix("IMPLICIT_ARMOR", 100, [Flags.FLAT, Flags.MANA, Flags.DESC_FLAT]),
    "arcane_robes": Affix("IMPLICIT_ARMOR", 200, [Flags.FLAT, Flags.MANA, Flags.DESC_FLAT]),
    "arcane_gown": Affix("IMPLICIT_ARMOR", 150, [Flags.FLAT, Flags.MANA, Flags.DESC_FLAT]),
    "arcane_gown2": Affix("IMPLICIT_ARMOR2", 0.05, [Flags.BOON, Flags.MANA_REGEN]),
    "royal_coat": Affix("IMPLICIT_ARMOR", 250, [Flags.FLAT, Flags.MANA, Flags.DESC_FLAT]),
    "royal_coat2": Affix("IMPLICIT_ARMOR2", 0.05, [Flags.BOON, Flags.MANAL_EFFICIENCY]),
    "priest": Affix("IMPLICIT_ARMOR", 300, [Flags.FLAT, Flags.MANA, Flags.DESC_FLAT]),
    "priest2": Affix("IMPLICIT_ARMOR2", 0.5, [Flags.BOON, Flags.HEAL_EFFICIENCY]),
}
AFFIXES = {
    "armors": {
        "str": ([
            (Affix("ARMOR_STR_1", 5, [Flags.FLAT, Flags.DESC_FLAT, Flags.STR]), 1, 0, 25),
            (Affix("ARMOR_STR_2", 10, [Flags.FLAT, Flags.DESC_FLAT, Flags.STR]), 0.8, 0, 30),
            (Affix("ARMOR_STR_3", 15, [Flags.FLAT, Flags.DESC_FLAT, Flags.STR]), 0.5, 10, 40),
            (Affix("ARMOR_STR_4", 20, [Flags.FLAT, Flags.DESC_FLAT, Flags.STR]), 0.3, 20, 60),
            (Affix("ARMOR_STR_5", 30, [Flags.FLAT, Flags.DESC_FLAT, Flags.STR]), 0.2, 30, 80),
            (Affix("ARMOR_STR_6", 40, [Flags.FLAT, Flags.DESC_FLAT, Flags.STR]), 0.1, 50, 999),
            (Affix("ARMOR_STR_7", 65, [Flags.FLAT, Flags.DESC_FLAT, Flags.STR]), 0.05, 75, 999),
        ], 1),
        "dex": ([
            (Affix("ARMOR_DEX_1", 5, [Flags.FLAT, Flags.DESC_FLAT, Flags.DEX]), 1, 0, 25),
            (Affix("ARMOR_DEX_2", 10, [Flags.FLAT, Flags.DESC_FLAT, Flags.DEX]), 0.8, 0, 30),
            (Affix("ARMOR_DEX_3", 15, [Flags.FLAT, Flags.DESC_FLAT, Flags.DEX]), 0.5, 10, 40),
            (Affix("ARMOR_DEX_4", 20, [Flags.FLAT, Flags.DESC_FLAT, Flags.DEX]), 0.3, 20, 60),
            (Affix("ARMOR_DEX_5", 30, [Flags.FLAT, Flags.DESC_FLAT, Flags.DEX]), 0.2, 30, 80),
            (Affix("ARMOR_DEX_6", 40, [Flags.FLAT, Flags.DESC_FLAT, Flags.DEX]), 0.1, 50, 999),
            (Affix("ARMOR_DEX_7", 65, [Flags.FLAT, Flags.DESC_FLAT, Flags.DEX]), 0.05, 75, 999),
        ], 1),
        "int": ([
            (Affix("ARMOR_INT_1", 5, [Flags.FLAT, Flags.DESC_FLAT, Flags.INT]), 1, 0, 25),
            (Affix("ARMOR_INT_2", 10, [Flags.FLAT, Flags.DESC_FLAT, Flags.INT]), 0.8, 0, 30),
            (Affix("ARMOR_INT_3", 15, [Flags.FLAT, Flags.DESC_FLAT, Flags.INT]), 0.5, 10, 40),
            (Affix("ARMOR_INT_4", 20, [Flags.FLAT, Flags.DESC_FLAT, Flags.INT]), 0.3, 20, 60),
            (Affix("ARMOR_INT_5", 30, [Flags.FLAT, Flags.DESC_FLAT, Flags.INT]), 0.2, 30, 80),
            (Affix("ARMOR_INT_6", 40, [Flags.FLAT, Flags.DESC_FLAT, Flags.INT]), 0.1, 50, 999),
            (Affix("ARMOR_INT_7", 65, [Flags.FLAT, Flags.DESC_FLAT, Flags.INT]), 0.05, 75, 999),
        ], 1),
        "life": ([
            (Affix("ARMOR_LIFE_1", 10, [Flags.FLAT, Flags.DESC_FLAT, Flags.LIFE]), 1, 0, 25),
            (Affix("ARMOR_LIFE_2", 25, [Flags.FLAT, Flags.DESC_FLAT, Flags.LIFE]), 0.8, 0, 30),
            (Affix("ARMOR_LIFE_3", 50, [Flags.FLAT, Flags.DESC_FLAT, Flags.LIFE]), 0.5, 10, 40),
            (Affix("ARMOR_LIFE_4", 75, [Flags.FLAT, Flags.DESC_FLAT, Flags.LIFE]), 0.3, 20, 60),
            (Affix("ARMOR_LIFE_5", 100, [Flags.FLAT, Flags.DESC_FLAT, Flags.LIFE]), 0.2, 30, 80),
            (Affix("ARMOR_LIFE_6", 150, [Flags.FLAT, Flags.DESC_FLAT, Flags.LIFE]), 0.1, 50, 999),
            (Affix("ARMOR_LIFE_7", 250, [Flags.FLAT, Flags.DESC_FLAT, Flags.LIFE]), 0.05, 75, 999),
        ], 1),
        "life_incr": ([
            (Affix("ARMOR_LIFE_INCR_1", 0.10, [Flags.BOON, Flags.LIFE]), 1, 0, 25),
            (Affix("ARMOR_LIFE_INCR_2", 0.15, [Flags.BOON, Flags.LIFE]), 0.6, 15, 40),
            (Affix("ARMOR_LIFE_INCR_3", 0.20, [Flags.BOON, Flags.LIFE]), 0.3, 25, 60),
            (Affix("ARMOR_LIFE_INCR_4", 0.30, [Flags.BOON, Flags.LIFE]), 0.15, 50, 999),
            (Affix("ARMOR_LIFE_INCR_5", 0.50, [Flags.BOON, Flags.LIFE]), 0.01, 75, 999)
        ], 0.8),
        "life_more": ([
            (Affix("ARMOR_LIFE_MORE_1", 0.5, [Flags.BLESS, Flags.LIFE]), 1, 25, 75),
            (Affix("ARMOR_LIFE_MORE_2", 0.15, [Flags.BLESS, Flags.LIFE]), 0.6, 30, 999),
            (Affix("ARMOR_LIFE_MORE_3", 0.20, [Flags.BLESS, Flags.LIFE]), 0.3, 75, 999),
        ], 0.2),
        "mana": ([
            (Affix("ARMOR_MANA_1", 10, [Flags.FLAT, Flags.DESC_FLAT, Flags.MANA]), 1, 0, 25),
            (Affix("ARMOR_MANA_2", 25, [Flags.FLAT, Flags.DESC_FLAT, Flags.MANA]), 0.8, 0, 30),
            (Affix("ARMOR_MANA_3", 50, [Flags.FLAT, Flags.DESC_FLAT, Flags.MANA]), 0.5, 10, 40),
            (Affix("ARMOR_MANA_4", 75, [Flags.FLAT, Flags.DESC_FLAT, Flags.MANA]), 0.3, 20, 60),
            (Affix("ARMOR_MANA_5", 100, [Flags.FLAT, Flags.DESC_FLAT, Flags.MANA]), 0.2, 30, 80),
            (Affix("ARMOR_MANA_6", 150, [Flags.FLAT, Flags.DESC_FLAT, Flags.MANA]), 0.1, 50, 999),
            (Affix("ARMOR_MANA_7", 250, [Flags.FLAT, Flags.DESC_FLAT, Flags.MANA]), 0.05, 75, 999),
        ], 1),
        "mana_incr": ([
            (Affix("ARMOR_MANA_INCR_1", 0.10, [Flags.BOON, Flags.MANA]), 1, 0, 25),
            (Affix("ARMOR_MANA_INCR_2", 0.15, [Flags.BOON, Flags.MANA]), 0.6, 15, 40),
            (Affix("ARMOR_MANA_INCR_3", 0.20, [Flags.BOON, Flags.MANA]), 0.3, 25, 60),
            (Affix("ARMOR_MANA_INCR_4", 0.30, [Flags.BOON, Flags.MANA]), 0.15, 50, 999),
            (Affix("ARMOR_MANA_INCR_5", 0.50, [Flags.BOON, Flags.MANA]), 0.01, 75, 999)
        ], 0.8),
        "mana_more": ([
            (Affix("ARMOR_MANA_MORE_1", 0.05, [Flags.BLESS, Flags.MANA]), 1, 25, 75),
            (Affix("ARMOR_MANA_MORE_2", 0.15, [Flags.BLESS, Flags.MANA]), 0.6, 30, 999),
            (Affix("ARMOR_MANA_MORE_3", 0.20, [Flags.BLESS, Flags.MANA]), 0.3, 75, 999),
        ], 0.2),
        "endurance": ([
            (Affix("ARMOR_DEF_1", 100, [Flags.FLAT, Flags.DESC_FLAT, Flags.DEF]), 1, 0, 30),
            (Affix("ARMOR_DEF_2", 250, [Flags.FLAT, Flags.DESC_FLAT, Flags.DEF]), 0.8, 0, 30),
            (Affix("ARMOR_DEF_3", 500, [Flags.FLAT, Flags.DESC_FLAT, Flags.DEF]), 0.5, 10, 40),
            (Affix("ARMOR_DEF_4", 750, [Flags.FLAT, Flags.DESC_FLAT, Flags.DEF]), 0.3, 20, 60),
            (Affix("ARMOR_DEF_5", 1000, [Flags.FLAT, Flags.DESC_FLAT, Flags.DEF]), 0.2, 30, 80),
            (Affix("ARMOR_DEF_6", 1500, [Flags.FLAT, Flags.DESC_FLAT, Flags.DEF]), 0.1, 50, 999),
            (Affix("ARMOR_DEF_7", 2500, [Flags.FLAT, Flags.DESC_FLAT, Flags.DEF]), 0.05, 75, 999),
        ], 1.2),
        "dodge": ([
            (Affix("ARMOR_DODGE_RATING_1", 100, [Flags.FLAT, Flags.DESC_FLAT, Flags.DODGE_RATING]), 1, 0, 30),
            (Affix("ARMOR_DODGE_RATING_2", 250, [Flags.FLAT, Flags.DESC_FLAT, Flags.DODGE_RATING]), 0.8, 0, 30),
            (Affix("ARMOR_DODGE_RATING_3", 500, [Flags.FLAT, Flags.DESC_FLAT, Flags.DODGE_RATING]), 0.5, 10, 40),
            (Affix("ARMOR_DODGE_RATING_4", 750, [Flags.FLAT, Flags.DESC_FLAT, Flags.DODGE_RATING]), 0.3, 20, 60),
            (Affix("ARMOR_DODGE_RATING_5", 1000, [Flags.FLAT, Flags.DESC_FLAT, Flags.DODGE_RATING]), 0.2, 30, 80),
            (Affix("ARMOR_DODGE_RATING_6", 1500, [Flags.FLAT, Flags.DESC_FLAT, Flags.DODGE_RATING]), 0.1, 50, 999),
            (Affix("ARMOR_DODGE_RATING_7", 2500, [Flags.FLAT, Flags.DESC_FLAT, Flags.DODGE_RATING]), 0.05, 75, 999),
        ], 1.2),
        "dodge": ([
            (Affix("ARMOR_DODGE_1", 0.01, [Flags.FLAT, Flags.DESC_PERCENT, Flags.DODGE]), 1, 0, 999),
            (Affix("ARMOR_DODGE_2", 0.02, [Flags.FLAT, Flags.DESC_PERCENT, Flags.DODGE]), 0.5, 25, 999),
            (Affix("ARMOR_DODGE_3", 0.05, [Flags.FLAT, Flags.DESC_PERCENT, Flags.DODGE]), 0.1, 75, 999),
        ], 0.2),
        "phys_res": ([
            (Affix("ARMOR_PHYS_RES_1", 0.10, [Flags.PHYS, Flags.FLAT]), 1, 0, 60),
            (Affix("ARMOR_PHYS_RES_2", 0.25, [Flags.PHYS, Flags.FLAT]), 0.6, 10, 90),
            (Affix("ARMOR_PHYS_RES_3", 0.40, [Flags.PHYS, Flags.FLAT]), 0.3, 25, 999),
        ], 1),
        "fire_res": ([
            (Affix("ARMOR_FIRE_RES_1", 0.10, [Flags.FIRE, Flags.FLAT]), 1, 0, 60),
            (Affix("ARMOR_FIRE_RES_2", 0.25, [Flags.FIRE, Flags.FLAT]), 0.6, 10, 90),
            (Affix("ARMOR_FIRE_RES_3", 0.40, [Flags.FIRE, Flags.FLAT]), 0.3, 25, 999),
        ], 1),
        "ice_res": ([
            (Affix("ARMOR_ICE_RES_1", 0.10, [Flags.ICE, Flags.FLAT]), 1, 0, 60),
            (Affix("ARMOR_ICE_RES_2", 0.25, [Flags.ICE, Flags.FLAT]), 0.6, 10, 90),
            (Affix("ARMOR_ICE_RES_3", 0.40, [Flags.ICE, Flags.FLAT]), 0.3, 25, 999),
        ], 1),
        "elec_res": ([
            (Affix("ARMOR_ELEC_RES_1", 0.10, [Flags.ELEC, Flags.FLAT]), 1, 0, 60),
            (Affix("ARMOR_ELEC_RES_2", 0.25, [Flags.ELEC, Flags.FLAT]), 0.6, 10, 90),
            (Affix("ARMOR_ELEC_RES_3", 0.40, [Flags.ELEC, Flags.FLAT]), 0.3, 25, 999),
        ], 1),
        "light_res": ([
            (Affix("ARMOR_LIGHT_RES_1", 0.10, [Flags.LIGHT, Flags.FLAT]), 1, 0, 60),
            (Affix("ARMOR_LIGHT_RES_2", 0.25, [Flags.LIGHT, Flags.FLAT]), 0.6, 10, 90),
            (Affix("ARMOR_LIGHT_RES_3", 0.40, [Flags.LIGHT, Flags.FLAT]), 0.3, 25, 999),
        ], 1),
        "dark_res": ([
            (Affix("ARMOR_DARK_RES_1", 0.10, [Flags.DARK, Flags.FLAT]), 1, 0, 60),
            (Affix("ARMOR_DARK_RES_2", 0.25, [Flags.DARK, Flags.FLAT]), 0.6, 10, 90),
            (Affix("ARMOR_DARK_RES_3", 0.40, [Flags.DARK, Flags.FLAT]), 0.3, 25, 999),
        ], 1),
        "energ_res": ([
            (Affix("ARMOR_ENERG_RES_1", 0.10, [Flags.ENERG, Flags.FLAT]), 1, 0, 60),
            (Affix("ARMOR_ENERG_RES_2", 0.25, [Flags.ENERG, Flags.FLAT]), 0.6, 10, 90),
            (Affix("ARMOR_ENERG_RES_3", 0.40, [Flags.ENERG, Flags.FLAT]), 0.3, 25, 999),
        ], 1),
        "elemental_res": ([
            (Affix("ARMOR_ELEMENTAL_RESISTANCES_1", 0.10, [Flags.ELEMENTAL_RESISTANCES,\
                                                            Flags.FLAT]), 1, 20, 60),
            (Affix("ARMOR_ELEMENTAL_RESISTANCES_2", 0.25, [Flags.ELEMENTAL_RESISTANCES,\
                                                            Flags.FLAT]), 0.6, 40, 90),
            (Affix("ARMOR_ELEMENTAL_RESISTANCES_3", 0.40, [Flags.ELEMENTAL_RESISTANCES,\
                                                            Flags.FLAT]), 0.3, 60, 999),
        ], 0.8),
        "crit_res": ([
            (Affix("ARMOR_CRIT_RES_1", 0.05, [Flags.CRIT_RES, Flags.FLAT]), 1, 0, 60),
            (Affix("ARMOR_CRIT_RES_2", 0.1, [Flags.ENERG, Flags.FLAT]), 0.6, 10, 90),
            (Affix("ARMOR_CRIT_RES_3", 0.2, [Flags.ENERG, Flags.FLAT]), 0.3, 25, 999),
        ], 0.5),
        "all_res": ([
            (Affix("ARMOR_ALL_RESISTANCES_1", 0.10, [Flags.ALL_RESISTANCES,\
                                                        Flags.FLAT]), 1, 20, 60),
            (Affix("ARMOR_ALL_RESISTANCES_2", 0.25, [Flags.ALL_RESISTANCES,\
                                                        Flags.FLAT]), 0.6, 40, 90),
            (Affix("ARMOR_ALL_RESISTANCES_3", 0.40, [Flags.ALL_RESISTANCES,\
                                                        Flags.FLAT]), 0.3, 60, 999),
        ], 0.25),
    },
    "helms": {
        "str": ([
            (Affix("HELM_STR_1", 5, [Flags.FLAT, Flags.DESC_FLAT, Flags.STR]), 1, 0, 25),
            (Affix("HELM_STR_2", 10, [Flags.FLAT, Flags.DESC_FLAT, Flags.STR]), 0.8, 0, 30),
            (Affix("HELM_STR_3", 15, [Flags.FLAT, Flags.DESC_FLAT, Flags.STR]), 0.5, 10, 40),
            (Affix("HELM_STR_4", 20, [Flags.FLAT, Flags.DESC_FLAT, Flags.STR]), 0.3, 20, 60),
            (Affix("HELM_STR_5", 30, [Flags.FLAT, Flags.DESC_FLAT, Flags.STR]), 0.2, 30, 80),
            (Affix("HELM_STR_6", 40, [Flags.FLAT, Flags.DESC_FLAT, Flags.STR]), 0.1, 50, 999),
            (Affix("HELM_STR_7", 65, [Flags.FLAT, Flags.DESC_FLAT, Flags.STR]), 0.05, 75, 999),
        ], 1),
        "dex": ([
            (Affix("HELM_DEX_1", 5, [Flags.FLAT, Flags.DESC_FLAT, Flags.DEX]), 1, 0, 25),
            (Affix("HELM_DEX_2", 10, [Flags.FLAT, Flags.DESC_FLAT, Flags.DEX]), 0.8, 0, 30),
            (Affix("HELM_DEX_3", 15, [Flags.FLAT, Flags.DESC_FLAT, Flags.DEX]), 0.5, 10, 40),
            (Affix("HELM_DEX_4", 20, [Flags.FLAT, Flags.DESC_FLAT, Flags.DEX]), 0.3, 20, 60),
            (Affix("HELM_DEX_5", 30, [Flags.FLAT, Flags.DESC_FLAT, Flags.DEX]), 0.2, 30, 80),
            (Affix("HELM_DEX_6", 40, [Flags.FLAT, Flags.DESC_FLAT, Flags.DEX]), 0.1, 50, 999),
            (Affix("HELM_DEX_7", 65, [Flags.FLAT, Flags.DESC_FLAT, Flags.DEX]), 0.05, 75, 999),
        ], 1),
        "int": ([
            (Affix("HELM_INT_1", 5, [Flags.FLAT, Flags.DESC_FLAT, Flags.INT]), 1, 0, 25),
            (Affix("HELM_INT_2", 10, [Flags.FLAT, Flags.DESC_FLAT, Flags.INT]), 0.8, 0, 30),
            (Affix("HELM_INT_3", 15, [Flags.FLAT, Flags.DESC_FLAT, Flags.INT]), 0.5, 10, 40),
            (Affix("HELM_INT_4", 20, [Flags.FLAT, Flags.DESC_FLAT, Flags.INT]), 0.3, 20, 60),
            (Affix("HELM_INT_5", 30, [Flags.FLAT, Flags.DESC_FLAT, Flags.INT]), 0.2, 30, 80),
            (Affix("HELM_INT_6", 40, [Flags.FLAT, Flags.DESC_FLAT, Flags.INT]), 0.1, 50, 999),
            (Affix("HELM_INT_7", 65, [Flags.FLAT, Flags.DESC_FLAT, Flags.INT]), 0.05, 75, 999),
        ], 1),
        "life": ([
            (Affix("HELM_LIFE_1", 5, [Flags.FLAT, Flags.DESC_FLAT, Flags.LIFE]), 1, 0, 25),
            (Affix("HELM_LIFE_2", 15, [Flags.FLAT, Flags.DESC_FLAT, Flags.LIFE]), 0.8, 0, 30),
            (Affix("HELM_LIFE_3", 25, [Flags.FLAT, Flags.DESC_FLAT, Flags.LIFE]), 0.5, 10, 40),
            (Affix("HELM_LIFE_4", 50, [Flags.FLAT, Flags.DESC_FLAT, Flags.LIFE]), 0.3, 20, 60),
            (Affix("HELM_LIFE_5", 80, [Flags.FLAT, Flags.DESC_FLAT, Flags.LIFE]), 0.2, 30, 80),
            (Affix("HELM_LIFE_6", 100, [Flags.FLAT, Flags.DESC_FLAT, Flags.LIFE]), 0.1, 50, 999),
            (Affix("HELM_LIFE_7", 125, [Flags.FLAT, Flags.DESC_FLAT, Flags.LIFE]), 0.05, 75, 999),
        ], 1),
        "life_incr": ([
            (Affix("HELM_LIFE_INCR_1", 0.05, [Flags.BOON, Flags.LIFE]), 1, 0, 25),
            (Affix("HELM_LIFE_INCR_2", 0.1, [Flags.BOON, Flags.LIFE]), 0.6, 15, 40),
            (Affix("HELM_LIFE_INCR_3", 0.15, [Flags.BOON, Flags.LIFE]), 0.3, 25, 60),
            (Affix("HELM_LIFE_INCR_4", 0.20, [Flags.BOON, Flags.LIFE]), 0.15, 50, 999),
            (Affix("HELM_LIFE_INCR_5", 0.25, [Flags.BOON, Flags.LIFE]), 0.01, 75, 999)
        ], 0.8),
        "mana": ([
            (Affix("HELM_MANA_1", 5, [Flags.FLAT, Flags.DESC_FLAT, Flags.MANA]), 1, 0, 25),
            (Affix("HELM_MANA_2", 15, [Flags.FLAT, Flags.DESC_FLAT, Flags.MANA]), 0.8, 0, 30),
            (Affix("HELM_MANA_3", 25, [Flags.FLAT, Flags.DESC_FLAT, Flags.MANA]), 0.5, 10, 40),
            (Affix("HELM_MANA_4", 50, [Flags.FLAT, Flags.DESC_FLAT, Flags.MANA]), 0.3, 20, 60),
            (Affix("HELM_MANA_5", 80, [Flags.FLAT, Flags.DESC_FLAT, Flags.MANA]), 0.2, 30, 80),
            (Affix("HELM_MANA_6", 100, [Flags.FLAT, Flags.DESC_FLAT, Flags.MANA]), 0.1, 50, 999),
            (Affix("HELM_MANA_7", 125, [Flags.FLAT, Flags.DESC_FLAT, Flags.MANA]), 0.05, 75, 999),
        ], 1),
        "mana_incr": ([
            (Affix("HELM_MANA_INCR_1", 0.05, [Flags.BOON, Flags.MANA]), 1, 0, 25),
            (Affix("HELM_MANA_INCR_2", 0.1, [Flags.BOON, Flags.MANA]), 0.6, 15, 40),
            (Affix("HELM_MANA_INCR_3", 0.15, [Flags.BOON, Flags.MANA]), 0.3, 25, 60),
            (Affix("HELM_MANA_INCR_4", 0.20, [Flags.BOON, Flags.MANA]), 0.15, 50, 999),
            (Affix("HELM_MANA_INCR_5", 0.25, [Flags.BOON, Flags.MANA]), 0.01, 75, 999)
        ], 0.8),
        "endurance": ([
            (Affix("HELM_DEF_1", 50, [Flags.FLAT, Flags.DESC_FLAT, Flags.DEF]), 1, 0, 30),
            (Affix("HELM_DEF_2", 100, [Flags.FLAT, Flags.DESC_FLAT, Flags.DEF]), 0.8, 0, 30),
            (Affix("HELM_DEF_3", 200, [Flags.FLAT, Flags.DESC_FLAT, Flags.DEF]), 0.5, 10, 40),
            (Affix("HELM_DEF_4", 300, [Flags.FLAT, Flags.DESC_FLAT, Flags.DEF]), 0.3, 20, 60),
            (Affix("HELM_DEF_5", 500, [Flags.FLAT, Flags.DESC_FLAT, Flags.DEF]), 0.2, 30, 80),
            (Affix("HELM_DEF_6", 750, [Flags.FLAT, Flags.DESC_FLAT, Flags.DEF]), 0.1, 50, 999),
            (Affix("HELM_DEF_7", 1000, [Flags.FLAT, Flags.DESC_FLAT, Flags.DEF]), 0.05, 75, 999),
        ], 1.2),
        "dodge": ([
            (Affix("HELM_DODGE_RATING_1", 50, [Flags.FLAT, Flags.DESC_FLAT, Flags.DODGE_RATING]), 1, 0, 30),
            (Affix("HELM_DODGE_RATING_2", 100, [Flags.FLAT, Flags.DESC_FLAT, Flags.DODGE_RATING]), 0.8, 0, 30),
            (Affix("HELM_DODGE_RATING_3", 200, [Flags.FLAT, Flags.DESC_FLAT, Flags.DODGE_RATING]), 0.5, 10, 40),
            (Affix("HELM_DODGE_RATING_4", 300, [Flags.FLAT, Flags.DESC_FLAT, Flags.DODGE_RATING]), 0.3, 20, 60),
            (Affix("HELM_DODGE_RATING_5", 500, [Flags.FLAT, Flags.DESC_FLAT, Flags.DODGE_RATING]), 0.2, 30, 80),
            (Affix("HELM_DODGE_RATING_6", 750, [Flags.FLAT, Flags.DESC_FLAT, Flags.DODGE_RATING]), 0.1, 50, 999),
            (Affix("HELM_DODGE_RATING_7", 1000, [Flags.FLAT, Flags.DESC_FLAT, Flags.DODGE_RATING]), 0.05, 75, 999),
        ], 1.2),
        "precision": ([
            (Affix("HELM_PRECISION_1", 50, [Flags.FLAT, Flags.DESC_FLAT, Flags.PRECISION]), 1, 0, 30),
            (Affix("HELM_PRECISION_2", 100, [Flags.FLAT, Flags.DESC_FLAT, Flags.PRECISION]), 0.8, 0, 30),
            (Affix("HELM_PRECISION_3", 200, [Flags.FLAT, Flags.DESC_FLAT, Flags.PRECISION]), 0.5, 10, 40),
            (Affix("HELM_PRECISION_4", 300, [Flags.FLAT, Flags.DESC_FLAT, Flags.PRECISION]), 0.3, 20, 60),
            (Affix("HELM_PRECISION_5", 500, [Flags.FLAT, Flags.DESC_FLAT, Flags.PRECISION]), 0.2, 30, 80),
            (Affix("HELM_PRECISION_6", 750, [Flags.FLAT, Flags.DESC_FLAT, Flags.PRECISION]), 0.1, 50, 999),
            (Affix("HELM_PRECISION_7", 1000, [Flags.FLAT, Flags.DESC_FLAT, Flags.PRECISION]), 0.05, 75, 999),
        ], 10.9),
        "phys_res": ([
            (Affix("HELM_PHYS_RES_1", 0.08, [Flags.PHYS, Flags.FLAT]), 1, 0, 60),
            (Affix("HELM_PHYS_RES_2", 0.12, [Flags.PHYS, Flags.FLAT]), 0.6, 10, 90),
            (Affix("HELM_PHYS_RES_3", 0.2, [Flags.PHYS, Flags.FLAT]), 0.3, 25, 999),
        ], 1),
        "fire_res": ([
            (Affix("HELM_FIRE_RES_1", 0.08, [Flags.FIRE, Flags.FLAT]), 1, 0, 60),
            (Affix("HELM_FIRE_RES_2", 0.12, [Flags.FIRE, Flags.FLAT]), 0.6, 10, 90),
            (Affix("HELM_FIRE_RES_3", 0.2, [Flags.FIRE, Flags.FLAT]), 0.3, 25, 999),
        ], 1),
        "ice_res": ([
            (Affix("HELM_ICE_RES_1", 0.08, [Flags.ICE, Flags.FLAT]), 1, 0, 60),
            (Affix("HELM_ICE_RES_2", 0.12, [Flags.ICE, Flags.FLAT]), 0.6, 10, 90),
            (Affix("HELM_ICE_RES_3", 0.2, [Flags.ICE, Flags.FLAT]), 0.3, 25, 999),
        ], 1),
        "elec_res": ([
            (Affix("HELM_ELEC_RES_1", 0.08, [Flags.ELEC, Flags.FLAT]), 1, 0, 60),
            (Affix("HELM_ELEC_RES_2", 0.12, [Flags.ELEC, Flags.FLAT]), 0.6, 10, 90),
            (Affix("HELM_ELEC_RES_3", 0.2, [Flags.ELEC, Flags.FLAT]), 0.3, 25, 999),
        ], 1),
        "light_res": ([
            (Affix("HELM_LIGHT_RES_1", 0.08, [Flags.LIGHT, Flags.FLAT]), 1, 0, 60),
            (Affix("HELM_LIGHT_RES_2", 0.12, [Flags.LIGHT, Flags.FLAT]), 0.6, 10, 90),
            (Affix("HELM_LIGHT_RES_3", 0.2, [Flags.LIGHT, Flags.FLAT]), 0.3, 25, 999),
        ], 1),
        "dark_res": ([
            (Affix("HELM_DARK_RES_1", 0.08, [Flags.DARK, Flags.FLAT]), 1, 0, 60),
            (Affix("HELM_DARK_RES_2", 0.12, [Flags.DARK, Flags.FLAT]), 0.6, 10, 90),
            (Affix("HELM_DARK_RES_3", 0.2, [Flags.DARK, Flags.FLAT]), 0.3, 25, 999),
        ], 1),
        "energ_res": ([
            (Affix("HELM_ENERG_RES_1", 0.08, [Flags.ENERG, Flags.FLAT]), 1, 0, 60),
            (Affix("HELM_ENERG_RES_2", 0.12, [Flags.ENERG, Flags.FLAT]), 0.6, 10, 90),
            (Affix("HELM_ENERG_RES_3", 0.2, [Flags.ENERG, Flags.FLAT]), 0.3, 25, 999),
        ], 1),
        "elemental_res": ([
            (Affix("HELM_ELEMENTAL_RESISTANCES_1", 0.08, [Flags.ELEMENTAL_RESISTANCES,\
                                                            Flags.FLAT]), 1, 20, 60),
            (Affix("HELM_ELEMENTAL_RESISTANCES_2", 0.12, [Flags.ELEMENTAL_RESISTANCES,\
                                                            Flags.FLAT]), 0.6, 40, 90),
            (Affix("HELM_ELEMENTAL_RESISTANCES_3", 0.2, [Flags.ELEMENTAL_RESISTANCES,\
                                                            Flags.FLAT]), 0.3, 60, 999),
        ], 0.8),
        "all_res": ([
            (Affix("HELM_ALL_RESISTANCES_1", 0.08, [Flags.ALL_RESISTANCES,\
                                                        Flags.FLAT]), 1, 20, 60),
            (Affix("HELM_ALL_RESISTANCES_2", 0.12, [Flags.ALL_RESISTANCES,\
                                                        Flags.FLAT]), 0.6, 40, 90),
            (Affix("HELM_ALL_RESISTANCES_3", 0.2, [Flags.ALL_RESISTANCES,\
                                                        Flags.FLAT]), 0.3, 60, 999),
        ], 0.25),
    },
    "boots": {
        
    },
    "gloves": {
        
    },
    "rings": {
        
    },
    "amulets": {
        
    },
    "relics": {
        
    },
    "weapons": {
        
    },
    "offhands": {
        
    }
}

class LootGenerator():
    """Creates the loot generator, and with it the base items."""
    def __init__(self):
        self._armors = [
                (Item("", "Rusted armor", 5, 0, 1, SYSTEM["images"]["armors"][0],\
                    0, [Flags.ARMOR, Flags.GEAR], implicits=[IMPLICITS["rusted_armor"]]), 1),
                (Item("", "Iron armor", 25, 0, 1, SYSTEM["images"]["armors"][1],\
                    0, [Flags.ARMOR, Flags.GEAR], implicits=[IMPLICITS["iron_armor"]]), 0.8),
                (Item("", "Chainmail", 100, 0, 1, SYSTEM["images"]["armors"][2],\
                    0, [Flags.ARMOR, Flags.GEAR], implicits=[IMPLICITS["chain_armor"],\
                                                             IMPLICITS["chain_armor2"]]), 0.6),
                (Item("", "Plate armor", 500, 0, 1, SYSTEM["images"]["armors"][18],\
                    0, [Flags.ARMOR, Flags.GEAR], implicits=[IMPLICITS["plate_armor"]]), 0.5),
                (Item("", "Dragon armor", 1000, 0, 1, SYSTEM["images"]["armors"][47],\
                    0, [Flags.ARMOR, Flags.GEAR], implicits=[IMPLICITS["dragon_armor"]]), 0.33),
                (Item("", "Bushi armor", 1500, 0, 1, SYSTEM["images"]["armors"][14],\
                    0, [Flags.ARMOR, Flags.GEAR], implicits=[IMPLICITS["bushi_armor"]]), 0.25),
                (Item("", "Diamond armor", 2500, 0, 1, SYSTEM["images"]["armors"][23],\
                    0, [Flags.ARMOR, Flags.GEAR], implicits=[IMPLICITS["diamond_armor"]]), 0.1),

                (Item("", "Worker clothes", 5, 0, 1, SYSTEM["images"]["armors"][4],\
                    0, [Flags.ARMOR, Flags.GEAR], implicits=[IMPLICITS["worker_clothes"]]), 1),
                (Item("", "Gambeson", 25, 0, 1, SYSTEM["images"]["armors"][6],\
                    0, [Flags.ARMOR, Flags.GEAR], implicits=[IMPLICITS["gambeson"]]), 0.8),
                (Item("", "Leather armor", 100, 0, 1, SYSTEM["images"]["armors"][38],\
                    0, [Flags.ARMOR, Flags.GEAR], implicits=[IMPLICITS["leather_armor"]]), 0.6),
                (Item("", "Brigandine", 500, 0, 1, SYSTEM["images"]["armors"][15],\
                    0, [Flags.ARMOR, Flags.GEAR], implicits=[IMPLICITS["brigandine"]]), 0.5),
                (Item("", "Vagabond coat", 1000, 0, 1, SYSTEM["images"]["armors"][55],\
                    0, [Flags.ARMOR, Flags.GEAR], implicits=[IMPLICITS["vagabond"]]), 0.33),
                (Item("", "Heroic garb", 1500, 0, 1, SYSTEM["images"]["armors"][46],\
                    0, [Flags.ARMOR, Flags.GEAR], implicits=[IMPLICITS["heroic"]]), 0.25),
                (Item("", "Dark veil", 2500, 0, 1, SYSTEM["images"]["armors"][44],\
                    0, [Flags.ARMOR, Flags.GEAR], implicits=[IMPLICITS["dark"]]), 0.1),

                (Item("", "Robes", 5, 0, 1, SYSTEM["images"]["armors"][27],\
                    0, [Flags.ARMOR, Flags.GEAR], implicits=[IMPLICITS["armor_mom"], IMPLICITS["robes"]]), 1),
                (Item("", "Gown", 25, 0, 1, SYSTEM["images"]["armors"][31],\
                    0, [Flags.ARMOR, Flags.GEAR], implicits=[IMPLICITS["armor_mom"], IMPLICITS["gown"]]), 0.8),
                (Item("", "Mage coat", 100, 0, 1, SYSTEM["images"]["armors"][3],\
                    0, [Flags.ARMOR, Flags.GEAR], implicits=[IMPLICITS["armor_mom"], IMPLICITS["mage_coat"]]), 0.6),
                (Item("", "Arcane robes", 500, 0, 1, SYSTEM["images"]["armors"][30],\
                    0, [Flags.ARMOR, Flags.GEAR], implicits=[IMPLICITS["armor_mom"], IMPLICITS["arcane_robes"]]), 0.5),
                (Item("", "Arcane gown", 1000, 0, 1, SYSTEM["images"]["armors"][33],\
                    0, [Flags.ARMOR, Flags.GEAR], implicits=[IMPLICITS["armor_mom"],\
                        IMPLICITS["arcane_gown"], IMPLICITS["arcane_gown2"]]), 0.33),
                (Item("", "Royal coat", 1500, 0, 1, SYSTEM["images"]["armors"][40],\
                    0, [Flags.ARMOR, Flags.GEAR], implicits=[IMPLICITS["armor_mom"],\
                        IMPLICITS["royal_coat"], IMPLICITS["royal_coat2"]]), 0.25),
                (Item("", "Priest robes", 2500, 0, 1, SYSTEM["images"]["armors"][43],\
                    0, [Flags.ARMOR, Flags.GEAR], implicits=[IMPLICITS["armor_mom"],\
                        IMPLICITS["priest"], IMPLICITS["priest2"]]), 0.1),
        ]
        self._helms = [
            (Item("", "Rusty helm", 5, 0, 1, SYSTEM["images"]["helmets"][0],\
                    0, [Flags.HELM, Flags.GEAR], implicits=[]), 1),
            (Item("", "Coif", 50, 0, 1, SYSTEM["images"]["helmets"][2],\
                    0, [Flags.HELM, Flags.GEAR], implicits=[]), 0.6),
            (Item("", "Crusader helm", 250, 0, 1, SYSTEM["images"]["helmets"][4],\
                    0, [Flags.HELM, Flags.GEAR], implicits=[]), 0.3),

            (Item("", "Leather hat", 5, 0, 1, SYSTEM["images"]["helmets"][6],\
                    0, [Flags.HELM, Flags.GEAR], implicits=[]), 1),
            (Item("", "Bowler hat", 50, 0, 1, SYSTEM["images"]["helmets"][0],\
                    0, [Flags.HELM, Flags.GEAR], implicits=[]), 0.6),
            (Item("", "Lucky tophat", 250, 0, 1, SYSTEM["images"]["helmets"][14],\
                    0, [Flags.HELM, Flags.GEAR], implicits=[]), 0.3),

            (Item("", "Bonnet", 5, 0, 1, SYSTEM["images"]["helmets"][11],\
                    0, [Flags.HELM, Flags.GEAR], implicits=[]), 1),
            (Item("", "Mage's coif", 50, 0, 1, SYSTEM["images"]["helmets"][8],\
                    0, [Flags.HELM, Flags.GEAR], implicits=[]), 0.6),
            (Item("", "Archmage's crown", 250, 0, 1, SYSTEM["images"]["helmets"][3],\
                    0, [Flags.HELM, Flags.GEAR], implicits=[]), 0.3),
        ]
        self._boots = [
            (Item("", "Leather boots", 25, 0, 1, SYSTEM["images"]["boots"][6],\
                    0, [Flags.BOOTS, Flags.GEAR], implicits=[]), 1),
            (Item("", "Chain boots", 250, 0, 1, SYSTEM["images"]["boots"][16],\
                    0, [Flags.BOOTS, Flags.GEAR], implicits=[]), 0.8),
            (Item("", "Mage's boots", 250, 0, 1, SYSTEM["images"]["boots"][11],\
                    0, [Flags.BOOTS, Flags.GEAR], implicits=[]), 0.8),
            (Item("", "Diamond's greaves", 500, 0, 1, SYSTEM["images"]["boots"][17],\
                    0, [Flags.BOOTS, Flags.GEAR], implicits=[]), 0.5),
            (Item("", "Golden steps", 2500, 0, 1, SYSTEM["images"]["boots"][20],\
                    0, [Flags.BOOTS, Flags.GEAR], implicits=[]), 0.05),
        ]
        self._gloves = [
            (Item("", "Leather gloves", 250, 0, 1, SYSTEM["images"]["gloves"][4],\
                    0, [Flags.HANDS, Flags.GEAR], implicits=[]), 1),
            (Item("", "Mage's gloves", 250, 0, 1, SYSTEM["images"]["gloves"][3],\
                    0, [Flags.HANDS, Flags.GEAR], implicits=[]), 1),
            (Item("", "Iron gloves", 250, 0, 1, SYSTEM["images"]["gloves"][0],\
                    0, [Flags.HANDS, Flags.GEAR], implicits=[]), 1),
        ]
        self._amulets = [
            (Item("", "Jade stone", 250, 0, 1, SYSTEM["images"]["amulets"][0],\
                    0, [Flags.AMULET, Flags.GEAR], implicits=[]), 1),
            (Item("", "Ruby stone", 250, 0, 1, SYSTEM["images"]["amulets"][1],\
                    0, [Flags.AMULET, Flags.GEAR], implicits=[]), 1),
            (Item("", "Lapis stone", 250, 0, 1, SYSTEM["images"]["amulets"][2],\
                    0, [Flags.AMULET, Flags.GEAR], implicits=[]), 1),
            (Item("", "Holy symbol", 250, 0, 1, SYSTEM["images"]["amulets"][5],\
                    0, [Flags.AMULET, Flags.GEAR], implicits=[]), 0.5),
            (Item("", "Mage pendant", 250, 0, 1, SYSTEM["images"]["amulets"][6],\
                    0, [Flags.AMULET, Flags.GEAR], implicits=[]), 1),
            (Item("", "Arcane stone", 250, 0, 1, SYSTEM["images"]["amulets"][11],\
                    0, [Flags.AMULET, Flags.GEAR], implicits=[]), 1),
        ]
        self._rings = [
            (Item("", "Iron ring", 250, 0, 1, SYSTEM["images"]["rings"][0],\
                    0, [Flags.RING, Flags.GEAR], implicits=[]), 1),
            (Item("", "Golden ring", 500, 0, 1, SYSTEM["images"]["rings"][1],\
                    0, [Flags.RING, Flags.GEAR], implicits=[]), 0.8),
            (Item("", "Arcane ring", 500, 0, 1, SYSTEM["images"]["rings"][3],\
                    0, [Flags.RING, Flags.GEAR], implicits=[]), 0.8),
            (Item("", "Abyss ring", 500, 0, 1, SYSTEM["images"]["rings"][4],\
                    0, [Flags.RING, Flags.GEAR], implicits=[]), 0.5),
            (Item("", "Twinned ring", 1000, 0, 1, SYSTEM["images"]["rings"][7],\
                    0, [Flags.RING, Flags.GEAR], implicits=[]), 0.3),
            (Item("", "Jewel ring", 2500, 0, 1, SYSTEM["images"]["rings"][12],\
                    0, [Flags.RING, Flags.GEAR], implicits=[]), 0.1),
        ]
        self._relics = [
            (Item("", "Mana lantern", 250, 0, 1, SYSTEM["images"]["relics"][0],\
                    0, [Flags.RELIC, Flags.GEAR], implicits=[]), 1),
            (Item("", "Forbidden scriptures", 250, 0, 1, SYSTEM["images"]["relics"][1],\
                    0, [Flags.RELIC, Flags.GEAR], implicits=[]), 1),
            (Item("", "Lucky horseshoe", 250, 0, 1, SYSTEM["images"]["relics"][2],\
                    0, [Flags.RELIC, Flags.GEAR], implicits=[]), 1),
            (Item("", "Mage's skull", 250, 0, 1, SYSTEM["images"]["relics"][3],\
                    0, [Flags.RELIC, Flags.GEAR], implicits=[]), 1),
            (Item("", "Lunar coral", 250, 0, 1, SYSTEM["images"]["relics"][4],\
                    0, [Flags.RELIC, Flags.GEAR], implicits=[]), 1),
            (Item("", "Golden anchor", 250, 0, 1, SYSTEM["images"]["relics"][5],\
                    0, [Flags.RELIC, Flags.GEAR], implicits=[]), 1),
            (Item("", "Blood grail", 250, 0, 1, SYSTEM["images"]["relics"][6],\
                    0, [Flags.RELIC, Flags.GEAR], implicits=[]), 1),
            (Item("", "Meteor stone", 250, 0, 1, SYSTEM["images"]["relics"][7],\
                    0, [Flags.RELIC, Flags.GEAR], implicits=[]), 1),
            (Item("", "Corrupted meteor stone", 25000, 0, 1, SYSTEM["images"]["relics"][8],\
                    0, [Flags.RELIC, Flags.GEAR], implicits=[]), 0.01),
        ]
        self._weapons = [
            (Item("", "Longbow", 250, 0, 1, SYSTEM["images"]["weapons"][18],\
                    0, [Flags.WEAPON, Flags.GEAR], implicits=[]), 1),
            (Item("", "Rogue's bow", 250, 0, 1, SYSTEM["images"]["weapons"][20],\
                    0, [Flags.WEAPON, Flags.GEAR], implicits=[]), 0.5),
            (Item("", "Steel bow", 250, 0, 1, SYSTEM["images"]["weapons"][7],\
                    0, [Flags.WEAPON, Flags.GEAR], implicits=[]), 0.1),

            (Item("", "Staff", 250, 0, 1, SYSTEM["images"]["weapons"][9],\
                    0, [Flags.WEAPON, Flags.GEAR], implicits=[]), 1),
            (Item("", "Scepter", 250, 0, 1, SYSTEM["images"]["weapons"][16],\
                    0, [Flags.WEAPON, Flags.GEAR], implicits=[]), 0.5),
            (Item("", "Grand cane", 250, 0, 1, SYSTEM["images"]["weapons"][19],\
                    0, [Flags.WEAPON, Flags.GEAR], implicits=[]), 0.1),

            (Item("", "Sword", 250, 0, 1, SYSTEM["images"]["weapons"][1],\
                    0, [Flags.WEAPON, Flags.GEAR], implicits=[]), 1),
            (Item("", "Saber", 250, 0, 1, SYSTEM["images"]["weapons"][8],\
                    0, [Flags.WEAPON, Flags.GEAR], implicits=[]), 0.5),
            (Item("", "Enchanted blade", 250, 0, 1, SYSTEM["images"]["weapons"][10],\
                    0, [Flags.WEAPON, Flags.GEAR], implicits=[]), 0.1),

            (Item("", "Axe", 250, 0, 1, SYSTEM["images"]["weapons"][12],\
                    0, [Flags.WEAPON, Flags.GEAR], implicits=[]), 1),
            (Item("", "Mace", 250, 0, 1, SYSTEM["images"]["weapons"][13],\
                    0, [Flags.WEAPON, Flags.GEAR], implicits=[]), 0.5),
            (Item("", "Scourge", 250, 0, 1, SYSTEM["images"]["weapons"][14],\
                    0, [Flags.WEAPON, Flags.GEAR], implicits=[]), 0.1),

            (Item("", "Crossbow", 250, 0, 1, SYSTEM["images"]["weapons"][3],\
                    0, [Flags.WEAPON, Flags.GEAR], implicits=[]), 0.05),
            (Item("", "Shuriken", 250, 0, 1, SYSTEM["images"]["weapons"][5],\
                    0, [Flags.WEAPON, Flags.GEAR], implicits=[]), 0.01),
        ]
        self._offhands = [
            (Item("", "Grimoire", 250, 0, 1, SYSTEM["images"]["offhands"][0],\
                    0, [Flags.OFFHAND, Flags.GEAR], implicits=[]), 1),
            (Item("", "Codex", 250, 0, 1, SYSTEM["images"]["offhands"][1],\
                    0, [Flags.OFFHAND, Flags.GEAR], implicits=[]), 0.8),
            (Item("", "Scepter", 250, 0, 1, SYSTEM["images"]["offhands"][2],\
                    0, [Flags.OFFHAND, Flags.GEAR], implicits=[]), 0.8),
            (Item("", "Club", 250, 0, 1, SYSTEM["images"]["offhands"][3],\
                    0, [Flags.OFFHAND, Flags.GEAR], implicits=[]), 0.33),
            (Item("", "Wooden shield", 250, 0, 1, SYSTEM["images"]["offhands"][8],\
                    0, [Flags.OFFHAND, Flags.GEAR], implicits=[]), 1),
            (Item("", "Tower shield", 250, 0, 1, SYSTEM["images"]["offhands"][6],\
                    0, [Flags.OFFHAND, Flags.GEAR], implicits=[]), 0.5),
            (Item("", "Diamond shield", 250, 0, 1, SYSTEM["images"]["offhands"][11],\
                    0, [Flags.OFFHAND, Flags.GEAR], implicits=[]), 0.1),
            (Item("", "Diamond arrow", 250, 0, 1, SYSTEM["images"]["offhands"][12],\
                    0, [Flags.OFFHAND, Flags.GEAR], implicits=[]), 1),
        ]

    def pick_weighted(self, items_with_weights):
        """Picks items with the weights"""
        items, weights = zip(*items_with_weights)
        return random.choices(items, weights=weights, k=1)[0]

    def weighted_sample_without_replacement(self, items_with_weights, k):
        """Manually sample k unique items by weight without replacement."""
        items = list(items_with_weights)
        result = []
        for _ in range(k):
            if not items:
                break
            total_weight = sum(w for _, w in items)
            r = random.uniform(0, total_weight)
            upto = 0
            for i, (item, weight) in enumerate(items):
                upto += weight
                if upto >= r:
                    result.append(item)
                    del items[i]
                    break
        return result

    def generate_affixes(self, item_type: str, num_affixes: int, item_level: int):
        affix_pool = AFFIXES[item_type]
        # Step 1: Build list of usable affixes with their valid tiers
        candidates = []
        for affix_key, (tiers, affix_weight) in affix_pool.items():
            valid_tiers = [
                (affix, weight)
                for (affix, weight, min_lvl, max_lvl) in tiers
                if min_lvl <= item_level <= max_lvl
            ]
            if valid_tiers:
                candidates.append(((valid_tiers, affix_key), affix_weight))  # affix_key is only used to enforce uniqueness

        if num_affixes > len(candidates):
            raise ValueError("Not enough unique affixes for this level.")

        # Step 2: Weighted sample without replacement
        chosen_affix_groups = self.weighted_sample_without_replacement(candidates, num_affixes)

        # Step 3: Pick one tier per chosen affix
        result_affixes = [self.pick_weighted(valid_tiers) for valid_tiers, _ in chosen_affix_groups]
        return result_affixes  # List of Affix objects

    def select_base(self, type: list):
        """Selects a random base of the type."""
        max_weight = 0
        for _, weight in type:
            max_weight += float(weight)
        roll = random.uniform(0, max_weight)
        cress = 0
        for item, weight in type:
            cress += float(weight)
            if cress >= roll:
                return item

    def generate_armor(self, level, rarity):
        """Generates a random armor."""
        match rarity:
            case 1:
                affx = 2
            case 2:
                affx = random.randint(3, 6)
            case 3:
                affx = 8
            case _:
                affx = 1
        affixes = [a.roll() for a in self.generate_affixes("armors", affx, level)]
        it = self.select_base(self._armors).copy()
        implicits = []
        for implicit in it.implicits:
            implicits.append(implicit.roll())
        it.implicits = implicits
        it.affixes.extend(affixes)
        it.rarity = rarity
        it.create_popup()
        it.create_popup_details()
        return it
