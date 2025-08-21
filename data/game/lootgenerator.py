"""Generates random loot."""

import numpy
import random
from data.item import Item
from data.constants import SYSTEM, Flags
from data.tables.affix_table import AFFIXES
from data.tables.implicits_table import IMPLICITS

RUNE_WEIGHT = [100, 80, 70, 50, 40, 30, 25, 5, 2, 1]
RUNES = [0, 7, 9, 8, 6, 1, 2, 3, 5, 4]
RUNE_LUCK = [-2, -1.8, -1.5, -1.3, 0, 0, 1.3, 1.15, 1.1, 1.05]

RARITY_WEIGHTS = [100,80,20,3,1]
RARITIES = [0,1,2,3,4]
RARITY_LUCK = [-2, -1.5, 1.3, 1.05, 1.01]

LOOT_WEIGHT = [30,50,80,70,8]
LOOT_VALUES = ["item", "gold", "mana", "life", "rune"]
LOOT_LUCK = [1.3, 0, -1.3, -1.3, 1.2]

WEIGHTS_RUNE = sum(RUNE_WEIGHT)
WEIGHTS_LOOT = sum(LOOT_WEIGHT)
WEIGHTS_RARE = sum(RARITY_WEIGHTS)

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

    def generate_affixes(self, item_type: str, num_affixes: int, item_level: int, already_exists = None):
        affix_pool = AFFIXES[item_type]
        existing_keys = set()
        if already_exists is not None:
                existing_keys = {affix.name for affix in already_exists}
        # Step 1: Build list of usable affixes with their valid tiers
        candidates = []
        for affix_key, (tiers, affix_weight) in affix_pool.items():
            if affix_key in existing_keys:
                continue
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

    def generate_item(self, level, rarity):
        """Generates a random armor."""
        match rarity:
            case 1:
                affx = numpy.random.randint(1, 2)
            case 2:
                affx = numpy.random.randint(3, 6)
            case 3:
                affx = numpy.random.randint(7, 8)
            case _:
                affx = 0
        item_type = numpy.random.randint(0, 9)
        match item_type:
            case 1:
                affixes = [a.roll() for a in self.generate_affixes("helms", affx, level)]
                it = self.select_base(self._helms).copy()
            case 2:
                affixes = [a.roll() for a in self.generate_affixes("boots", affx, level)]
                it = self.select_base(self._boots).copy()
            case 3:
                affixes = [a.roll() for a in self.generate_affixes("gloves", affx, level)]
                it = self.select_base(self._gloves).copy()
            case 4:
                affixes = [a.roll() for a in self.generate_affixes("amulets", affx, level)]
                it = self.select_base(self._amulets).copy()
            case 5:
                affixes = [a.roll() for a in self.generate_affixes("rings", affx, level)]
                it = self.select_base(self._rings).copy()
            case 6:
                affixes = [a.roll() for a in self.generate_affixes("relics", affx, level)]
                it = self.select_base(self._relics).copy()
            case 7:
                affixes = [a.roll() for a in self.generate_affixes("weapons", affx, level)]
                it = self.select_base(self._weapons).copy()
            case 8:
                affixes = [a.roll() for a in self.generate_affixes("offhands", affx, level)]
                it = self.select_base(self._offhands).copy()
            case 9:
                affixes = [a.roll() for a in self.generate_affixes("belts", affx, level)]
                it = self.select_base(self._belts).copy()
            case _:
                affixes = [a.roll() for a in self.generate_affixes("armors", affx, level)]
                it = self.select_base(self._armors).copy()
        implicits = []
        for implicit in it.implicits:
            implicits.append(implicit.roll())
        it.implicits = implicits
        it.affixes.extend(affixes)
        it.level = level
        it.rarity = rarity
        it.update()
        return it.stamp

    def compute_adjusted_weights(self, base_weights, rarity):
        adjusted = []
        for i, weight in enumerate(base_weights):
                exponent = 1.0 - SYSTEM["player"].creature.stats["item_qual"].get_value() * 0.15
                exponent = max(0.1, exponent)
                adjusted_weight = (weight ** exponent) * rarity 
                adjusted.append(adjusted_weight)
        return adjusted

    def roll(self, quantity: int, level: int, rarity: int = 1):
        """Rolls a certain amount of items."""
        quant = quantity * (1 + SYSTEM["player"].creature.stats["item_quant"].get_value())
        level_roll = min(max(level + numpy.random.randint(-3, 5), 1), 100)
        loot = []
        base_weights = [100, 80, 20, 3]
        for _ in range(int(quant)):
            weight = self.compute_adjusted_weights(base_weights, rarity)
            rarities = [0, 1, 2, 3]
            roll = random.choices(rarities, weights=weight, k=1)[0]
            loot.append(self.generate_item(level_roll, roll))
        return loot

    def factor_luck(self, luck):
            """Rebuilds the weight tables using the luck factors."""
            factor = {
                "runes": RUNE_WEIGHT.copy(),
                "rune_weight": 0,
                "loot": LOOT_WEIGHT.copy(),
                "loot_weight": 0,
                "rarity": RARITY_WEIGHTS.copy(),
                "rarity_weight": 0
            }
            for f in factor["runes"]:
                if f == 0:
                    continue
                elif f < 0:
                    factor["runes"]  
            return factor

    def enemy_drop(self, enemy):
        """Handles enemy loot process."""
        loot = {
            "gold": 0,
            "mana": [],
            "life": [],
            "items": [],
            "runes": []
        }
        luck = SYSTEM["player"].creature.stats["item_qual"].c_value + 1
        rarity = enemy.tier
        amount = max(rarity * numpy.random.randint(-2, 6) *\
                (SYSTEM["player"].creature.stats["item_quant"].c_value + 1), 0)
        while amount > 0:
            choice = numpy.random.choice(LOOT_VALUES, p=[d / WEIGHTS_LOOT for d in LOOT_WEIGHT])
            match choice:
                case "item":
                    roll = numpy.random.choice(RARITIES, p=[d / WEIGHTS_RARE for d in RARITY_WEIGHTS])
                    level = round(enemy.creature.level * (0.7 + numpy.random.rand()))
                    loot["items"].append(self.generate_item(level, roll))
                case "mana":
                    roll = numpy.random.randint(1, 6)
                    loot["mana"].append(roll)
                case "life":
                    roll = numpy.random.randint(1, 6)
                    loot["life"].append(roll)
                case "rune":
                    roll = numpy.random.choice(RUNES, p=[d / WEIGHTS_RUNE for d in RUNE_WEIGHT])
                    loot["runes"].append(roll)
                case _: #gold
                    gold = enemy.gold_value * (0.7 + numpy.random.rand()) *\
                        (SYSTEM["player"].creature.stats["item_quant"].c_value + 1)
                    loot["gold"] += gold
            amount -= 1
        return loot
