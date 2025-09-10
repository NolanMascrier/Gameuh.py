"""Tables of unique items."""

from data.item import Item
from data.constants import SYSTEM, Flags
from data.numerics.affix import Affix

#Format: Item, weight, min lvl

UNIQUE_AFFIXES = {
    "coc_jewel": Affix("trigger_on_crit", 1,\
        [Flags.DESC_UNIQUE, Flags.TRIGGER, Flags.TRIGGER_ON_CRIT]),
    "weight_jewel": [Affix("weight_0", 5, [Flags.DAMAGE_MOD, Flags.BLESS]),
    Affix("weight_1", 5, [Flags.MANA_COST, Flags.BLESS]),
    Affix("weight_2", 5, [Flags.LIFE_COST, Flags.BLESS]),
    Affix("weight_3", 3, [Flags.AREA, Flags.BLESS]),]
}

UNIQUES = []

def load_uniques():
    """Loads up all unique items."""
    UNIQUES.extend([
        (Item("coc_jewel", "Spirit Jewel", 3500, 0, 0, SYSTEM["images"]["jewels"][3], 4,\
            [Flags.JEWEL, Flags.TRIGGER, Flags.TRIGGER_ON_CRIT], [UNIQUE_AFFIXES["coc_jewel"]]), 10, 0),
        (Item("weight_jewel", "Might Jewel", 3500, 0, 0, SYSTEM["images"]["jewels"][4], 4,\
            [Flags.JEWEL, Flags.TRIGGER, Flags.TRIGGER_ON_CRIT], UNIQUE_AFFIXES["weight_jewel"]), 10, 0)
    ])
