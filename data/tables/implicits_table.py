"""Table for implicits. Surely there's a better way to store
them that that"""

from data.constants import Flags
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