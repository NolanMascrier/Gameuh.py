"""Centralized affix pool with gear type filtering."""

from data.constants import Flags
from data.numerics.affix import Affix
from data.numerics.double_affix import DoubleAffix

class AffixDefinition:
    """Defines an affix type with its tiers and applicable gear slots."""  
    def __init__(self, affix_id: str, tiers: list, base_weight: float, 
                 allowed_slots: list[Flags], value_multipliers: dict = None):
        """
        Args:
            affix_id: Unique identifier for this affix type
            tiers: List of (affix, weight, min_lvl, max_lvl) tuples
            base_weight: Base weight for affix selection
            allowed_slots: List of Flags indicating which gear slots can have this affix
            value_multipliers: Optional dict of {Flags: multiplier} for custom scaling per slot.
                              If None, uses SLOT_MULTIPLIERS
        """
        self.affix_id = affix_id
        self.tiers = tiers
        self.base_weight = base_weight
        self.allowed_slots = allowed_slots
        self.value_multipliers = value_multipliers or {}

SLOT_MULTIPLIERS = {
    Flags.ARMOR: 1.0,
    Flags.WEAPON: 1.0,
    Flags.HELM: 0.7,
    Flags.BOOTS: 0.7,
    Flags.HANDS: 0.7,
    Flags.BELT: 0.6,
    Flags.RING: 0.5,
    Flags.AMULET: 0.8,
    Flags.OFFHAND: 0.7,
    Flags.RELIC: 0.6,
    Flags.JEWEL: 1,
    Flags.LIFE_POT: 1,
    Flags.MANA_POT: 1
}

AFFIX_POOL = [
    # ===== ATTRIBUTE AFFIXES =====
    AffixDefinition(
        "strength",
        [
            (Affix("STR_1", 5, [Flags.FLAT, Flags.DESC_FLAT, Flags.STR]), 1, 0, 25),
            (Affix("STR_2", 10, [Flags.FLAT, Flags.DESC_FLAT, Flags.STR]), 0.8, 0, 30),
            (Affix("STR_3", 15, [Flags.FLAT, Flags.DESC_FLAT, Flags.STR]), 0.5, 10, 40),
            (Affix("STR_4", 20, [Flags.FLAT, Flags.DESC_FLAT, Flags.STR]), 0.3, 20, 60),
            (Affix("STR_5", 30, [Flags.FLAT, Flags.DESC_FLAT, Flags.STR]), 0.2, 30, 80),
            (Affix("STR_6", 40, [Flags.FLAT, Flags.DESC_FLAT, Flags.STR]), 0.1, 50, 999),
            (Affix("STR_7", 65, [Flags.FLAT, Flags.DESC_FLAT, Flags.STR]), 0.05, 75, 999),
        ],
        1.0,
        [Flags.ARMOR, Flags.HELM, Flags.BOOTS, Flags.HANDS, Flags.RING,
         Flags.AMULET, Flags.BELT],
        {Flags.RING: 2.0, Flags.AMULET: 2.5, Flags.BELT: 2.0}
    ),

    AffixDefinition(
        "dexterity",
        [
            (Affix("DEX_1", 5, [Flags.FLAT, Flags.DESC_FLAT, Flags.DEX]), 1, 0, 25),
            (Affix("DEX_2", 10, [Flags.FLAT, Flags.DESC_FLAT, Flags.DEX]), 0.8, 0, 30),
            (Affix("DEX_3", 15, [Flags.FLAT, Flags.DESC_FLAT, Flags.DEX]), 0.5, 10, 40),
            (Affix("DEX_4", 20, [Flags.FLAT, Flags.DESC_FLAT, Flags.DEX]), 0.3, 20, 60),
            (Affix("DEX_5", 30, [Flags.FLAT, Flags.DESC_FLAT, Flags.DEX]), 0.2, 30, 80),
            (Affix("DEX_6", 40, [Flags.FLAT, Flags.DESC_FLAT, Flags.DEX]), 0.1, 50, 999),
            (Affix("DEX_7", 65, [Flags.FLAT, Flags.DESC_FLAT, Flags.DEX]), 0.05, 75, 999),
        ],
        1.0,
        [Flags.ARMOR, Flags.HELM, Flags.BOOTS, Flags.HANDS, Flags.RING,
         Flags.AMULET, Flags.BELT],
        {Flags.RING: 2.0, Flags.AMULET: 2.5, Flags.BELT: 2.0}
    ),

    AffixDefinition(
        "intelligence",
        [
            (Affix("INT_1", 5, [Flags.FLAT, Flags.DESC_FLAT, Flags.INT]), 1, 0, 25),
            (Affix("INT_2", 10, [Flags.FLAT, Flags.DESC_FLAT, Flags.INT]), 0.8, 0, 30),
            (Affix("INT_3", 15, [Flags.FLAT, Flags.DESC_FLAT, Flags.INT]), 0.5, 10, 40),
            (Affix("INT_4", 20, [Flags.FLAT, Flags.DESC_FLAT, Flags.INT]), 0.3, 20, 60),
            (Affix("INT_5", 30, [Flags.FLAT, Flags.DESC_FLAT, Flags.INT]), 0.2, 30, 80),
            (Affix("INT_6", 40, [Flags.FLAT, Flags.DESC_FLAT, Flags.INT]), 0.1, 50, 999),
            (Affix("INT_7", 65, [Flags.FLAT, Flags.DESC_FLAT, Flags.INT]), 0.05, 75, 999),
        ],
        1.0,
        [Flags.ARMOR, Flags.HELM, Flags.BOOTS, Flags.HANDS, Flags.RING,
         Flags.AMULET, Flags.BELT],
        {Flags.RING: 2.0, Flags.AMULET: 2.5, Flags.BELT: 2.0}
    ),

    # ===== LIFE AFFIXES =====
    AffixDefinition(
        "life_flat",
        [
            (Affix("LIFE_1", 10, [Flags.FLAT, Flags.DESC_FLAT, Flags.LIFE]), 1, 0, 25),
            (Affix("LIFE_2", 25, [Flags.FLAT, Flags.DESC_FLAT, Flags.LIFE]), 0.8, 0, 30),
            (Affix("LIFE_3", 50, [Flags.FLAT, Flags.DESC_FLAT, Flags.LIFE]), 0.5, 10, 40),
            (Affix("LIFE_4", 75, [Flags.FLAT, Flags.DESC_FLAT, Flags.LIFE]), 0.3, 20, 60),
            (Affix("LIFE_5", 100, [Flags.FLAT, Flags.DESC_FLAT, Flags.LIFE]), 0.2, 30, 80),
            (Affix("LIFE_6", 150, [Flags.FLAT, Flags.DESC_FLAT, Flags.LIFE]), 0.1, 50, 999),
            (Affix("LIFE_7", 250, [Flags.FLAT, Flags.DESC_FLAT, Flags.LIFE]), 0.05, 75, 999),
        ],
        1.0,
        [Flags.ARMOR, Flags.HELM, Flags.BOOTS, Flags.HANDS, Flags.RING,
         Flags.AMULET, Flags.BELT]
    ),

    AffixDefinition(
        "life_increased",
        [
            (Affix("LIFE_INCR_1", 0.10, [Flags.BOON, Flags.LIFE]), 1, 0, 25),
            (Affix("LIFE_INCR_2", 0.15, [Flags.BOON, Flags.LIFE]), 0.6, 15, 40),
            (Affix("LIFE_INCR_3", 0.20, [Flags.BOON, Flags.LIFE]), 0.3, 25, 60),
            (Affix("LIFE_INCR_4", 0.30, [Flags.BOON, Flags.LIFE]), 0.15, 50, 999),
            (Affix("LIFE_INCR_5", 0.50, [Flags.BOON, Flags.LIFE]), 0.01, 75, 999),
        ],
        0.8,
        [Flags.ARMOR, Flags.HELM, Flags.BOOTS, Flags.HANDS, Flags.RING,
         Flags.AMULET, Flags.BELT]
    ),

    AffixDefinition(
        "life_more",
        [
            (Affix("LIFE_MORE_1", 0.05, [Flags.BLESS, Flags.LIFE]), 1, 25, 75),
            (Affix("LIFE_MORE_2", 0.15, [Flags.BLESS, Flags.LIFE]), 0.6, 30, 999),
            (Affix("LIFE_MORE_3", 0.20, [Flags.BLESS, Flags.LIFE]), 0.3, 75, 999),
        ],
        0.2,
        [Flags.ARMOR]
    ),

    # ===== MANA AFFIXES =====
    AffixDefinition(
        "mana_flat",
        [
            (Affix("MANA_1", 10, [Flags.FLAT, Flags.DESC_FLAT, Flags.MANA]), 1, 0, 25),
            (Affix("MANA_2", 25, [Flags.FLAT, Flags.DESC_FLAT, Flags.MANA]), 0.8, 0, 30),
            (Affix("MANA_3", 50, [Flags.FLAT, Flags.DESC_FLAT, Flags.MANA]), 0.5, 10, 40),
            (Affix("MANA_4", 75, [Flags.FLAT, Flags.DESC_FLAT, Flags.MANA]), 0.3, 20, 60),
            (Affix("MANA_5", 100, [Flags.FLAT, Flags.DESC_FLAT, Flags.MANA]), 0.2, 30, 80),
            (Affix("MANA_6", 150, [Flags.FLAT, Flags.DESC_FLAT, Flags.MANA]), 0.1, 50, 999),
            (Affix("MANA_7", 250, [Flags.FLAT, Flags.DESC_FLAT, Flags.MANA]), 0.05, 75, 999),
        ],
        1.0,
        [Flags.ARMOR, Flags.HELM, Flags.BOOTS, Flags.HANDS, Flags.RING,
         Flags.AMULET, Flags.BELT]
    ),

    AffixDefinition(
        "mana_increased",
        [
            (Affix("MANA_INCR_1", 0.10, [Flags.BOON, Flags.MANA]), 1, 0, 25),
            (Affix("MANA_INCR_2", 0.15, [Flags.BOON, Flags.MANA]), 0.6, 15, 40),
            (Affix("MANA_INCR_3", 0.20, [Flags.BOON, Flags.MANA]), 0.3, 25, 60),
            (Affix("MANA_INCR_4", 0.30, [Flags.BOON, Flags.MANA]), 0.15, 50, 999),
            (Affix("MANA_INCR_5", 0.50, [Flags.BOON, Flags.MANA]), 0.01, 75, 999),
        ],
        0.8,
        [Flags.ARMOR, Flags.HELM, Flags.BOOTS, Flags.HANDS, Flags.RING,
         Flags.AMULET, Flags.BELT]
    ),

    # ===== DEFENSE AFFIXES =====
    AffixDefinition(
        "endurance",
        [
            (Affix("DEF_1", 100, [Flags.FLAT, Flags.DESC_FLAT, Flags.DEF]), 1, 0, 30),
            (Affix("DEF_2", 250, [Flags.FLAT, Flags.DESC_FLAT, Flags.DEF]), 0.8, 0, 30),
            (Affix("DEF_3", 500, [Flags.FLAT, Flags.DESC_FLAT, Flags.DEF]), 0.5, 10, 40),
            (Affix("DEF_4", 750, [Flags.FLAT, Flags.DESC_FLAT, Flags.DEF]), 0.3, 20, 60),
            (Affix("DEF_5", 1000, [Flags.FLAT, Flags.DESC_FLAT, Flags.DEF]), 0.2, 30, 80),
            (Affix("DEF_6", 1500, [Flags.FLAT, Flags.DESC_FLAT, Flags.DEF]), 0.1, 50, 999),
            (Affix("DEF_7", 2500, [Flags.FLAT, Flags.DESC_FLAT, Flags.DEF]), 0.05, 75, 999),
        ],
        1.2,
        [Flags.ARMOR, Flags.HELM, Flags.BOOTS, Flags.HANDS, Flags.OFFHAND]
    ),

    AffixDefinition(
        "dodge_rating",
        [
            (Affix("DODGE_RATING_1", 100, [Flags.FLAT, Flags.DESC_FLAT, Flags.DODGE_RATING]),
                    1, 0, 30),
            (Affix("DODGE_RATING_2", 250, [Flags.FLAT, Flags.DESC_FLAT, Flags.DODGE_RATING]),
                    0.8, 0, 30),
            (Affix("DODGE_RATING_3", 500, [Flags.FLAT, Flags.DESC_FLAT, Flags.DODGE_RATING]),
                    0.5, 10, 40),
            (Affix("DODGE_RATING_4", 750, [Flags.FLAT, Flags.DESC_FLAT, Flags.DODGE_RATING]),
                    0.3, 20, 60),
            (Affix("DODGE_RATING_5", 1000, [Flags.FLAT, Flags.DESC_FLAT, Flags.DODGE_RATING]),
                    0.2, 30, 80),
            (Affix("DODGE_RATING_6", 1500, [Flags.FLAT, Flags.DESC_FLAT, Flags.DODGE_RATING]),
                    0.1, 50, 999),
            (Affix("DODGE_RATING_7", 2500, [Flags.FLAT, Flags.DESC_FLAT, Flags.DODGE_RATING]),
                    0.05, 75, 999),
        ],
        1.2,
        [Flags.ARMOR, Flags.HELM, Flags.BOOTS, Flags.HANDS, Flags.OFFHAND]
    ),

    AffixDefinition(
        "dodge",
        [
            (Affix("DODGE_1", 0.01, [Flags.FLAT, Flags.DESC_PERCENT, Flags.DODGE]), 1, 0, 999),
            (Affix("DODGE_2", 0.02, [Flags.FLAT, Flags.DESC_PERCENT, Flags.DODGE]), 0.5, 25, 999),
            (Affix("DODGE_3", 0.05, [Flags.FLAT, Flags.DESC_PERCENT, Flags.DODGE]), 0.1, 75, 999),
        ],
        0.2,
        [Flags.ARMOR, Flags.OFFHAND]
    ),

    AffixDefinition(
        "block",
        [
            (Affix("BLOCK_1", 0.05, [Flags.FLAT, Flags.DESC_PERCENT, Flags.BLOCK]), 1, 0, 999),
            (Affix("BLOCK_2", 0.10, [Flags.FLAT, Flags.DESC_PERCENT, Flags.BLOCK]), 0.5, 25, 999),
            (Affix("BLOCK_3", 0.15, [Flags.FLAT, Flags.DESC_PERCENT, Flags.BLOCK]), 0.1, 75, 999),
        ],
        0.2,
        [Flags.OFFHAND]
    ),

    # ===== RESISTANCE AFFIXES =====
    AffixDefinition(
        "physical_resistance",
        [
            (Affix("PHYS_RES_1", 0.10, [Flags.PHYS, Flags.FLAT]), 1, 0, 60),
            (Affix("PHYS_RES_2", 0.25, [Flags.PHYS, Flags.FLAT]), 0.6, 10, 90),
            (Affix("PHYS_RES_3", 0.40, [Flags.PHYS, Flags.FLAT]), 0.3, 25, 999),
        ],
        1.0,
        [Flags.ARMOR, Flags.HELM, Flags.BOOTS, Flags.HANDS, Flags.RING,
         Flags.AMULET, Flags.BELT, Flags.OFFHAND]
    ),

    AffixDefinition(
        "fire_resistance",
        [
            (Affix("FIRE_RES_1", 0.10, [Flags.FIRE, Flags.FLAT]), 1, 0, 60),
            (Affix("FIRE_RES_2", 0.25, [Flags.FIRE, Flags.FLAT]), 0.6, 10, 90),
            (Affix("FIRE_RES_3", 0.40, [Flags.FIRE, Flags.FLAT]), 0.3, 25, 999),
        ],
        1.0,
        [Flags.ARMOR, Flags.HELM, Flags.BOOTS, Flags.HANDS, Flags.RING,
         Flags.AMULET, Flags.BELT, Flags.OFFHAND]
    ),

    AffixDefinition(
        "ice_resistance",
        [
            (Affix("ICE_RES_1", 0.10, [Flags.ICE, Flags.FLAT]), 1, 0, 60),
            (Affix("ICE_RES_2", 0.25, [Flags.ICE, Flags.FLAT]), 0.6, 10, 90),
            (Affix("ICE_RES_3", 0.40, [Flags.ICE, Flags.FLAT]), 0.3, 25, 999),
        ],
        1.0,
        [Flags.ARMOR, Flags.HELM, Flags.BOOTS, Flags.HANDS, Flags.RING,
         Flags.AMULET, Flags.BELT, Flags.OFFHAND]
    ),

    AffixDefinition(
        "electric_resistance",
        [
            (Affix("ELEC_RES_1", 0.10, [Flags.ELEC, Flags.FLAT]), 1, 0, 60),
            (Affix("ELEC_RES_2", 0.25, [Flags.ELEC, Flags.FLAT]), 0.6, 10, 90),
            (Affix("ELEC_RES_3", 0.40, [Flags.ELEC, Flags.FLAT]), 0.3, 25, 999),
        ],
        1.0,
        [Flags.ARMOR, Flags.HELM, Flags.BOOTS, Flags.HANDS, Flags.RING,
         Flags.AMULET, Flags.BELT, Flags.OFFHAND]
    ),

    AffixDefinition(
        "energy_resistance",
        [
            (Affix("ENERG_RES_1", 0.10, [Flags.ENERG, Flags.FLAT]), 1, 0, 60),
            (Affix("ENERG_RES_2", 0.25, [Flags.ENERG, Flags.FLAT]), 0.6, 10, 90),
            (Affix("ENERG_RES_3", 0.40, [Flags.ENERG, Flags.FLAT]), 0.3, 25, 999),
        ],
        1.0,
        [Flags.ARMOR, Flags.HELM, Flags.BOOTS, Flags.HANDS, Flags.RING,
         Flags.AMULET, Flags.BELT, Flags.OFFHAND]
    ),

    AffixDefinition(
        "light_resistance",
        [
            (Affix("LIGHT_RES_1", 0.10, [Flags.LIGHT, Flags.FLAT]), 1, 0, 60),
            (Affix("LIGHT_RES_2", 0.25, [Flags.LIGHT, Flags.FLAT]), 0.6, 10, 90),
            (Affix("LIGHT_RES_3", 0.40, [Flags.LIGHT, Flags.FLAT]), 0.3, 25, 999),
        ],
        1.0,
        [Flags.ARMOR, Flags.HELM, Flags.BOOTS, Flags.HANDS, Flags.RING,
         Flags.AMULET, Flags.BELT, Flags.OFFHAND]
    ),

    AffixDefinition(
        "dark_resistance",
        [
            (Affix("DARK_RES_1", 0.10, [Flags.DARK, Flags.FLAT]), 1, 0, 60),
            (Affix("DARK_RES_2", 0.25, [Flags.DARK, Flags.FLAT]), 0.6, 10, 90),
            (Affix("DARK_RES_3", 0.40, [Flags.DARK, Flags.FLAT]), 0.3, 25, 999),
        ],
        1.0,
        [Flags.ARMOR, Flags.HELM, Flags.BOOTS, Flags.HANDS, Flags.RING,
         Flags.AMULET, Flags.BELT, Flags.OFFHAND]
    ),

    AffixDefinition(
        "elemental_resistances",
        [
            (Affix("ELEMENTAL_RES_1", 0.10, [Flags.ELEMENTAL_RESISTANCES, Flags.FLAT]),
                    1, 20, 60),
            (Affix("ELEMENTAL_RES_2", 0.25, [Flags.ELEMENTAL_RESISTANCES, Flags.FLAT]),
                    0.6, 40, 90),
            (Affix("ELEMENTAL_RES_3", 0.40, [Flags.ELEMENTAL_RESISTANCES, Flags.FLAT]),
                    0.3, 60, 999),
        ],
        0.8,
        [Flags.ARMOR, Flags.HELM, Flags.BOOTS, Flags.HANDS, Flags.RING,
         Flags.AMULET, Flags.BELT, Flags.OFFHAND]
    ),

    AffixDefinition(
        "all_resistances",
        [
            (Affix("ALL_RES_1", 0.10, [Flags.ALL_RESISTANCES, Flags.FLAT]), 1, 20, 60),
            (Affix("ALL_RES_2", 0.25, [Flags.ALL_RESISTANCES, Flags.FLAT]), 0.6, 40, 90),
            (Affix("ALL_RES_3", 0.40, [Flags.ALL_RESISTANCES, Flags.FLAT]), 0.3, 60, 999),
        ],
        0.25,
        [Flags.ARMOR, Flags.HELM, Flags.BOOTS, Flags.HANDS, Flags.RING,
         Flags.AMULET, Flags.BELT, Flags.OFFHAND]
    ),

    # ===== OFFENSIVE STATS (Precision, Cast Speed, etc.) =====
    AffixDefinition(
        "precision",
        [
            (Affix("PRECISION_1", 50, [Flags.FLAT, Flags.DESC_FLAT, Flags.PRECISION]),
                    1, 0, 30),
            (Affix("PRECISION_2", 100, [Flags.FLAT, Flags.DESC_FLAT, Flags.PRECISION]),
                    0.8, 0, 30),
            (Affix("PRECISION_3", 200, [Flags.FLAT, Flags.DESC_FLAT, Flags.PRECISION]),
                    0.5, 10, 40),
            (Affix("PRECISION_4", 300, [Flags.FLAT, Flags.DESC_FLAT, Flags.PRECISION]),
                    0.3, 20, 60),
            (Affix("PRECISION_5", 500, [Flags.FLAT, Flags.DESC_FLAT, Flags.PRECISION]),
                    0.2, 30, 80),
            (Affix("PRECISION_6", 750, [Flags.FLAT, Flags.DESC_FLAT, Flags.PRECISION]),
                    0.1, 50, 999),
            (Affix("PRECISION_7", 1000, [Flags.FLAT, Flags.DESC_FLAT, Flags.PRECISION]),
                    0.05, 75, 999),
        ],
        0.9,
        [Flags.HELM, Flags.RING, Flags.AMULET, Flags.BELT, Flags.WEAPON, Flags.OFFHAND]
    ),

    AffixDefinition(
        "cast_speed",
        [
            (Affix("CSPEED_1", 0.05, [Flags.HEX, Flags.CSPEED]), 1, 0, 50),
            (Affix("CSPEED_2", 0.1, [Flags.HEX, Flags.CSPEED]), 0.8, 0, 70),
            (Affix("CSPEED_3", 0.15, [Flags.HEX, Flags.CSPEED]), 0.5, 10, 90),
            (Affix("CSPEED_4", 0.2, [Flags.HEX, Flags.CSPEED]), 0.3, 20, 999),
            (Affix("CSPEED_5", 0.25, [Flags.HEX, Flags.CSPEED]), 0.2, 30, 999),
        ],
        0.9,
        [Flags.HANDS, Flags.RING, Flags.AMULET, Flags.BELT]
    ),

    AffixDefinition(
        "movement_speed",
        [
            (Affix("SPEED_1", 0.1, [Flags.BOON, Flags.SPEED]), 1, 0, 30),
            (Affix("SPEED_2", 0.15, [Flags.BOON, Flags.SPEED]), 0.8, 0, 30),
            (Affix("SPEED_3", 0.2, [Flags.BOON, Flags.SPEED]), 0.5, 10, 40),
            (Affix("SPEED_4", 0.25, [Flags.BOON, Flags.SPEED]), 0.3, 20, 60),
            (Affix("SPEED_5", 0.3, [Flags.BOON, Flags.SPEED]), 0.2, 30, 80),
            (Affix("SPEED_6", 0.4, [Flags.BOON, Flags.SPEED]), 0.1, 50, 999),
            (Affix("SPEED_7", 0.5, [Flags.BOON, Flags.SPEED]), 0.05, 75, 999),
        ],
        0.9,
        [Flags.BOOTS]
    ),

    AffixDefinition(
        "life_regen",
        [
            (Affix("LIFE_REGEN_1", 5, [Flags.FLAT, Flags.LIFE_REGEN, Flags.DESC_FLAT]),
                    1, 0, 60),
            (Affix("LIFE_REGEN_2", 10, [Flags.FLAT, Flags.LIFE_REGEN, Flags.DESC_FLAT]),
                    1, 20, 60),
            (Affix("LIFE_REGEN_3", 20, [Flags.FLAT, Flags.LIFE_REGEN, Flags.DESC_FLAT]),
                    1, 40, 999),
            (Affix("LIFE_REGEN_4", 30, [Flags.FLAT, Flags.LIFE_REGEN, Flags.DESC_FLAT]),
                    1, 50, 999),
            (Affix("LIFE_REGEN_5", 50, [Flags.FLAT, Flags.LIFE_REGEN, Flags.DESC_FLAT]),
                    1, 70, 999),
        ],
        0.8,
        [Flags.ARMOR, Flags.AMULET, Flags.RELIC]
    ),

    AffixDefinition(
        "crit_resistance",
        [
            (Affix("CRIT_RES_1", 0.05, [Flags.CRIT_RES, Flags.FLAT]), 1, 0, 60),
            (Affix("CRIT_RES_2", 0.1, [Flags.CRIT_RES, Flags.FLAT]), 0.6, 10, 90),
            (Affix("CRIT_RES_3", 0.2, [Flags.CRIT_RES, Flags.FLAT]), 0.3, 25, 999),
        ],
        0.5,
        [Flags.ARMOR, Flags.OFFHAND]
    ),

    # ===== DAMAGE AFFIXES (Weapons, Rings, Amulets, Belts, Relics, Offhands) =====
    AffixDefinition(
        "physical_damage_flat",
        [
            (DoubleAffix("PHYS_FLAT_1", 8, 15, [Flags.PHYS_FLAT, Flags.DESC_FLAT,
                                                 Flags.FLAT], 0.5, 1.5, 0.5, 1.5), 1, 0, 75),
            (DoubleAffix("PHYS_FLAT_2", 20, 30, [Flags.PHYS_FLAT, Flags.DESC_FLAT,
                                                  Flags.FLAT], 0.5, 1.5, 0.5, 1.5), 0.8, 20, 80),
            (DoubleAffix("PHYS_FLAT_3", 40, 60, [Flags.PHYS_FLAT, Flags.DESC_FLAT,
                                                  Flags.FLAT], 0.5, 1.5, 0.5, 1.5), 0.6, 40, 999),
            (DoubleAffix("PHYS_FLAT_4", 80, 100, [Flags.PHYS_FLAT, Flags.DESC_FLAT,
                                                   Flags.FLAT], 0.5, 1.5, 0.5, 1.5), 0.25, 60, 999),
            (DoubleAffix("PHYS_FLAT_5", 150, 200, [Flags.PHYS_FLAT, Flags.DESC_FLAT,
                                                    Flags.FLAT], 0.5, 1.5, 0.5, 1.5), 0.1, 75, 999),
        ],
        2.0,
        [Flags.WEAPON]
    ),

    AffixDefinition(
        "fire_damage_flat",
        [
            (DoubleAffix("FIRE_FLAT_1", 8, 15, [Flags.FIRE_FLAT, Flags.DESC_FLAT,
                                                 Flags.FLAT], 0.5, 1.5, 0.5, 1.5), 1, 0, 75),
            (DoubleAffix("FIRE_FLAT_2", 20, 30, [Flags.FIRE_FLAT, Flags.DESC_FLAT,
                                                  Flags.FLAT], 0.5, 1.5, 0.5, 1.5), 0.8, 20, 80),
            (DoubleAffix("FIRE_FLAT_3", 40, 60, [Flags.FIRE_FLAT, Flags.DESC_FLAT,
                                                  Flags.FLAT], 0.5, 1.5, 0.5, 1.5), 0.6, 40, 999),
            (DoubleAffix("FIRE_FLAT_4", 80, 100, [Flags.FIRE_FLAT, Flags.DESC_FLAT,
                                                   Flags.FLAT], 0.5, 1.5, 0.5, 1.5), 0.25, 60, 999),
            (DoubleAffix("FIRE_FLAT_5", 150, 200, [Flags.FIRE_FLAT, Flags.DESC_FLAT,
                                                    Flags.FLAT], 0.5, 1.5, 0.5, 1.5), 0.1, 75, 999),
        ],
        1.5,
        [Flags.WEAPON]
    ),

    AffixDefinition(
        "ice_damage_flat",
        [
            (DoubleAffix("ICE_FLAT_1", 8, 15, [Flags.ICE_FLAT, Flags.DESC_FLAT,
                                                Flags.FLAT], 0.5, 1.5, 0.5, 1.5), 1, 0, 75),
            (DoubleAffix("ICE_FLAT_2", 20, 30, [Flags.ICE_FLAT, Flags.DESC_FLAT,
                                                 Flags.FLAT], 0.5, 1.5, 0.5, 1.5), 0.8, 20, 80),
            (DoubleAffix("ICE_FLAT_3", 40, 60, [Flags.ICE_FLAT, Flags.DESC_FLAT,
                                                 Flags.FLAT], 0.5, 1.5, 0.5, 1.5), 0.6, 40, 999),
            (DoubleAffix("ICE_FLAT_4", 80, 100, [Flags.ICE_FLAT, Flags.DESC_FLAT,
                                                  Flags.FLAT], 0.5, 1.5, 0.5, 1.5), 0.25, 60, 999),
            (DoubleAffix("ICE_FLAT_5", 150, 200, [Flags.ICE_FLAT, Flags.DESC_FLAT,
                                                   Flags.FLAT], 0.5, 1.5, 0.5, 1.5), 0.1, 75, 999),
        ],
        1.5,
        [Flags.WEAPON]
    ),

    AffixDefinition(
        "electric_damage_flat",
        [
            (DoubleAffix("ELEC_FLAT_1", 1, 20, [Flags.ELEC_FLAT, Flags.DESC_FLAT,
                                                 Flags.FLAT], 0.5, 1.5, 0.5, 1.5), 1, 0, 75),
            (DoubleAffix("ELEC_FLAT_2", 3, 40, [Flags.ELEC_FLAT, Flags.DESC_FLAT,
                                                 Flags.FLAT], 0.5, 1.5, 0.5, 1.5), 0.8, 20, 80),
            (DoubleAffix("ELEC_FLAT_3", 5, 75, [Flags.ELEC_FLAT, Flags.DESC_FLAT,
                                                 Flags.FLAT], 0.5, 1.5, 0.5, 1.5), 0.6, 40, 999),
            (DoubleAffix("ELEC_FLAT_4", 10, 150, [Flags.ELEC_FLAT, Flags.DESC_FLAT,
                                                   Flags.FLAT], 0.5, 1.5, 0.5, 1.5), 0.25, 60, 999),
            (DoubleAffix("ELEC_FLAT_5", 25, 300, [Flags.ELEC_FLAT, Flags.DESC_FLAT,
                                                   Flags.FLAT], 0.5, 1.5, 0.5, 1.5), 0.1, 75, 999),
        ],
        1.5,
        [Flags.WEAPON]
    ),

    AffixDefinition(
        "energy_damage_flat",
        [
            (DoubleAffix("ENERG_FLAT_1", 8, 15, [Flags.ENERG_FLAT, Flags.DESC_FLAT,
                                                 Flags.FLAT], 0.5, 1.5, 0.5, 1.5), 1, 0, 75),
            (DoubleAffix("ENERG_FLAT_2", 20, 30, [Flags.ENERG_FLAT, Flags.DESC_FLAT,
                                                  Flags.FLAT], 0.5, 1.5, 0.5, 1.5), 0.8, 20, 80),
            (DoubleAffix("ENERG_FLAT_3", 40, 60, [Flags.ENERG_FLAT, Flags.DESC_FLAT,
                                                  Flags.FLAT], 0.5, 1.5, 0.5, 1.5), 0.6, 40, 999),
            (DoubleAffix("ENERG_FLAT_4", 80, 100, [Flags.ENERG_FLAT, Flags.DESC_FLAT,
                                                   Flags.FLAT], 0.5, 1.5, 0.5, 1.5), 0.25, 60, 999),
            (DoubleAffix("ENERG_FLAT_5", 150, 200, [Flags.ENERG_FLAT, Flags.DESC_FLAT,
                                                    Flags.FLAT], 0.5, 1.5, 0.5, 1.5), 0.1, 75, 999),
        ],
        1.5,
        [Flags.WEAPON]
    ),

    AffixDefinition(
        "light_damage_flat",
        [
            (DoubleAffix("LIGHT_FLAT_1", 8, 15, [Flags.LIGHT_FLAT, Flags.DESC_FLAT,
                                                 Flags.FLAT], 0.5, 1.5, 0.5, 1.5), 1, 0, 75),
            (DoubleAffix("LIGHT_FLAT_2", 20, 30, [Flags.LIGHT_FLAT, Flags.DESC_FLAT,
                                                  Flags.FLAT], 0.5, 1.5, 0.5, 1.5), 0.8, 20, 80),
            (DoubleAffix("LIGHT_FLAT_3", 40, 60, [Flags.LIGHT_FLAT, Flags.DESC_FLAT,
                                                  Flags.FLAT], 0.5, 1.5, 0.5, 1.5), 0.6, 40, 999),
            (DoubleAffix("LIGHT_FLAT_4", 80, 100, [Flags.LIGHT_FLAT, Flags.DESC_FLAT,
                                                   Flags.FLAT], 0.5, 1.5, 0.5, 1.5), 0.25, 60, 999),
            (DoubleAffix("LIGHT_FLAT_5", 150, 200, [Flags.LIGHT_FLAT, Flags.DESC_FLAT,
                                                    Flags.FLAT], 0.5, 1.5, 0.5, 1.5), 0.1, 75, 999),
        ],
        0.9,
        [Flags.WEAPON]
    ),

    AffixDefinition(
        "dark_damage_flat",
        [
            (DoubleAffix("DARK_FLAT_1", 8, 15, [Flags.DARK_FLAT, Flags.DESC_FLAT,
                                                 Flags.FLAT], 0.5, 1.5, 0.5, 1.5), 1, 0, 75),
            (DoubleAffix("DARK_FLAT_2", 20, 30, [Flags.DARK_FLAT, Flags.DESC_FLAT,
                                                  Flags.FLAT], 0.5, 1.5, 0.5, 1.5), 0.8, 20, 80),
            (DoubleAffix("DARK_FLAT_3", 40, 60, [Flags.DARK_FLAT, Flags.DESC_FLAT,
                                                  Flags.FLAT], 0.5, 1.5, 0.5, 1.5), 0.6, 40, 999),
            (DoubleAffix("DARK_FLAT_4", 80, 100, [Flags.DARK_FLAT, Flags.DESC_FLAT,
                                                   Flags.FLAT], 0.5, 1.5, 0.5, 1.5), 0.25, 60, 999),
            (DoubleAffix("DARK_FLAT_5", 150, 200, [Flags.DARK_FLAT, Flags.DESC_FLAT,
                                                    Flags.FLAT], 0.5, 1.5, 0.5, 1.5), 0.1, 75, 999),
        ],
        0.9,
        [Flags.WEAPON]
    ),

    # ===== INCREASED DAMAGE AFFIXES =====
    AffixDefinition(
        "physical_damage_increased",
        [
            (Affix("PHYS_DMG_1", 0.1, [Flags.PHYS_DMG, Flags.BOON], 0.5, 1.5), 1, 0, 75),
            (Affix("PHYS_DMG_2", 0.2, [Flags.PHYS_DMG, Flags.BOON], 0.5, 1.5), 0.8, 20, 80),
            (Affix("PHYS_DMG_3", 0.4, [Flags.PHYS_DMG, Flags.BOON], 0.5, 1.5), 0.6, 40, 999),
            (Affix("PHYS_DMG_4", 0.6, [Flags.PHYS_DMG, Flags.BOON], 0.5, 1.5), 0.25, 60, 999),
            (Affix("PHYS_DMG_5", 1.0, [Flags.PHYS_DMG, Flags.BOON], 0.5, 1.5), 0.1, 75, 999),
        ],
        1.0,
        [Flags.WEAPON, Flags.RING, Flags.AMULET, Flags.BELT, Flags.RELIC, Flags.OFFHAND]
    ),

    AffixDefinition(
        "fire_damage_increased",
        [
            (Affix("FIRE_DMG_1", 0.1, [Flags.FIRE_DMG, Flags.BOON], 0.5, 1.5), 1, 0, 75),
            (Affix("FIRE_DMG_2", 0.2, [Flags.FIRE_DMG, Flags.BOON], 0.5, 1.5), 0.8, 20, 80),
            (Affix("FIRE_DMG_3", 0.4, [Flags.FIRE_DMG, Flags.BOON], 0.5, 1.5), 0.6, 40, 999),
            (Affix("FIRE_DMG_4", 0.6, [Flags.FIRE_DMG, Flags.BOON], 0.5, 1.5), 0.25, 60, 999),
            (Affix("FIRE_DMG_5", 1.0, [Flags.FIRE_DMG, Flags.BOON], 0.5, 1.5), 0.1, 75, 999),
        ],
        1.0,
        [Flags.WEAPON, Flags.RING, Flags.AMULET, Flags.BELT, Flags.RELIC, Flags.OFFHAND]
    ),

    AffixDefinition(
        "ice_damage_increased",
        [
            (Affix("ICE_DMG_1", 0.1, [Flags.ICE_DMG, Flags.BOON], 0.5, 1.5), 1, 0, 75),
            (Affix("ICE_DMG_2", 0.2, [Flags.ICE_DMG, Flags.BOON], 0.5, 1.5), 0.8, 20, 80),
            (Affix("ICE_DMG_3", 0.4, [Flags.ICE_DMG, Flags.BOON], 0.5, 1.5), 0.6, 40, 999),
            (Affix("ICE_DMG_4", 0.6, [Flags.ICE_DMG, Flags.BOON], 0.5, 1.5), 0.25, 60, 999),
            (Affix("ICE_DMG_5", 1.0, [Flags.ICE_DMG, Flags.BOON], 0.5, 1.5), 0.1, 75, 999),
        ],
        1.0,
        [Flags.WEAPON, Flags.RING, Flags.AMULET, Flags.BELT, Flags.RELIC, Flags.OFFHAND]
    ),

    AffixDefinition(
        "electric_damage_increased",
        [
            (Affix("ELEC_DMG_1", 0.1, [Flags.ELEC_DMG, Flags.BOON], 0.5, 1.5), 1, 0, 75),
            (Affix("ELEC_DMG_2", 0.2, [Flags.ELEC_DMG, Flags.BOON], 0.5, 1.5), 0.8, 20, 80),
            (Affix("ELEC_DMG_3", 0.4, [Flags.ELEC_DMG, Flags.BOON], 0.5, 1.5), 0.6, 40, 999),
            (Affix("ELEC_DMG_4", 0.6, [Flags.ELEC_DMG, Flags.BOON], 0.5, 1.5), 0.25, 60, 999),
            (Affix("ELEC_DMG_5", 1.0, [Flags.ELEC_DMG, Flags.BOON], 0.5, 1.5), 0.1, 75, 999),
        ],
        1.0,
        [Flags.WEAPON, Flags.RING, Flags.AMULET, Flags.BELT, Flags.RELIC, Flags.OFFHAND]
    ),

    AffixDefinition(
        "energy_damage_increased",
        [
            (Affix("ENERG_DMG_1", 0.1, [Flags.ENERG_DMG, Flags.BOON], 0.5, 1.5), 1, 0, 75),
            (Affix("ENERG_DMG_2", 0.2, [Flags.ENERG_DMG, Flags.BOON], 0.5, 1.5), 0.8, 20, 80),
            (Affix("ENERG_DMG_3", 0.4, [Flags.ENERG_DMG, Flags.BOON], 0.5, 1.5), 0.6, 40, 999),
            (Affix("ENERG_DMG_4", 0.6, [Flags.ENERG_DMG, Flags.BOON], 0.5, 1.5), 0.25, 60, 999),
            (Affix("ENERG_DMG_5", 1.0, [Flags.ENERG_DMG, Flags.BOON], 0.5, 1.5), 0.1, 75, 999),
        ],
        1.0,
        [Flags.WEAPON, Flags.RING, Flags.AMULET, Flags.BELT, Flags.RELIC, Flags.OFFHAND]
    ),

    AffixDefinition(
        "light_damage_increased",
        [
            (Affix("LIGHT_DMG_1", 0.1, [Flags.LIGHT_DMG, Flags.BOON], 0.5, 1.5), 1, 0, 75),
            (Affix("LIGHT_DMG_2", 0.2, [Flags.LIGHT_DMG, Flags.BOON], 0.5, 1.5), 0.8, 20, 80),
            (Affix("LIGHT_DMG_3", 0.4, [Flags.LIGHT_DMG, Flags.BOON], 0.5, 1.5), 0.6, 40, 999),
            (Affix("LIGHT_DMG_4", 0.6, [Flags.LIGHT_DMG, Flags.BOON], 0.5, 1.5), 0.25, 60, 999),
            (Affix("LIGHT_DMG_5", 1.0, [Flags.LIGHT_DMG, Flags.BOON], 0.5, 1.5), 0.1, 75, 999),
        ],
        1.0,
        [Flags.WEAPON, Flags.RING, Flags.AMULET, Flags.BELT, Flags.RELIC, Flags.OFFHAND]
    ),

    AffixDefinition(
        "dark_damage_increased",
        [
            (Affix("DARK_DMG_1", 0.1, [Flags.DARK_DMG, Flags.BOON], 0.5, 1.5), 1, 0, 75),
            (Affix("DARK_DMG_2", 0.2, [Flags.DARK_DMG, Flags.BOON], 0.5, 1.5), 0.8, 20, 80),
            (Affix("DARK_DMG_3", 0.4, [Flags.DARK_DMG, Flags.BOON], 0.5, 1.5), 0.6, 40, 999),
            (Affix("DARK_DMG_4", 0.6, [Flags.DARK_DMG, Flags.BOON], 0.5, 1.5), 0.25, 60, 999),
            (Affix("DARK_DMG_5", 1.0, [Flags.DARK_DMG, Flags.BOON], 0.5, 1.5), 0.1, 75, 999),
        ],
        1.0,
        [Flags.WEAPON, Flags.RING, Flags.AMULET, Flags.BELT, Flags.RELIC, Flags.OFFHAND]
    ),

    # ===== PENETRATION AFFIXES =====
    AffixDefinition(
        "physical_penetration",
        [
            (Affix("PHYS_PEN_1", 0.1, [Flags.PHYS_PEN, Flags.FLAT], 0.5, 1.5), 1, 0, 75),
            (Affix("PHYS_PEN_2", 0.2, [Flags.PHYS_PEN, Flags.FLAT], 0.5, 1.5), 0.8, 20, 80),
            (Affix("PHYS_PEN_3", 0.4, [Flags.PHYS_PEN, Flags.FLAT], 0.5, 1.5), 0.6, 40, 999),
        ],
        0.2,
        [Flags.WEAPON, Flags.RELIC, Flags.OFFHAND]
    ),

    AffixDefinition(
        "fire_penetration",
        [
            (Affix("FIRE_PEN_1", 0.1, [Flags.FIRE_PEN, Flags.FLAT], 0.5, 1.5), 1, 0, 75),
            (Affix("FIRE_PEN_2", 0.2, [Flags.FIRE_PEN, Flags.FLAT], 0.5, 1.5), 0.8, 20, 80),
            (Affix("FIRE_PEN_3", 0.4, [Flags.FIRE_PEN, Flags.FLAT], 0.5, 1.5), 0.6, 40, 999),
        ],
        0.2,
        [Flags.WEAPON, Flags.RELIC, Flags.OFFHAND]
    ),

    AffixDefinition(
        "ice_penetration",
        [
            (Affix("ICE_PEN_1", 0.1, [Flags.ICE_PEN, Flags.FLAT], 0.5, 1.5), 1, 0, 75),
            (Affix("ICE_PEN_2", 0.2, [Flags.ICE_PEN, Flags.FLAT], 0.5, 1.5), 0.8, 20, 80),
            (Affix("ICE_PEN_3", 0.4, [Flags.ICE_PEN, Flags.FLAT], 0.5, 1.5), 0.6, 40, 999),
        ],
        0.2,
        [Flags.WEAPON, Flags.RELIC, Flags.OFFHAND]
    ),

    AffixDefinition(
        "electric_penetration",
        [
            (Affix("ELEC_PEN_1", 0.1, [Flags.ELEC_PEN, Flags.FLAT], 0.5, 1.5), 1, 0, 75),
            (Affix("ELEC_PEN_2", 0.2, [Flags.ELEC_PEN, Flags.FLAT], 0.5, 1.5), 0.8, 20, 80),
            (Affix("ELEC_PEN_3", 0.4, [Flags.ELEC_PEN, Flags.FLAT], 0.5, 1.5), 0.6, 40, 999),
        ],
        0.2,
        [Flags.WEAPON, Flags.RELIC, Flags.OFFHAND]
    ),

    AffixDefinition(
        "energy_penetration",
        [
            (Affix("ENERG_PEN_1", 0.1, [Flags.ENERG_PEN, Flags.FLAT], 0.5, 1.5), 1, 0, 75),
            (Affix("ENERG_PEN_2", 0.2, [Flags.ENERG_PEN, Flags.FLAT], 0.5, 1.5), 0.8, 20, 80),
            (Affix("ENERG_PEN_3", 0.4, [Flags.ENERG_PEN, Flags.FLAT], 0.5, 1.5), 0.6, 40, 999),
        ],
        0.2,
        [Flags.WEAPON, Flags.RELIC, Flags.OFFHAND]
    ),

    AffixDefinition(
        "light_penetration",
        [
            (Affix("LIGHT_PEN_1", 0.1, [Flags.LIGHT_PEN, Flags.FLAT], 0.5, 1.5), 1, 0, 75),
            (Affix("LIGHT_PEN_2", 0.2, [Flags.LIGHT_PEN, Flags.FLAT], 0.5, 1.5), 0.8, 20, 80),
            (Affix("LIGHT_PEN_3", 0.4, [Flags.LIGHT_PEN, Flags.FLAT], 0.5, 1.5), 0.6, 40, 999),
        ],
        0.2,
        [Flags.WEAPON, Flags.RELIC, Flags.OFFHAND]
    ),

    AffixDefinition(
        "dark_penetration",
        [
            (Affix("DARK_PEN_1", 0.1, [Flags.DARK_PEN, Flags.FLAT], 0.5, 1.5), 1, 0, 75),
            (Affix("DARK_PEN_2", 0.2, [Flags.DARK_PEN, Flags.FLAT], 0.5, 1.5), 0.8, 20, 80),
            (Affix("DARK_PEN_3", 0.4, [Flags.DARK_PEN, Flags.FLAT], 0.5, 1.5), 0.6, 40, 999),
        ],
        0.2,
        [Flags.WEAPON, Flags.RELIC, Flags.OFFHAND]
    ),

    # ===== ATTACK TYPE DAMAGE =====
    AffixDefinition(
        "melee_damage",
        [
            (Affix("MELEE_1", 0.1, [Flags.MELEE, Flags.BOON], 0.5, 1.5), 1, 0, 75),
            (Affix("MELEE_2", 0.2, [Flags.MELEE, Flags.BOON], 0.5, 1.5), 0.8, 20, 80),
            (Affix("MELEE_3", 0.4, [Flags.MELEE, Flags.BOON], 0.5, 1.5), 0.6, 40, 999),
            (Affix("MELEE_4", 0.6, [Flags.MELEE, Flags.BOON], 0.5, 1.5), 0.25, 60, 999),
            (Affix("MELEE_5", 1.0, [Flags.MELEE, Flags.BOON], 0.5, 1.5), 0.1, 75, 999),
        ],
        1.2,
        [Flags.WEAPON, Flags.OFFHAND]
    ),

    AffixDefinition(
        "ranged_damage",
        [
            (Affix("RANGED_1", 0.1, [Flags.RANGED, Flags.BOON], 0.5, 1.5), 1, 0, 75),
            (Affix("RANGED_2", 0.2, [Flags.RANGED, Flags.BOON], 0.5, 1.5), 0.8, 20, 80),
            (Affix("RANGED_3", 0.4, [Flags.RANGED, Flags.BOON], 0.5, 1.5), 0.6, 40, 999),
            (Affix("RANGED_4", 0.6, [Flags.RANGED, Flags.BOON], 0.5, 1.5), 0.25, 60, 999),
            (Affix("RANGED_5", 1.0, [Flags.RANGED, Flags.BOON], 0.5, 1.5), 0.1, 75, 999),
        ],
        1.2,
        [Flags.WEAPON, Flags.OFFHAND]
    ),

    AffixDefinition(
        "spell_damage",
        [
            (Affix("SPELL_1", 0.1, [Flags.SPELL, Flags.BOON], 0.5, 1.5), 1, 0, 75),
            (Affix("SPELL_2", 0.2, [Flags.SPELL, Flags.BOON], 0.5, 1.5), 0.8, 20, 80),
            (Affix("SPELL_3", 0.4, [Flags.SPELL, Flags.BOON], 0.5, 1.5), 0.6, 40, 999),
            (Affix("SPELL_4", 0.6, [Flags.SPELL, Flags.BOON], 0.5, 1.5), 0.25, 60, 999),
            (Affix("SPELL_5", 1.0, [Flags.SPELL, Flags.BOON], 0.5, 1.5), 0.1, 75, 999),
        ],
        1.2,
        [Flags.WEAPON, Flags.OFFHAND]
    ),

    # ===== MULTI-ELEMENT DAMAGE =====
    AffixDefinition(
        "elemental_damage",
        [
            (Affix("ELEMENTAL_DMG_1", 0.15, [Flags.ELEMENTAL_DAMAGE, Flags.BOON], 0.5, 1.5),
                    1, 0, 75),
            (Affix("ELEMENTAL_DMG_2", 0.25, [Flags.ELEMENTAL_DAMAGE, Flags.BOON], 0.5, 1.5),
                    0.8, 20, 80),
            (Affix("ELEMENTAL_DMG_3", 0.50, [Flags.ELEMENTAL_DAMAGE, Flags.BOON], 0.5, 1.5),
                    0.6, 40, 999),
        ],
        0.7,
        [Flags.WEAPON, Flags.RING, Flags.AMULET, Flags.BELT, Flags.RELIC, Flags.OFFHAND]
    ),

    AffixDefinition(
        "all_damage",
        [
            (Affix("ALL_DMG_1", 0.15, [Flags.ALL_DAMAGE, Flags.BOON], 0.5, 1.5), 1, 0, 75),
            (Affix("ALL_DMG_2", 0.25, [Flags.ALL_DAMAGE, Flags.BOON], 0.5, 1.5), 0.8, 20, 80),
            (Affix("ALL_DMG_3", 0.50, [Flags.ALL_DAMAGE, Flags.BOON], 0.5, 1.5), 0.6, 40, 999),
        ],
        0.1,
        [Flags.WEAPON, Flags.RING, Flags.AMULET, Flags.BELT, Flags.RELIC, Flags.OFFHAND]
    ),

    # ===== CRIT AFFIXES =====
    AffixDefinition(
        "crit_chance",
        [
            (Affix("CRIT_CHANCE_1", 0.1, [Flags.CRIT_CHANCE, Flags.BOON], 0.5, 1.5), 1, 0, 75),
            (Affix("CRIT_CHANCE_2", 0.2, [Flags.CRIT_CHANCE, Flags.BOON], 0.5, 1.5), 0.8, 20, 80),
            (Affix("CRIT_CHANCE_3", 0.4, [Flags.CRIT_CHANCE, Flags.BOON], 0.5, 1.5), 0.6, 40, 999),
            (Affix("CRIT_CHANCE_4", 0.6, [Flags.CRIT_CHANCE, Flags.BOON], 0.5, 1.5), 0.25, 60, 999),
            (Affix("CRIT_CHANCE_5", 1.0, [Flags.CRIT_CHANCE, Flags.BOON], 0.5, 1.5), 0.1, 75, 999),
        ],
        0.8,
        [Flags.WEAPON, Flags.OFFHAND, Flags.RING, Flags.AMULET]
    ),

    AffixDefinition(
        "crit_damage",
        [
            (Affix("CRIT_DAMAGE_1", 0.1, [Flags.CRIT_DAMAGE, Flags.FLAT], 0.5, 1.5), 1, 0, 75),
            (Affix("CRIT_DAMAGE_2", 0.2, [Flags.CRIT_DAMAGE, Flags.FLAT], 0.5, 1.5), 0.8, 20, 80),
            (Affix("CRIT_DAMAGE_3", 0.4, [Flags.CRIT_DAMAGE, Flags.FLAT], 0.5, 1.5), 0.6, 40, 999),
            (Affix("CRIT_DAMAGE_4", 0.6, [Flags.CRIT_DAMAGE, Flags.FLAT], 0.5, 1.5), 0.25, 60, 999),
            (Affix("CRIT_DAMAGE_5", 1.0, [Flags.CRIT_DAMAGE, Flags.FLAT], 0.5, 1.5), 0.1, 75, 999),
        ],
        0.5,
        [Flags.WEAPON, Flags.OFFHAND, Flags.RING, Flags.AMULET]
    ),

    # ===== DEBUFF AFFIXES =====
    AffixDefinition(
        "debuff_res",
        [
            (Affix("DEBUFF_RES_1", 0.05, [Flags.BOON, Flags.DEBUFF_RES]), 1, 0, 999),
            (Affix("DEBUFF_RES_2", 0.1, [Flags.BOON, Flags.DEBUFF_RES]), 0.5, 25, 999),
            (Affix("DEBUFF_RES_3", 0.2, [Flags.BOON, Flags.DEBUFF_RES]), 0.1, 80, 999)
        ],
        0.1,
        [Flags.RING, Flags.AMULET, Flags.RELIC, Flags.HELM],
        {Flags.RING: 1, Flags.AMULET: 1.5, Flags.RELIC: 2.1, Flags.HELM: 2.1}
    ),

    AffixDefinition(
        "debuff_rte",
        [
            (Affix("DEBUFF_RTE_1", 0.1, [Flags.BOON, Flags.DEBUFF_RTE]), 1, 0, 999),
            (Affix("DEBUFF_RTE_2", 0.25, [Flags.BOON, Flags.DEBUFF_RTE]), 0.5, 25, 999),
            (Affix("DEBUFF_RTE_3", 0.5, [Flags.BOON, Flags.DEBUFF_RTE]), 0.1, 80, 999)
        ],
        0.4,
        [Flags.RING, Flags.AMULET, Flags.RELIC, Flags.HELM],
        {Flags.RING: 0.8, Flags.AMULET: 1.1, Flags.RELIC: 1.8, Flags.HELM: 2}
    ),

    AffixDefinition(
        "debuff_pot",
        [
            (Affix("DEBUFF_POT_1", 0.1, [Flags.BOON, Flags.DEBUFF_POT]), 1, 0, 999),
            (Affix("DEBUFF_POT_2", 0.25, [Flags.BOON, Flags.DEBUFF_POT]), 0.5, 25, 999),
            (Affix("DEBUFF_POT_3", 0.5, [Flags.BOON, Flags.DEBUFF_POT]), 0.1, 80, 999)
        ],
        0.7,
        [Flags.RING, Flags.AMULET, Flags.RELIC, Flags.HELM],
        {Flags.RING: 0.8, Flags.AMULET: 1.1, Flags.RELIC: 1.8, Flags.HELM: 2}
    ),

    AffixDefinition(
        "debuff_chance",
        [
            (Affix("DEBUFF_CHANCE_1", 0.1, [Flags.BOON, Flags.DEBUFF_CHANCE]), 1, 0, 999),
            (Affix("DEBUFF_CHANCE_2", 0.25, [Flags.BOON, Flags.DEBUFF_CHANCE]), 0.5, 25, 999),
            (Affix("DEBUFF_CHANCE_3", 0.5, [Flags.BOON, Flags.DEBUFF_CHANCE]), 0.1, 80, 999)
        ],
        0.5,
        [Flags.RING, Flags.AMULET, Flags.RELIC, Flags.HELM],
        {Flags.RING: 0.8, Flags.AMULET: 1.1, Flags.RELIC: 1.8, Flags.HELM: 2}
    ),

    # ===== RELIC-SPECIFIC AFFIXES =====
    AffixDefinition(
        "absolute_defense",
        [
            (Affix("ABS_DEF_1", 1, [Flags.ABS_DEF, Flags.FLAT]), 1, 0, 75),
            (Affix("ABS_DEF_2", 5, [Flags.ABS_DEF, Flags.FLAT]), 0.8, 20, 80),
            (Affix("ABS_DEF_3", 10, [Flags.ABS_DEF, Flags.FLAT]), 0.6, 40, 999),
        ],
        0.5,
        [Flags.RELIC]
    ),

    AffixDefinition(
        "item_quantity",
        [
            (Affix("IIQ_1", 0.3, [Flags.BOON, Flags.IIQ]), 1, 0, 60),
            (Affix("IIQ_2", 0.5, [Flags.BOON, Flags.IIQ]), 0.5, 25, 80),
            (Affix("IIQ_3", 0.8, [Flags.BOON, Flags.IIQ]), 0.1, 50, 999),
            (Affix("IIQ_4", 1.1, [Flags.BOON, Flags.IIQ]), 0.05, 50, 999),
            (Affix("IIQ_5", 1.5, [Flags.BOON, Flags.IIQ]), 0.01, 50, 999),
        ],
        0.8,
        [Flags.RELIC]
    ),

    AffixDefinition(
        "item_rarity",
        [
            (Affix("IIR_1", 0.2, [Flags.BOON, Flags.IIR]), 1, 0, 60),
            (Affix("IIR_2", 0.3, [Flags.BOON, Flags.IIR]), 0.5, 25, 80),
            (Affix("IIR_3", 0.4, [Flags.BOON, Flags.IIR]), 0.1, 50, 999),
            (Affix("IIR_4", 0.5, [Flags.BOON, Flags.IIR]), 0.05, 50, 999),
            (Affix("IIR_5", 1.0, [Flags.BOON, Flags.IIR]), 0.01, 50, 999),
        ],
        0.6,
        [Flags.RELIC]
    ),

    # ===== JEWEL-ONLY AFFIXES =====
    AffixDefinition(
        "damage_modifier",
        [
            (Affix("JEWEL_DAMAGE_1", 0.1, [Flags.BOON, Flags.DAMAGE_MOD]), 1, 0, 80),
            (Affix("JEWEL_DAMAGE_2", 0.2, [Flags.BOON, Flags.DAMAGE_MOD]), 0.8, 20, 90),
            (Affix("JEWEL_DAMAGE_3", 0.3, [Flags.BOON, Flags.DAMAGE_MOD]), 0.6, 40, 999),
            (Affix("JEWEL_DAMAGE_4", 0.4, [Flags.BOON, Flags.DAMAGE_MOD]), 0.25, 60, 999),
            (Affix("JEWEL_DAMAGE_5", 0.8, [Flags.BOON, Flags.DAMAGE_MOD]), 0.1, 80, 999),
        ],
        1.0,
        [Flags.JEWEL]
    ),

    AffixDefinition(
        "cooldown_reduction",
        [
            (Affix("JEWEL_CD_1", 0.1, [Flags.CURSE, Flags.COOLDOWN]), 1, 0, 80),
            (Affix("JEWEL_CD_2", 0.2, [Flags.CURSE, Flags.COOLDOWN]), 0.8, 20, 90),
            (Affix("JEWEL_CD_3", 0.3, [Flags.CURSE, Flags.COOLDOWN]), 0.6, 40, 999),
            (Affix("JEWEL_CD_4", 0.4, [Flags.CURSE, Flags.COOLDOWN]), 0.25, 60, 999),
        ],
        0.8,
        [Flags.JEWEL]
    ),

    AffixDefinition(
        "area_of_effect",
        [
            (Affix("JEWEL_AREA_1", 0.2, [Flags.BOON, Flags.AREA]), 1, 0, 80),
            (Affix("JEWEL_AREA_2", 0.4, [Flags.BOON, Flags.AREA]), 0.8, 20, 90),
            (Affix("JEWEL_AREA_3", 0.6, [Flags.BOON, Flags.AREA]), 0.6, 40, 999),
            (Affix("JEWEL_AREA_4", 0.8, [Flags.BOON, Flags.AREA]), 0.25, 60, 999),
            (Affix("JEWEL_AREA_5", 1.1, [Flags.BOON, Flags.AREA]), 0.1, 60, 999),
        ],
        0.8,
        [Flags.JEWEL]
    ),

    AffixDefinition(
        "projectile_count",
        [
            (Affix("JEWEL_PROJECTILE_1", 1, [Flags.FLAT, Flags.PROJECTILES, Flags.DESC_FLAT], 1, 1),
             1, 0, 80),
            (Affix("JEWEL_PROJECTILE_2", 2, [Flags.FLAT, Flags.PROJECTILES, Flags.DESC_FLAT], 1, 1),
             0.8, 20, 90),
            (Affix("JEWEL_PROJECTILE_3", 3, [Flags.FLAT, Flags.PROJECTILES, Flags.DESC_FLAT], 1, 1),
             0.6, 40, 999),
        ],
        0.01,
        [Flags.JEWEL]
    ),

    # ===== POTION-ONLY AFFIXES =====
    AffixDefinition(
        "life_potion_count",
        [
            (Affix("LIFE_COUNT_1", 1, [Flags.POT_HEAL_COUNT, Flags.FLAT, Flags.DESC_FLAT], 1, 2),
             1, 0, 999),
            (Affix("LIFE_COUNT_2", 1, [Flags.POT_HEAL_COUNT, Flags.FLAT, Flags.DESC_FLAT], 1, 3),
             25, 0, 999),
            (Affix("LIFE_COUNT_3", 1, [Flags.POT_HEAL_COUNT, Flags.FLAT, Flags.DESC_FLAT], 2, 5),
             50, 0, 999),
        ],
        0.2,
        [Flags.LIFE_POT]
    ),

    AffixDefinition(
        "life_potion_flat",
        [
            (Affix("LIFE_FLAT_1", 50, [Flags.POT_HEAL_FLAT, Flags.DESC_LIFE, Flags.FLAT,
                                Flags.DESC_HEAL_FLAT, Flags.DESC_FLAT], 0.5, 1.25), 1, 0, 70),
            (Affix("LIFE_FLAT_2", 150, [Flags.POT_HEAL_FLAT, Flags.DESC_LIFE, Flags.FLAT,
                                Flags.DESC_HEAL_FLAT, Flags.DESC_FLAT], 0.5, 1.25), 0.8, 0, 999),
            (Affix("LIFE_FLAT_3", 500, [Flags.POT_HEAL_FLAT, Flags.DESC_LIFE, Flags.FLAT,
                                Flags.DESC_HEAL_FLAT, Flags.DESC_FLAT], 0.5, 1.25), 0.5, 15, 999),
            (Affix("LIFE_FLAT_4", 1000, [Flags.POT_HEAL_FLAT, Flags.DESC_LIFE, Flags.FLAT,
                                Flags.DESC_HEAL_FLAT, Flags.DESC_FLAT], 0.5, 1.25), 0.3, 25, 999),
            (Affix("LIFE_FLAT_5", 2000, [Flags.POT_HEAL_FLAT, Flags.DESC_LIFE, Flags.FLAT,
                                Flags.DESC_HEAL_FLAT, Flags.DESC_FLAT], 0.5, 1.25), 0.1, 50, 999)
        ],
        1,
        [Flags.LIFE_POT]
    ),

    AffixDefinition(
        "life_potion_rela",
        [
            (Affix("LIFE_RELA_1", 0.04, [Flags.POT_HEAL_RELAT, Flags.DESC_LIFE, Flags.FLAT,
                                Flags.DESC_HEAL], 0.8, 1.3), 1, 0, 70),
            (Affix("LIFE_RELA_2", 0.04, [Flags.POT_HEAL_RELAT, Flags.DESC_LIFE, Flags.FLAT,
                                Flags.DESC_HEAL], 0.8, 1.3), 0.8, 0, 70),
            (Affix("LIFE_RELA_3", 0.04, [Flags.POT_HEAL_RELAT, Flags.DESC_LIFE, Flags.FLAT,
                                Flags.DESC_HEAL], 0.8, 1.3), 0.5, 15, 9999),
            (Affix("LIFE_RELA_4", 0.04, [Flags.POT_HEAL_RELAT, Flags.DESC_LIFE, Flags.FLAT,
                                Flags.DESC_HEAL], 0.8, 1.3), 0.3, 25, 999),
            (Affix("LIFE_RELA_5", 0.04, [Flags.POT_HEAL_RELAT, Flags.DESC_LIFE, Flags.FLAT,
                                Flags.DESC_HEAL], 0.8, 1.3), 0.1, 50, 999),
        ],
        0.6,
        [Flags.LIFE_POT]
    ),

    AffixDefinition(
        "mana_potion_count",
        [
            (Affix("MANA_COUNT_1", 1, [Flags.POT_MANA_COUNT, Flags.FLAT, Flags.DESC_FLAT], 1, 2),
             1, 0, 999),
            (Affix("MANA_COUNT_2", 1, [Flags.POT_MANA_COUNT, Flags.FLAT, Flags.DESC_FLAT], 1, 3),
             25, 0, 999),
            (Affix("MANA_COUNT_3", 1, [Flags.POT_MANA_COUNT, Flags.FLAT, Flags.DESC_FLAT], 2, 5),
             50, 0, 999),
        ],
        0.2,
        [Flags.MANA_POT]
    ),

    AffixDefinition(
        "life_mana_flat",
        [
            (Affix("MANA_FLAT_1", 20, [Flags.POT_MANA_FLAT, Flags.DESC_MANA, Flags.FLAT,
                                Flags.DESC_HEAL_FLAT, Flags.DESC_FLAT], 0.5, 1.25), 1, 0, 70),
            (Affix("MANA_FLAT_2", 70, [Flags.POT_MANA_FLAT, Flags.DESC_MANA, Flags.FLAT,
                                Flags.DESC_HEAL_FLAT, Flags.DESC_FLAT], 0.5, 1.25), 0.8, 0, 999),
            (Affix("MANA_FLAT_3", 110, [Flags.POT_MANA_FLAT, Flags.DESC_MANA, Flags.FLAT,
                                Flags.DESC_HEAL_FLAT, Flags.DESC_FLAT], 0.5, 1.25), 0.5, 15, 999),
            (Affix("MANA_FLAT_4", 200, [Flags.POT_MANA_FLAT, Flags.DESC_MANA, Flags.FLAT,
                                Flags.DESC_HEAL_FLAT, Flags.DESC_FLAT], 0.5, 1.25), 0.3, 25, 999),
            (Affix("MANA_FLAT_5", 500, [Flags.POT_MANA_FLAT, Flags.DESC_MANA, Flags.FLAT,
                                Flags.DESC_HEAL_FLAT, Flags.DESC_FLAT], 0.5, 1.25), 0.1, 50, 999)
        ],
        1,
        [Flags.MANA_POT]
    ),

    AffixDefinition(
        "mana_potion_rela",
        [
            (Affix("MANA_RELA_1", 0.04, [Flags.POT_MANA_RELAT, Flags.DESC_LIFE, Flags.FLAT,
                                Flags.DESC_MANA, Flags.DESC_HEAL], 0.8, 1.3), 1, 0, 70),
            (Affix("MANA_RELA_2", 0.04, [Flags.POT_MANA_RELAT, Flags.DESC_LIFE, Flags.FLAT,
                                Flags.DESC_MANA, Flags.DESC_HEAL], 0.8, 1.3), 0.8, 0, 70),
            (Affix("MANA_RELA_3", 0.04, [Flags.POT_MANA_RELAT, Flags.DESC_LIFE, Flags.FLAT,
                                Flags.DESC_MANA, Flags.DESC_HEAL], 0.8, 1.3), 0.5, 15, 9999),
            (Affix("MANA_RELA_4", 0.04, [Flags.POT_MANA_RELAT, Flags.DESC_LIFE, Flags.FLAT,
                                Flags.DESC_MANA, Flags.DESC_HEAL], 0.8, 1.3), 0.3, 25, 999),
            (Affix("MANA_RELA_5", 0.04, [Flags.POT_MANA_RELAT, Flags.DESC_LIFE, Flags.FLAT,
                                Flags.DESC_MANA, Flags.DESC_HEAL], 0.8, 1.3), 0.1, 50, 999),
        ],
        0.6,
        [Flags.MANA_POT]
    ),

]

def get_affixes_for_slot(slot_flag: Flags, item_level: int) -> dict:
    """
    Get all applicable affixes for a given gear slot.
    
    Args:
        slot_flag: The gear slot flag (e.g., Flags.ARMOR, Flags.WEAPON)
        item_level: The level of the item being generated
    
    Returns:
        Dictionary mapping affix_id to (tiers, adjusted_weight)
    """
    result = {}
    for affix_def in AFFIX_POOL:
        if slot_flag not in affix_def.allowed_slots:
            continue
        if slot_flag in affix_def.value_multipliers:
            slot_multiplier = affix_def.value_multipliers[slot_flag]
        else:
            slot_multiplier = SLOT_MULTIPLIERS.get(slot_flag, 1.0)
        valid_tiers = []
        for (affix, weight, min_lvl, max_lvl) in affix_def.tiers:
            if min_lvl <= item_level <= max_lvl:
                scaled_affix = _scale_affix(affix, slot_multiplier)
                valid_tiers.append((scaled_affix, weight, min_lvl, max_lvl))
        if valid_tiers:
            result[affix_def.affix_id] = (valid_tiers, affix_def.base_weight)
    return result

def _scale_affix(affix, multiplier: float):
    """
    Scale an affix's values by the given multiplier.
    
    Args:
        affix: The affix to scale (Affix or DoubleAffix)
        multiplier: The scaling factor
    
    Returns:
        A scaled copy of the affix
    """
    scaled = affix.copy()
    if isinstance(scaled, Affix):
        scaled._value *= multiplier
        scaled.bounds = (
            scaled.bounds[0] * multiplier,
            scaled.bounds[1] * multiplier
        )
    elif isinstance(scaled, DoubleAffix):
        scaled._value_min *= multiplier
        scaled._value_max *= multiplier
        scaled.bounds_min = (
            scaled.bounds_min[0] * multiplier,
            scaled.bounds_min[1] * multiplier
        )
        scaled.bounds_max = (
            scaled.bounds_max[0] * multiplier,
            scaled.bounds_max[1] * multiplier
        )
    return scaled
