"""Table for affixes. Surely there's a better way to store
them that that"""

from data.constants import Flags
from data.numerics.affix import Affix
from data.numerics.double_affix import DoubleAffix

AFFIXES = {
    "jewels": 
    {
        "dmg_jew": ([
            (Affix("JEWEL_DAMAGE_1", 0.1, [Flags.BOON, Flags.DAMAGE_MOD]), 1, 0, 80),
            (Affix("JEWEL_DAMAGE_2", 0.2, [Flags.BOON, Flags.DAMAGE_MOD]), 0.8, 20, 90),
            (Affix("JEWEL_DAMAGE_3", 0.3, [Flags.BOON, Flags.DAMAGE_MOD]), 0.6, 40, 999),
            (Affix("JEWEL_DAMAGE_4", 0.4, [Flags.BOON, Flags.DAMAGE_MOD]), 0.25, 60, 999),
            (Affix("JEWEL_DAMAGE_5", 0.8, [Flags.BOON, Flags.DAMAGE_MOD]), 0.1, 80, 999)
        ], 1),
        "cd_jew": ([
            (Affix("JEWEL_CD_1", 0.1, [Flags.CURSE, Flags.COOLDOWN]), 1, 0, 80),
            (Affix("JEWEL_CD_2", 0.2, [Flags.CURSE, Flags.COOLDOWN]), 0.8, 20, 90),
            (Affix("JEWEL_CD_3", 0.3, [Flags.CURSE, Flags.COOLDOWN]), 0.6, 40, 999),
            (Affix("JEWEL_CD_4", 0.4, [Flags.CURSE, Flags.COOLDOWN]), 0.25, 60, 999)
        ], 0.8),
        "area_jew": ([
            (Affix("JEWEL_AREA_1", 0.2, [Flags.BOON, Flags.AREA]), 1, 0, 80),
            (Affix("JEWEL_AREA_2", 0.4, [Flags.BOON, Flags.AREA]), 0.8, 20, 90),
            (Affix("JEWEL_AREA_3", 0.6, [Flags.BOON, Flags.AREA]), 0.6, 40, 999),
            (Affix("JEWEL_AREA_4", 0.8, [Flags.BOON, Flags.AREA]), 0.25, 60, 999),
            (Affix("JEWEL_AREA_5", 1.1, [Flags.BOON, Flags.AREA]), 0.1, 60, 999)
        ], 0.8),
        "crit_d_jew": ([
            (Affix("JEWEL_CRIT_DAMAGE_1", 0.2, [Flags.BOON, Flags.CRIT_DAMAGE]), 1, 0, 80),
            (Affix("JEWEL_CRIT_DAMAGE_2", 0.4, [Flags.BOON, Flags.CRIT_DAMAGE]), 0.8, 20, 90),
            (Affix("JEWEL_CRIT_DAMAGE_3", 0.6, [Flags.BOON, Flags.CRIT_DAMAGE]), 0.6, 40, 999),
            (Affix("JEWEL_CRIT_DAMAGE_4", 0.8, [Flags.BOON, Flags.CRIT_DAMAGE]), 0.25, 60, 999),
            (Affix("JEWEL_CRIT_DAMAGE_5", 1.5, [Flags.BOON, Flags.CRIT_DAMAGE]), 0.01, 80, 999)
        ], 0.8),
        "crit_r_jew": ([
            (Affix("JEWEL_CRIT_CHANCE_1", 0.05, [Flags.BOON, Flags.CRIT_CHANCE]), 1, 0, 80),
            (Affix("JEWEL_CRIT_CHANCE_2", 0.1, [Flags.BOON, Flags.CRIT_CHANCE]), 0.8, 20, 90),
            (Affix("JEWEL_CRIT_CHANCE_3", 0.15, [Flags.BOON, Flags.CRIT_CHANCE]), 0.6, 40, 999),
            (Affix("JEWEL_CRIT_CHANCE_4", 0.2, [Flags.BOON, Flags.CRIT_CHANCE]), 0.25, 60, 999),
            (Affix("JEWEL_CRIT_CHANCE_5", 0.3, [Flags.BOON, Flags.CRIT_CHANCE]), 0.01, 80, 999)
        ], 0.4),
        "hp_cost": ([
            (Affix("JEWEL_LIFE_COST_1", 0.1, [Flags.CURSE, Flags.LIFE_COST]), 1, 0, 80),
            (Affix("JEWEL_LIFE_COST_2", 0.2, [Flags.CURSE, Flags.LIFE_COST]), 0.8, 20, 90),
            (Affix("JEWEL_LIFE_COST_3", 0.3, [Flags.CURSE, Flags.LIFE_COST]), 0.6, 40, 999),
            (Affix("JEWEL_LIFE_COST_4", 0.4, [Flags.CURSE, Flags.LIFE_COST]), 0.25, 60, 999),
            (Affix("JEWEL_LIFE_COST_5", 0.6, [Flags.CURSE, Flags.LIFE_COST]), 0.1, 80, 999)
        ], 0.5),
        "mp_cost": ([
            (Affix("JEWEL_MANA_COST_1", 0.1, [Flags.CURSE, Flags.MANA_COST]), 1, 0, 80),
            (Affix("JEWEL_MANA_COST_2", 0.2, [Flags.CURSE, Flags.MANA_COST]), 0.8, 20, 90),
            (Affix("JEWEL_MANA_COST_3", 0.3, [Flags.CURSE, Flags.MANA_COST]), 0.6, 40, 999),
            (Affix("JEWEL_MANA_COST_4", 0.4, [Flags.CURSE, Flags.MANA_COST]), 0.25, 60, 999),
            (Affix("JEWEL_MANA_COST_5", 0.6, [Flags.CURSE, Flags.MANA_COST]), 0.1, 80, 999)
        ], 0.5),
        "projs": ([
            (Affix("JEWEL_PROJECTILE_1", 1, [Flags.FLAT, Flags.PROJECTILES], 1, 1), 1, 0, 80),
            (Affix("JEWEL_PROJECTILE_2", 2, [Flags.FLAT, Flags.PROJECTILES], 1, 1), 0.8, 20, 90),
            (Affix("JEWEL_PROJECTILE_3", 3, [Flags.FLAT, Flags.PROJECTILES], 1, 1), 0.6, 40, 999)
        ], 0.01),
    },
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
        "dodge_rate": ([
            (Affix("ARMOR_DODGE_RATING_1", 100, [Flags.FLAT, Flags.DESC_FLAT,\
                                                        Flags.DODGE_RATING]), 1, 0, 30),
            (Affix("ARMOR_DODGE_RATING_2", 250, [Flags.FLAT, Flags.DESC_FLAT,\
                                                        Flags.DODGE_RATING]), 0.8, 0, 30),
            (Affix("ARMOR_DODGE_RATING_3", 500, [Flags.FLAT, Flags.DESC_FLAT,\
                                                        Flags.DODGE_RATING]), 0.5, 10, 40),
            (Affix("ARMOR_DODGE_RATING_4", 750, [Flags.FLAT, Flags.DESC_FLAT,\
                                                        Flags.DODGE_RATING]), 0.3, 20, 60),
            (Affix("ARMOR_DODGE_RATING_5", 1000, [Flags.FLAT, Flags.DESC_FLAT,\
                                                        Flags.DODGE_RATING]), 0.2, 30, 80),
            (Affix("ARMOR_DODGE_RATING_6", 1500, [Flags.FLAT, Flags.DESC_FLAT,\
                                                        Flags.DODGE_RATING]), 0.1, 50, 999),
            (Affix("ARMOR_DODGE_RATING_7", 2500, [Flags.FLAT, Flags.DESC_FLAT,\
                                                        Flags.DODGE_RATING]), 0.05, 75, 999),
        ], 1.2),
        "dodge": ([
            (Affix("ARMOR_DODGE_1", 0.01, [Flags.FLAT, Flags.DESC_PERCENT,\
                                                        Flags.DODGE]), 1, 0, 999),
            (Affix("ARMOR_DODGE_2", 0.02, [Flags.FLAT, Flags.DESC_PERCENT,\
                                                        Flags.DODGE]), 0.5, 25, 999),
            (Affix("ARMOR_DODGE_3", 0.05, [Flags.FLAT, Flags.DESC_PERCENT,\
                                                        Flags.DODGE]), 0.1, 75, 999),
        ], 0.2),
        "life_regen": ([
            (Affix("ARMOR_LIFE_REGEN_1", 5, [Flags.FLAT, Flags.LIFE_REGEN, Flags.DESC_FLAT]), 1, 0, 60),
            (Affix("ARMOR_LIFE_REGEN_2", 10, [Flags.FLAT, Flags.LIFE_REGEN, Flags.DESC_FLAT]), 1, 20, 60),
            (Affix("ARMOR_LIFE_REGEN_3", 20, [Flags.FLAT, Flags.LIFE_REGEN, Flags.DESC_FLAT]), 1, 40, 999),
            (Affix("ARMOR_LIFE_REGEN_4", 30, [Flags.FLAT, Flags.LIFE_REGEN, Flags.DESC_FLAT]), 1, 50, 999),
            (Affix("ARMOR_LIFE_REGEN_5", 50, [Flags.FLAT, Flags.LIFE_REGEN, Flags.DESC_FLAT]), 1, 70, 999),
        ], 0.8),
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
            (Affix("HELM_STR_4", 15, [Flags.FLAT, Flags.DESC_FLAT, Flags.STR]), 0.3, 20, 60),
            (Affix("HELM_STR_5", 20, [Flags.FLAT, Flags.DESC_FLAT, Flags.STR]), 0.2, 30, 80),
            (Affix("HELM_STR_6", 25, [Flags.FLAT, Flags.DESC_FLAT, Flags.STR]), 0.1, 50, 999),
            (Affix("HELM_STR_7", 40, [Flags.FLAT, Flags.DESC_FLAT, Flags.STR]), 0.05, 75, 999),
        ], 1),
        "dex": ([
            (Affix("HELM_DEX_1", 5, [Flags.FLAT, Flags.DESC_FLAT, Flags.DEX]), 1, 0, 25),
            (Affix("HELM_DEX_2", 10, [Flags.FLAT, Flags.DESC_FLAT, Flags.DEX]), 0.8, 0, 30),
            (Affix("HELM_DEX_3", 15, [Flags.FLAT, Flags.DESC_FLAT, Flags.DEX]), 0.5, 10, 40),
            (Affix("HELM_DEX_4", 15, [Flags.FLAT, Flags.DESC_FLAT, Flags.DEX]), 0.3, 20, 60),
            (Affix("HELM_DEX_5", 20, [Flags.FLAT, Flags.DESC_FLAT, Flags.DEX]), 0.2, 30, 80),
            (Affix("HELM_DEX_6", 25, [Flags.FLAT, Flags.DESC_FLAT, Flags.DEX]), 0.1, 50, 999),
            (Affix("HELM_DEX_7", 40, [Flags.FLAT, Flags.DESC_FLAT, Flags.DEX]), 0.05, 75, 999),
        ], 1),
        "int": ([
            (Affix("HELM_INT_1", 5, [Flags.FLAT, Flags.DESC_FLAT, Flags.INT]), 1, 0, 25),
            (Affix("HELM_INT_2", 10, [Flags.FLAT, Flags.DESC_FLAT, Flags.INT]), 0.8, 0, 30),
            (Affix("HELM_INT_3", 15, [Flags.FLAT, Flags.DESC_FLAT, Flags.INT]), 0.5, 10, 40),
            (Affix("HELM_INT_4", 15, [Flags.FLAT, Flags.DESC_FLAT, Flags.INT]), 0.3, 20, 60),
            (Affix("HELM_INT_5", 20, [Flags.FLAT, Flags.DESC_FLAT, Flags.INT]), 0.2, 30, 80),
            (Affix("HELM_INT_6", 25, [Flags.FLAT, Flags.DESC_FLAT, Flags.INT]), 0.1, 50, 999),
            (Affix("HELM_INT_7", 40, [Flags.FLAT, Flags.DESC_FLAT, Flags.INT]), 0.05, 75, 999),
        ], 1),
        "life": ([
            (Affix("HELM_LIFE_1", 5, [Flags.FLAT, Flags.DESC_FLAT, Flags.LIFE]), 1, 0, 25),
            (Affix("HELM_LIFE_2", 10, [Flags.FLAT, Flags.DESC_FLAT, Flags.LIFE]), 0.8, 0, 30),
            (Affix("HELM_LIFE_3", 15, [Flags.FLAT, Flags.DESC_FLAT, Flags.LIFE]), 0.5, 10, 40),
            (Affix("HELM_LIFE_4", 20, [Flags.FLAT, Flags.DESC_FLAT, Flags.LIFE]), 0.3, 20, 60),
            (Affix("HELM_LIFE_5", 25, [Flags.FLAT, Flags.DESC_FLAT, Flags.LIFE]), 0.2, 30, 80),
            (Affix("HELM_LIFE_6", 50, [Flags.FLAT, Flags.DESC_FLAT, Flags.LIFE]), 0.1, 50, 999),
            (Affix("HELM_LIFE_7", 75, [Flags.FLAT, Flags.DESC_FLAT, Flags.LIFE]), 0.05, 75, 999),
        ], 1),
        "life_incr": ([
            (Affix("HELM_LIFE_INCR_1", 0.03, [Flags.BOON, Flags.LIFE]), 1, 0, 25),
            (Affix("HELM_LIFE_INCR_2", 0.08, [Flags.BOON, Flags.LIFE]), 0.6, 15, 40),
            (Affix("HELM_LIFE_INCR_3", 0.1, [Flags.BOON, Flags.LIFE]), 0.3, 25, 60),
            (Affix("HELM_LIFE_INCR_4", 0.15, [Flags.BOON, Flags.LIFE]), 0.15, 50, 999),
            (Affix("HELM_LIFE_INCR_5", 0.2, [Flags.BOON, Flags.LIFE]), 0.01, 75, 999)
        ], 0.8),
        "mana": ([
            (Affix("HELM_MANA_1", 5, [Flags.FLAT, Flags.DESC_FLAT, Flags.MANA]), 1, 0, 25),
            (Affix("HELM_MANA_2", 10, [Flags.FLAT, Flags.DESC_FLAT, Flags.MANA]), 0.8, 0, 30),
            (Affix("HELM_MANA_3", 15, [Flags.FLAT, Flags.DESC_FLAT, Flags.MANA]), 0.5, 10, 40),
            (Affix("HELM_MANA_4", 20, [Flags.FLAT, Flags.DESC_FLAT, Flags.MANA]), 0.3, 20, 60),
            (Affix("HELM_MANA_5", 25, [Flags.FLAT, Flags.DESC_FLAT, Flags.MANA]), 0.2, 30, 80),
            (Affix("HELM_MANA_6", 50, [Flags.FLAT, Flags.DESC_FLAT, Flags.MANA]), 0.1, 50, 999),
            (Affix("HELM_MANA_7", 75, [Flags.FLAT, Flags.DESC_FLAT, Flags.MANA]), 0.05, 75, 999),
        ], 1),
        "mana_incr": ([
            (Affix("HELM_MANA_INCR_1", 0.03, [Flags.BOON, Flags.MANA]), 1, 0, 25),
            (Affix("HELM_MANA_INCR_2", 0.08, [Flags.BOON, Flags.MANA]), 0.6, 15, 40),
            (Affix("HELM_MANA_INCR_3", 0.1, [Flags.BOON, Flags.MANA]), 0.3, 25, 60),
            (Affix("HELM_MANA_INCR_4", 0.15, [Flags.BOON, Flags.MANA]), 0.15, 50, 999),
            (Affix("HELM_MANA_INCR_5", 0.2, [Flags.BOON, Flags.MANA]), 0.01, 75, 999)
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
            (Affix("HELM_DODGE_RATING_1", 50, [Flags.FLAT, Flags.DESC_FLAT,\
                                                Flags.DODGE_RATING]), 1, 0, 30),
            (Affix("HELM_DODGE_RATING_2", 100, [Flags.FLAT, Flags.DESC_FLAT,\
                                                Flags.DODGE_RATING]), 0.8, 0, 30),
            (Affix("HELM_DODGE_RATING_3", 200, [Flags.FLAT, Flags.DESC_FLAT,\
                                                Flags.DODGE_RATING]), 0.5, 10, 40),
            (Affix("HELM_DODGE_RATING_4", 300, [Flags.FLAT, Flags.DESC_FLAT,\
                                                Flags.DODGE_RATING]), 0.3, 20, 60),
            (Affix("HELM_DODGE_RATING_5", 500, [Flags.FLAT, Flags.DESC_FLAT,\
                                                Flags.DODGE_RATING]), 0.2, 30, 80),
            (Affix("HELM_DODGE_RATING_6", 750, [Flags.FLAT, Flags.DESC_FLAT,\
                                                Flags.DODGE_RATING]), 0.1, 50, 999),
            (Affix("HELM_DODGE_RATING_7", 1000, [Flags.FLAT, Flags.DESC_FLAT,\
                                                Flags.DODGE_RATING]), 0.05, 75, 999),
        ], 1.2),
        "precision": ([
            (Affix("HELM_PRECISION_1", 50, [Flags.FLAT, Flags.DESC_FLAT,\
                                            Flags.PRECISION]), 1, 0, 30),
            (Affix("HELM_PRECISION_2", 100, [Flags.FLAT, Flags.DESC_FLAT,\
                                            Flags.PRECISION]), 0.8, 0, 30),
            (Affix("HELM_PRECISION_3", 200, [Flags.FLAT, Flags.DESC_FLAT,\
                                            Flags.PRECISION]), 0.5, 10, 40),
            (Affix("HELM_PRECISION_4", 300, [Flags.FLAT, Flags.DESC_FLAT,\
                                            Flags.PRECISION]), 0.3, 20, 60),
            (Affix("HELM_PRECISION_5", 500, [Flags.FLAT, Flags.DESC_FLAT,\
                                            Flags.PRECISION]), 0.2, 30, 80),
            (Affix("HELM_PRECISION_6", 750, [Flags.FLAT, Flags.DESC_FLAT,\
                                            Flags.PRECISION]), 0.1, 50, 999),
            (Affix("HELM_PRECISION_7", 1000, [Flags.FLAT, Flags.DESC_FLAT,\
                                            Flags.PRECISION]), 0.05, 75, 999),
        ], 0.9),
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
        "str": ([
            (Affix("BOOTS_STR_1", 5, [Flags.FLAT, Flags.DESC_FLAT, Flags.STR]), 1, 0, 25),
            (Affix("BOOTS_STR_2", 10, [Flags.FLAT, Flags.DESC_FLAT, Flags.STR]), 0.8, 0, 30),
            (Affix("BOOTS_STR_3", 15, [Flags.FLAT, Flags.DESC_FLAT, Flags.STR]), 0.5, 10, 40),
            (Affix("BOOTS_STR_4", 15, [Flags.FLAT, Flags.DESC_FLAT, Flags.STR]), 0.3, 20, 60),
            (Affix("BOOTS_STR_5", 20, [Flags.FLAT, Flags.DESC_FLAT, Flags.STR]), 0.2, 30, 80),
            (Affix("BOOTS_STR_6", 25, [Flags.FLAT, Flags.DESC_FLAT, Flags.STR]), 0.1, 50, 999),
            (Affix("BOOTS_STR_7", 40, [Flags.FLAT, Flags.DESC_FLAT, Flags.STR]), 0.05, 75, 999),
        ], 1),
        "dex": ([
            (Affix("BOOTS_DEX_1", 5, [Flags.FLAT, Flags.DESC_FLAT, Flags.DEX]), 1, 0, 25),
            (Affix("BOOTS_DEX_2", 10, [Flags.FLAT, Flags.DESC_FLAT, Flags.DEX]), 0.8, 0, 30),
            (Affix("BOOTS_DEX_3", 15, [Flags.FLAT, Flags.DESC_FLAT, Flags.DEX]), 0.5, 10, 40),
            (Affix("BOOTS_DEX_4", 15, [Flags.FLAT, Flags.DESC_FLAT, Flags.DEX]), 0.3, 20, 60),
            (Affix("BOOTS_DEX_5", 20, [Flags.FLAT, Flags.DESC_FLAT, Flags.DEX]), 0.2, 30, 80),
            (Affix("BOOTS_DEX_6", 25, [Flags.FLAT, Flags.DESC_FLAT, Flags.DEX]), 0.1, 50, 999),
            (Affix("BOOTS_DEX_7", 40, [Flags.FLAT, Flags.DESC_FLAT, Flags.DEX]), 0.05, 75, 999),
        ], 1),
        "int": ([
            (Affix("BOOTS_INT_1", 5, [Flags.FLAT, Flags.DESC_FLAT, Flags.INT]), 1, 0, 25),
            (Affix("BOOTS_INT_2", 10, [Flags.FLAT, Flags.DESC_FLAT, Flags.INT]), 0.8, 0, 30),
            (Affix("BOOTS_INT_3", 15, [Flags.FLAT, Flags.DESC_FLAT, Flags.INT]), 0.5, 10, 40),
            (Affix("BOOTS_INT_4", 15, [Flags.FLAT, Flags.DESC_FLAT, Flags.INT]), 0.3, 20, 60),
            (Affix("BOOTS_INT_5", 20, [Flags.FLAT, Flags.DESC_FLAT, Flags.INT]), 0.2, 30, 80),
            (Affix("BOOTS_INT_6", 25, [Flags.FLAT, Flags.DESC_FLAT, Flags.INT]), 0.1, 50, 999),
            (Affix("BOOTS_INT_7", 40, [Flags.FLAT, Flags.DESC_FLAT, Flags.INT]), 0.05, 75, 999),
        ], 1),
        "life": ([
            (Affix("BOOTS_LIFE_1", 5, [Flags.FLAT, Flags.DESC_FLAT, Flags.LIFE]), 1, 0, 25),
            (Affix("BOOTS_LIFE_2", 10, [Flags.FLAT, Flags.DESC_FLAT, Flags.LIFE]), 0.8, 0, 30),
            (Affix("BOOTS_LIFE_3", 15, [Flags.FLAT, Flags.DESC_FLAT, Flags.LIFE]), 0.5, 10, 40),
            (Affix("BOOTS_LIFE_4", 20, [Flags.FLAT, Flags.DESC_FLAT, Flags.LIFE]), 0.3, 20, 60),
            (Affix("BOOTS_LIFE_5", 25, [Flags.FLAT, Flags.DESC_FLAT, Flags.LIFE]), 0.2, 30, 80),
            (Affix("BOOTS_LIFE_6", 50, [Flags.FLAT, Flags.DESC_FLAT, Flags.LIFE]), 0.1, 50, 999),
            (Affix("BOOTS_LIFE_7", 75, [Flags.FLAT, Flags.DESC_FLAT, Flags.LIFE]), 0.05, 75, 999),
        ], 1),
        "life_incr": ([
            (Affix("BOOTS_LIFE_INCR_1", 0.03, [Flags.BOON, Flags.LIFE]), 1, 0, 25),
            (Affix("BOOTS_LIFE_INCR_2", 0.08, [Flags.BOON, Flags.LIFE]), 0.6, 15, 40),
            (Affix("BOOTS_LIFE_INCR_3", 0.1, [Flags.BOON, Flags.LIFE]), 0.3, 25, 60),
            (Affix("BOOTS_LIFE_INCR_4", 0.15, [Flags.BOON, Flags.LIFE]), 0.15, 50, 999),
            (Affix("BOOTS_LIFE_INCR_5", 0.2, [Flags.BOON, Flags.LIFE]), 0.01, 75, 999)
        ], 0.8),
        "mana": ([
            (Affix("BOOTS_MANA_1", 5, [Flags.FLAT, Flags.DESC_FLAT, Flags.MANA]), 1, 0, 25),
            (Affix("BOOTS_MANA_2", 10, [Flags.FLAT, Flags.DESC_FLAT, Flags.MANA]), 0.8, 0, 30),
            (Affix("BOOTS_MANA_3", 15, [Flags.FLAT, Flags.DESC_FLAT, Flags.MANA]), 0.5, 10, 40),
            (Affix("BOOTS_MANA_4", 20, [Flags.FLAT, Flags.DESC_FLAT, Flags.MANA]), 0.3, 20, 60),
            (Affix("BOOTS_MANA_5", 25, [Flags.FLAT, Flags.DESC_FLAT, Flags.MANA]), 0.2, 30, 80),
            (Affix("BOOTS_MANA_6", 50, [Flags.FLAT, Flags.DESC_FLAT, Flags.MANA]), 0.1, 50, 999),
            (Affix("BOOTS_MANA_7", 75, [Flags.FLAT, Flags.DESC_FLAT, Flags.MANA]), 0.05, 75, 999),
        ], 1),
        "mana_incr": ([
            (Affix("BOOTS_MANA_INCR_1", 0.03, [Flags.BOON, Flags.MANA]), 1, 0, 25),
            (Affix("BOOTS_MANA_INCR_2", 0.08, [Flags.BOON, Flags.MANA]), 0.6, 15, 40),
            (Affix("BOOTS_MANA_INCR_3", 0.1, [Flags.BOON, Flags.MANA]), 0.3, 25, 60),
            (Affix("BOOTS_MANA_INCR_4", 0.15, [Flags.BOON, Flags.MANA]), 0.15, 50, 999),
            (Affix("BOOTS_MANA_INCR_5", 0.2, [Flags.BOON, Flags.MANA]), 0.01, 75, 999)
        ], 0.8),
        "endurance": ([
            (Affix("BOOTS_DEF_1", 50, [Flags.FLAT, Flags.DESC_FLAT, Flags.DEF]), 1, 0, 30),
            (Affix("BOOTS_DEF_2", 100, [Flags.FLAT, Flags.DESC_FLAT, Flags.DEF]), 0.8, 0, 30),
            (Affix("BOOTS_DEF_3", 200, [Flags.FLAT, Flags.DESC_FLAT, Flags.DEF]), 0.5, 10, 40),
            (Affix("BOOTS_DEF_4", 300, [Flags.FLAT, Flags.DESC_FLAT, Flags.DEF]), 0.3, 20, 60),
            (Affix("BOOTS_DEF_5", 500, [Flags.FLAT, Flags.DESC_FLAT, Flags.DEF]), 0.2, 30, 80),
            (Affix("BOOTS_DEF_6", 750, [Flags.FLAT, Flags.DESC_FLAT, Flags.DEF]), 0.1, 50, 999),
            (Affix("BOOTS_DEF_7", 1000, [Flags.FLAT, Flags.DESC_FLAT, Flags.DEF]), 0.05, 75, 999),
        ], 1.2),
        "dodge": ([
            (Affix("BOOTS_DODGE_RATING_1", 50, [Flags.FLAT, Flags.DESC_FLAT,\
                                                Flags.DODGE_RATING]), 1, 0, 30),
            (Affix("BOOTS_DODGE_RATING_2", 100, [Flags.FLAT, Flags.DESC_FLAT,\
                                                Flags.DODGE_RATING]), 0.8, 0, 30),
            (Affix("BOOTS_DODGE_RATING_3", 200, [Flags.FLAT, Flags.DESC_FLAT,\
                                                Flags.DODGE_RATING]), 0.5, 10, 40),
            (Affix("BOOTS_DODGE_RATING_4", 300, [Flags.FLAT, Flags.DESC_FLAT,\
                                                Flags.DODGE_RATING]), 0.3, 20, 60),
            (Affix("BOOTS_DODGE_RATING_5", 500, [Flags.FLAT, Flags.DESC_FLAT,\
                                                Flags.DODGE_RATING]), 0.2, 30, 80),
            (Affix("BOOTS_DODGE_RATING_6", 750, [Flags.FLAT, Flags.DESC_FLAT,\
                                                Flags.DODGE_RATING]), 0.1, 50, 999),
            (Affix("BOOTS_DODGE_RATING_7", 1000, [Flags.FLAT, Flags.DESC_FLAT,\
                                                Flags.DODGE_RATING]), 0.05, 75, 999),
        ], 1.2),
        "speed": ([
            (Affix("BOOTS_SPEED_1", 0.1, [Flags.BOON,\
                                            Flags.SPEED]), 1, 0, 30),
            (Affix("BOOTS_SPEED_2", 0.15, [Flags.BOON,\
                                            Flags.SPEED]), 0.8, 0, 30),
            (Affix("BOOTS_SPEED_3", 0.2, [Flags.BOON,\
                                            Flags.SPEED]), 0.5, 10, 40),
            (Affix("BOOTS_SPEED_4", 0.25, [Flags.BOON,\
                                            Flags.SPEED]), 0.3, 20, 60),
            (Affix("BOOTS_SPEED_5", 0.3, [Flags.BOON,\
                                            Flags.SPEED]), 0.2, 30, 80),
            (Affix("BOOTS_SPEED_6", 0.4, [Flags.BOON,\
                                            Flags.SPEED]), 0.1, 50, 999),
            (Affix("BOOTS_SPEED_7", 0.5, [Flags.BOON,\
                                            Flags.SPEED]), 0.05, 75, 999),
        ], 0.9),
        "phys_res": ([
            (Affix("BOOTS_PHYS_RES_1", 0.08, [Flags.PHYS, Flags.FLAT]), 1, 0, 60),
            (Affix("BOOTS_PHYS_RES_2", 0.12, [Flags.PHYS, Flags.FLAT]), 0.6, 10, 90),
            (Affix("BOOTS_PHYS_RES_3", 0.2, [Flags.PHYS, Flags.FLAT]), 0.3, 25, 999),
        ], 1),
        "fire_res": ([
            (Affix("BOOTS_FIRE_RES_1", 0.08, [Flags.FIRE, Flags.FLAT]), 1, 0, 60),
            (Affix("BOOTS_FIRE_RES_2", 0.12, [Flags.FIRE, Flags.FLAT]), 0.6, 10, 90),
            (Affix("BOOTS_FIRE_RES_3", 0.2, [Flags.FIRE, Flags.FLAT]), 0.3, 25, 999),
        ], 1),
        "ice_res": ([
            (Affix("BOOTS_ICE_RES_1", 0.08, [Flags.ICE, Flags.FLAT]), 1, 0, 60),
            (Affix("BOOTS_ICE_RES_2", 0.12, [Flags.ICE, Flags.FLAT]), 0.6, 10, 90),
            (Affix("BOOTS_ICE_RES_3", 0.2, [Flags.ICE, Flags.FLAT]), 0.3, 25, 999),
        ], 1),
        "elec_res": ([
            (Affix("BOOTS_ELEC_RES_1", 0.08, [Flags.ELEC, Flags.FLAT]), 1, 0, 60),
            (Affix("BOOTS_ELEC_RES_2", 0.12, [Flags.ELEC, Flags.FLAT]), 0.6, 10, 90),
            (Affix("BOOTS_ELEC_RES_3", 0.2, [Flags.ELEC, Flags.FLAT]), 0.3, 25, 999),
        ], 1),
        "light_res": ([
            (Affix("BOOTS_LIGHT_RES_1", 0.08, [Flags.LIGHT, Flags.FLAT]), 1, 0, 60),
            (Affix("BOOTS_LIGHT_RES_2", 0.12, [Flags.LIGHT, Flags.FLAT]), 0.6, 10, 90),
            (Affix("BOOTS_LIGHT_RES_3", 0.2, [Flags.LIGHT, Flags.FLAT]), 0.3, 25, 999),
        ], 1),
        "dark_res": ([
            (Affix("BOOTS_DARK_RES_1", 0.08, [Flags.DARK, Flags.FLAT]), 1, 0, 60),
            (Affix("BOOTS_DARK_RES_2", 0.12, [Flags.DARK, Flags.FLAT]), 0.6, 10, 90),
            (Affix("BOOTS_DARK_RES_3", 0.2, [Flags.DARK, Flags.FLAT]), 0.3, 25, 999),
        ], 1),
        "energ_res": ([
            (Affix("BOOTS_ENERG_RES_1", 0.08, [Flags.ENERG, Flags.FLAT]), 1, 0, 60),
            (Affix("BOOTS_ENERG_RES_2", 0.12, [Flags.ENERG, Flags.FLAT]), 0.6, 10, 90),
            (Affix("BOOTS_ENERG_RES_3", 0.2, [Flags.ENERG, Flags.FLAT]), 0.3, 25, 999),
        ], 1),
        "elemental_res": ([
            (Affix("BOOTS_ELEMENTAL_RESISTANCES_1", 0.08, [Flags.ELEMENTAL_RESISTANCES,\
                                                            Flags.FLAT]), 1, 20, 60),
            (Affix("BOOTS_ELEMENTAL_RESISTANCES_2", 0.12, [Flags.ELEMENTAL_RESISTANCES,\
                                                            Flags.FLAT]), 0.6, 40, 90),
            (Affix("BOOTS_ELEMENTAL_RESISTANCES_3", 0.2, [Flags.ELEMENTAL_RESISTANCES,\
                                                            Flags.FLAT]), 0.3, 60, 999),
        ], 0.8),
        "all_res": ([
            (Affix("BOOTS_ALL_RESISTANCES_1", 0.08, [Flags.ALL_RESISTANCES,\
                                                        Flags.FLAT]), 1, 20, 60),
            (Affix("BOOTS_ALL_RESISTANCES_2", 0.12, [Flags.ALL_RESISTANCES,\
                                                        Flags.FLAT]), 0.6, 40, 90),
            (Affix("BOOTS_ALL_RESISTANCES_3", 0.2, [Flags.ALL_RESISTANCES,\
                                                        Flags.FLAT]), 0.3, 60, 999),
        ], 0.25)
    },
    "gloves": {
       "str": ([
            (Affix("GLOVES_STR_1", 5, [Flags.FLAT, Flags.DESC_FLAT, Flags.STR]), 1, 0, 25),
            (Affix("GLOVES_STR_2", 10, [Flags.FLAT, Flags.DESC_FLAT, Flags.STR]), 0.8, 0, 30),
            (Affix("GLOVES_STR_3", 15, [Flags.FLAT, Flags.DESC_FLAT, Flags.STR]), 0.5, 10, 40),
            (Affix("GLOVES_STR_4", 15, [Flags.FLAT, Flags.DESC_FLAT, Flags.STR]), 0.3, 20, 60),
            (Affix("GLOVES_STR_5", 20, [Flags.FLAT, Flags.DESC_FLAT, Flags.STR]), 0.2, 30, 80),
            (Affix("GLOVES_STR_6", 25, [Flags.FLAT, Flags.DESC_FLAT, Flags.STR]), 0.1, 50, 999),
            (Affix("GLOVES_STR_7", 40, [Flags.FLAT, Flags.DESC_FLAT, Flags.STR]), 0.05, 75, 999),
        ], 1),
        "dex": ([
            (Affix("GLOVES_DEX_1", 5, [Flags.FLAT, Flags.DESC_FLAT, Flags.DEX]), 1, 0, 25),
            (Affix("GLOVES_DEX_2", 10, [Flags.FLAT, Flags.DESC_FLAT, Flags.DEX]), 0.8, 0, 30),
            (Affix("GLOVES_DEX_3", 15, [Flags.FLAT, Flags.DESC_FLAT, Flags.DEX]), 0.5, 10, 40),
            (Affix("GLOVES_DEX_4", 15, [Flags.FLAT, Flags.DESC_FLAT, Flags.DEX]), 0.3, 20, 60),
            (Affix("GLOVES_DEX_5", 20, [Flags.FLAT, Flags.DESC_FLAT, Flags.DEX]), 0.2, 30, 80),
            (Affix("GLOVES_DEX_6", 25, [Flags.FLAT, Flags.DESC_FLAT, Flags.DEX]), 0.1, 50, 999),
            (Affix("GLOVES_DEX_7", 40, [Flags.FLAT, Flags.DESC_FLAT, Flags.DEX]), 0.05, 75, 999),
        ], 1),
        "int": ([
            (Affix("GLOVES_INT_1", 5, [Flags.FLAT, Flags.DESC_FLAT, Flags.INT]), 1, 0, 25),
            (Affix("GLOVES_INT_2", 10, [Flags.FLAT, Flags.DESC_FLAT, Flags.INT]), 0.8, 0, 30),
            (Affix("GLOVES_INT_3", 15, [Flags.FLAT, Flags.DESC_FLAT, Flags.INT]), 0.5, 10, 40),
            (Affix("GLOVES_INT_4", 15, [Flags.FLAT, Flags.DESC_FLAT, Flags.INT]), 0.3, 20, 60),
            (Affix("GLOVES_INT_5", 20, [Flags.FLAT, Flags.DESC_FLAT, Flags.INT]), 0.2, 30, 80),
            (Affix("GLOVES_INT_6", 25, [Flags.FLAT, Flags.DESC_FLAT, Flags.INT]), 0.1, 50, 999),
            (Affix("GLOVES_INT_7", 40, [Flags.FLAT, Flags.DESC_FLAT, Flags.INT]), 0.05, 75, 999),
        ], 1),
        "life": ([
            (Affix("GLOVES_LIFE_1", 5, [Flags.FLAT, Flags.DESC_FLAT, Flags.LIFE]), 1, 0, 25),
            (Affix("GLOVES_LIFE_2", 10, [Flags.FLAT, Flags.DESC_FLAT, Flags.LIFE]), 0.8, 0, 30),
            (Affix("GLOVES_LIFE_3", 15, [Flags.FLAT, Flags.DESC_FLAT, Flags.LIFE]), 0.5, 10, 40),
            (Affix("GLOVES_LIFE_4", 20, [Flags.FLAT, Flags.DESC_FLAT, Flags.LIFE]), 0.3, 20, 60),
            (Affix("GLOVES_LIFE_5", 25, [Flags.FLAT, Flags.DESC_FLAT, Flags.LIFE]), 0.2, 30, 80),
            (Affix("GLOVES_LIFE_6", 50, [Flags.FLAT, Flags.DESC_FLAT, Flags.LIFE]), 0.1, 50, 999),
            (Affix("GLOVES_LIFE_7", 75, [Flags.FLAT, Flags.DESC_FLAT, Flags.LIFE]), 0.05, 75, 999),
        ], 1),
        "life_incr": ([
            (Affix("GLOVES_LIFE_INCR_1", 0.03, [Flags.BOON, Flags.LIFE]), 1, 0, 25),
            (Affix("GLOVES_LIFE_INCR_2", 0.08, [Flags.BOON, Flags.LIFE]), 0.6, 15, 40),
            (Affix("GLOVES_LIFE_INCR_3", 0.1, [Flags.BOON, Flags.LIFE]), 0.3, 25, 60),
            (Affix("GLOVES_LIFE_INCR_4", 0.15, [Flags.BOON, Flags.LIFE]), 0.15, 50, 999),
            (Affix("GLOVES_LIFE_INCR_5", 0.2, [Flags.BOON, Flags.LIFE]), 0.01, 75, 999)
        ], 0.8),
        "mana": ([
            (Affix("GLOVES_MANA_1", 5, [Flags.FLAT, Flags.DESC_FLAT, Flags.MANA]), 1, 0, 25),
            (Affix("GLOVES_MANA_2", 10, [Flags.FLAT, Flags.DESC_FLAT, Flags.MANA]), 0.8, 0, 30),
            (Affix("GLOVES_MANA_3", 15, [Flags.FLAT, Flags.DESC_FLAT, Flags.MANA]), 0.5, 10, 40),
            (Affix("GLOVES_MANA_4", 20, [Flags.FLAT, Flags.DESC_FLAT, Flags.MANA]), 0.3, 20, 60),
            (Affix("GLOVES_MANA_5", 25, [Flags.FLAT, Flags.DESC_FLAT, Flags.MANA]), 0.2, 30, 80),
            (Affix("GLOVES_MANA_6", 50, [Flags.FLAT, Flags.DESC_FLAT, Flags.MANA]), 0.1, 50, 999),
            (Affix("GLOVES_MANA_7", 75, [Flags.FLAT, Flags.DESC_FLAT, Flags.MANA]), 0.05, 75, 999),
        ], 1),
        "mana_incr": ([
            (Affix("GLOVES_MANA_INCR_1", 0.03, [Flags.BOON, Flags.MANA]), 1, 0, 25),
            (Affix("GLOVES_MANA_INCR_2", 0.08, [Flags.BOON, Flags.MANA]), 0.6, 15, 40),
            (Affix("GLOVES_MANA_INCR_3", 0.1, [Flags.BOON, Flags.MANA]), 0.3, 25, 60),
            (Affix("GLOVES_MANA_INCR_4", 0.15, [Flags.BOON, Flags.MANA]), 0.15, 50, 999),
            (Affix("GLOVES_MANA_INCR_5", 0.2, [Flags.BOON, Flags.MANA]), 0.01, 75, 999)
        ], 0.8),
        "endurance": ([
            (Affix("GLOVES_DEF_1", 50, [Flags.FLAT, Flags.DESC_FLAT, Flags.DEF]), 1, 0, 30),
            (Affix("GLOVES_DEF_2", 100, [Flags.FLAT, Flags.DESC_FLAT, Flags.DEF]), 0.8, 0, 30),
            (Affix("GLOVES_DEF_3", 200, [Flags.FLAT, Flags.DESC_FLAT, Flags.DEF]), 0.5, 10, 40),
            (Affix("GLOVES_DEF_4", 300, [Flags.FLAT, Flags.DESC_FLAT, Flags.DEF]), 0.3, 20, 60),
            (Affix("GLOVES_DEF_5", 500, [Flags.FLAT, Flags.DESC_FLAT, Flags.DEF]), 0.2, 30, 80),
            (Affix("GLOVES_DEF_6", 750, [Flags.FLAT, Flags.DESC_FLAT, Flags.DEF]), 0.1, 50, 999),
            (Affix("GLOVES_DEF_7", 1000, [Flags.FLAT, Flags.DESC_FLAT, Flags.DEF]), 0.05, 75, 999),
        ], 1.2),
        "dodge": ([
            (Affix("GLOVES_DODGE_RATING_1", 50, [Flags.FLAT, Flags.DESC_FLAT,\
                                                Flags.DODGE_RATING]), 1, 0, 30),
            (Affix("GLOVES_DODGE_RATING_2", 100, [Flags.FLAT, Flags.DESC_FLAT,\
                                                Flags.DODGE_RATING]), 0.8, 0, 30),
            (Affix("GLOVES_DODGE_RATING_3", 200, [Flags.FLAT, Flags.DESC_FLAT,\
                                                Flags.DODGE_RATING]), 0.5, 10, 40),
            (Affix("GLOVES_DODGE_RATING_4", 300, [Flags.FLAT, Flags.DESC_FLAT,\
                                                Flags.DODGE_RATING]), 0.3, 20, 60),
            (Affix("GLOVES_DODGE_RATING_5", 500, [Flags.FLAT, Flags.DESC_FLAT,\
                                                Flags.DODGE_RATING]), 0.2, 30, 80),
            (Affix("GLOVES_DODGE_RATING_6", 750, [Flags.FLAT, Flags.DESC_FLAT,\
                                                Flags.DODGE_RATING]), 0.1, 50, 999),
            (Affix("GLOVES_DODGE_RATING_7", 1000, [Flags.FLAT, Flags.DESC_FLAT,\
                                                Flags.DODGE_RATING]), 0.05, 75, 999),
        ], 1.2),
        "cooldown": ([
            (Affix("GLOVES_CSPEED_1", 0.05, [Flags.BOON,\
                                            Flags.CSPEED]), 1, 0, 50),
            (Affix("GLOVES_CSPEED_2", 0.1, [Flags.BOON,\
                                            Flags.CSPEED]), 0.8, 0, 70),
            (Affix("GLOVES_CSPEED_3", 0.15, [Flags.BOON,\
                                            Flags.CSPEED]), 0.5, 10, 90),
            (Affix("GLOVES_CSPEED_4", 0.2, [Flags.BOON,\
                                            Flags.CSPEED]), 0.3, 20, 999),
            (Affix("GLOVES_CSPEED_5", 0.25, [Flags.BOON,\
                                            Flags.CSPEED]), 0.2, 30, 999)
        ], 0.9),
        "phys_res": ([
            (Affix("GLOVES_PHYS_RES_1", 0.08, [Flags.PHYS, Flags.FLAT]), 1, 0, 60),
            (Affix("GLOVES_PHYS_RES_2", 0.12, [Flags.PHYS, Flags.FLAT]), 0.6, 10, 90),
            (Affix("GLOVES_PHYS_RES_3", 0.2, [Flags.PHYS, Flags.FLAT]), 0.3, 25, 999),
        ], 1),
        "fire_res": ([
            (Affix("GLOVES_FIRE_RES_1", 0.08, [Flags.FIRE, Flags.FLAT]), 1, 0, 60),
            (Affix("GLOVES_FIRE_RES_2", 0.12, [Flags.FIRE, Flags.FLAT]), 0.6, 10, 90),
            (Affix("GLOVES_FIRE_RES_3", 0.2, [Flags.FIRE, Flags.FLAT]), 0.3, 25, 999),
        ], 1),
        "ice_res": ([
            (Affix("GLOVES_ICE_RES_1", 0.08, [Flags.ICE, Flags.FLAT]), 1, 0, 60),
            (Affix("GLOVES_ICE_RES_2", 0.12, [Flags.ICE, Flags.FLAT]), 0.6, 10, 90),
            (Affix("GLOVES_ICE_RES_3", 0.2, [Flags.ICE, Flags.FLAT]), 0.3, 25, 999),
        ], 1),
        "elec_res": ([
            (Affix("GLOVES_ELEC_RES_1", 0.08, [Flags.ELEC, Flags.FLAT]), 1, 0, 60),
            (Affix("GLOVES_ELEC_RES_2", 0.12, [Flags.ELEC, Flags.FLAT]), 0.6, 10, 90),
            (Affix("GLOVES_ELEC_RES_3", 0.2, [Flags.ELEC, Flags.FLAT]), 0.3, 25, 999),
        ], 1),
        "light_res": ([
            (Affix("GLOVES_LIGHT_RES_1", 0.08, [Flags.LIGHT, Flags.FLAT]), 1, 0, 60),
            (Affix("GLOVES_LIGHT_RES_2", 0.12, [Flags.LIGHT, Flags.FLAT]), 0.6, 10, 90),
            (Affix("GLOVES_LIGHT_RES_3", 0.2, [Flags.LIGHT, Flags.FLAT]), 0.3, 25, 999),
        ], 1),
        "dark_res": ([
            (Affix("GLOVES_DARK_RES_1", 0.08, [Flags.DARK, Flags.FLAT]), 1, 0, 60),
            (Affix("GLOVES_DARK_RES_2", 0.12, [Flags.DARK, Flags.FLAT]), 0.6, 10, 90),
            (Affix("GLOVES_DARK_RES_3", 0.2, [Flags.DARK, Flags.FLAT]), 0.3, 25, 999),
        ], 1),
        "energ_res": ([
            (Affix("GLOVES_ENERG_RES_1", 0.08, [Flags.ENERG, Flags.FLAT]), 1, 0, 60),
            (Affix("GLOVES_ENERG_RES_2", 0.12, [Flags.ENERG, Flags.FLAT]), 0.6, 10, 90),
            (Affix("GLOVES_ENERG_RES_3", 0.2, [Flags.ENERG, Flags.FLAT]), 0.3, 25, 999),
        ], 1),
        "elemental_res": ([
            (Affix("GLOVES_ELEMENTAL_RESISTANCES_1", 0.08, [Flags.ELEMENTAL_RESISTANCES,\
                                                            Flags.FLAT]), 1, 20, 60),
            (Affix("GLOVES_ELEMENTAL_RESISTANCES_2", 0.12, [Flags.ELEMENTAL_RESISTANCES,\
                                                            Flags.FLAT]), 0.6, 40, 90),
            (Affix("GLOVES_ELEMENTAL_RESISTANCES_3", 0.2, [Flags.ELEMENTAL_RESISTANCES,\
                                                            Flags.FLAT]), 0.3, 60, 999),
        ], 0.8),
        "all_res": ([
            (Affix("GLOVES_ALL_RESISTANCES_1", 0.08, [Flags.ALL_RESISTANCES,\
                                                        Flags.FLAT]), 1, 20, 60),
            (Affix("GLOVES_ALL_RESISTANCES_2", 0.12, [Flags.ALL_RESISTANCES,\
                                                        Flags.FLAT]), 0.6, 40, 90),
            (Affix("GLOVES_ALL_RESISTANCES_3", 0.2, [Flags.ALL_RESISTANCES,\
                                                        Flags.FLAT]), 0.3, 60, 999),
        ], 0.25)
    },
    "rings": {
       "str": ([
            (Affix("RINGS_STR_1", 10, [Flags.FLAT, Flags.DESC_FLAT, Flags.STR]), 1, 0, 25),
            (Affix("RINGS_STR_2", 20, [Flags.FLAT, Flags.DESC_FLAT, Flags.STR]), 0.8, 0, 30),
            (Affix("RINGS_STR_3", 30, [Flags.FLAT, Flags.DESC_FLAT, Flags.STR]), 0.5, 10, 40),
            (Affix("RINGS_STR_4", 50, [Flags.FLAT, Flags.DESC_FLAT, Flags.STR]), 0.3, 20, 60),
            (Affix("RINGS_STR_5", 75, [Flags.FLAT, Flags.DESC_FLAT, Flags.STR]), 0.2, 30, 80),
            (Affix("RINGS_STR_6", 100, [Flags.FLAT, Flags.DESC_FLAT, Flags.STR]), 0.1, 50, 999),
            (Affix("RINGS_STR_7", 125, [Flags.FLAT, Flags.DESC_FLAT, Flags.STR]), 0.05, 75, 999),
        ], 1),
        "dex": ([
            (Affix("RINGS_DEX_1", 10, [Flags.FLAT, Flags.DESC_FLAT, Flags.DEX]), 1, 0, 25),
            (Affix("RINGS_DEX_2", 20, [Flags.FLAT, Flags.DESC_FLAT, Flags.DEX]), 0.8, 0, 30),
            (Affix("RINGS_DEX_3", 30, [Flags.FLAT, Flags.DESC_FLAT, Flags.DEX]), 0.5, 10, 40),
            (Affix("RINGS_DEX_4", 50, [Flags.FLAT, Flags.DESC_FLAT, Flags.DEX]), 0.3, 20, 60),
            (Affix("RINGS_DEX_5", 75, [Flags.FLAT, Flags.DESC_FLAT, Flags.DEX]), 0.2, 30, 80),
            (Affix("RINGS_DEX_6", 100, [Flags.FLAT, Flags.DESC_FLAT, Flags.DEX]), 0.1, 50, 999),
            (Affix("RINGS_DEX_7", 125, [Flags.FLAT, Flags.DESC_FLAT, Flags.DEX]), 0.05, 75, 999),
        ], 1),
        "int": ([
            (Affix("RINGS_INT_1", 10, [Flags.FLAT, Flags.DESC_FLAT, Flags.INT]), 1, 0, 25),
            (Affix("RINGS_INT_2", 20, [Flags.FLAT, Flags.DESC_FLAT, Flags.INT]), 0.8, 0, 30),
            (Affix("RINGS_INT_3", 30, [Flags.FLAT, Flags.DESC_FLAT, Flags.INT]), 0.5, 10, 40),
            (Affix("RINGS_INT_4", 50, [Flags.FLAT, Flags.DESC_FLAT, Flags.INT]), 0.3, 20, 60),
            (Affix("RINGS_INT_5", 75, [Flags.FLAT, Flags.DESC_FLAT, Flags.INT]), 0.2, 30, 80),
            (Affix("RINGS_INT_6", 100, [Flags.FLAT, Flags.DESC_FLAT, Flags.INT]), 0.1, 50, 999),
            (Affix("RINGS_INT_7", 125, [Flags.FLAT, Flags.DESC_FLAT, Flags.INT]), 0.05, 75, 999),
        ], 1),
        "life": ([
            (Affix("RINGS_LIFE_1", 5, [Flags.FLAT, Flags.DESC_FLAT, Flags.LIFE]), 1, 0, 25),
            (Affix("RINGS_LIFE_2", 10, [Flags.FLAT, Flags.DESC_FLAT, Flags.LIFE]), 0.8, 0, 30),
            (Affix("RINGS_LIFE_3", 15, [Flags.FLAT, Flags.DESC_FLAT, Flags.LIFE]), 0.5, 10, 40),
            (Affix("RINGS_LIFE_4", 20, [Flags.FLAT, Flags.DESC_FLAT, Flags.LIFE]), 0.3, 20, 60),
            (Affix("RINGS_LIFE_5", 25, [Flags.FLAT, Flags.DESC_FLAT, Flags.LIFE]), 0.2, 30, 80),
            (Affix("RINGS_LIFE_6", 50, [Flags.FLAT, Flags.DESC_FLAT, Flags.LIFE]), 0.1, 50, 999),
            (Affix("RINGS_LIFE_7", 75, [Flags.FLAT, Flags.DESC_FLAT, Flags.LIFE]), 0.05, 75, 999),
        ], 1),
        "life_incr": ([
            (Affix("RINGS_LIFE_INCR_1", 0.03, [Flags.BOON, Flags.LIFE]), 1, 0, 25),
            (Affix("RINGS_LIFE_INCR_2", 0.08, [Flags.BOON, Flags.LIFE]), 0.6, 15, 40),
            (Affix("RINGS_LIFE_INCR_3", 0.1, [Flags.BOON, Flags.LIFE]), 0.3, 25, 60),
            (Affix("RINGS_LIFE_INCR_4", 0.15, [Flags.BOON, Flags.LIFE]), 0.15, 50, 999),
            (Affix("RINGS_LIFE_INCR_5", 0.2, [Flags.BOON, Flags.LIFE]), 0.01, 75, 999)
        ], 0.8),
        "mana": ([
            (Affix("RINGS_MANA_1", 5, [Flags.FLAT, Flags.DESC_FLAT, Flags.MANA]), 1, 0, 25),
            (Affix("RINGS_MANA_2", 10, [Flags.FLAT, Flags.DESC_FLAT, Flags.MANA]), 0.8, 0, 30),
            (Affix("RINGS_MANA_3", 15, [Flags.FLAT, Flags.DESC_FLAT, Flags.MANA]), 0.5, 10, 40),
            (Affix("RINGS_MANA_4", 20, [Flags.FLAT, Flags.DESC_FLAT, Flags.MANA]), 0.3, 20, 60),
            (Affix("RINGS_MANA_5", 25, [Flags.FLAT, Flags.DESC_FLAT, Flags.MANA]), 0.2, 30, 80),
            (Affix("RINGS_MANA_6", 50, [Flags.FLAT, Flags.DESC_FLAT, Flags.MANA]), 0.1, 50, 999),
            (Affix("RINGS_MANA_7", 75, [Flags.FLAT, Flags.DESC_FLAT, Flags.MANA]), 0.05, 75, 999),
        ], 1),
        "mana_incr": ([
            (Affix("RINGS_MANA_INCR_1", 0.03, [Flags.BOON, Flags.MANA]), 1, 0, 25),
            (Affix("RINGS_MANA_INCR_2", 0.08, [Flags.BOON, Flags.MANA]), 0.6, 15, 40),
            (Affix("RINGS_MANA_INCR_3", 0.1, [Flags.BOON, Flags.MANA]), 0.3, 25, 60),
            (Affix("RINGS_MANA_INCR_4", 0.15, [Flags.BOON, Flags.MANA]), 0.15, 50, 999),
            (Affix("RINGS_MANA_INCR_5", 0.2, [Flags.BOON, Flags.MANA]), 0.01, 75, 999)
        ], 0.8),
        "cooldown": ([
            (Affix("RINGS_CSPEED_1", 0.05, [Flags.BOON,\
                                            Flags.CSPEED]), 1, 0, 50),
            (Affix("RINGS_CSPEED_2", 0.1, [Flags.BOON,\
                                            Flags.CSPEED]), 0.8, 0, 70),
            (Affix("RINGS_CSPEED_3", 0.15, [Flags.BOON,\
                                            Flags.CSPEED]), 0.5, 10, 90),
            (Affix("RINGS_CSPEED_4", 0.2, [Flags.BOON,\
                                            Flags.CSPEED]), 0.3, 20, 999),
            (Affix("RINGS_CSPEED_5", 0.25, [Flags.BOON,\
                                            Flags.CSPEED]), 0.2, 30, 999)
        ], 0.9),
        "precision": ([
            (Affix("RINGS_PRECISION_1", 50, [Flags.FLAT, Flags.DESC_FLAT,\
                                            Flags.PRECISION]), 1, 0, 30),
            (Affix("RINGS_PRECISION_2", 100, [Flags.FLAT, Flags.DESC_FLAT,\
                                            Flags.PRECISION]), 0.8, 0, 30),
            (Affix("RINGS_PRECISION_3", 200, [Flags.FLAT, Flags.DESC_FLAT,\
                                            Flags.PRECISION]), 0.5, 10, 40),
            (Affix("RINGS_PRECISION_4", 300, [Flags.FLAT, Flags.DESC_FLAT,\
                                            Flags.PRECISION]), 0.3, 20, 60),
            (Affix("RINGS_PRECISION_5", 500, [Flags.FLAT, Flags.DESC_FLAT,\
                                            Flags.PRECISION]), 0.2, 30, 80),
            (Affix("RINGS_PRECISION_6", 750, [Flags.FLAT, Flags.DESC_FLAT,\
                                            Flags.PRECISION]), 0.1, 50, 999),
            (Affix("RINGS_PRECISION_7", 1000, [Flags.FLAT, Flags.DESC_FLAT,\
                                            Flags.PRECISION]), 0.05, 75, 999),
        ], 0.9),
        "phys_res": ([
            (Affix("RINGS_PHYS_RES_1", 0.08, [Flags.PHYS, Flags.FLAT]), 1, 0, 60),
            (Affix("RINGS_PHYS_RES_2", 0.12, [Flags.PHYS, Flags.FLAT]), 0.6, 10, 90),
            (Affix("RINGS_PHYS_RES_3", 0.2, [Flags.PHYS, Flags.FLAT]), 0.3, 25, 999),
        ], 1),
        "fire_res": ([
            (Affix("RINGS_FIRE_RES_1", 0.08, [Flags.FIRE, Flags.FLAT]), 1, 0, 60),
            (Affix("RINGS_FIRE_RES_2", 0.12, [Flags.FIRE, Flags.FLAT]), 0.6, 10, 90),
            (Affix("RINGS_FIRE_RES_3", 0.2, [Flags.FIRE, Flags.FLAT]), 0.3, 25, 999),
        ], 1),
        "ice_res": ([
            (Affix("RINGS_ICE_RES_1", 0.08, [Flags.ICE, Flags.FLAT]), 1, 0, 60),
            (Affix("RINGS_ICE_RES_2", 0.12, [Flags.ICE, Flags.FLAT]), 0.6, 10, 90),
            (Affix("RINGS_ICE_RES_3", 0.2, [Flags.ICE, Flags.FLAT]), 0.3, 25, 999),
        ], 1),
        "elec_res": ([
            (Affix("RINGS_ELEC_RES_1", 0.08, [Flags.ELEC, Flags.FLAT]), 1, 0, 60),
            (Affix("RINGS_ELEC_RES_2", 0.12, [Flags.ELEC, Flags.FLAT]), 0.6, 10, 90),
            (Affix("RINGS_ELEC_RES_3", 0.2, [Flags.ELEC, Flags.FLAT]), 0.3, 25, 999),
        ], 1),
        "light_res": ([
            (Affix("RINGS_LIGHT_RES_1", 0.08, [Flags.LIGHT, Flags.FLAT]), 1, 0, 60),
            (Affix("RINGS_LIGHT_RES_2", 0.12, [Flags.LIGHT, Flags.FLAT]), 0.6, 10, 90),
            (Affix("RINGS_LIGHT_RES_3", 0.2, [Flags.LIGHT, Flags.FLAT]), 0.3, 25, 999),
        ], 1),
        "dark_res": ([
            (Affix("RINGS_DARK_RES_1", 0.08, [Flags.DARK, Flags.FLAT]), 1, 0, 60),
            (Affix("RINGS_DARK_RES_2", 0.12, [Flags.DARK, Flags.FLAT]), 0.6, 10, 90),
            (Affix("RINGS_DARK_RES_3", 0.2, [Flags.DARK, Flags.FLAT]), 0.3, 25, 999),
        ], 1),
        "energ_res": ([
            (Affix("RINGS_ENERG_RES_1", 0.08, [Flags.ENERG, Flags.FLAT]), 1, 0, 60),
            (Affix("RINGS_ENERG_RES_2", 0.12, [Flags.ENERG, Flags.FLAT]), 0.6, 10, 90),
            (Affix("RINGS_ENERG_RES_3", 0.2, [Flags.ENERG, Flags.FLAT]), 0.3, 25, 999),
        ], 1),
        "elemental_res": ([
            (Affix("RINGS_ELEMENTAL_RESISTANCES_1", 0.08, [Flags.ELEMENTAL_RESISTANCES,\
                                                            Flags.FLAT]), 1, 20, 60),
            (Affix("RINGS_ELEMENTAL_RESISTANCES_2", 0.12, [Flags.ELEMENTAL_RESISTANCES,\
                                                            Flags.FLAT]), 0.6, 40, 90),
            (Affix("RINGS_ELEMENTAL_RESISTANCES_3", 0.2, [Flags.ELEMENTAL_RESISTANCES,\
                                                            Flags.FLAT]), 0.3, 60, 999),
        ], 0.8),
        "all_res": ([
            (Affix("RINGS_ALL_RESISTANCES_1", 0.08, [Flags.ALL_RESISTANCES,\
                                                        Flags.FLAT]), 1, 20, 60),
            (Affix("RINGS_ALL_RESISTANCES_2", 0.12, [Flags.ALL_RESISTANCES,\
                                                        Flags.FLAT]), 0.6, 40, 90),
            (Affix("RINGS_ALL_RESISTANCES_3", 0.2, [Flags.ALL_RESISTANCES,\
                                                        Flags.FLAT]), 0.3, 60, 999),
        ], 0.25),
        "phys_dmg": ([
            (Affix("RINGS_PHYS_DMG_1", 0.1, [Flags.PHYS_DMG,\
                                                        Flags.BOON]), 1, 0, 75),
            (Affix("RINGS_PHYS_DMG_2", 0.2, [Flags.PHYS_DMG,\
                                                        Flags.BOON]), 0.8, 20, 80),
            (Affix("RINGS_PHYS_DMG_3", 0.4, [Flags.PHYS_DMG,\
                                                        Flags.BOON]), 0.6, 40, 999),
            (Affix("RINGS_PHYS_DMG_4", 0.6, [Flags.PHYS_DMG,\
                                                        Flags.BOON]), 0.25, 60, 999),
            (Affix("RINGS_PHYS_DMG_5", 1, [Flags.PHYS_DMG,\
                                                        Flags.BOON]), 0.1, 75, 999),
        ], 1),
        "fire_dmg": ([
            (Affix("RINGS_FIRE_DMG_1", 0.1, [Flags.FIRE_DMG,\
                                                        Flags.BOON]), 1, 0, 75),
            (Affix("RINGS_FIRE_DMG_2", 0.2, [Flags.FIRE_DMG,\
                                                        Flags.BOON]), 0.8, 20, 80),
            (Affix("RINGS_FIRE_DMG_3", 0.4, [Flags.FIRE_DMG,\
                                                        Flags.BOON]), 0.6, 40, 999),
            (Affix("RINGS_FIRE_DMG_4", 0.6, [Flags.FIRE_DMG,\
                                                        Flags.BOON]), 0.25, 60, 999),
            (Affix("RINGS_FIRE_DMG_5", 1, [Flags.FIRE_DMG,\
                                                        Flags.BOON]), 0.1, 75, 999),
        ], 1),
        "ice_dmg": ([
            (Affix("RINGS_ICE_DMG_1", 0.1, [Flags.ICE_DMG,\
                                                        Flags.BOON]), 1, 0, 75),
            (Affix("RINGS_ICE_DMG_2", 0.2, [Flags.ICE_DMG,\
                                                        Flags.BOON]), 0.8, 20, 80),
            (Affix("RINGS_ICE_DMG_3", 0.4, [Flags.ICE_DMG,\
                                                        Flags.BOON]), 0.6, 40, 999),
            (Affix("RINGS_ICE_DMG_4", 0.6, [Flags.ICE_DMG,\
                                                        Flags.BOON]), 0.25, 60, 999),
            (Affix("RINGS_ICE_DMG_5", 1, [Flags.ICE_DMG,\
                                                        Flags.BOON]), 0.1, 75, 999),
        ], 1),
        "elec_dmg": ([
            (Affix("RINGS_ELEC_DMG_1", 0.1, [Flags.ELEC_DMG,\
                                                        Flags.BOON]), 1, 0, 75),
            (Affix("RINGS_ELEC_DMG_2", 0.2, [Flags.ELEC_DMG,\
                                                        Flags.BOON]), 0.8, 20, 80),
            (Affix("RINGS_ELEC_DMG_3", 0.4, [Flags.ELEC_DMG,\
                                                        Flags.BOON]), 0.6, 40, 999),
            (Affix("RINGS_ELEC_DMG_4", 0.6, [Flags.ELEC_DMG,\
                                                        Flags.BOON]), 0.25, 60, 999),
            (Affix("RINGS_ELEC_DMG_5", 1, [Flags.ELEC_DMG,\
                                                        Flags.BOON]), 0.1, 75, 999),
        ], 1),
        "energy_dmg": ([
            (Affix("RINGS_ENERG_DMG_1", 0.1, [Flags.ENERG_DMG,\
                                                        Flags.BOON]), 1, 0, 75),
            (Affix("RINGS_ENERG_DMG_2", 0.2, [Flags.ENERG_DMG,\
                                                        Flags.BOON]), 0.8, 20, 80),
            (Affix("RINGS_ENERG_DMG_3", 0.4, [Flags.ENERG_DMG,\
                                                        Flags.BOON]), 0.6, 40, 999),
            (Affix("RINGS_ENERG_DMG_4", 0.6, [Flags.ENERG_DMG,\
                                                        Flags.BOON]), 0.25, 60, 999),
            (Affix("RINGS_ENERG_DMG_5", 1, [Flags.ENERG_DMG,\
                                                        Flags.BOON]), 0.1, 75, 999),
        ], 1),
        "light_dmg": ([
            (Affix("RINGS_LIGHT_DMG_1", 0.1, [Flags.LIGHT_DMG,\
                                                        Flags.BOON]), 1, 0, 75),
            (Affix("RINGS_LIGHT_DMG_2", 0.2, [Flags.LIGHT_DMG,\
                                                        Flags.BOON]), 0.8, 20, 80),
            (Affix("RINGS_LIGHT_DMG_3", 0.4, [Flags.LIGHT_DMG,\
                                                        Flags.BOON]), 0.6, 40, 999),
            (Affix("RINGS_LIGHT_DMG_4", 0.6, [Flags.LIGHT_DMG,\
                                                        Flags.BOON]), 0.25, 60, 999),
            (Affix("RINGS_LIGHT_DMG_5", 1, [Flags.LIGHT_DMG,\
                                                        Flags.BOON]), 0.1, 75, 999),
        ], 1),
        "dark_dmg": ([
            (Affix("RINGS_DARK_DMG_1", 0.1, [Flags.DARK_DMG,\
                                                        Flags.BOON]), 1, 0, 75),
            (Affix("RINGS_DARK_DMG_2", 0.2, [Flags.DARK_DMG,\
                                                        Flags.BOON]), 0.8, 20, 80),
            (Affix("RINGS_DARK_DMG_3", 0.4, [Flags.DARK_DMG,\
                                                        Flags.BOON]), 0.6, 40, 999),
            (Affix("RINGS_DARK_DMG_4", 0.6, [Flags.DARK_DMG,\
                                                        Flags.BOON]), 0.25, 60, 999),
            (Affix("RINGS_DARK_DMG_5", 1, [Flags.DARK_DMG,\
                                                        Flags.BOON]), 0.1, 75, 999),
        ], 1),
        "elemental_dmg": ([
            (Affix("RINGS_ELEMENTAL_DMG_1", 0.15, [Flags.ELEMENTAL_DAMAGE,\
                                                        Flags.BOON]), 1, 0, 75),
            (Affix("RINGS_ELEMENTAL_DMG_2", 0.25, [Flags.ELEMENTAL_DAMAGE,\
                                                        Flags.BOON]), 0.8, 20, 80),
            (Affix("RINGS_ELEMENTAL_DMG_3", 0.50, [Flags.ELEMENTAL_DAMAGE,\
                                                        Flags.BOON]), 0.6, 40, 999)
        ], 0.7),
        "all_dmg": ([
            (Affix("RINGS_ALL_DMG_1", 0.15, [Flags.ALL_DAMAGE,\
                                                        Flags.BOON]), 1, 0, 75),
            (Affix("RINGS_ALL_DMG_2", 0.25, [Flags.ALL_DAMAGE,\
                                                        Flags.BOON]), 0.8, 20, 80),
            (Affix("RINGS_ALL_DMG_3", 0.50, [Flags.ALL_DAMAGE,\
                                                        Flags.BOON]), 0.6, 40, 999)
        ], 0.1),
    },
    "amulets": {
        "str": ([
            (Affix("AMULET_STR_1", 15, [Flags.FLAT, Flags.DESC_FLAT, Flags.STR]), 1, 0, 25),
            (Affix("AMULET_STR_2", 30, [Flags.FLAT, Flags.DESC_FLAT, Flags.STR]), 0.8, 0, 30),
            (Affix("AMULET_STR_3", 50, [Flags.FLAT, Flags.DESC_FLAT, Flags.STR]), 0.5, 10, 40),
            (Affix("AMULET_STR_4", 80, [Flags.FLAT, Flags.DESC_FLAT, Flags.STR]), 0.3, 20, 60),
            (Affix("AMULET_STR_5", 100, [Flags.FLAT, Flags.DESC_FLAT, Flags.STR]), 0.2, 30, 80),
            (Affix("AMULET_STR_6", 125, [Flags.FLAT, Flags.DESC_FLAT, Flags.STR]), 0.1, 50, 999),
            (Affix("AMULET_STR_7", 200, [Flags.FLAT, Flags.DESC_FLAT, Flags.STR]), 0.05, 75, 999),
        ], 1),
        "dex": ([
            (Affix("AMULET_DEX_1", 15, [Flags.FLAT, Flags.DESC_FLAT, Flags.DEX]), 1, 0, 25),
            (Affix("AMULET_DEX_2", 30, [Flags.FLAT, Flags.DESC_FLAT, Flags.DEX]), 0.8, 0, 30),
            (Affix("AMULET_DEX_3", 50, [Flags.FLAT, Flags.DESC_FLAT, Flags.DEX]), 0.5, 10, 40),
            (Affix("AMULET_DEX_4", 80, [Flags.FLAT, Flags.DESC_FLAT, Flags.DEX]), 0.3, 20, 60),
            (Affix("AMULET_DEX_5", 100, [Flags.FLAT, Flags.DESC_FLAT, Flags.DEX]), 0.2, 30, 80),
            (Affix("AMULET_DEX_6", 125, [Flags.FLAT, Flags.DESC_FLAT, Flags.DEX]), 0.1, 50, 999),
            (Affix("AMULET_DEX_7", 200, [Flags.FLAT, Flags.DESC_FLAT, Flags.DEX]), 0.05, 75, 999),
        ], 1),
        "int": ([
            (Affix("AMULET_INT_1", 15, [Flags.FLAT, Flags.DESC_FLAT, Flags.INT]), 1, 0, 25),
            (Affix("AMULET_INT_2", 30, [Flags.FLAT, Flags.DESC_FLAT, Flags.INT]), 0.8, 0, 30),
            (Affix("AMULET_INT_3", 50, [Flags.FLAT, Flags.DESC_FLAT, Flags.INT]), 0.5, 10, 40),
            (Affix("AMULET_INT_4", 80, [Flags.FLAT, Flags.DESC_FLAT, Flags.INT]), 0.3, 20, 60),
            (Affix("AMULET_INT_5", 100, [Flags.FLAT, Flags.DESC_FLAT, Flags.INT]), 0.2, 30, 80),
            (Affix("AMULET_INT_6", 125, [Flags.FLAT, Flags.DESC_FLAT, Flags.INT]), 0.1, 50, 999),
            (Affix("AMULET_INT_7", 200, [Flags.FLAT, Flags.DESC_FLAT, Flags.INT]), 0.05, 75, 999),
        ], 1),
        "life": ([
            (Affix("AMULET_LIFE_1", 5, [Flags.FLAT, Flags.DESC_FLAT, Flags.LIFE]), 1, 0, 25),
            (Affix("AMULET_LIFE_2", 10, [Flags.FLAT, Flags.DESC_FLAT, Flags.LIFE]), 0.8, 0, 30),
            (Affix("AMULET_LIFE_3", 15, [Flags.FLAT, Flags.DESC_FLAT, Flags.LIFE]), 0.5, 10, 40),
            (Affix("AMULET_LIFE_4", 20, [Flags.FLAT, Flags.DESC_FLAT, Flags.LIFE]), 0.3, 20, 60),
            (Affix("AMULET_LIFE_5", 25, [Flags.FLAT, Flags.DESC_FLAT, Flags.LIFE]), 0.2, 30, 80),
            (Affix("AMULET_LIFE_6", 50, [Flags.FLAT, Flags.DESC_FLAT, Flags.LIFE]), 0.1, 50, 999),
            (Affix("AMULET_LIFE_7", 75, [Flags.FLAT, Flags.DESC_FLAT, Flags.LIFE]), 0.05, 75, 999),
        ], 1),
        "life_incr": ([
            (Affix("AMULET_LIFE_INCR_1", 0.03, [Flags.BOON, Flags.LIFE]), 1, 0, 25),
            (Affix("AMULET_LIFE_INCR_2", 0.08, [Flags.BOON, Flags.LIFE]), 0.6, 15, 40),
            (Affix("AMULET_LIFE_INCR_3", 0.1, [Flags.BOON, Flags.LIFE]), 0.3, 25, 60),
            (Affix("AMULET_LIFE_INCR_4", 0.15, [Flags.BOON, Flags.LIFE]), 0.15, 50, 999),
            (Affix("AMULET_LIFE_INCR_5", 0.2, [Flags.BOON, Flags.LIFE]), 0.01, 75, 999)
        ], 0.8),
        "mana": ([
            (Affix("AMULET_MANA_1", 5, [Flags.FLAT, Flags.DESC_FLAT, Flags.MANA]), 1, 0, 25),
            (Affix("AMULET_MANA_2", 10, [Flags.FLAT, Flags.DESC_FLAT, Flags.MANA]), 0.8, 0, 30),
            (Affix("AMULET_MANA_3", 15, [Flags.FLAT, Flags.DESC_FLAT, Flags.MANA]), 0.5, 10, 40),
            (Affix("AMULET_MANA_4", 20, [Flags.FLAT, Flags.DESC_FLAT, Flags.MANA]), 0.3, 20, 60),
            (Affix("AMULET_MANA_5", 25, [Flags.FLAT, Flags.DESC_FLAT, Flags.MANA]), 0.2, 30, 80),
            (Affix("AMULET_MANA_6", 50, [Flags.FLAT, Flags.DESC_FLAT, Flags.MANA]), 0.1, 50, 999),
            (Affix("AMULET_MANA_7", 75, [Flags.FLAT, Flags.DESC_FLAT, Flags.MANA]), 0.05, 75, 999),
        ], 1),
        "mana_incr": ([
            (Affix("AMULET_MANA_INCR_1", 0.03, [Flags.BOON, Flags.MANA]), 1, 0, 25),
            (Affix("AMULET_MANA_INCR_2", 0.08, [Flags.BOON, Flags.MANA]), 0.6, 15, 40),
            (Affix("AMULET_MANA_INCR_3", 0.1, [Flags.BOON, Flags.MANA]), 0.3, 25, 60),
            (Affix("AMULET_MANA_INCR_4", 0.15, [Flags.BOON, Flags.MANA]), 0.15, 50, 999),
            (Affix("AMULET_MANA_INCR_5", 0.2, [Flags.BOON, Flags.MANA]), 0.01, 75, 999)
        ], 0.8),
        "cooldown": ([
            (Affix("AMULET_CSPEED_1", 0.05, [Flags.BOON,\
                                            Flags.CSPEED]), 1, 0, 50),
            (Affix("AMULET_CSPEED_2", 0.1, [Flags.BOON,\
                                            Flags.CSPEED]), 0.8, 0, 70),
            (Affix("AMULET_CSPEED_3", 0.15, [Flags.BOON,\
                                            Flags.CSPEED]), 0.5, 10, 90),
            (Affix("AMULET_CSPEED_4", 0.2, [Flags.BOON,\
                                            Flags.CSPEED]), 0.3, 20, 999),
            (Affix("AMULET_CSPEED_5", 0.25, [Flags.BOON,\
                                            Flags.CSPEED]), 0.2, 30, 999)
        ], 0.9),
        "precision": ([
            (Affix("AMULET_PRECISION_1", 50, [Flags.FLAT, Flags.DESC_FLAT,\
                                            Flags.PRECISION]), 1, 0, 30),
            (Affix("AMULET_PRECISION_2", 100, [Flags.FLAT, Flags.DESC_FLAT,\
                                            Flags.PRECISION]), 0.8, 0, 30),
            (Affix("AMULET_PRECISION_3", 200, [Flags.FLAT, Flags.DESC_FLAT,\
                                            Flags.PRECISION]), 0.5, 10, 40),
            (Affix("AMULET_PRECISION_4", 300, [Flags.FLAT, Flags.DESC_FLAT,\
                                            Flags.PRECISION]), 0.3, 20, 60),
            (Affix("AMULET_PRECISION_5", 500, [Flags.FLAT, Flags.DESC_FLAT,\
                                            Flags.PRECISION]), 0.2, 30, 80),
            (Affix("AMULET_PRECISION_6", 750, [Flags.FLAT, Flags.DESC_FLAT,\
                                            Flags.PRECISION]), 0.1, 50, 999),
            (Affix("AMULET_PRECISION_7", 1000, [Flags.FLAT, Flags.DESC_FLAT,\
                                            Flags.PRECISION]), 0.05, 75, 999),
        ], 0.9),
        "phys_res": ([
            (Affix("AMULET_PHYS_RES_1", 0.08, [Flags.PHYS, Flags.FLAT]), 1, 0, 60),
            (Affix("AMULET_PHYS_RES_2", 0.12, [Flags.PHYS, Flags.FLAT]), 0.6, 10, 90),
            (Affix("AMULET_PHYS_RES_3", 0.2, [Flags.PHYS, Flags.FLAT]), 0.3, 25, 999),
        ], 1),
        "fire_res": ([
            (Affix("AMULET_FIRE_RES_1", 0.08, [Flags.FIRE, Flags.FLAT]), 1, 0, 60),
            (Affix("AMULET_FIRE_RES_2", 0.12, [Flags.FIRE, Flags.FLAT]), 0.6, 10, 90),
            (Affix("AMULET_FIRE_RES_3", 0.2, [Flags.FIRE, Flags.FLAT]), 0.3, 25, 999),
        ], 1),
        "ice_res": ([
            (Affix("AMULET_ICE_RES_1", 0.08, [Flags.ICE, Flags.FLAT]), 1, 0, 60),
            (Affix("AMULET_ICE_RES_2", 0.12, [Flags.ICE, Flags.FLAT]), 0.6, 10, 90),
            (Affix("AMULET_ICE_RES_3", 0.2, [Flags.ICE, Flags.FLAT]), 0.3, 25, 999),
        ], 1),
        "elec_res": ([
            (Affix("AMULET_ELEC_RES_1", 0.08, [Flags.ELEC, Flags.FLAT]), 1, 0, 60),
            (Affix("AMULET_ELEC_RES_2", 0.12, [Flags.ELEC, Flags.FLAT]), 0.6, 10, 90),
            (Affix("AMULET_ELEC_RES_3", 0.2, [Flags.ELEC, Flags.FLAT]), 0.3, 25, 999),
        ], 1),
        "light_res": ([
            (Affix("AMULET_LIGHT_RES_1", 0.08, [Flags.LIGHT, Flags.FLAT]), 1, 0, 60),
            (Affix("AMULET_LIGHT_RES_2", 0.12, [Flags.LIGHT, Flags.FLAT]), 0.6, 10, 90),
            (Affix("AMULET_LIGHT_RES_3", 0.2, [Flags.LIGHT, Flags.FLAT]), 0.3, 25, 999),
        ], 1),
        "dark_res": ([
            (Affix("AMULET_DARK_RES_1", 0.08, [Flags.DARK, Flags.FLAT]), 1, 0, 60),
            (Affix("AMULET_DARK_RES_2", 0.12, [Flags.DARK, Flags.FLAT]), 0.6, 10, 90),
            (Affix("AMULET_DARK_RES_3", 0.2, [Flags.DARK, Flags.FLAT]), 0.3, 25, 999),
        ], 1),
        "energ_res": ([
            (Affix("AMULET_ENERG_RES_1", 0.08, [Flags.ENERG, Flags.FLAT]), 1, 0, 60),
            (Affix("AMULET_ENERG_RES_2", 0.12, [Flags.ENERG, Flags.FLAT]), 0.6, 10, 90),
            (Affix("AMULET_ENERG_RES_3", 0.2, [Flags.ENERG, Flags.FLAT]), 0.3, 25, 999),
        ], 1),
        "elemental_res": ([
            (Affix("AMULET_ELEMENTAL_RESISTANCES_1", 0.08, [Flags.ELEMENTAL_RESISTANCES,\
                                                            Flags.FLAT]), 1, 20, 60),
            (Affix("AMULET_ELEMENTAL_RESISTANCES_2", 0.12, [Flags.ELEMENTAL_RESISTANCES,\
                                                            Flags.FLAT]), 0.6, 40, 90),
            (Affix("AMULET_ELEMENTAL_RESISTANCES_3", 0.2, [Flags.ELEMENTAL_RESISTANCES,\
                                                            Flags.FLAT]), 0.3, 60, 999),
        ], 0.8),
        "all_res": ([
            (Affix("AMULET_ALL_RESISTANCES_1", 0.08, [Flags.ALL_RESISTANCES,\
                                                        Flags.FLAT]), 1, 20, 60),
            (Affix("AMULET_ALL_RESISTANCES_2", 0.12, [Flags.ALL_RESISTANCES,\
                                                        Flags.FLAT]), 0.6, 40, 90),
            (Affix("AMULET_ALL_RESISTANCES_3", 0.2, [Flags.ALL_RESISTANCES,\
                                                        Flags.FLAT]), 0.3, 60, 999),
        ], 0.25),
        "phys_dmg": ([
            (Affix("AMULET_PHYS_DMG_1", 0.1, [Flags.PHYS_DMG,\
                                                        Flags.BOON]), 1, 0, 75),
            (Affix("AMULET_PHYS_DMG_2", 0.2, [Flags.PHYS_DMG,\
                                                        Flags.BOON]), 0.8, 20, 80),
            (Affix("AMULET_PHYS_DMG_3", 0.4, [Flags.PHYS_DMG,\
                                                        Flags.BOON]), 0.6, 40, 999),
            (Affix("AMULET_PHYS_DMG_4", 0.6, [Flags.PHYS_DMG,\
                                                        Flags.BOON]), 0.25, 60, 999),
            (Affix("AMULET_PHYS_DMG_5", 1, [Flags.PHYS_DMG,\
                                                        Flags.BOON]), 0.1, 75, 999),
        ], 1),
        "fire_dmg": ([
            (Affix("AMULET_FIRE_DMG_1", 0.1, [Flags.FIRE_DMG,\
                                                        Flags.BOON]), 1, 0, 75),
            (Affix("AMULET_FIRE_DMG_2", 0.2, [Flags.FIRE_DMG,\
                                                        Flags.BOON]), 0.8, 20, 80),
            (Affix("AMULET_FIRE_DMG_3", 0.4, [Flags.FIRE_DMG,\
                                                        Flags.BOON]), 0.6, 40, 999),
            (Affix("AMULET_FIRE_DMG_4", 0.6, [Flags.FIRE_DMG,\
                                                        Flags.BOON]), 0.25, 60, 999),
            (Affix("AMULET_FIRE_DMG_5", 1, [Flags.FIRE_DMG,\
                                                        Flags.BOON]), 0.1, 75, 999),
        ], 1),
        "ice_dmg": ([
            (Affix("AMULET_ICE_DMG_1", 0.1, [Flags.ICE_DMG,\
                                                        Flags.BOON]), 1, 0, 75),
            (Affix("AMULET_ICE_DMG_2", 0.2, [Flags.ICE_DMG,\
                                                        Flags.BOON]), 0.8, 20, 80),
            (Affix("AMULET_ICE_DMG_3", 0.4, [Flags.ICE_DMG,\
                                                        Flags.BOON]), 0.6, 40, 999),
            (Affix("AMULET_ICE_DMG_4", 0.6, [Flags.ICE_DMG,\
                                                        Flags.BOON]), 0.25, 60, 999),
            (Affix("AMULET_ICE_DMG_5", 1, [Flags.ICE_DMG,\
                                                        Flags.BOON]), 0.1, 75, 999),
        ], 1),
        "elec_dmg": ([
            (Affix("AMULET_ELEC_DMG_1", 0.1, [Flags.ELEC_DMG,\
                                                        Flags.BOON]), 1, 0, 75),
            (Affix("AMULET_ELEC_DMG_2", 0.2, [Flags.ELEC_DMG,\
                                                        Flags.BOON]), 0.8, 20, 80),
            (Affix("AMULET_ELEC_DMG_3", 0.4, [Flags.ELEC_DMG,\
                                                        Flags.BOON]), 0.6, 40, 999),
            (Affix("AMULET_ELEC_DMG_4", 0.6, [Flags.ELEC_DMG,\
                                                        Flags.BOON]), 0.25, 60, 999),
            (Affix("AMULET_ELEC_DMG_5", 1, [Flags.ELEC_DMG,\
                                                        Flags.BOON]), 0.1, 75, 999),
        ], 1),
        "energy_dmg": ([
            (Affix("AMULET_ENERG_DMG_1", 0.1, [Flags.ENERG_DMG,\
                                                        Flags.BOON]), 1, 0, 75),
            (Affix("AMULET_ENERG_DMG_2", 0.2, [Flags.ENERG_DMG,\
                                                        Flags.BOON]), 0.8, 20, 80),
            (Affix("AMULET_ENERG_DMG_3", 0.4, [Flags.ENERG_DMG,\
                                                        Flags.BOON]), 0.6, 40, 999),
            (Affix("AMULET_ENERG_DMG_4", 0.6, [Flags.ENERG_DMG,\
                                                        Flags.BOON]), 0.25, 60, 999),
            (Affix("AMULET_ENERG_DMG_5", 1, [Flags.ENERG_DMG,\
                                                        Flags.BOON]), 0.1, 75, 999),
        ], 1),
        "light_dmg": ([
            (Affix("AMULET_LIGHT_DMG_1", 0.1, [Flags.LIGHT_DMG,\
                                                        Flags.BOON]), 1, 0, 75),
            (Affix("AMULET_LIGHT_DMG_2", 0.2, [Flags.LIGHT_DMG,\
                                                        Flags.BOON]), 0.8, 20, 80),
            (Affix("AMULET_LIGHT_DMG_3", 0.4, [Flags.LIGHT_DMG,\
                                                        Flags.BOON]), 0.6, 40, 999),
            (Affix("AMULET_LIGHT_DMG_4", 0.6, [Flags.LIGHT_DMG,\
                                                        Flags.BOON]), 0.25, 60, 999),
            (Affix("AMULET_LIGHT_DMG_5", 1, [Flags.LIGHT_DMG,\
                                                        Flags.BOON]), 0.1, 75, 999),
        ], 1),
        "dark_dmg": ([
            (Affix("AMULET_DARK_DMG_1", 0.1, [Flags.DARK_DMG,\
                                                        Flags.BOON]), 1, 0, 75),
            (Affix("AMULET_DARK_DMG_2", 0.2, [Flags.DARK_DMG,\
                                                        Flags.BOON]), 0.8, 20, 80),
            (Affix("AMULET_DARK_DMG_3", 0.4, [Flags.DARK_DMG,\
                                                        Flags.BOON]), 0.6, 40, 999),
            (Affix("AMULET_DARK_DMG_4", 0.6, [Flags.DARK_DMG,\
                                                        Flags.BOON]), 0.25, 60, 999),
            (Affix("AMULET_DARK_DMG_5", 1, [Flags.DARK_DMG,\
                                                        Flags.BOON]), 0.1, 75, 999),
        ], 1),
        "elemental_dmg": ([
            (Affix("AMULET_ELEMENTAL_DMG_1", 0.15, [Flags.ELEMENTAL_DAMAGE,\
                                                        Flags.BOON]), 1, 0, 75),
            (Affix("AMULET_ELEMENTAL_DMG_2", 0.25, [Flags.ELEMENTAL_DAMAGE,\
                                                        Flags.BOON]), 0.8, 20, 80),
            (Affix("AMULET_ELEMENTAL_DMG_3", 0.50, [Flags.ELEMENTAL_DAMAGE,\
                                                        Flags.BOON]), 0.6, 40, 999)
        ], 0.7),
        "all_dmg": ([
            (Affix("AMULET_ALL_DMG_1", 0.15, [Flags.ALL_DAMAGE,\
                                                        Flags.BOON]), 1, 0, 75),
            (Affix("AMULET_ALL_DMG_2", 0.25, [Flags.ALL_DAMAGE,\
                                                        Flags.BOON]), 0.8, 20, 80),
            (Affix("AMULET_ALL_DMG_3", 0.50, [Flags.ALL_DAMAGE,\
                                                        Flags.BOON]), 0.6, 40, 999)
        ], 0.1),
    },
    "belts": {
        "str": ([
            (Affix("BELT_STR_1", 15, [Flags.FLAT, Flags.DESC_FLAT, Flags.STR]), 1, 0, 25),
            (Affix("BELT_STR_2", 30, [Flags.FLAT, Flags.DESC_FLAT, Flags.STR]), 0.8, 0, 30),
            (Affix("BELT_STR_3", 50, [Flags.FLAT, Flags.DESC_FLAT, Flags.STR]), 0.5, 10, 40),
            (Affix("BELT_STR_4", 80, [Flags.FLAT, Flags.DESC_FLAT, Flags.STR]), 0.3, 20, 60),
            (Affix("BELT_STR_5", 100, [Flags.FLAT, Flags.DESC_FLAT, Flags.STR]), 0.2, 30, 80),
            (Affix("BELT_STR_6", 125, [Flags.FLAT, Flags.DESC_FLAT, Flags.STR]), 0.1, 50, 999),
            (Affix("BELT_STR_7", 200, [Flags.FLAT, Flags.DESC_FLAT, Flags.STR]), 0.05, 75, 999),
        ], 1),
        "dex": ([
            (Affix("BELT_DEX_1", 15, [Flags.FLAT, Flags.DESC_FLAT, Flags.DEX]), 1, 0, 25),
            (Affix("BELT_DEX_2", 30, [Flags.FLAT, Flags.DESC_FLAT, Flags.DEX]), 0.8, 0, 30),
            (Affix("BELT_DEX_3", 50, [Flags.FLAT, Flags.DESC_FLAT, Flags.DEX]), 0.5, 10, 40),
            (Affix("BELT_DEX_4", 80, [Flags.FLAT, Flags.DESC_FLAT, Flags.DEX]), 0.3, 20, 60),
            (Affix("BELT_DEX_5", 100, [Flags.FLAT, Flags.DESC_FLAT, Flags.DEX]), 0.2, 30, 80),
            (Affix("BELT_DEX_6", 125, [Flags.FLAT, Flags.DESC_FLAT, Flags.DEX]), 0.1, 50, 999),
            (Affix("BELT_DEX_7", 200, [Flags.FLAT, Flags.DESC_FLAT, Flags.DEX]), 0.05, 75, 999),
        ], 1),
        "int": ([
            (Affix("BELT_INT_1", 15, [Flags.FLAT, Flags.DESC_FLAT, Flags.INT]), 1, 0, 25),
            (Affix("BELT_INT_2", 30, [Flags.FLAT, Flags.DESC_FLAT, Flags.INT]), 0.8, 0, 30),
            (Affix("BELT_INT_3", 50, [Flags.FLAT, Flags.DESC_FLAT, Flags.INT]), 0.5, 10, 40),
            (Affix("BELT_INT_4", 80, [Flags.FLAT, Flags.DESC_FLAT, Flags.INT]), 0.3, 20, 60),
            (Affix("BELT_INT_5", 100, [Flags.FLAT, Flags.DESC_FLAT, Flags.INT]), 0.2, 30, 80),
            (Affix("BELT_INT_6", 125, [Flags.FLAT, Flags.DESC_FLAT, Flags.INT]), 0.1, 50, 999),
            (Affix("BELT_INT_7", 200, [Flags.FLAT, Flags.DESC_FLAT, Flags.INT]), 0.05, 75, 999),
        ], 1),
        "life": ([
            (Affix("BELT_LIFE_1", 5, [Flags.FLAT, Flags.DESC_FLAT, Flags.LIFE]), 1, 0, 25),
            (Affix("BELT_LIFE_2", 10, [Flags.FLAT, Flags.DESC_FLAT, Flags.LIFE]), 0.8, 0, 30),
            (Affix("BELT_LIFE_3", 15, [Flags.FLAT, Flags.DESC_FLAT, Flags.LIFE]), 0.5, 10, 40),
            (Affix("BELT_LIFE_4", 20, [Flags.FLAT, Flags.DESC_FLAT, Flags.LIFE]), 0.3, 20, 60),
            (Affix("BELT_LIFE_5", 25, [Flags.FLAT, Flags.DESC_FLAT, Flags.LIFE]), 0.2, 30, 80),
            (Affix("BELT_LIFE_6", 50, [Flags.FLAT, Flags.DESC_FLAT, Flags.LIFE]), 0.1, 50, 999),
            (Affix("BELT_LIFE_7", 75, [Flags.FLAT, Flags.DESC_FLAT, Flags.LIFE]), 0.05, 75, 999),
        ], 1),
        "life_incr": ([
            (Affix("BELT_LIFE_INCR_1", 0.03, [Flags.BOON, Flags.LIFE]), 1, 0, 25),
            (Affix("BELT_LIFE_INCR_2", 0.08, [Flags.BOON, Flags.LIFE]), 0.6, 15, 40),
            (Affix("BELT_LIFE_INCR_3", 0.1, [Flags.BOON, Flags.LIFE]), 0.3, 25, 60),
            (Affix("BELT_LIFE_INCR_4", 0.15, [Flags.BOON, Flags.LIFE]), 0.15, 50, 999),
            (Affix("BELT_LIFE_INCR_5", 0.2, [Flags.BOON, Flags.LIFE]), 0.01, 75, 999)
        ], 0.8),
        "mana": ([
            (Affix("BELT_MANA_1", 5, [Flags.FLAT, Flags.DESC_FLAT, Flags.MANA]), 1, 0, 25),
            (Affix("BELT_MANA_2", 10, [Flags.FLAT, Flags.DESC_FLAT, Flags.MANA]), 0.8, 0, 30),
            (Affix("BELT_MANA_3", 15, [Flags.FLAT, Flags.DESC_FLAT, Flags.MANA]), 0.5, 10, 40),
            (Affix("BELT_MANA_4", 20, [Flags.FLAT, Flags.DESC_FLAT, Flags.MANA]), 0.3, 20, 60),
            (Affix("BELT_MANA_5", 25, [Flags.FLAT, Flags.DESC_FLAT, Flags.MANA]), 0.2, 30, 80),
            (Affix("BELT_MANA_6", 50, [Flags.FLAT, Flags.DESC_FLAT, Flags.MANA]), 0.1, 50, 999),
            (Affix("BELT_MANA_7", 75, [Flags.FLAT, Flags.DESC_FLAT, Flags.MANA]), 0.05, 75, 999),
        ], 1),
        "mana_incr": ([
            (Affix("BELT_MANA_INCR_1", 0.03, [Flags.BOON, Flags.MANA]), 1, 0, 25),
            (Affix("BELT_MANA_INCR_2", 0.08, [Flags.BOON, Flags.MANA]), 0.6, 15, 40),
            (Affix("BELT_MANA_INCR_3", 0.1, [Flags.BOON, Flags.MANA]), 0.3, 25, 60),
            (Affix("BELT_MANA_INCR_4", 0.15, [Flags.BOON, Flags.MANA]), 0.15, 50, 999),
            (Affix("BELT_MANA_INCR_5", 0.2, [Flags.BOON, Flags.MANA]), 0.01, 75, 999)
        ], 0.8),
        "cooldown": ([
            (Affix("BELT_CSPEED_1", 0.05, [Flags.BOON,\
                                            Flags.CSPEED]), 1, 0, 50),
            (Affix("BELT_CSPEED_2", 0.1, [Flags.BOON,\
                                            Flags.CSPEED]), 0.8, 0, 70),
            (Affix("BELT_CSPEED_3", 0.15, [Flags.BOON,\
                                            Flags.CSPEED]), 0.5, 10, 90),
            (Affix("BELT_CSPEED_4", 0.2, [Flags.BOON,\
                                            Flags.CSPEED]), 0.3, 20, 999),
            (Affix("BELT_CSPEED_5", 0.25, [Flags.BOON,\
                                            Flags.CSPEED]), 0.2, 30, 999)
        ], 0.9),
        "precision": ([
            (Affix("BELT_PRECISION_1", 50, [Flags.FLAT, Flags.DESC_FLAT,\
                                            Flags.PRECISION]), 1, 0, 30),
            (Affix("BELT_PRECISION_2", 100, [Flags.FLAT, Flags.DESC_FLAT,\
                                            Flags.PRECISION]), 0.8, 0, 30),
            (Affix("BELT_PRECISION_3", 200, [Flags.FLAT, Flags.DESC_FLAT,\
                                            Flags.PRECISION]), 0.5, 10, 40),
            (Affix("BELT_PRECISION_4", 300, [Flags.FLAT, Flags.DESC_FLAT,\
                                            Flags.PRECISION]), 0.3, 20, 60),
            (Affix("BELT_PRECISION_5", 500, [Flags.FLAT, Flags.DESC_FLAT,\
                                            Flags.PRECISION]), 0.2, 30, 80),
            (Affix("BELT_PRECISION_6", 750, [Flags.FLAT, Flags.DESC_FLAT,\
                                            Flags.PRECISION]), 0.1, 50, 999),
            (Affix("BELT_PRECISION_7", 1000, [Flags.FLAT, Flags.DESC_FLAT,\
                                            Flags.PRECISION]), 0.05, 75, 999),
        ], 0.9),
        "phys_res": ([
            (Affix("BELT_PHYS_RES_1", 0.08, [Flags.PHYS, Flags.FLAT]), 1, 0, 60),
            (Affix("BELT_PHYS_RES_2", 0.12, [Flags.PHYS, Flags.FLAT]), 0.6, 10, 90),
            (Affix("BELT_PHYS_RES_3", 0.2, [Flags.PHYS, Flags.FLAT]), 0.3, 25, 999),
        ], 1),
        "fire_res": ([
            (Affix("BELT_FIRE_RES_1", 0.08, [Flags.FIRE, Flags.FLAT]), 1, 0, 60),
            (Affix("BELT_FIRE_RES_2", 0.12, [Flags.FIRE, Flags.FLAT]), 0.6, 10, 90),
            (Affix("BELT_FIRE_RES_3", 0.2, [Flags.FIRE, Flags.FLAT]), 0.3, 25, 999),
        ], 1),
        "ice_res": ([
            (Affix("BELT_ICE_RES_1", 0.08, [Flags.ICE, Flags.FLAT]), 1, 0, 60),
            (Affix("BELT_ICE_RES_2", 0.12, [Flags.ICE, Flags.FLAT]), 0.6, 10, 90),
            (Affix("BELT_ICE_RES_3", 0.2, [Flags.ICE, Flags.FLAT]), 0.3, 25, 999),
        ], 1),
        "elec_res": ([
            (Affix("BELT_ELEC_RES_1", 0.08, [Flags.ELEC, Flags.FLAT]), 1, 0, 60),
            (Affix("BELT_ELEC_RES_2", 0.12, [Flags.ELEC, Flags.FLAT]), 0.6, 10, 90),
            (Affix("BELT_ELEC_RES_3", 0.2, [Flags.ELEC, Flags.FLAT]), 0.3, 25, 999),
        ], 1),
        "light_res": ([
            (Affix("BELT_LIGHT_RES_1", 0.08, [Flags.LIGHT, Flags.FLAT]), 1, 0, 60),
            (Affix("BELT_LIGHT_RES_2", 0.12, [Flags.LIGHT, Flags.FLAT]), 0.6, 10, 90),
            (Affix("BELT_LIGHT_RES_3", 0.2, [Flags.LIGHT, Flags.FLAT]), 0.3, 25, 999),
        ], 1),
        "dark_res": ([
            (Affix("BELT_DARK_RES_1", 0.08, [Flags.DARK, Flags.FLAT]), 1, 0, 60),
            (Affix("BELT_DARK_RES_2", 0.12, [Flags.DARK, Flags.FLAT]), 0.6, 10, 90),
            (Affix("BELT_DARK_RES_3", 0.2, [Flags.DARK, Flags.FLAT]), 0.3, 25, 999),
        ], 1),
        "energ_res": ([
            (Affix("BELT_ENERG_RES_1", 0.08, [Flags.ENERG, Flags.FLAT]), 1, 0, 60),
            (Affix("BELT_ENERG_RES_2", 0.12, [Flags.ENERG, Flags.FLAT]), 0.6, 10, 90),
            (Affix("BELT_ENERG_RES_3", 0.2, [Flags.ENERG, Flags.FLAT]), 0.3, 25, 999),
        ], 1),
        "elemental_res": ([
            (Affix("BELT_ELEMENTAL_RESISTANCES_1", 0.08, [Flags.ELEMENTAL_RESISTANCES,\
                                                            Flags.FLAT]), 1, 20, 60),
            (Affix("BELT_ELEMENTAL_RESISTANCES_2", 0.12, [Flags.ELEMENTAL_RESISTANCES,\
                                                            Flags.FLAT]), 0.6, 40, 90),
            (Affix("BELT_ELEMENTAL_RESISTANCES_3", 0.2, [Flags.ELEMENTAL_RESISTANCES,\
                                                            Flags.FLAT]), 0.3, 60, 999),
        ], 0.8),
        "all_res": ([
            (Affix("BELT_ALL_RESISTANCES_1", 0.08, [Flags.ALL_RESISTANCES,\
                                                        Flags.FLAT]), 1, 20, 60),
            (Affix("BELT_ALL_RESISTANCES_2", 0.12, [Flags.ALL_RESISTANCES,\
                                                        Flags.FLAT]), 0.6, 40, 90),
            (Affix("BELT_ALL_RESISTANCES_3", 0.2, [Flags.ALL_RESISTANCES,\
                                                        Flags.FLAT]), 0.3, 60, 999),
        ], 0.25),
        "phys_dmg": ([
            (Affix("BELT_PHYS_DMG_1", 0.1, [Flags.PHYS_DMG,\
                                                        Flags.BOON]), 1, 0, 75),
            (Affix("BELT_PHYS_DMG_2", 0.2, [Flags.PHYS_DMG,\
                                                        Flags.BOON]), 0.8, 20, 80),
            (Affix("BELT_PHYS_DMG_3", 0.4, [Flags.PHYS_DMG,\
                                                        Flags.BOON]), 0.6, 40, 999),
            (Affix("BELT_PHYS_DMG_4", 0.6, [Flags.PHYS_DMG,\
                                                        Flags.BOON]), 0.25, 60, 999),
            (Affix("BELT_PHYS_DMG_5", 1, [Flags.PHYS_DMG,\
                                                        Flags.BOON]), 0.1, 75, 999),
        ], 1),
        "fire_dmg": ([
            (Affix("BELT_FIRE_DMG_1", 0.1, [Flags.FIRE_DMG,\
                                                        Flags.BOON]), 1, 0, 75),
            (Affix("BELT_FIRE_DMG_2", 0.2, [Flags.FIRE_DMG,\
                                                        Flags.BOON]), 0.8, 20, 80),
            (Affix("BELT_FIRE_DMG_3", 0.4, [Flags.FIRE_DMG,\
                                                        Flags.BOON]), 0.6, 40, 999),
            (Affix("BELT_FIRE_DMG_4", 0.6, [Flags.FIRE_DMG,\
                                                        Flags.BOON]), 0.25, 60, 999),
            (Affix("BELT_FIRE_DMG_5", 1, [Flags.FIRE_DMG,\
                                                        Flags.BOON]), 0.1, 75, 999),
        ], 1),
        "ice_dmg": ([
            (Affix("BELT_ICE_DMG_1", 0.1, [Flags.ICE_DMG,\
                                                        Flags.BOON]), 1, 0, 75),
            (Affix("BELT_ICE_DMG_2", 0.2, [Flags.ICE_DMG,\
                                                        Flags.BOON]), 0.8, 20, 80),
            (Affix("BELT_ICE_DMG_3", 0.4, [Flags.ICE_DMG,\
                                                        Flags.BOON]), 0.6, 40, 999),
            (Affix("BELT_ICE_DMG_4", 0.6, [Flags.ICE_DMG,\
                                                        Flags.BOON]), 0.25, 60, 999),
            (Affix("BELT_ICE_DMG_5", 1, [Flags.ICE_DMG,\
                                                        Flags.BOON]), 0.1, 75, 999),
        ], 1),
        "elec_dmg": ([
            (Affix("BELT_ELEC_DMG_1", 0.1, [Flags.ELEC_DMG,\
                                                        Flags.BOON]), 1, 0, 75),
            (Affix("BELT_ELEC_DMG_2", 0.2, [Flags.ELEC_DMG,\
                                                        Flags.BOON]), 0.8, 20, 80),
            (Affix("BELT_ELEC_DMG_3", 0.4, [Flags.ELEC_DMG,\
                                                        Flags.BOON]), 0.6, 40, 999),
            (Affix("BELT_ELEC_DMG_4", 0.6, [Flags.ELEC_DMG,\
                                                        Flags.BOON]), 0.25, 60, 999),
            (Affix("BELT_ELEC_DMG_5", 1, [Flags.ELEC_DMG,\
                                                        Flags.BOON]), 0.1, 75, 999),
        ], 1),
        "energy_dmg": ([
            (Affix("BELT_ENERG_DMG_1", 0.1, [Flags.ENERG_DMG,\
                                                        Flags.BOON]), 1, 0, 75),
            (Affix("BELT_ENERG_DMG_2", 0.2, [Flags.ENERG_DMG,\
                                                        Flags.BOON]), 0.8, 20, 80),
            (Affix("BELT_ENERG_DMG_3", 0.4, [Flags.ENERG_DMG,\
                                                        Flags.BOON]), 0.6, 40, 999),
            (Affix("BELT_ENERG_DMG_4", 0.6, [Flags.ENERG_DMG,\
                                                        Flags.BOON]), 0.25, 60, 999),
            (Affix("BELT_ENERG_DMG_5", 1, [Flags.ENERG_DMG,\
                                                        Flags.BOON]), 0.1, 75, 999),
        ], 1),
        "light_dmg": ([
            (Affix("BELT_LIGHT_DMG_1", 0.1, [Flags.LIGHT_DMG,\
                                                        Flags.BOON]), 1, 0, 75),
            (Affix("BELT_LIGHT_DMG_2", 0.2, [Flags.LIGHT_DMG,\
                                                        Flags.BOON]), 0.8, 20, 80),
            (Affix("BELT_LIGHT_DMG_3", 0.4, [Flags.LIGHT_DMG,\
                                                        Flags.BOON]), 0.6, 40, 999),
            (Affix("BELT_LIGHT_DMG_4", 0.6, [Flags.LIGHT_DMG,\
                                                        Flags.BOON]), 0.25, 60, 999),
            (Affix("BELT_LIGHT_DMG_5", 1, [Flags.LIGHT_DMG,\
                                                        Flags.BOON]), 0.1, 75, 999),
        ], 1),
        "dark_dmg": ([
            (Affix("BELT_DARK_DMG_1", 0.1, [Flags.DARK_DMG,\
                                                        Flags.BOON]), 1, 0, 75),
            (Affix("BELT_DARK_DMG_2", 0.2, [Flags.DARK_DMG,\
                                                        Flags.BOON]), 0.8, 20, 80),
            (Affix("BELT_DARK_DMG_3", 0.4, [Flags.DARK_DMG,\
                                                        Flags.BOON]), 0.6, 40, 999),
            (Affix("BELT_DARK_DMG_4", 0.6, [Flags.DARK_DMG,\
                                                        Flags.BOON]), 0.25, 60, 999),
            (Affix("BELT_DARK_DMG_5", 1, [Flags.DARK_DMG,\
                                                        Flags.BOON]), 0.1, 75, 999),
        ], 1),
        "elemental_dmg": ([
            (Affix("BELT_ELEMENTAL_DMG_1", 0.15, [Flags.ELEMENTAL_DAMAGE,\
                                                        Flags.BOON]), 1, 0, 75),
            (Affix("BELT_ELEMENTAL_DMG_2", 0.25, [Flags.ELEMENTAL_DAMAGE,\
                                                        Flags.BOON]), 0.8, 20, 80),
            (Affix("BELT_ELEMENTAL_DMG_3", 0.50, [Flags.ELEMENTAL_DAMAGE,\
                                                        Flags.BOON]), 0.6, 40, 999)
        ], 0.7),
        "all_dmg": ([
            (Affix("BELT_ALL_DMG_1", 0.15, [Flags.ALL_DAMAGE,\
                                                        Flags.BOON]), 1, 0, 75),
            (Affix("BELT_ALL_DMG_2", 0.25, [Flags.ALL_DAMAGE,\
                                                        Flags.BOON]), 0.8, 20, 80),
            (Affix("BELT_ALL_DMG_3", 0.50, [Flags.ALL_DAMAGE,\
                                                        Flags.BOON]), 0.6, 40, 999)
        ], 0.1),
    },
    "relics": {
        "abs_def": ([
            (Affix("RELIC_ABS_DEF_1", 1, [Flags.ABS_DEF,\
                                                        Flags.FLAT]), 1, 0, 75),
            (Affix("RELIC_ABS_DEF_2", 5, [Flags.ABS_DEF,\
                                                        Flags.FLAT]), 0.8, 20, 80),
            (Affix("RELIC_ABS_DEF_3", 10, [Flags.ABS_DEF,\
                                                        Flags.FLAT]), 0.6, 40, 999)
        ], 0.5),
        "iiq": ([
            (Affix("RELIC_IIQ_1", 0.3, [Flags.BOON, Flags.IIQ]), 1, 0, 60),
            (Affix("RELIC_IIQ_2", 0.5, [Flags.BOON, Flags.IIQ]), 0.5, 25, 80),
            (Affix("RELIC_IIQ_3", 0.8, [Flags.BOON, Flags.IIQ]), 0.1, 50, 999),
            (Affix("RELIC_IIQ_4", 1.1, [Flags.BOON, Flags.IIQ]), 0.05, 50, 999),
            (Affix("RELIC_IIQ_5", 1.5, [Flags.BOON, Flags.IIQ]), 0.01, 50, 999),
        ], 0.8),
        "iir": ([
            (Affix("RELIC_IIR_1", 0.2, [Flags.BOON, Flags.IIR]), 1, 0, 60),
            (Affix("RELIC_IIR_2", 0.3, [Flags.BOON, Flags.IIR]), 0.5, 25, 80),
            (Affix("RELIC_IIR_3", 0.4, [Flags.BOON, Flags.IIR]), 0.1, 50, 999),
            (Affix("RELIC_IIR_4", 0.5, [Flags.BOON, Flags.IIR]), 0.05, 50, 999),
            (Affix("RELIC_IIR_5", 1, [Flags.BOON, Flags.IIR]), 0.01, 50, 999),
        ], 0.6),
        "phys_dmg": ([
            (Affix("RELIC_PHYS_DMG_1", 0.1, [Flags.PHYS_DMG,\
                                                        Flags.BOON], 0.5, 1.5), 1, 0, 75),
            (Affix("RELIC_PHYS_DMG_2", 0.2, [Flags.PHYS_DMG,\
                                                        Flags.BOON], 0.5, 1.5), 0.8, 20, 80),
            (Affix("RELIC_PHYS_DMG_3", 0.4, [Flags.PHYS_DMG,\
                                                        Flags.BOON], 0.5, 1.5), 0.6, 40, 999),
            (Affix("RELIC_PHYS_DMG_4", 0.6, [Flags.PHYS_DMG,\
                                                        Flags.BOON], 0.5, 1.5), 0.25, 60, 999),
            (Affix("RELIC_PHYS_DMG_5", 1, [Flags.PHYS_DMG,\
                                                        Flags.BOON], 0.5, 1.5), 0.1, 75, 999),
        ], 1),
        "fire_dmg": ([
            (Affix("RELIC_FIRE_DMG_1", 0.1, [Flags.FIRE_DMG,\
                                                        Flags.BOON], 0.5, 1.5), 1, 0, 75),
            (Affix("RELIC_FIRE_DMG_2", 0.2, [Flags.FIRE_DMG,\
                                                        Flags.BOON], 0.5, 1.5), 0.8, 20, 80),
            (Affix("RELIC_FIRE_DMG_3", 0.4, [Flags.FIRE_DMG,\
                                                        Flags.BOON], 0.5, 1.5), 0.6, 40, 999),
            (Affix("RELIC_FIRE_DMG_4", 0.6, [Flags.FIRE_DMG,\
                                                        Flags.BOON], 0.5, 1.5), 0.25, 60, 999),
            (Affix("RELIC_FIRE_DMG_5", 1, [Flags.FIRE_DMG,\
                                                        Flags.BOON], 0.5, 1.5), 0.1, 75, 999),
        ], 1),
        "ice_dmg": ([
            (Affix("RELIC_ICE_DMG_1", 0.1, [Flags.ICE_DMG,\
                                                        Flags.BOON], 0.5, 1.5), 1, 0, 75),
            (Affix("RELIC_ICE_DMG_2", 0.2, [Flags.ICE_DMG,\
                                                        Flags.BOON], 0.5, 1.5), 0.8, 20, 80),
            (Affix("RELIC_ICE_DMG_3", 0.4, [Flags.ICE_DMG,\
                                                        Flags.BOON], 0.5, 1.5), 0.6, 40, 999),
            (Affix("RELIC_ICE_DMG_4", 0.6, [Flags.ICE_DMG,\
                                                        Flags.BOON], 0.5, 1.5), 0.25, 60, 999),
            (Affix("RELIC_ICE_DMG_5", 1, [Flags.ICE_DMG,\
                                                        Flags.BOON], 0.5, 1.5), 0.1, 75, 999),
        ], 1),
        "elec_dmg": ([
            (Affix("RELIC_ELEC_DMG_1", 0.1, [Flags.ELEC_DMG,\
                                                        Flags.BOON], 0.5, 1.5), 1, 0, 75),
            (Affix("RELIC_ELEC_DMG_2", 0.2, [Flags.ELEC_DMG,\
                                                        Flags.BOON], 0.5, 1.5), 0.8, 20, 80),
            (Affix("RELIC_ELEC_DMG_3", 0.4, [Flags.ELEC_DMG,\
                                                        Flags.BOON], 0.5, 1.5), 0.6, 40, 999),
            (Affix("RELIC_ELEC_DMG_4", 0.6, [Flags.ELEC_DMG,\
                                                        Flags.BOON], 0.5, 1.5), 0.25, 60, 999),
            (Affix("RELIC_ELEC_DMG_5", 1, [Flags.ELEC_DMG,\
                                                        Flags.BOON], 0.5, 1.5), 0.1, 75, 999),
        ], 1),
        "energy_dmg": ([
            (Affix("RELIC_ENERG_DMG_1", 0.1, [Flags.ENERG_DMG,\
                                                        Flags.BOON], 0.5, 1.5), 1, 0, 75),
            (Affix("RELIC_ENERG_DMG_2", 0.2, [Flags.ENERG_DMG,\
                                                        Flags.BOON], 0.5, 1.5), 0.8, 20, 80),
            (Affix("RELIC_ENERG_DMG_3", 0.4, [Flags.ENERG_DMG,\
                                                        Flags.BOON], 0.5, 1.5), 0.6, 40, 999),
            (Affix("RELIC_ENERG_DMG_4", 0.6, [Flags.ENERG_DMG,\
                                                        Flags.BOON], 0.5, 1.5), 0.25, 60, 999),
            (Affix("RELIC_ENERG_DMG_5", 1, [Flags.ENERG_DMG,\
                                                        Flags.BOON], 0.5, 1.5), 0.1, 75, 999),
        ], 1),
        "light_dmg": ([
            (Affix("RELIC_LIGHT_DMG_1", 0.1, [Flags.LIGHT_DMG,\
                                                        Flags.BOON], 0.5, 1.5), 1, 0, 75),
            (Affix("RELIC_LIGHT_DMG_2", 0.2, [Flags.LIGHT_DMG,\
                                                        Flags.BOON], 0.5, 1.5), 0.8, 20, 80),
            (Affix("RELIC_LIGHT_DMG_3", 0.4, [Flags.LIGHT_DMG,\
                                                        Flags.BOON], 0.5, 1.5), 0.6, 40, 999),
            (Affix("RELIC_LIGHT_DMG_4", 0.6, [Flags.LIGHT_DMG,\
                                                        Flags.BOON], 0.5, 1.5), 0.25, 60, 999),
            (Affix("RELIC_LIGHT_DMG_5", 1, [Flags.LIGHT_DMG,\
                                                        Flags.BOON], 0.5, 1.5), 0.1, 75, 999),
        ], 1),
        "dark_dmg": ([
            (Affix("RELIC_DARK_DMG_1", 0.1, [Flags.DARK_DMG,\
                                                        Flags.BOON], 0.5, 1.5), 1, 0, 75),
            (Affix("RELIC_DARK_DMG_2", 0.2, [Flags.DARK_DMG,\
                                                        Flags.BOON], 0.5, 1.5), 0.8, 20, 80),
            (Affix("RELIC_DARK_DMG_3", 0.4, [Flags.DARK_DMG,\
                                                        Flags.BOON], 0.5, 1.5), 0.6, 40, 999),
            (Affix("RELIC_DARK_DMG_4", 0.6, [Flags.DARK_DMG,\
                                                        Flags.BOON], 0.5, 1.5), 0.25, 60, 999),
            (Affix("RELIC_DARK_DMG_5", 1, [Flags.DARK_DMG,\
                                                        Flags.BOON], 0.5, 1.5), 0.1, 75, 999),
        ], 1),
        "elemental_dmg": ([
            (Affix("RELIC_ELEMENTAL_DMG_1", 0.15, [Flags.ELEMENTAL_DAMAGE,\
                                                        Flags.BOON], 0.5, 1.5), 1, 0, 75),
            (Affix("RELIC_ELEMENTAL_DMG_2", 0.25, [Flags.ELEMENTAL_DAMAGE,\
                                                        Flags.BOON], 0.5, 1.5), 0.8, 20, 80),
            (Affix("RELIC_ELEMENTAL_DMG_3", 0.50, [Flags.ELEMENTAL_DAMAGE,\
                                                        Flags.BOON], 0.5, 1.5), 0.6, 40, 999)
        ], 0.7),
        "all_dmg": ([
            (Affix("RELIC_ALL_DMG_1", 0.15, [Flags.ALL_DAMAGE,\
                                                        Flags.BOON], 0.5, 1.5), 1, 0, 75),
            (Affix("RELIC_ALL_DMG_2", 0.25, [Flags.ALL_DAMAGE,\
                                                        Flags.BOON], 0.5, 1.5), 0.8, 20, 80),
            (Affix("RELIC_ALL_DMG_3", 0.50, [Flags.ALL_DAMAGE,\
                                                        Flags.BOON], 0.5, 1.5), 0.6, 40, 999)
        ], 0.1),
        "phys_PEN": ([
            (Affix("RELIC_PHYS_PEN_1", 0.1, [Flags.PHYS_PEN,\
                                                        Flags.FLAT], 0.5, 1.5), 1, 0, 75),
            (Affix("RELIC_PHYS_PEN_2", 0.2, [Flags.PHYS_PEN,\
                                                        Flags.FLAT], 0.5, 1.5), 0.8, 20, 80),
            (Affix("RELIC_PHYS_PEN_3", 0.4, [Flags.PHYS_PEN,\
                                                        Flags.FLAT], 0.5, 1.5), 0.6, 40, 999),
        ], 0.2),
        "fire_PEN": ([
            (Affix("RELIC_FIRE_PEN_1", 0.1, [Flags.FIRE_PEN,\
                                                        Flags.FLAT], 0.5, 1.5), 1, 0, 75),
            (Affix("RELIC_FIRE_PEN_2", 0.2, [Flags.FIRE_PEN,\
                                                        Flags.FLAT], 0.5, 1.5), 0.8, 20, 80),
            (Affix("RELIC_FIRE_PEN_3", 0.4, [Flags.FIRE_PEN,\
                                                        Flags.FLAT], 0.5, 1.5), 0.6, 40, 999),
        ], 0.2),
        "ice_PEN": ([
            (Affix("RELIC_ICE_PEN_1", 0.1, [Flags.ICE_PEN,\
                                                        Flags.FLAT], 0.5, 1.5), 1, 0, 75),
            (Affix("RELIC_ICE_PEN_2", 0.2, [Flags.ICE_PEN,\
                                                        Flags.FLAT], 0.5, 1.5), 0.8, 20, 80),
            (Affix("RELIC_ICE_PEN_3", 0.4, [Flags.ICE_PEN,\
                                                        Flags.FLAT], 0.5, 1.5), 0.6, 40, 999),
        ], 0.2),
        "elec_PEN": ([
            (Affix("RELIC_ELEC_PEN_1", 0.1, [Flags.ELEC_PEN,\
                                                        Flags.FLAT], 0.5, 1.5), 1, 0, 75),
            (Affix("RELIC_ELEC_PEN_2", 0.2, [Flags.ELEC_PEN,\
                                                        Flags.FLAT], 0.5, 1.5), 0.8, 20, 80),
            (Affix("RELIC_ELEC_PEN_3", 0.4, [Flags.ELEC_PEN,\
                                                        Flags.FLAT], 0.5, 1.5), 0.6, 40, 999),
        ], 0.2),
        "energy_PEN": ([
            (Affix("RELIC_ENERG_PEN_1", 0.1, [Flags.ENERG_PEN,\
                                                        Flags.FLAT], 0.5, 1.5), 1, 0, 75),
            (Affix("RELIC_ENERG_PEN_2", 0.2, [Flags.ENERG_PEN,\
                                                        Flags.FLAT], 0.5, 1.5), 0.8, 20, 80),
            (Affix("RELIC_ENERG_PEN_3", 0.4, [Flags.ENERG_PEN,\
                                                        Flags.FLAT], 0.5, 1.5), 0.6, 40, 999),
        ], 0.2),
        "light_PEN": ([
            (Affix("RELIC_LIGHT_PEN_1", 0.1, [Flags.LIGHT_PEN,\
                                                        Flags.FLAT], 0.5, 1.5), 1, 0, 75),
            (Affix("RELIC_LIGHT_PEN_2", 0.2, [Flags.LIGHT_PEN,\
                                                        Flags.FLAT], 0.5, 1.5), 0.8, 20, 80),
            (Affix("RELIC_LIGHT_PEN_3", 0.4, [Flags.LIGHT_PEN,\
                                                        Flags.FLAT], 0.5, 1.5), 0.6, 40, 999),
        ], 0.2),
        "dark_PEN": ([
            (Affix("RELIC_DARK_PEN_1", 0.1, [Flags.DARK_PEN,\
                                                        Flags.FLAT], 0.5, 1.5), 1, 0, 75),
            (Affix("RELIC_DARK_PEN_2", 0.2, [Flags.DARK_PEN,\
                                                        Flags.FLAT], 0.5, 1.5), 0.8, 20, 80),
            (Affix("RELIC_DARK_PEN_3", 0.4, [Flags.DARK_PEN,\
                                                        Flags.FLAT], 0.5, 1.5), 0.6, 40, 999),
        ], 0.2),
    },
    "weapons": {
        "phys_flat": ([
            (DoubleAffix("WEAPON_PHYS_FLAT_1", 8, 15, [Flags.PHYS_FLAT, Flags.DESC_FLAT,\
                                                        Flags.FLAT], 0.5, 1.5, 0.5, 1.5), 1, 0, 75),
            (DoubleAffix("WEAPON_PHYS_FLAT_2", 20, 30, [Flags.PHYS_FLAT, Flags.DESC_FLAT,\
                                                        Flags.FLAT], 0.5, 1.5, 0.5, 1.5),\
                                                            0.8, 20, 80),
            (DoubleAffix("WEAPON_PHYS_FLAT_3", 40, 60, [Flags.PHYS_FLAT, Flags.DESC_FLAT,\
                                                        Flags.FLAT], 0.5, 1.5, 0.5, 1.5),\
                                                            0.6, 40, 999),
            (DoubleAffix("WEAPON_PHYS_FLAT_4", 80, 100, [Flags.PHYS_FLAT, Flags.DESC_FLAT,\
                                                        Flags.FLAT], 0.5, 1.5, 0.5, 1.5),\
                                                            0.25, 60, 999),
            (DoubleAffix("WEAPON_PHYS_FLAT_5", 150, 200, [Flags.PHYS_FLAT, Flags.DESC_FLAT,\
                                                        Flags.FLAT], 0.5, 1.5, 0.5, 1.5),\
                                                            0.1, 75, 999),
        ], 2),
        "fire_flat": ([
            (DoubleAffix("WEAPON_FIRE_FLAT_1", 8, 15, [Flags.FIRE_FLAT, Flags.DESC_FLAT,\
                                                        Flags.FLAT], 0.5, 1.5, 0.5, 1.5), 1, 0, 75),
            (DoubleAffix("WEAPON_FIRE_FLAT_2", 20, 30, [Flags.FIRE_FLAT, Flags.DESC_FLAT,\
                                                        Flags.FLAT], 0.5, 1.5, 0.5, 1.5),\
                                                            0.8, 20, 80),
            (DoubleAffix("WEAPON_FIRE_FLAT_3", 40, 60, [Flags.FIRE_FLAT, Flags.DESC_FLAT,\
                                                        Flags.FLAT], 0.5, 1.5, 0.5, 1.5),\
                                                            0.6, 40, 999),
            (DoubleAffix("WEAPON_FIRE_FLAT_4", 80, 100, [Flags.FIRE_FLAT, Flags.DESC_FLAT,\
                                                        Flags.FLAT], 0.5, 1.5, 0.5, 1.5),\
                                                            0.25, 60, 999),
            (DoubleAffix("WEAPON_FIRE_FLAT_5", 150, 200, [Flags.FIRE_FLAT, Flags.DESC_FLAT,\
                                                        Flags.FLAT], 0.5, 1.5, 0.5, 1.5),\
                                                            0.1, 75, 999),
        ], 1.5),
        "ice_flat": ([
            (DoubleAffix("WEAPON_ICE_FLAT_1", 8, 15, [Flags.ICE_FLAT, Flags.DESC_FLAT,\
                                                        Flags.FLAT], 0.5, 1.5, 0.5, 1.5), 1, 0, 75),
            (DoubleAffix("WEAPON_ICE_FLAT_2", 20, 30, [Flags.ICE_FLAT, Flags.DESC_FLAT,\
                                                        Flags.FLAT], 0.5, 1.5, 0.5, 1.5),\
                                                            0.8, 20, 80),
            (DoubleAffix("WEAPON_ICE_FLAT_3", 40, 60, [Flags.ICE_FLAT, Flags.DESC_FLAT,\
                                                        Flags.FLAT], 0.5, 1.5, 0.5, 1.5),\
                                                            0.6, 40, 999),
            (DoubleAffix("WEAPON_ICE_FLAT_4", 80, 100, [Flags.ICE_FLAT, Flags.DESC_FLAT,\
                                                        Flags.FLAT], 0.5, 1.5, 0.5, 1.5),\
                                                            0.25, 60, 999),
            (DoubleAffix("WEAPON_ICE_FLAT_5", 150, 200, [Flags.ICE_FLAT, Flags.DESC_FLAT,\
                                                        Flags.FLAT], 0.5, 1.5, 0.5, 1.5),\
                                                            0.1, 75, 999),
        ], 1.5),
        "elec_flat": ([
            (DoubleAffix("WEAPON_ELEC_FLAT_1", 1, 20, [Flags.ELEC_FLAT, Flags.DESC_FLAT,\
                                                        Flags.FLAT], 0.5, 1.5, 0.5, 1.5), 1, 0, 75),
            (DoubleAffix("WEAPON_ELEC_FLAT_2", 3, 40, [Flags.ELEC_FLAT, Flags.DESC_FLAT,\
                                                        Flags.FLAT], 0.5, 1.5, 0.5, 1.5),\
                                                            0.8, 20, 80),
            (DoubleAffix("WEAPON_ELEC_FLAT_3", 5, 75, [Flags.ELEC_FLAT, Flags.DESC_FLAT,\
                                                        Flags.FLAT], 0.5, 1.5, 0.5, 1.5),\
                                                            0.6, 40, 999),
            (DoubleAffix("WEAPON_ELEC_FLAT_4", 10, 150, [Flags.ELEC_FLAT, Flags.DESC_FLAT,\
                                                        Flags.FLAT], 0.5, 1.5, 0.5, 1.5),\
                                                            0.25, 60, 999),
            (DoubleAffix("WEAPON_ELEC_FLAT_5", 25, 300, [Flags.ELEC_FLAT, Flags.DESC_FLAT,\
                                                        Flags.FLAT], 0.5, 1.5, 0.5, 1.5),\
                                                            0.1, 75, 999),
        ], 1.5),
        "energ_flat": ([
            (DoubleAffix("WEAPON_ENERG_FLAT_1", 8, 15, [Flags.ENERG_FLAT, Flags.DESC_FLAT,\
                                                        Flags.FLAT], 0.5, 1.5, 0.5, 1.5), 1, 0, 75),
            (DoubleAffix("WEAPON_ENERG_FLAT_2", 20, 30, [Flags.ENERG_FLAT, Flags.DESC_FLAT,\
                                                        Flags.FLAT], 0.5, 1.5, 0.5, 1.5),\
                                                            0.8, 20, 80),
            (DoubleAffix("WEAPON_ENERG_FLAT_3", 40, 60, [Flags.ENERG_FLAT, Flags.DESC_FLAT,\
                                                        Flags.FLAT], 0.5, 1.5, 0.5, 1.5),\
                                                            0.6, 40, 999),
            (DoubleAffix("WEAPON_ENERG_FLAT_4", 80, 100, [Flags.ENERG_FLAT, Flags.DESC_FLAT,\
                                                        Flags.FLAT], 0.5, 1.5, 0.5, 1.5),\
                                                            0.25, 60, 999),
            (DoubleAffix("WEAPON_ENERG_FLAT_5", 150, 200, [Flags.ENERG_FLAT, Flags.DESC_FLAT,\
                                                        Flags.FLAT], 0.5, 1.5, 0.5, 1.5),\
                                                            0.1, 75, 999),
        ], 1.5),
        "light_flat": ([
            (DoubleAffix("WEAPON_LIGHT_FLAT_1", 8, 15, [Flags.LIGHT_FLAT, Flags.DESC_FLAT,\
                                                        Flags.FLAT], 0.5, 1.5, 0.5, 1.5), 1, 0, 75),
            (DoubleAffix("WEAPON_LIGHT_FLAT_2", 20, 30, [Flags.LIGHT_FLAT, Flags.DESC_FLAT,\
                                                        Flags.FLAT], 0.5, 1.5, 0.5, 1.5),\
                                                            0.8, 20, 80),
            (DoubleAffix("WEAPON_LIGHT_FLAT_3", 40, 60, [Flags.LIGHT_FLAT, Flags.DESC_FLAT,\
                                                        Flags.FLAT], 0.5, 1.5, 0.5, 1.5),\
                                                            0.6, 40, 999),
            (DoubleAffix("WEAPON_LIGHT_FLAT_4", 80, 100, [Flags.LIGHT_FLAT, Flags.DESC_FLAT,\
                                                        Flags.FLAT], 0.5, 1.5, 0.5, 1.5),\
                                                            0.25, 60, 999),
            (DoubleAffix("WEAPON_LIGHT_FLAT_5", 150, 200, [Flags.LIGHT_FLAT, Flags.DESC_FLAT,\
                                                        Flags.FLAT], 0.5, 1.5, 0.5, 1.5),\
                                                            0.1, 75, 999),
        ], 0.9),
        "dark_flat": ([
            (DoubleAffix("WEAPON_DARK_FLAT_1", 8, 15, [Flags.DARK_FLAT, Flags.DESC_FLAT,\
                                                        Flags.FLAT], 0.5, 1.5, 0.5, 1.5), 1, 0, 75),
            (DoubleAffix("WEAPON_DARK_FLAT_2", 20, 30, [Flags.DARK_FLAT, Flags.DESC_FLAT,\
                                                        Flags.FLAT], 0.5, 1.5, 0.5, 1.5),\
                                                            0.8, 20, 80),
            (DoubleAffix("WEAPON_DARK_FLAT_3", 40, 60, [Flags.DARK_FLAT, Flags.DESC_FLAT,\
                                                        Flags.FLAT], 0.5, 1.5, 0.5, 1.5),\
                                                            0.6, 40, 999),
            (DoubleAffix("WEAPON_DARK_FLAT_4", 80, 100, [Flags.DARK_FLAT, Flags.DESC_FLAT,\
                                                        Flags.FLAT], 0.5, 1.5, 0.5, 1.5),\
                                                            0.25, 60, 999),
            (DoubleAffix("WEAPON_DARK_FLAT_5", 150, 200, [Flags.DARK_FLAT, Flags.DESC_FLAT,\
                                                        Flags.FLAT], 0.5, 1.5, 0.5, 1.5),\
                                                            0.1, 75, 999),
        ], 0.9),
        "phys_dmg": ([
            (Affix("WEAPON_PHYS_DMG_1", 0.1, [Flags.PHYS_DMG,\
                                                        Flags.BOON], 0.5, 1.5), 1, 0, 75),
            (Affix("WEAPON_PHYS_DMG_2", 0.2, [Flags.PHYS_DMG,\
                                                        Flags.BOON], 0.5, 1.5), 0.8, 20, 80),
            (Affix("WEAPON_PHYS_DMG_3", 0.4, [Flags.PHYS_DMG,\
                                                        Flags.BOON], 0.5, 1.5), 0.6, 40, 999),
            (Affix("WEAPON_PHYS_DMG_4", 0.6, [Flags.PHYS_DMG,\
                                                        Flags.BOON], 0.5, 1.5), 0.25, 60, 999),
            (Affix("WEAPON_PHYS_DMG_5", 1, [Flags.PHYS_DMG,\
                                                        Flags.BOON], 0.5, 1.5), 0.1, 75, 999),
        ], 1),
        "fire_dmg": ([
            (Affix("WEAPON_FIRE_DMG_1", 0.1, [Flags.FIRE_DMG,\
                                                        Flags.BOON], 0.5, 1.5), 1, 0, 75),
            (Affix("WEAPON_FIRE_DMG_2", 0.2, [Flags.FIRE_DMG,\
                                                        Flags.BOON], 0.5, 1.5), 0.8, 20, 80),
            (Affix("WEAPON_FIRE_DMG_3", 0.4, [Flags.FIRE_DMG,\
                                                        Flags.BOON], 0.5, 1.5), 0.6, 40, 999),
            (Affix("WEAPON_FIRE_DMG_4", 0.6, [Flags.FIRE_DMG,\
                                                        Flags.BOON], 0.5, 1.5), 0.25, 60, 999),
            (Affix("WEAPON_FIRE_DMG_5", 1, [Flags.FIRE_DMG,\
                                                        Flags.BOON], 0.5, 1.5), 0.1, 75, 999),
        ], 1),
        "ice_dmg": ([
            (Affix("WEAPON_ICE_DMG_1", 0.1, [Flags.ICE_DMG,\
                                                        Flags.BOON], 0.5, 1.5), 1, 0, 75),
            (Affix("WEAPON_ICE_DMG_2", 0.2, [Flags.ICE_DMG,\
                                                        Flags.BOON], 0.5, 1.5), 0.8, 20, 80),
            (Affix("WEAPON_ICE_DMG_3", 0.4, [Flags.ICE_DMG,\
                                                        Flags.BOON], 0.5, 1.5), 0.6, 40, 999),
            (Affix("WEAPON_ICE_DMG_4", 0.6, [Flags.ICE_DMG,\
                                                        Flags.BOON], 0.5, 1.5), 0.25, 60, 999),
            (Affix("WEAPON_ICE_DMG_5", 1, [Flags.ICE_DMG,\
                                                        Flags.BOON], 0.5, 1.5), 0.1, 75, 999),
        ], 1),
        "elec_dmg": ([
            (Affix("WEAPON_ELEC_DMG_1", 0.1, [Flags.ELEC_DMG,\
                                                        Flags.BOON], 0.5, 1.5), 1, 0, 75),
            (Affix("WEAPON_ELEC_DMG_2", 0.2, [Flags.ELEC_DMG,\
                                                        Flags.BOON], 0.5, 1.5), 0.8, 20, 80),
            (Affix("WEAPON_ELEC_DMG_3", 0.4, [Flags.ELEC_DMG,\
                                                        Flags.BOON], 0.5, 1.5), 0.6, 40, 999),
            (Affix("WEAPON_ELEC_DMG_4", 0.6, [Flags.ELEC_DMG,\
                                                        Flags.BOON], 0.5, 1.5), 0.25, 60, 999),
            (Affix("WEAPON_ELEC_DMG_5", 1, [Flags.ELEC_DMG,\
                                                        Flags.BOON], 0.5, 1.5), 0.1, 75, 999),
        ], 1),
        "energy_dmg": ([
            (Affix("WEAPON_ENERG_DMG_1", 0.1, [Flags.ENERG_DMG,\
                                                        Flags.BOON], 0.5, 1.5), 1, 0, 75),
            (Affix("WEAPON_ENERG_DMG_2", 0.2, [Flags.ENERG_DMG,\
                                                        Flags.BOON], 0.5, 1.5), 0.8, 20, 80),
            (Affix("WEAPON_ENERG_DMG_3", 0.4, [Flags.ENERG_DMG,\
                                                        Flags.BOON], 0.5, 1.5), 0.6, 40, 999),
            (Affix("WEAPON_ENERG_DMG_4", 0.6, [Flags.ENERG_DMG,\
                                                        Flags.BOON], 0.5, 1.5), 0.25, 60, 999),
            (Affix("WEAPON_ENERG_DMG_5", 1, [Flags.ENERG_DMG,\
                                                        Flags.BOON], 0.5, 1.5), 0.1, 75, 999),
        ], 1),
        "light_dmg": ([
            (Affix("WEAPON_LIGHT_DMG_1", 0.1, [Flags.LIGHT_DMG,\
                                                        Flags.BOON], 0.5, 1.5), 1, 0, 75),
            (Affix("WEAPON_LIGHT_DMG_2", 0.2, [Flags.LIGHT_DMG,\
                                                        Flags.BOON], 0.5, 1.5), 0.8, 20, 80),
            (Affix("WEAPON_LIGHT_DMG_3", 0.4, [Flags.LIGHT_DMG,\
                                                        Flags.BOON], 0.5, 1.5), 0.6, 40, 999),
            (Affix("WEAPON_LIGHT_DMG_4", 0.6, [Flags.LIGHT_DMG,\
                                                        Flags.BOON], 0.5, 1.5), 0.25, 60, 999),
            (Affix("WEAPON_LIGHT_DMG_5", 1, [Flags.LIGHT_DMG,\
                                                        Flags.BOON], 0.5, 1.5), 0.1, 75, 999),
        ], 1),
        "dark_dmg": ([
            (Affix("WEAPON_DARK_DMG_1", 0.1, [Flags.DARK_DMG,\
                                                        Flags.BOON], 0.5, 1.5), 1, 0, 75),
            (Affix("WEAPON_DARK_DMG_2", 0.2, [Flags.DARK_DMG,\
                                                        Flags.BOON], 0.5, 1.5), 0.8, 20, 80),
            (Affix("WEAPON_DARK_DMG_3", 0.4, [Flags.DARK_DMG,\
                                                        Flags.BOON], 0.5, 1.5), 0.6, 40, 999),
            (Affix("WEAPON_DARK_DMG_4", 0.6, [Flags.DARK_DMG,\
                                                        Flags.BOON], 0.5, 1.5), 0.25, 60, 999),
            (Affix("WEAPON_DARK_DMG_5", 1, [Flags.DARK_DMG,\
                                                        Flags.BOON], 0.5, 1.5), 0.1, 75, 999),
        ], 1),
        "melee_dmg": ([
            (Affix("WEAPON_MELEE_1", 0.1, [Flags.MELEE,\
                                                        Flags.BOON], 0.5, 1.5), 1, 0, 75),
            (Affix("WEAPON_MELEE_2", 0.2, [Flags.MELEE,\
                                                        Flags.BOON], 0.5, 1.5), 0.8, 20, 80),
            (Affix("WEAPON_MELEE_3", 0.4, [Flags.MELEE,\
                                                        Flags.BOON], 0.5, 1.5), 0.6, 40, 999),
            (Affix("WEAPON_MELEE_4", 0.6, [Flags.MELEE,\
                                                        Flags.BOON], 0.5, 1.5), 0.25, 60, 999),
            (Affix("WEAPON_MELEE_5", 1, [Flags.MELEE,\
                                                        Flags.BOON], 0.5, 1.5), 0.1, 75, 999),
        ], 1.2),
        "ranged_dmg": ([
            (Affix("WEAPON_RANGED_1", 0.1, [Flags.RANGED,\
                                                        Flags.BOON], 0.5, 1.5), 1, 0, 75),
            (Affix("WEAPON_RANGED_2", 0.2, [Flags.RANGED,\
                                                        Flags.BOON], 0.5, 1.5), 0.8, 20, 80),
            (Affix("WEAPON_RANGED_3", 0.4, [Flags.RANGED,\
                                                        Flags.BOON], 0.5, 1.5), 0.6, 40, 999),
            (Affix("WEAPON_RANGED_4", 0.6, [Flags.RANGED,\
                                                        Flags.BOON], 0.5, 1.5), 0.25, 60, 999),
            (Affix("WEAPON_RANGED_5", 1, [Flags.RANGED,\
                                                        Flags.BOON], 0.5, 1.5), 0.1, 75, 999),
        ], 1.2),
        "spell_dmg": ([
            (Affix("WEAPON_SPELL_1", 0.1, [Flags.SPELL,\
                                                        Flags.BOON], 0.5, 1.5), 1, 0, 75),
            (Affix("WEAPON_SPELL_2", 0.2, [Flags.SPELL,\
                                                        Flags.BOON], 0.5, 1.5), 0.8, 20, 80),
            (Affix("WEAPON_SPELL_3", 0.4, [Flags.SPELL,\
                                                        Flags.BOON], 0.5, 1.5), 0.6, 40, 999),
            (Affix("WEAPON_SPELL_4", 0.6, [Flags.SPELL,\
                                                        Flags.BOON], 0.5, 1.5), 0.25, 60, 999),
            (Affix("WEAPON_SPELL_5", 1, [Flags.SPELL,\
                                                        Flags.BOON], 0.5, 1.5), 0.1, 75, 999),
        ], 1.2),
        "elemental_dmg": ([
            (Affix("WEAPON_ELEMENTAL_DMG_1", 0.15, [Flags.ELEMENTAL_DAMAGE,\
                                                        Flags.BOON], 0.5, 1.5), 1, 0, 75),
            (Affix("WEAPON_ELEMENTAL_DMG_2", 0.25, [Flags.ELEMENTAL_DAMAGE,\
                                                        Flags.BOON], 0.5, 1.5), 0.8, 20, 80),
            (Affix("WEAPON_ELEMENTAL_DMG_3", 0.50, [Flags.ELEMENTAL_DAMAGE,\
                                                        Flags.BOON], 0.5, 1.5), 0.6, 40, 999)
        ], 0.7),
        "all_dmg": ([
            (Affix("WEAPON_ALL_DMG_1", 0.15, [Flags.ALL_DAMAGE,\
                                                        Flags.BOON], 0.5, 1.5), 1, 0, 75),
            (Affix("WEAPON_ALL_DMG_2", 0.25, [Flags.ALL_DAMAGE,\
                                                        Flags.BOON], 0.5, 1.5), 0.8, 20, 80),
            (Affix("WEAPON_ALL_DMG_3", 0.50, [Flags.ALL_DAMAGE,\
                                                        Flags.BOON], 0.5, 1.5), 0.6, 40, 999)
        ], 0.1),
        "phys_PEN": ([
            (Affix("WEAPON_PHYS_PEN_1", 0.1, [Flags.PHYS_PEN,\
                                                        Flags.FLAT], 0.5, 1.5), 1, 0, 75),
            (Affix("WEAPON_PHYS_PEN_2", 0.2, [Flags.PHYS_PEN,\
                                                        Flags.FLAT], 0.5, 1.5), 0.8, 20, 80),
            (Affix("WEAPON_PHYS_PEN_3", 0.4, [Flags.PHYS_PEN,\
                                                        Flags.FLAT], 0.5, 1.5), 0.6, 40, 999),
        ], 0.2),
        "fire_PEN": ([
            (Affix("WEAPON_FIRE_PEN_1", 0.1, [Flags.FIRE_PEN,\
                                                        Flags.FLAT], 0.5, 1.5), 1, 0, 75),
            (Affix("WEAPON_FIRE_PEN_2", 0.2, [Flags.FIRE_PEN,\
                                                        Flags.FLAT], 0.5, 1.5), 0.8, 20, 80),
            (Affix("WEAPON_FIRE_PEN_3", 0.4, [Flags.FIRE_PEN,\
                                                        Flags.FLAT], 0.5, 1.5), 0.6, 40, 999),
        ], 0.2),
        "ice_PEN": ([
            (Affix("WEAPON_ICE_PEN_1", 0.1, [Flags.ICE_PEN,\
                                                        Flags.FLAT], 0.5, 1.5), 1, 0, 75),
            (Affix("WEAPON_ICE_PEN_2", 0.2, [Flags.ICE_PEN,\
                                                        Flags.FLAT], 0.5, 1.5), 0.8, 20, 80),
            (Affix("WEAPON_ICE_PEN_3", 0.4, [Flags.ICE_PEN,\
                                                        Flags.FLAT], 0.5, 1.5), 0.6, 40, 999),
        ], 0.2),
        "elec_PEN": ([
            (Affix("WEAPON_ELEC_PEN_1", 0.1, [Flags.ELEC_PEN,\
                                                        Flags.FLAT], 0.5, 1.5), 1, 0, 75),
            (Affix("WEAPON_ELEC_PEN_2", 0.2, [Flags.ELEC_PEN,\
                                                        Flags.FLAT], 0.5, 1.5), 0.8, 20, 80),
            (Affix("WEAPON_ELEC_PEN_3", 0.4, [Flags.ELEC_PEN,\
                                                        Flags.FLAT], 0.5, 1.5), 0.6, 40, 999),
        ], 0.2),
        "energy_PEN": ([
            (Affix("WEAPON_ENERG_PEN_1", 0.1, [Flags.ENERG_PEN,\
                                                        Flags.FLAT], 0.5, 1.5), 1, 0, 75),
            (Affix("WEAPON_ENERG_PEN_2", 0.2, [Flags.ENERG_PEN,\
                                                        Flags.FLAT], 0.5, 1.5), 0.8, 20, 80),
            (Affix("WEAPON_ENERG_PEN_3", 0.4, [Flags.ENERG_PEN,\
                                                        Flags.FLAT], 0.5, 1.5), 0.6, 40, 999),
        ], 0.2),
        "light_PEN": ([
            (Affix("WEAPON_LIGHT_PEN_1", 0.1, [Flags.LIGHT_PEN,\
                                                        Flags.FLAT], 0.5, 1.5), 1, 0, 75),
            (Affix("WEAPON_LIGHT_PEN_2", 0.2, [Flags.LIGHT_PEN,\
                                                        Flags.FLAT], 0.5, 1.5), 0.8, 20, 80),
            (Affix("WEAPON_LIGHT_PEN_3", 0.4, [Flags.LIGHT_PEN,\
                                                        Flags.FLAT], 0.5, 1.5), 0.6, 40, 999),
        ], 0.2),
        "dark_PEN": ([
            (Affix("WEAPON_DARK_PEN_1", 0.1, [Flags.DARK_PEN,\
                                                        Flags.FLAT], 0.5, 1.5), 1, 0, 75),
            (Affix("WEAPON_DARK_PEN_2", 0.2, [Flags.DARK_PEN,\
                                                        Flags.FLAT], 0.5, 1.5), 0.8, 20, 80),
            (Affix("WEAPON_DARK_PEN_3", 0.4, [Flags.DARK_PEN,\
                                                        Flags.FLAT], 0.5, 1.5), 0.6, 40, 999),
        ], 0.2),
        "crit_rate": ([
            (Affix("WEAPON_CRIT_CHANCE_1", 0.1, [Flags.CRIT_CHANCE,\
                                                        Flags.BOON], 0.5, 1.5), 1, 0, 75),
            (Affix("WEAPON_CRIT_CHANCE_2", 0.2, [Flags.CRIT_CHANCE,\
                                                        Flags.BOON], 0.5, 1.5), 0.8, 20, 80),
            (Affix("WEAPON_CRIT_CHANCE_3", 0.4, [Flags.CRIT_CHANCE,\
                                                        Flags.BOON], 0.5, 1.5), 0.6, 40, 999),
            (Affix("WEAPON_CRIT_CHANCE_4", 0.6, [Flags.CRIT_CHANCE,\
                                                        Flags.BOON], 0.5, 1.5), 0.25, 60, 999),
            (Affix("WEAPON_CRIT_CHANCE_5", 1, [Flags.CRIT_CHANCE,\
                                                        Flags.BOON], 0.5, 1.5), 0.1, 75, 999),
        ], 0.8),
        "crit_damage": ([
            (Affix("WEAPON_CRIT_DAMAGE_1", 0.1, [Flags.CRIT_DAMAGE,\
                                                        Flags.FLAT], 0.5, 1.5), 1, 0, 75),
            (Affix("WEAPON_CRIT_DAMAGE_2", 0.2, [Flags.CRIT_DAMAGE,\
                                                        Flags.FLAT], 0.5, 1.5), 0.8, 20, 80),
            (Affix("WEAPON_CRIT_DAMAGE_3", 0.4, [Flags.CRIT_DAMAGE,\
                                                        Flags.FLAT], 0.5, 1.5), 0.6, 40, 999),
            (Affix("WEAPON_CRIT_DAMAGE_4", 0.6, [Flags.CRIT_DAMAGE,\
                                                        Flags.FLAT], 0.5, 1.5), 0.25, 60, 999),
            (Affix("WEAPON_CRIT_DAMAGE_5", 1, [Flags.CRIT_DAMAGE,\
                                                        Flags.FLAT], 0.5, 1.5), 0.1, 75, 999),
        ], 0.5),
        "precision": ([
            (Affix("WEAPON_PRECISION_1", 50, [Flags.FLAT, Flags.DESC_FLAT,\
                                            Flags.PRECISION]), 1, 0, 30),
            (Affix("WEAPON_PRECISION_2", 100, [Flags.FLAT, Flags.DESC_FLAT,\
                                            Flags.PRECISION]), 0.8, 0, 30),
            (Affix("WEAPON_PRECISION_3", 200, [Flags.FLAT, Flags.DESC_FLAT,\
                                            Flags.PRECISION]), 0.5, 10, 40),
            (Affix("WEAPON_PRECISION_4", 300, [Flags.FLAT, Flags.DESC_FLAT,\
                                            Flags.PRECISION]), 0.3, 20, 60),
            (Affix("WEAPON_PRECISION_5", 500, [Flags.FLAT, Flags.DESC_FLAT,\
                                            Flags.PRECISION]), 0.2, 30, 80),
            (Affix("WEAPON_PRECISION_6", 750, [Flags.FLAT, Flags.DESC_FLAT,\
                                            Flags.PRECISION]), 0.1, 50, 999),
            (Affix("WEAPON_PRECISION_7", 1000, [Flags.FLAT, Flags.DESC_FLAT,\
                                            Flags.PRECISION]), 0.05, 75, 999),
        ], 0.9),
    },
    "offhands": {
        "phys_dmg": ([
            (Affix("OH_PHYS_DMG_1", 0.1, [Flags.PHYS_DMG,\
                                                        Flags.BOON], 0.5, 1.5), 1, 0, 75),
            (Affix("OH_PHYS_DMG_2", 0.2, [Flags.PHYS_DMG,\
                                                        Flags.BOON], 0.5, 1.5), 0.8, 20, 80),
            (Affix("OH_PHYS_DMG_3", 0.4, [Flags.PHYS_DMG,\
                                                        Flags.BOON], 0.5, 1.5), 0.6, 40, 999),
            (Affix("OH_PHYS_DMG_4", 0.6, [Flags.PHYS_DMG,\
                                                        Flags.BOON], 0.5, 1.5), 0.25, 60, 999),
            (Affix("OH_PHYS_DMG_5", 1, [Flags.PHYS_DMG,\
                                                        Flags.BOON], 0.5, 1.5), 0.1, 75, 999),
        ], 1),
        "fire_dmg": ([
            (Affix("OH_FIRE_DMG_1", 0.1, [Flags.FIRE_DMG,\
                                                        Flags.BOON], 0.5, 1.5), 1, 0, 75),
            (Affix("OH_FIRE_DMG_2", 0.2, [Flags.FIRE_DMG,\
                                                        Flags.BOON], 0.5, 1.5), 0.8, 20, 80),
            (Affix("OH_FIRE_DMG_3", 0.4, [Flags.FIRE_DMG,\
                                                        Flags.BOON], 0.5, 1.5), 0.6, 40, 999),
            (Affix("OH_FIRE_DMG_4", 0.6, [Flags.FIRE_DMG,\
                                                        Flags.BOON], 0.5, 1.5), 0.25, 60, 999),
            (Affix("OH_FIRE_DMG_5", 1, [Flags.FIRE_DMG,\
                                                        Flags.BOON], 0.5, 1.5), 0.1, 75, 999),
        ], 1),
        "ice_dmg": ([
            (Affix("OH_ICE_DMG_1", 0.1, [Flags.ICE_DMG,\
                                                        Flags.BOON], 0.5, 1.5), 1, 0, 75),
            (Affix("OH_ICE_DMG_2", 0.2, [Flags.ICE_DMG,\
                                                        Flags.BOON], 0.5, 1.5), 0.8, 20, 80),
            (Affix("OH_ICE_DMG_3", 0.4, [Flags.ICE_DMG,\
                                                        Flags.BOON], 0.5, 1.5), 0.6, 40, 999),
            (Affix("OH_ICE_DMG_4", 0.6, [Flags.ICE_DMG,\
                                                        Flags.BOON], 0.5, 1.5), 0.25, 60, 999),
            (Affix("OH_ICE_DMG_5", 1, [Flags.ICE_DMG,\
                                                        Flags.BOON], 0.5, 1.5), 0.1, 75, 999),
        ], 1),
        "elec_dmg": ([
            (Affix("OH_ELEC_DMG_1", 0.1, [Flags.ELEC_DMG,\
                                                        Flags.BOON], 0.5, 1.5), 1, 0, 75),
            (Affix("OH_ELEC_DMG_2", 0.2, [Flags.ELEC_DMG,\
                                                        Flags.BOON], 0.5, 1.5), 0.8, 20, 80),
            (Affix("OH_ELEC_DMG_3", 0.4, [Flags.ELEC_DMG,\
                                                        Flags.BOON], 0.5, 1.5), 0.6, 40, 999),
            (Affix("OH_ELEC_DMG_4", 0.6, [Flags.ELEC_DMG,\
                                                        Flags.BOON], 0.5, 1.5), 0.25, 60, 999),
            (Affix("OH_ELEC_DMG_5", 1, [Flags.ELEC_DMG,\
                                                        Flags.BOON], 0.5, 1.5), 0.1, 75, 999),
        ], 1),
        "energy_dmg": ([
            (Affix("OH_ENERG_DMG_1", 0.1, [Flags.ENERG_DMG,\
                                                        Flags.BOON], 0.5, 1.5), 1, 0, 75),
            (Affix("OH_ENERG_DMG_2", 0.2, [Flags.ENERG_DMG,\
                                                        Flags.BOON], 0.5, 1.5), 0.8, 20, 80),
            (Affix("OH_ENERG_DMG_3", 0.4, [Flags.ENERG_DMG,\
                                                        Flags.BOON], 0.5, 1.5), 0.6, 40, 999),
            (Affix("OH_ENERG_DMG_4", 0.6, [Flags.ENERG_DMG,\
                                                        Flags.BOON], 0.5, 1.5), 0.25, 60, 999),
            (Affix("OH_ENERG_DMG_5", 1, [Flags.ENERG_DMG,\
                                                        Flags.BOON], 0.5, 1.5), 0.1, 75, 999),
        ], 1),
        "light_dmg": ([
            (Affix("OH_LIGHT_DMG_1", 0.1, [Flags.LIGHT_DMG,\
                                                        Flags.BOON], 0.5, 1.5), 1, 0, 75),
            (Affix("OH_LIGHT_DMG_2", 0.2, [Flags.LIGHT_DMG,\
                                                        Flags.BOON], 0.5, 1.5), 0.8, 20, 80),
            (Affix("OH_LIGHT_DMG_3", 0.4, [Flags.LIGHT_DMG,\
                                                        Flags.BOON], 0.5, 1.5), 0.6, 40, 999),
            (Affix("OH_LIGHT_DMG_4", 0.6, [Flags.LIGHT_DMG,\
                                                        Flags.BOON], 0.5, 1.5), 0.25, 60, 999),
            (Affix("OH_LIGHT_DMG_5", 1, [Flags.LIGHT_DMG,\
                                                        Flags.BOON], 0.5, 1.5), 0.1, 75, 999),
        ], 1),
        "dark_dmg": ([
            (Affix("OH_DARK_DMG_1", 0.1, [Flags.DARK_DMG,\
                                                        Flags.BOON], 0.5, 1.5), 1, 0, 75),
            (Affix("OH_DARK_DMG_2", 0.2, [Flags.DARK_DMG,\
                                                        Flags.BOON], 0.5, 1.5), 0.8, 20, 80),
            (Affix("OH_DARK_DMG_3", 0.4, [Flags.DARK_DMG,\
                                                        Flags.BOON], 0.5, 1.5), 0.6, 40, 999),
            (Affix("OH_DARK_DMG_4", 0.6, [Flags.DARK_DMG,\
                                                        Flags.BOON], 0.5, 1.5), 0.25, 60, 999),
            (Affix("OH_DARK_DMG_5", 1, [Flags.DARK_DMG,\
                                                        Flags.BOON], 0.5, 1.5), 0.1, 75, 999),
        ], 1),
        "melee_dmg": ([
            (Affix("OH_MELEE_1", 0.1, [Flags.MELEE,\
                                                        Flags.BOON], 0.5, 1.5), 1, 0, 75),
            (Affix("OH_MELEE_2", 0.2, [Flags.MELEE,\
                                                        Flags.BOON], 0.5, 1.5), 0.8, 20, 80),
            (Affix("OH_MELEE_3", 0.4, [Flags.MELEE,\
                                                        Flags.BOON], 0.5, 1.5), 0.6, 40, 999),
            (Affix("OH_MELEE_4", 0.6, [Flags.MELEE,\
                                                        Flags.BOON], 0.5, 1.5), 0.25, 60, 999),
            (Affix("OH_MELEE_5", 1, [Flags.MELEE,\
                                                        Flags.BOON], 0.5, 1.5), 0.1, 75, 999),
        ], 1.2),
        "ranged_dmg": ([
            (Affix("OH_RANGED_1", 0.1, [Flags.RANGED,\
                                                        Flags.BOON], 0.5, 1.5), 1, 0, 75),
            (Affix("OH_RANGED_2", 0.2, [Flags.RANGED,\
                                                        Flags.BOON], 0.5, 1.5), 0.8, 20, 80),
            (Affix("OH_RANGED_3", 0.4, [Flags.RANGED,\
                                                        Flags.BOON], 0.5, 1.5), 0.6, 40, 999),
            (Affix("OH_RANGED_4", 0.6, [Flags.RANGED,\
                                                        Flags.BOON], 0.5, 1.5), 0.25, 60, 999),
            (Affix("OH_RANGED_5", 1, [Flags.RANGED,\
                                                        Flags.BOON], 0.5, 1.5), 0.1, 75, 999),
        ], 1.2),
        "spell_dmg": ([
            (Affix("OH_SPELL_1", 0.1, [Flags.SPELL,\
                                                        Flags.BOON], 0.5, 1.5), 1, 0, 75),
            (Affix("OH_SPELL_2", 0.2, [Flags.SPELL,\
                                                        Flags.BOON], 0.5, 1.5), 0.8, 20, 80),
            (Affix("OH_SPELL_3", 0.4, [Flags.SPELL,\
                                                        Flags.BOON], 0.5, 1.5), 0.6, 40, 999),
            (Affix("OH_SPELL_4", 0.6, [Flags.SPELL,\
                                                        Flags.BOON], 0.5, 1.5), 0.25, 60, 999),
            (Affix("OH_SPELL_5", 1, [Flags.SPELL,\
                                                        Flags.BOON], 0.5, 1.5), 0.1, 75, 999),
        ], 1.2),
        "elemental_dmg": ([
            (Affix("OH_ELEMENTAL_DMG_1", 0.15, [Flags.ELEMENTAL_DAMAGE,\
                                                        Flags.BOON], 0.5, 1.5), 1, 0, 75),
            (Affix("OH_ELEMENTAL_DMG_2", 0.25, [Flags.ELEMENTAL_DAMAGE,\
                                                        Flags.BOON], 0.5, 1.5), 0.8, 20, 80),
            (Affix("OH_ELEMENTAL_DMG_3", 0.50, [Flags.ELEMENTAL_DAMAGE,\
                                                        Flags.BOON], 0.5, 1.5), 0.6, 40, 999)
        ], 0.7),
        "all_dmg": ([
            (Affix("OH_ALL_DMG_1", 0.15, [Flags.ALL_DAMAGE,\
                                                        Flags.BOON], 0.5, 1.5), 1, 0, 75),
            (Affix("OH_ALL_DMG_2", 0.25, [Flags.ALL_DAMAGE,\
                                                        Flags.BOON], 0.5, 1.5), 0.8, 20, 80),
            (Affix("OH_ALL_DMG_3", 0.50, [Flags.ALL_DAMAGE,\
                                                        Flags.BOON], 0.5, 1.5), 0.6, 40, 999)
        ], 0.1),
        "phys_PEN": ([
            (Affix("OH_PHYS_PEN_1", 0.1, [Flags.PHYS_PEN,\
                                                        Flags.FLAT], 0.5, 1.5), 1, 0, 75),
            (Affix("OH_PHYS_PEN_2", 0.2, [Flags.PHYS_PEN,\
                                                        Flags.FLAT], 0.5, 1.5), 0.8, 20, 80),
            (Affix("OH_PHYS_PEN_3", 0.4, [Flags.PHYS_PEN,\
                                                        Flags.FLAT], 0.5, 1.5), 0.6, 40, 999),
        ], 0.2),
        "fire_PEN": ([
            (Affix("OH_FIRE_PEN_1", 0.1, [Flags.FIRE_PEN,\
                                                        Flags.FLAT], 0.5, 1.5), 1, 0, 75),
            (Affix("OH_FIRE_PEN_2", 0.2, [Flags.FIRE_PEN,\
                                                        Flags.FLAT], 0.5, 1.5), 0.8, 20, 80),
            (Affix("OH_FIRE_PEN_3", 0.4, [Flags.FIRE_PEN,\
                                                        Flags.FLAT], 0.5, 1.5), 0.6, 40, 999),
        ], 0.2),
        "ice_PEN": ([
            (Affix("OH_ICE_PEN_1", 0.1, [Flags.ICE_PEN,\
                                                        Flags.FLAT], 0.5, 1.5), 1, 0, 75),
            (Affix("OH_ICE_PEN_2", 0.2, [Flags.ICE_PEN,\
                                                        Flags.FLAT], 0.5, 1.5), 0.8, 20, 80),
            (Affix("OH_ICE_PEN_3", 0.4, [Flags.ICE_PEN,\
                                                        Flags.FLAT], 0.5, 1.5), 0.6, 40, 999),
        ], 0.2),
        "elec_PEN": ([
            (Affix("OH_ELEC_PEN_1", 0.1, [Flags.ELEC_PEN,\
                                                        Flags.FLAT], 0.5, 1.5), 1, 0, 75),
            (Affix("OH_ELEC_PEN_2", 0.2, [Flags.ELEC_PEN,\
                                                        Flags.FLAT], 0.5, 1.5), 0.8, 20, 80),
            (Affix("OH_ELEC_PEN_3", 0.4, [Flags.ELEC_PEN,\
                                                        Flags.FLAT], 0.5, 1.5), 0.6, 40, 999),
        ], 0.2),
        "energy_PEN": ([
            (Affix("OH_ENERG_PEN_1", 0.1, [Flags.ENERG_PEN,\
                                                        Flags.FLAT], 0.5, 1.5), 1, 0, 75),
            (Affix("OH_ENERG_PEN_2", 0.2, [Flags.ENERG_PEN,\
                                                        Flags.FLAT], 0.5, 1.5), 0.8, 20, 80),
            (Affix("OH_ENERG_PEN_3", 0.4, [Flags.ENERG_PEN,\
                                                        Flags.FLAT], 0.5, 1.5), 0.6, 40, 999),
        ], 0.2),
        "light_PEN": ([
            (Affix("OH_LIGHT_PEN_1", 0.1, [Flags.LIGHT_PEN,\
                                                        Flags.FLAT], 0.5, 1.5), 1, 0, 75),
            (Affix("OH_LIGHT_PEN_2", 0.2, [Flags.LIGHT_PEN,\
                                                        Flags.FLAT], 0.5, 1.5), 0.8, 20, 80),
            (Affix("OH_LIGHT_PEN_3", 0.4, [Flags.LIGHT_PEN,\
                                                        Flags.FLAT], 0.5, 1.5), 0.6, 40, 999),
        ], 0.2),
        "dark_PEN": ([
            (Affix("OH_DARK_PEN_1", 0.1, [Flags.DARK_PEN,\
                                                        Flags.FLAT], 0.5, 1.5), 1, 0, 75),
            (Affix("OH_DARK_PEN_2", 0.2, [Flags.DARK_PEN,\
                                                        Flags.FLAT], 0.5, 1.5), 0.8, 20, 80),
            (Affix("OH_DARK_PEN_3", 0.4, [Flags.DARK_PEN,\
                                                        Flags.FLAT], 0.5, 1.5), 0.6, 40, 999),
        ], 0.2),
        "crit_rate": ([
            (Affix("OH_CRIT_CHANCE_1", 0.1, [Flags.CRIT_CHANCE,\
                                                        Flags.BOON], 0.5, 1.5), 1, 0, 75),
            (Affix("OH_CRIT_CHANCE_2", 0.2, [Flags.CRIT_CHANCE,\
                                                        Flags.BOON], 0.5, 1.5), 0.8, 20, 80),
            (Affix("OH_CRIT_CHANCE_3", 0.4, [Flags.CRIT_CHANCE,\
                                                        Flags.BOON], 0.5, 1.5), 0.6, 40, 999),
            (Affix("OH_CRIT_CHANCE_4", 0.6, [Flags.CRIT_CHANCE,\
                                                        Flags.BOON], 0.5, 1.5), 0.25, 60, 999),
            (Affix("OH_CRIT_CHANCE_5", 1, [Flags.CRIT_CHANCE,\
                                                        Flags.BOON], 0.5, 1.5), 0.1, 75, 999),
        ], 0.8),
        "crit_damage": ([
            (Affix("OH_CRIT_DAMAGE_1", 0.1, [Flags.CRIT_DAMAGE,\
                                                        Flags.FLAT], 0.5, 1.5), 1, 0, 75),
            (Affix("OH_CRIT_DAMAGE_2", 0.2, [Flags.CRIT_DAMAGE,\
                                                        Flags.FLAT], 0.5, 1.5), 0.8, 20, 80),
            (Affix("OH_CRIT_DAMAGE_3", 0.4, [Flags.CRIT_DAMAGE,\
                                                        Flags.FLAT], 0.5, 1.5), 0.6, 40, 999),
            (Affix("OH_CRIT_DAMAGE_4", 0.6, [Flags.CRIT_DAMAGE,\
                                                        Flags.FLAT], 0.5, 1.5), 0.25, 60, 999),
            (Affix("OH_CRIT_DAMAGE_5", 1, [Flags.CRIT_DAMAGE,\
                                                        Flags.FLAT], 0.5, 1.5), 0.1, 75, 999),
        ], 0.5),
        "precision": ([
            (Affix("OH_PRECISION_1", 50, [Flags.FLAT, Flags.DESC_FLAT,\
                                            Flags.PRECISION]), 1, 0, 30),
            (Affix("OH_PRECISION_2", 100, [Flags.FLAT, Flags.DESC_FLAT,\
                                            Flags.PRECISION]), 0.8, 0, 30),
            (Affix("OH_PRECISION_3", 200, [Flags.FLAT, Flags.DESC_FLAT,\
                                            Flags.PRECISION]), 0.5, 10, 40),
            (Affix("OH_PRECISION_4", 300, [Flags.FLAT, Flags.DESC_FLAT,\
                                            Flags.PRECISION]), 0.3, 20, 60),
            (Affix("OH_PRECISION_5", 500, [Flags.FLAT, Flags.DESC_FLAT,\
                                            Flags.PRECISION]), 0.2, 30, 80),
            (Affix("OH_PRECISION_6", 750, [Flags.FLAT, Flags.DESC_FLAT,\
                                            Flags.PRECISION]), 0.1, 50, 999),
            (Affix("OH_PRECISION_7", 1000, [Flags.FLAT, Flags.DESC_FLAT,\
                                            Flags.PRECISION]), 0.05, 75, 999),
        ], 0.9),
        "endurance": ([
            (Affix("OH_DEF_1", 100, [Flags.FLAT, Flags.DESC_FLAT, Flags.DEF]), 1, 0, 30),
            (Affix("OH_DEF_2", 250, [Flags.FLAT, Flags.DESC_FLAT, Flags.DEF]), 0.8, 0, 30),
            (Affix("OH_DEF_3", 500, [Flags.FLAT, Flags.DESC_FLAT, Flags.DEF]), 0.5, 10, 40),
            (Affix("OH_DEF_4", 750, [Flags.FLAT, Flags.DESC_FLAT, Flags.DEF]), 0.3, 20, 60),
            (Affix("OH_DEF_5", 1000, [Flags.FLAT, Flags.DESC_FLAT, Flags.DEF]), 0.2, 30, 80),
            (Affix("OH_DEF_6", 1500, [Flags.FLAT, Flags.DESC_FLAT, Flags.DEF]), 0.1, 50, 999),
            (Affix("OH_DEF_7", 2500, [Flags.FLAT, Flags.DESC_FLAT, Flags.DEF]), 0.05, 75, 999),
        ], 1.2),
        "dodge_rate": ([
            (Affix("OH_DODGE_RATING_1", 100, [Flags.FLAT, Flags.DESC_FLAT,\
                                                        Flags.DODGE_RATING]), 1, 0, 30),
            (Affix("OH_DODGE_RATING_2", 250, [Flags.FLAT, Flags.DESC_FLAT,\
                                                        Flags.DODGE_RATING]), 0.8, 0, 30),
            (Affix("OH_DODGE_RATING_3", 500, [Flags.FLAT, Flags.DESC_FLAT,\
                                                        Flags.DODGE_RATING]), 0.5, 10, 40),
            (Affix("OH_DODGE_RATING_4", 750, [Flags.FLAT, Flags.DESC_FLAT,\
                                                        Flags.DODGE_RATING]), 0.3, 20, 60),
            (Affix("OH_DODGE_RATING_5", 1000, [Flags.FLAT, Flags.DESC_FLAT,\
                                                        Flags.DODGE_RATING]), 0.2, 30, 80),
            (Affix("OH_DODGE_RATING_6", 1500, [Flags.FLAT, Flags.DESC_FLAT,\
                                                        Flags.DODGE_RATING]), 0.1, 50, 999),
            (Affix("OH_DODGE_RATING_7", 2500, [Flags.FLAT, Flags.DESC_FLAT,\
                                                        Flags.DODGE_RATING]), 0.05, 75, 999),
        ], 1.2),
        "dodge": ([
            (Affix("OH_DODGE_1", 0.01, [Flags.FLAT, Flags.DESC_PERCENT,\
                                                        Flags.DODGE]), 1, 0, 999),
            (Affix("OH_DODGE_2", 0.02, [Flags.FLAT, Flags.DESC_PERCENT,\
                                                        Flags.DODGE]), 0.5, 25, 999),
            (Affix("OH_DODGE_3", 0.05, [Flags.FLAT, Flags.DESC_PERCENT,\
                                                        Flags.DODGE]), 0.1, 75, 999),
        ], 0.2),
        "block": ([
            (Affix("OH_BLOCK_1", 0.05, [Flags.FLAT, Flags.DESC_PERCENT,\
                                                        Flags.BLOCK]), 1, 0, 999),
            (Affix("OH_BLOCK_2", 0.10, [Flags.FLAT, Flags.DESC_PERCENT,\
                                                        Flags.BLOCK]), 0.5, 25, 999),
            (Affix("OH_BLOCK_3", 0.15, [Flags.FLAT, Flags.DESC_PERCENT,\
                                                        Flags.BLOCK]), 0.1, 75, 999),
        ], 0.2),
        "phys_res": ([
            (Affix("OH_PHYS_RES_1", 0.10, [Flags.PHYS, Flags.FLAT]), 1, 0, 60),
            (Affix("OH_PHYS_RES_2", 0.25, [Flags.PHYS, Flags.FLAT]), 0.6, 10, 90),
            (Affix("OH_PHYS_RES_3", 0.40, [Flags.PHYS, Flags.FLAT]), 0.3, 25, 999),
        ], 1),
        "fire_res": ([
            (Affix("OH_FIRE_RES_1", 0.10, [Flags.FIRE, Flags.FLAT]), 1, 0, 60),
            (Affix("OH_FIRE_RES_2", 0.25, [Flags.FIRE, Flags.FLAT]), 0.6, 10, 90),
            (Affix("OH_FIRE_RES_3", 0.40, [Flags.FIRE, Flags.FLAT]), 0.3, 25, 999),
        ], 1),
        "ice_res": ([
            (Affix("OH_ICE_RES_1", 0.10, [Flags.ICE, Flags.FLAT]), 1, 0, 60),
            (Affix("OH_ICE_RES_2", 0.25, [Flags.ICE, Flags.FLAT]), 0.6, 10, 90),
            (Affix("OH_ICE_RES_3", 0.40, [Flags.ICE, Flags.FLAT]), 0.3, 25, 999),
        ], 1),
        "elec_res": ([
            (Affix("OH_ELEC_RES_1", 0.10, [Flags.ELEC, Flags.FLAT]), 1, 0, 60),
            (Affix("OH_ELEC_RES_2", 0.25, [Flags.ELEC, Flags.FLAT]), 0.6, 10, 90),
            (Affix("OH_ELEC_RES_3", 0.40, [Flags.ELEC, Flags.FLAT]), 0.3, 25, 999),
        ], 1),
        "light_res": ([
            (Affix("OH_LIGHT_RES_1", 0.10, [Flags.LIGHT, Flags.FLAT]), 1, 0, 60),
            (Affix("OH_LIGHT_RES_2", 0.25, [Flags.LIGHT, Flags.FLAT]), 0.6, 10, 90),
            (Affix("OH_LIGHT_RES_3", 0.40, [Flags.LIGHT, Flags.FLAT]), 0.3, 25, 999),
        ], 1),
        "dark_res": ([
            (Affix("OH_DARK_RES_1", 0.10, [Flags.DARK, Flags.FLAT]), 1, 0, 60),
            (Affix("OH_DARK_RES_2", 0.25, [Flags.DARK, Flags.FLAT]), 0.6, 10, 90),
            (Affix("OH_DARK_RES_3", 0.40, [Flags.DARK, Flags.FLAT]), 0.3, 25, 999),
        ], 1),
        "energ_res": ([
            (Affix("OH_ENERG_RES_1", 0.10, [Flags.ENERG, Flags.FLAT]), 1, 0, 60),
            (Affix("OH_ENERG_RES_2", 0.25, [Flags.ENERG, Flags.FLAT]), 0.6, 10, 90),
            (Affix("OH_ENERG_RES_3", 0.40, [Flags.ENERG, Flags.FLAT]), 0.3, 25, 999),
        ], 1),
        "elemental_res": ([
            (Affix("OH_ELEMENTAL_RESISTANCES_1", 0.10, [Flags.ELEMENTAL_RESISTANCES,\
                                                            Flags.FLAT]), 1, 20, 60),
            (Affix("OH_ELEMENTAL_RESISTANCES_2", 0.25, [Flags.ELEMENTAL_RESISTANCES,\
                                                            Flags.FLAT]), 0.6, 40, 90),
            (Affix("OH_ELEMENTAL_RESISTANCES_3", 0.40, [Flags.ELEMENTAL_RESISTANCES,\
                                                            Flags.FLAT]), 0.3, 60, 999),
        ], 0.8),
        "crit_res": ([
            (Affix("OH_CRIT_RES_1", 0.05, [Flags.CRIT_RES, Flags.FLAT]), 1, 0, 60),
            (Affix("OH_CRIT_RES_2", 0.1, [Flags.ENERG, Flags.FLAT]), 0.6, 10, 90),
            (Affix("OH_CRIT_RES_3", 0.2, [Flags.ENERG, Flags.FLAT]), 0.3, 25, 999),
        ], 0.5),
        "all_res": ([
            (Affix("OH_ALL_RESISTANCES_1", 0.10, [Flags.ALL_RESISTANCES,\
                                                        Flags.FLAT]), 1, 20, 60),
            (Affix("OH_ALL_RESISTANCES_2", 0.25, [Flags.ALL_RESISTANCES,\
                                                        Flags.FLAT]), 0.6, 40, 90),
            (Affix("OH_ALL_RESISTANCES_3", 0.40, [Flags.ALL_RESISTANCES,\
                                                        Flags.FLAT]), 0.3, 60, 999),
        ], 0.25),
    }
}