"""Handles the gear tab."""

from data.interface.general import draw_bottom_bar, setup_bottom_bar
from data.constants import SYSTEM, MENU_GEAR, Flags, SCREEN_HEIGHT, SCREEN_WIDTH
from data.image.slotpanel import SlotPanel
from data.item import Item
from data.image.slot import Slot
from data.image.tabs import Tabs
from data.interface.render import render, renders

STAT_LIST = {}
DEFAULT_STATS = ["life", "mana", "int", "str", "dex"]
DEFENSE_STATS = ["def", "abs_def", "block", "dodge_rating", "crit_res"\
    "phys", "fire", "ice", "elec", "energy", "light", "dark", "heal_factor"]
OFFENSE_STATS = ["crit_rate", "crit_dmg", "mana_efficiency", "cast_speed",
    "melee_dmg", "spell_dmg", "ranged_dmg", "precision", "phys_dmg", "fire_dmg",
    "ice_dmg", "elec_dmg", "energy_dmg", "light_dmg", "dark_dmg"]
OTHER_STATS = ["exp_mult", "item_quant", "item_qual", "speed", "proj_quant", "proj_speed", "chains"]
STATES = ["defenses", "damages", "other"]

def equip(item: Item, slot: Slot):
    """Equips an item on the player character."""
    if item is None:
        return
    if slot.flag not in item.flags:
        SYSTEM["gear_panel"].insert(slot.contains)
        slot.remove()
    else:
        SYSTEM["player"].creature.equip(slot.flag, item, slot.left)
        SYSTEM["player"].inventory.remove(item)
    lst = SYSTEM["player"].creature.generate_stat_details(True)
    for f in lst:
        STAT_LIST[f] = lst[f]

def overwrite_gear(item: Item, slot: Slot):
    """Overwrites the item in the slot."""
    if item is None:
        return
    it = SYSTEM["player"].creature.unequip(slot.flag, slot.left)
    if it is not None:
        SYSTEM["player"].inventory.append(it)
        SYSTEM["gear_panel"].insert(None, None, it)
    lst = SYSTEM["player"].creature.generate_stat_details(True)
    for f in lst:
        STAT_LIST[f] = lst[f]

def unequip(item: Item, slot: Slot):
    """Removes the equiped item from the slot."""
    if item is None:
        return
    it = SYSTEM["player"].creature.unequip(slot.flag, slot.left)
    if it is not None:
        SYSTEM["player"].inventory.append(it)
    lst = SYSTEM["player"].creature.generate_stat_details(True)
    for f in lst:
        STAT_LIST[f] = lst[f]

def open_gear_screen():
    """Sets up the gear screen."""
    SYSTEM["game_state"] = MENU_GEAR
    setup_bottom_bar()
    SYSTEM["gear_tab"] = STATES[0]
    SYSTEM["gear_tabs"] = Tabs(15, 200, STATES, STATES, "gear_tab")
    x = SCREEN_WIDTH / 2- 32
    y = SCREEN_HEIGHT / 2 - 128
    SYSTEM["ui"]["gear_helm"] = Slot(x, y - 32, "gear_helm", equip, unequip, overwrite_gear,\
         Flags.HELM, SYSTEM["player"].creature.gear["helms"])
    SYSTEM["ui"]["gear_amulet"] = Slot(x, y + 32, "gear_amulet", equip, unequip, overwrite_gear,\
         Flags.AMULET, SYSTEM["player"].creature.gear["amulets"])
    SYSTEM["ui"]["gear_armor"] = Slot(x, y + 96, "gear_armor", equip, unequip, overwrite_gear,\
         Flags.ARMOR, SYSTEM["player"].creature.gear["armors"])
    SYSTEM["ui"]["gear_weapon"] = Slot(x - 128, y + 96, "gear_weapon", equip, unequip, overwrite_gear,\
         Flags.WEAPON, SYSTEM["player"].creature.gear["weapons"])
    SYSTEM["ui"]["gear_ring"] = Slot(x - 64, y + 64, "gear_ring", equip, unequip, overwrite_gear,\
         Flags.RING, SYSTEM["player"].creature.gear["rings"]["left"], True)
    SYSTEM["ui"]["gear_ring2"] = Slot(x + 64, y + 64, "gear_ring", equip, unequip, overwrite_gear,\
         Flags.RING, SYSTEM["player"].creature.gear["rings"]["right"])
    SYSTEM["ui"]["gear_offhand"] = Slot(x + 128, y + 96, "gear_offhand", equip, unequip, overwrite_gear,\
         Flags.OFFHAND, SYSTEM["player"].creature.gear["offhand"])
    SYSTEM["ui"]["gear_hands"] = Slot(x + 64, y + 128, "gear_hands", equip, unequip, overwrite_gear,\
         Flags.HANDS, SYSTEM["player"].creature.gear["gloves"])
    SYSTEM["ui"]["gear_relic"] = Slot(x - 64, y + 128, "gear_relic", equip, unequip, overwrite_gear,\
         Flags.RELIC, SYSTEM["player"].creature.gear["relics"])
    SYSTEM["ui"]["gear_belt"] = Slot(x, y + 174, "gear_belt", equip, unequip, overwrite_gear,\
         Flags.BELT, SYSTEM["player"].creature.gear["belts"])
    SYSTEM["ui"]["gear_boots"] = Slot(x, y + 238, "gear_boots", equip, unequip, overwrite_gear,\
         Flags.BOOTS, SYSTEM["player"].creature.gear["boots"])
    SYSTEM["gear_panel"] = SlotPanel(SCREEN_WIDTH - 535, 10, default=SYSTEM["player"].inventory)
    lst = SYSTEM["player"].creature.generate_stat_details()
    for f in lst:
        STAT_LIST[f] = lst[f]

def unloader():
    """Unloads all gear-specific data."""
    SYSTEM["gear_tabs"] = None
    SYSTEM["ui"]["gear_helm"] = None
    SYSTEM["ui"]["gear_amulet"] = None
    SYSTEM["ui"]["gear_armor"] = None
    SYSTEM["ui"]["gear_weapon"] = None
    SYSTEM["ui"]["gear_ring"] = None
    SYSTEM["ui"]["gear_ring2"] = None
    SYSTEM["ui"]["gear_offhand"] = None
    SYSTEM["ui"]["gear_hands"] = None
    SYSTEM["ui"]["gear_relic"] = None
    SYSTEM["ui"]["gear_belt"] = None
    SYSTEM["ui"]["gear_boots"] = None
    SYSTEM["gear_panel"] = None
    STAT_LIST.clear()

def draw_gear(events):
    """Draws the gear menu."""
    renders(SYSTEM["city_back"].as_background)
    x_offset = SCREEN_WIDTH / 2 - SYSTEM["images"]["menu_bg"].width / 2
    y_offset = SCREEN_HEIGHT / 2 - SYSTEM["images"]["menu_bg"].height / 2
    render(SYSTEM["images"]["menu_bg"].image, (x_offset, y_offset))
    SYSTEM["ui"]["gear_weapon"].tick().draw()
    SYSTEM["ui"]["gear_offhand"].tick().draw()
    SYSTEM["ui"]["gear_helm"].tick().draw()
    SYSTEM["ui"]["gear_boots"].tick().draw()
    SYSTEM["ui"]["gear_hands"].tick().draw()
    SYSTEM["ui"]["gear_armor"].tick().draw()
    SYSTEM["ui"]["gear_belt"].tick().draw()
    SYSTEM["ui"]["gear_ring"].tick().draw()
    SYSTEM["ui"]["gear_ring2"].tick().draw()
    SYSTEM["ui"]["gear_amulet"].tick().draw()
    SYSTEM["ui"]["gear_relic"].tick().draw()
    SYSTEM["gear_panel"].tick().draw()
    x = 10
    y = 10
    render(SYSTEM["images"]["char_details"].image, (x, y))
    SYSTEM["gear_tabs"].tick()
    y_offset = 0
    y_offset_tab = 220
    for l, line in STAT_LIST.items():
        if l in DEFAULT_STATS:
            x_offset = 20
            count = 0
            for data in line:
                if count >= 2:
                    count = 0
                    y_offset += 20
                    x_offset = 20
                if data is None:
                    count += 1
                    continue
                data.set(x_offset, 20 + y_offset).tick().draw()
                count += 1
                x_offset += data.width
            y_offset += 20
        if (SYSTEM["gear_tab"] == STATES[0] and l in DEFENSE_STATS) or\
            (SYSTEM["gear_tab"] == STATES[1] and l in OFFENSE_STATS) or\
            (SYSTEM["gear_tab"] == STATES[2] and l in OTHER_STATS):
            x_offset = 20
            count = 0
            for data in line:
                if count >= 2:
                    count = 0
                    y_offset_tab += 20
                    x_offset = 20
                if data is None:
                    count += 1
                    continue
                data.set(x_offset, 20 + y_offset_tab).tick().draw()
                x_offset += data.width
                count += 1
            y_offset_tab += 20
    draw_bottom_bar(events)
