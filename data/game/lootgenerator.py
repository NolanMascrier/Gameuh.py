"""Generates random loot."""

import random
import numpy
from data.item import Item
from data.constants import SYSTEM, Flags
from data.tables.implicits_table import IMPLICITS
from data.tables.affix_table import get_affixes_for_slot

RUNE_WEIGHT = [100, 80, 70, 50, 40, 30, 25, 5, 2, 1]
RUNES = [0, 7, 9, 8, 6, 1, 2, 3, 5, 4]
RUNE_LUCK = [0.9, 0.7, 0.8, 0.85, 1, 1, 1.2, 2, 2.5, 3]

RARITY_WEIGHTS = [100, 80, 20, 3, 1]
RARITIES = [0,1,2,3,4]
RARITY_LUCK = [0.7, 0.9, 1.85, 3, 3]

LOOT_WEIGHT = [10, 90, 80, 70, 8]
LOOT_VALUES = ["item", "gold", "mana", "life", "rune"]
LOOT_LUCK = [1.8, 1.1, 0.8, 0.7, 1.5]

WEIGHTS_RUNE = sum(RUNE_WEIGHT)
WEIGHTS_LOOT = sum(LOOT_WEIGHT)
WEIGHTS_RARE = sum(RARITY_WEIGHTS)

def diminishing_multiplier(factor: float, luck: float) -> float:
    """Compute the luck multiplier for a single weight."""
    if luck <= 2:
        return 1 + (luck - 1) * (factor - 1)
    return 1 + (factor - 1) * (2 - 2 ** (-(luck - 2)))

def apply_luck(weights, luck_factors, luck_value):
    """Applies the luck factor and returns the computed weights."""
    adjusted = []
    for base, factor in zip(weights, luck_factors):
        multiplier = diminishing_multiplier(factor, luck_value)
        adjusted.append(numpy.ceil(base * multiplier))
    return numpy.array(adjusted)

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
                    0, [Flags.ARMOR, Flags.GEAR], implicits=[IMPLICITS["armor_mom"],\
                                                                IMPLICITS["robes"]]), 1),
                (Item("", "Gown", 25, 0, 1, SYSTEM["images"]["armors"][31],\
                    0, [Flags.ARMOR, Flags.GEAR], implicits=[IMPLICITS["armor_mom"],\
                                                                IMPLICITS["gown"]]), 0.8),
                (Item("", "Mage coat", 100, 0, 1, SYSTEM["images"]["armors"][3],\
                    0, [Flags.ARMOR, Flags.GEAR], implicits=[IMPLICITS["armor_mom"],\
                                                                IMPLICITS["mage_coat"]]), 0.6),
                (Item("", "Arcane robes", 500, 0, 1, SYSTEM["images"]["armors"][30],\
                    0, [Flags.ARMOR, Flags.GEAR], implicits=[IMPLICITS["armor_mom"],\
                                                                IMPLICITS["arcane_robes"]]), 0.5),
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
                    0, [Flags.WEAPON, Flags.GEAR], implicits=[IMPLICITS["weapon1"]]), 1),
            (Item("", "Rogue's bow", 250, 0, 1, SYSTEM["images"]["weapons"][20],\
                    0, [Flags.WEAPON, Flags.GEAR], implicits=[IMPLICITS["weapon2"]]), 0.5),
            (Item("", "Steel bow", 250, 0, 1, SYSTEM["images"]["weapons"][7],\
                    0, [Flags.WEAPON, Flags.GEAR], implicits=[IMPLICITS["weapon3"]]), 0.1),

            (Item("", "Staff", 250, 0, 1, SYSTEM["images"]["weapons"][9],\
                    0, [Flags.WEAPON, Flags.GEAR], implicits=[IMPLICITS["weapon1"]]), 1),
            (Item("", "Scepter", 250, 0, 1, SYSTEM["images"]["weapons"][16],\
                    0, [Flags.WEAPON, Flags.GEAR], implicits=[IMPLICITS["weapon2"]]), 0.5),
            (Item("", "Grand cane", 250, 0, 1, SYSTEM["images"]["weapons"][19],\
                    0, [Flags.WEAPON, Flags.GEAR], implicits=[IMPLICITS["weapon3"]]), 0.1),

            (Item("", "Sword", 250, 0, 1, SYSTEM["images"]["weapons"][1],\
                    0, [Flags.WEAPON, Flags.GEAR], implicits=[IMPLICITS["weapon2"]]), 1),
            (Item("", "Saber", 250, 0, 1, SYSTEM["images"]["weapons"][8],\
                    0, [Flags.WEAPON, Flags.GEAR], implicits=[IMPLICITS["weapon3"]]), 0.5),
            (Item("", "Enchanted blade", 250, 0, 1, SYSTEM["images"]["weapons"][10],\
                    0, [Flags.WEAPON, Flags.GEAR], implicits=[IMPLICITS["weapon4"]]), 0.1),

            (Item("", "Axe", 250, 0, 1, SYSTEM["images"]["weapons"][12],\
                    0, [Flags.WEAPON, Flags.GEAR], implicits=[IMPLICITS["weapon2"]]), 1),
            (Item("", "Mace", 250, 0, 1, SYSTEM["images"]["weapons"][13],\
                    0, [Flags.WEAPON, Flags.GEAR], implicits=[IMPLICITS["weapon3"]]), 0.5),
            (Item("", "Scourge", 250, 0, 1, SYSTEM["images"]["weapons"][14],\
                    0, [Flags.WEAPON, Flags.GEAR], implicits=[IMPLICITS["weapon4"]]), 0.1),

            (Item("", "Crossbow", 250, 0, 1, SYSTEM["images"]["weapons"][3],\
                    0, [Flags.WEAPON, Flags.GEAR], implicits=[IMPLICITS["weapon1"]]), 0.05),
            (Item("", "Shuriken", 250, 0, 1, SYSTEM["images"]["weapons"][5],\
                    0, [Flags.WEAPON, Flags.GEAR], implicits=[IMPLICITS["weapon1"]]), 0.01),
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
        self._belts = [
            (Item("", "Iron Belt", 250, 0, 1, SYSTEM["images"]["belts"][0],\
                    0, [Flags.BELT, Flags.GEAR], implicits=[]), 1),
            (Item("", "Barbed belt", 250, 0, 1, SYSTEM["images"]["belts"][1],\
                    0, [Flags.BELT, Flags.GEAR], implicits=[]), 1),
            (Item("", "Gi belt", 250, 0, 1, SYSTEM["images"]["belts"][2],\
                    0, [Flags.BELT, Flags.GEAR], implicits=[]), 1),
            (Item("", "Mage belt", 250, 0, 1, SYSTEM["images"]["belts"][3],\
                    0, [Flags.BELT, Flags.GEAR], implicits=[]), 1),
        ]
        self._jewels = [
            (Item("", "Mind Jewel", 500, 0, 1, SYSTEM["images"]["jewels"][0],\
                  0, [Flags.JEWEL]), 1),
            (Item("", "Wit Jewel", 500, 0, 1, SYSTEM["images"]["jewels"][1],\
                  0, [Flags.JEWEL]), 1),
            (Item("", "Might Jewel", 500, 0, 1, SYSTEM["images"]["jewels"][2],\
                  0, [Flags.JEWEL]), 1)
        ]
        self._lifepots = [
            (Item("", "Life Extract", 100, 0, 1, SYSTEM["images"]["life"][0],\
                  0, [Flags.LIFE_POT, Flags.GEAR], implicits=[IMPLICITS["life_pot_count"],
                  IMPLICITS["life_pot_heal_1_a"], IMPLICITS["life_pot_heal_1_b"]]), 1),
            (Item("", "Life Flask", 100, 0, 1, SYSTEM["images"]["life"][1],\
                  0, [Flags.LIFE_POT, Flags.GEAR], implicits=[IMPLICITS["life_pot_count"]]), 10),
            (Item("", "Life Potion", 100, 0, 1, SYSTEM["images"]["life"][2],\
                  0, [Flags.LIFE_POT, Flags.GEAR], implicits=[IMPLICITS["life_pot_count"]]), 15),
            (Item("", "Large Life Potion", 100, 0, 1, SYSTEM["images"]["life"][3],\
                  0, [Flags.LIFE_POT, Flags.GEAR], implicits=[IMPLICITS["life_pot_count"]]), 25),
            (Item("", "Life Decoction", 100, 0, 1, SYSTEM["images"]["life"][4],\
                  0, [Flags.LIFE_POT, Flags.GEAR], implicits=[IMPLICITS["life_pot_count_2"]]), 35),
            (Item("", "Strong Life Decoction", 100, 0, 1, SYSTEM["images"]["life"][5],\
                  0, [Flags.LIFE_POT, Flags.GEAR], implicits=[IMPLICITS["life_pot_count_2"]]), 50),
            (Item("", "Life Elixir", 100, 0, 1, SYSTEM["images"]["life"][6],\
                  0, [Flags.LIFE_POT, Flags.GEAR], implicits=[IMPLICITS["life_pot_count"]]), 70),
        ]
        self._manapots = [
            (Item("", "Mana Extract", 100, 0, 1, SYSTEM["images"]["mana"][0],\
                  0, [Flags.MANA_POT, Flags.GEAR], implicits=[IMPLICITS["mana_pot_count"],
                  IMPLICITS["life_pot_mana_1_a"], IMPLICITS["life_pot_mana_1_b"]]), 1),
            (Item("", "Mana Flask", 100, 0, 1, SYSTEM["images"]["mana"][1],\
                  0, [Flags.MANA_POT, Flags.GEAR], implicits=[IMPLICITS["mana_pot_count"]]), 10),
            (Item("", "Mana Potion", 100, 0, 1, SYSTEM["images"]["mana"][2],\
                  0, [Flags.MANA_POT, Flags.GEAR], implicits=[IMPLICITS["mana_pot_count"]]), 15),
            (Item("", "Large Mana Potion", 100, 0, 1, SYSTEM["images"]["mana"][3],\
                  0, [Flags.MANA_POT, Flags.GEAR], implicits=[IMPLICITS["mana_pot_count"]]), 25),
            (Item("", "Mana Decoction", 100, 0, 1, SYSTEM["images"]["mana"][4],\
                  0, [Flags.MANA_POT, Flags.GEAR], implicits=[IMPLICITS["mana_pot_count_2"]]), 35),
            (Item("", "Strong Mana Decoction", 100, 0, 1, SYSTEM["images"]["mana"][5],\
                  0, [Flags.MANA_POT, Flags.GEAR], implicits=[IMPLICITS["mana_pot_count_2"]]), 50),
            (Item("", "Mana Elixir", 100, 0, 1, SYSTEM["images"]["mana"][6],\
                  0, [Flags.MANA_POT, Flags.GEAR], implicits=[IMPLICITS["mana_pot_count"]]), 70),
        ]
        self._slot_mapping = {
            0: Flags.ARMOR,
            1: Flags.HELM,
            2: Flags.BOOTS,
            3: Flags.HANDS,
            4: Flags.AMULET,
            5: Flags.RING,
            6: Flags.RELIC,
            7: Flags.WEAPON,
            8: Flags.OFFHAND,
            9: Flags.BELT,
            10: Flags.JEWEL,
            11: Flags.LIFE_POT,
            12: Flags.MANA_POT
        }

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

    def generate_affixes(self, item_type: int, num_affixes: int,
                         item_level: int, already_exists = None):
        """Generates a list of affixes for the item."""
        slot_flag = self._slot_mapping.get(item_type, Flags.ARMOR)
        affix_pool = get_affixes_for_slot(slot_flag, item_level)
        existing_keys = set()
        if already_exists is not None:
            existing_keys = {self._extract_affix_id(affix.name) for affix in already_exists}
        candidates = []
        for affix_key, (tiers, affix_weight) in affix_pool.items():
            if affix_key in existing_keys:
                continue
            valid_tiers = [(affix, weight) for (affix, weight, _, _) in tiers]
            if valid_tiers:
                candidates.append(((valid_tiers, affix_key), affix_weight))
        if num_affixes > len(candidates):
            num_affixes = len(candidates)
            if num_affixes == 0:
                return []
        chosen_affix_groups = self.weighted_sample_without_replacement(
            candidates, num_affixes)
        result_affixes = [
            self.pick_weighted(valid_tiers)
            for valid_tiers, _ in chosen_affix_groups
        ]
        return result_affixes

    def _extract_affix_id(self, affix_name: str) -> str:
        """
        Extract the base affix identifier from an affix name.
        E.g., "STR_1" -> "strength", "PHYS_DMG_3" -> "physical_damage_increased"
        
        This is a simple heuristic - you may need to adjust based on your naming scheme.
        """
        return affix_name[:-1]

    def select_base(self, types: list, is_leveled = False, level = 0):
        """Selects a random base of the type."""
        if is_leveled:
            choice = []
            for item, lvl in types:
                if lvl <= level:
                    choice.append(item)
            return random.choice(choice)
        else:
            max_weight = 0
            for _, weight in types:
                max_weight += float(weight)
            roll = random.uniform(0, max_weight)
            cress = 0
            for item, weight in types:
                cress += float(weight)
                if cress >= roll:
                    return item
        return None

    def generate_item(self, level, rarity):
        """Generates a random armor."""
        item_type = numpy.random.randint(0, 13)
        if item_type == 11 or item_type == 12:
            rarity = numpy.random.randint(0, 2)
        match rarity:
            case 1:
                if item_type == 10:
                    affx = 1
                else:
                    affx = numpy.random.randint(1, 3)
            case 2:
                if item_type == 10:
                    affx = 2
                else:
                    affx = numpy.random.randint(3, 6)
            case 3:
                if item_type == 10:
                    affx = numpy.random.randint(3, 4)
                else:
                    affx = numpy.random.randint(7, 9)
            case _:
                affx = 0
        match item_type:
            case 1:
                it = self.select_base(self._helms).copy()
            case 2:
                it = self.select_base(self._boots).copy()
            case 3:
                it = self.select_base(self._gloves).copy()
            case 4:
                it = self.select_base(self._amulets).copy()
            case 5:
                it = self.select_base(self._rings).copy()
            case 6:
                it = self.select_base(self._relics).copy()
            case 7:
                it = self.select_base(self._weapons).copy()
            case 8:
                it = self.select_base(self._offhands).copy()
            case 9:
                it = self.select_base(self._belts).copy()
            case 10:
                it = self.select_base(self._jewels).copy()
            case 11:
                it = self.select_base(self._lifepots, True, level).copy()
            case 12:
                it = self.select_base(self._manapots, True, level).copy()
            case _:
                it = self.select_base(self._armors).copy()
        affixes = [a.roll() for a in self.generate_affixes(item_type, affx, level)]
        implicits = []
        for implicit in it.implicits:
            implicits.append(implicit.roll())
        it.implicits = implicits
        it.affixes.extend(affixes)
        it.level = level
        it.rarity = rarity
        it.update()
        return it.stamp

    def enemy_drop(self, enemy):
        """Handles enemy loot process."""
        loot = {
            "gold": 0,
            "mana": [],
            "life": [],
            "items": set(),
            "runes": []
        }
        luck = SYSTEM["player"].creature.stats["item_qual"].c_value +\
            enemy.creature.stats["item_qual"].c_value
        adjusted_loot = apply_luck(LOOT_WEIGHT, LOOT_LUCK, luck)
        adjusted_rare = apply_luck(RARITY_WEIGHTS, RARITY_LUCK, luck)
        adjusted_rune = apply_luck(RUNE_WEIGHT, RUNE_LUCK, luck)
        loot_sum = sum(adjusted_loot)
        rare_sum = sum(adjusted_rare)
        rune_sum = sum(adjusted_rune)
        rarity = enemy.tier
        amount = max(rarity * numpy.random.randint(-2, 6) *\
                (SYSTEM["player"].creature.stats["item_quant"].c_value +\
                enemy.creature.stats["item_quant"].c_value), 0)
        while amount > 0:
            choice = numpy.random.choice(LOOT_VALUES, p=[d / loot_sum for d in adjusted_loot])
            match choice:
                case "item":
                    roll = numpy.random.choice(RARITIES, p=[d / rare_sum for d in adjusted_rare])
                    level = round(enemy.creature.level * (0.7 + numpy.random.rand()))
                    loot["items"].add(self.generate_item(level, roll))
                case "mana":
                    roll = numpy.random.randint(1, 6)
                    loot["mana"].append(roll)
                case "life":
                    roll = numpy.random.randint(1, 6)
                    loot["life"].append(roll)
                case "rune":
                    roll = numpy.random.choice(RUNES, p=[d / rune_sum for d in adjusted_rune])
                    loot["runes"].append(roll)
                case _: #gold
                    gold = enemy.gold_value * (0.7 + numpy.random.rand()) *\
                        (SYSTEM["player"].creature.stats["item_quant"].c_value +\
                        enemy.creature.stats["item_quant"].c_value)
                    loot["gold"] += gold
            amount -= 1
        return loot
