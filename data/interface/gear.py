"""Handles the gear tab."""

from data.interface.general import draw_bottom_bar
from data.constants import SYSTEM, MENU_GEAR, Flags, SCREEN_HEIGHT, SCREEN_WIDTH
from data.image.slotpanel import SlotPanel
from data.item import Item
from data.image.slot import Slot

STAT_LIST = []

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
    STAT_LIST.clear()
    STAT_LIST.extend(SYSTEM["player"].creature.generate_stat_details(20, 20))

def unequip(item: Item, slot: Slot):
    """Removes the equiped item from the slot."""
    if item is None:
        return
    it = SYSTEM["player"].creature.unequip(slot.flag, slot.left)
    SYSTEM["player"].inventory.append(it)

def open_gear_screen():
    """Sets up the gear screen."""
    SYSTEM["game_state"] = MENU_GEAR
    x = SCREEN_WIDTH / 2- 32
    y = SCREEN_HEIGHT / 2 - 128
    SYSTEM["ui"]["gear_helm"] = Slot(x, y - 32, "gear_helm", equip, unequip,\
         Flags.HELM, SYSTEM["player"].creature.gear["helms"])
    SYSTEM["ui"]["gear_amulet"] = Slot(x, y + 32, "gear_amulet", equip, unequip,\
         Flags.AMULET, SYSTEM["player"].creature.gear["amulets"])
    SYSTEM["ui"]["gear_armor"] = Slot(x, y + 96, "gear_armor", equip, unequip,\
         Flags.ARMOR, SYSTEM["player"].creature.gear["armors"])
    SYSTEM["ui"]["gear_weapon"] = Slot(x - 128, y + 96, "gear_weapon", equip, unequip,\
         Flags.WEAPON, SYSTEM["player"].creature.gear["weapons"])
    SYSTEM["ui"]["gear_ring"] = Slot(x - 64, y + 64, "gear_ring", equip, unequip,\
         Flags.RING, SYSTEM["player"].creature.gear["rings"]["left"], True)
    SYSTEM["ui"]["gear_ring2"] = Slot(x + 64, y + 64, "gear_ring", equip, unequip,\
         Flags.RING, SYSTEM["player"].creature.gear["rings"]["right"])
    SYSTEM["ui"]["gear_offhand"] = Slot(x + 128, y + 96, "gear_offhand", equip, unequip,\
         Flags.OFFHAND, SYSTEM["player"].creature.gear["offhand"])
    SYSTEM["ui"]["gear_hands"] = Slot(x + 64, y + 128, "gear_hands", equip, unequip,\
         Flags.HANDS, SYSTEM["player"].creature.gear["gloves"])
    SYSTEM["ui"]["gear_relic"] = Slot(x - 64, y + 128, "gear_relic", equip, unequip,\
         Flags.RELIC, SYSTEM["player"].creature.gear["relics"])
    SYSTEM["ui"]["gear_belt"] = Slot(x, y + 174, "gear_belt", equip, unequip,\
         Flags.BELT, SYSTEM["player"].creature.gear["belts"])
    SYSTEM["ui"]["gear_boots"] = Slot(x, y + 238, "gear_boots", equip, unequip,\
         Flags.BOOTS, SYSTEM["player"].creature.gear["boots"])
    data = []
    for item in SYSTEM["player"].inventory:
        if isinstance(item, Item):
            if Flags.GEAR in item.flags:
                data.append(item)
    SYSTEM["gear_panel"] = SlotPanel(SCREEN_WIDTH - 535, 10, default=data)
    STAT_LIST.clear()
    STAT_LIST.extend(SYSTEM["player"].creature.generate_stat_details(20, 20))

def draw_gear(events):
    """Draws the gear menu."""
    SYSTEM["windows"].blit(SYSTEM["city_back"].draw(), (0, 0))
    x_offset = SCREEN_WIDTH / 2 - SYSTEM["images"]["menu_bg"].width / 2
    y_offset = SCREEN_HEIGHT / 2 - SYSTEM["images"]["menu_bg"].height / 2
    SYSTEM["windows"].blit(SYSTEM["images"]["menu_bg"].image, (x_offset, y_offset))
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
    SYSTEM["windows"].blit(SYSTEM["images"]["char_details"].image, (x, y))
    for l in STAT_LIST:
        l.draw(SYSTEM["windows"])
        l.tick()
    draw_bottom_bar(events)
