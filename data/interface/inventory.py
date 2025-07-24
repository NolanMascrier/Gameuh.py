"""Handles the inventory tab of the main menu."""

import pygame
from data.interface.general import draw_bottom_bar, draw_game, tick, setup_bottom_bar
from data.constants import SYSTEM, MENU_INVENTORY, Flags, trad, TEXT_TRACKER
from data.image.button import Button
from data.image.slotpanel import SlotPanel
from data.item import Item
from data.image.text import Text
from data.image.hoverable import Hoverable
from data.image.slot import Slot

def sell(item: Item, slot: Slot):
    """Sells the item."""
    TEXT_TRACKER.append([item.get_image(), SYSTEM["mouse"][0], SYSTEM["mouse"][1], 255])
    SYSTEM["player"].gold += item.price
    slot.contains = None
    SYSTEM["player"].inventory.remove(item)

def sort_inventory(method = 0, desc = False):
    """Sorts the inventory.
    
    Args:
        method (int, optional): Which method to use. 1 is \
        sort by item rarity, 2 is sort by item price, 3 is\
        by item drop time and any other value is sort by name.
        desc (bool, optional): Order by decrescent order rather\
        than crescent order. Defaults to False.
    """
    match method:
        case 1:
            if desc:
                SYSTEM["player"].inventory.sort(True, key=lambda i: i.rarity)
                SYSTEM["items_panel"].slots.sort(True, key=lambda i: i.contains.contains.rarity)
            else:
                SYSTEM["player"].inventory.sort(key=lambda i: i.rarity)
                SYSTEM["items_panel"].slots.sort(key=lambda i: i.contains.contains.rarity)
        case 2:
            if desc:
                SYSTEM["player"].inventory.sort(True, key=lambda i: i.price)
                SYSTEM["items_panel"].slots.sort(True, key=lambda i: i.contains.contains.price)
            else:
                SYSTEM["player"].inventory.sort(key=lambda i: i.price)
                SYSTEM["items_panel"].slots.sort(key=lambda i: i.contains.contains.price)
        case 3:
            if desc:
                SYSTEM["player"].inventory.sort(True, key=lambda i: i.drop_time)
                SYSTEM["items_panel"].slots.sort(True, key=lambda i: i.contains.contains.drop_time)
            else:
                SYSTEM["player"].inventory.sort(key=lambda i: i.drop_time)
                SYSTEM["items_panel"].slots.sort(key=lambda i: i.contains.contains.drop_time)
        case _:
            if desc:
                SYSTEM["player"].inventory.sort(True, key=lambda i: i.name)
                SYSTEM["items_panel"].slots.sort(True, key=lambda i: i.contains.contains.name)
            else:
                SYSTEM["player"].inventory.sort(key=lambda i: i.name)
                SYSTEM["items_panel"].slots.sort(key=lambda i: i.contains.contains.name)

def rune(rune_id):
    """Sets up the rune input."""
    if SYSTEM["player"].runes[rune_id] <= 0:
        return
    SYSTEM["rune"] = rune_id
    SYSTEM["rune_display"] = SYSTEM["images"][f"rune_{rune_id}"].clone().opacity(155)

def open_inventory():
    """Sets up the inventory screen."""
    SYSTEM["game_state"] = MENU_INVENTORY
    setup_bottom_bar()
    SYSTEM["ui"]["sell_slot"] = Slot(1556, 850, "sell_slot", sell)
    SYSTEM["buttons"]["button_sort_name"] = Button(SYSTEM["images"]["btn_small"], None,\
                                    lambda: sort_inventory(0, False),\
                                    f"{trad('buttons', 'sort')} {trad('buttons', 'by_name')}")
    SYSTEM["buttons"]["button_sort_rarity"] = Button(SYSTEM["images"]["btn_small"], None,\
                                    lambda: sort_inventory(1, False),\
                                    f"{trad('buttons', 'sort')} {trad('buttons', 'by_rarity')}")
    SYSTEM["buttons"]["button_sort_value"] = Button(SYSTEM["images"]["btn_small"], None,\
                                    lambda: sort_inventory(2, False),\
                                    f"{trad('buttons', 'sort')} {trad('buttons', 'by_value')}")
    SYSTEM["buttons"]["button_sort_date"] = Button(SYSTEM["images"]["btn_small"], None,\
                                    lambda: sort_inventory(3, False),\
                                    f"{trad('buttons', 'sort')} {trad('buttons', 'by_date')}")
    SYSTEM["buttons"]["button_rune_0"] = Button(SYSTEM["images"]["rune_0"], None,\
                                            lambda: rune(0))
    SYSTEM["images"]["pop_rune_0"] = Hoverable(0, 0, None, trad("runes", "blank"),\
                            surface=SYSTEM["buttons"]["button_rune_0"].get_image())
    SYSTEM["buttons"]["button_rune_1"] = Button(SYSTEM["images"]["rune_1"], None,\
                                            lambda: rune(1))
    SYSTEM["images"]["pop_rune_1"] = Hoverable(0, 0, None, trad("runes", "thurisaz"),\
                            surface=SYSTEM["buttons"]["button_rune_1"].get_image())
    SYSTEM["buttons"]["button_rune_2"] = Button(SYSTEM["images"]["rune_2"], None,\
                                            lambda: rune(2))
    SYSTEM["images"]["pop_rune_2"] = Hoverable(0, 0, None, trad("runes", "ansuz"),\
                            surface=SYSTEM["buttons"]["button_rune_2"].get_image())
    SYSTEM["buttons"]["button_rune_3"] = Button(SYSTEM["images"]["rune_3"], None,\
                                            lambda: rune(3))
    SYSTEM["images"]["pop_rune_3"] = Hoverable(0, 0, None, trad("runes", "ingwaz"),\
                            surface=SYSTEM["buttons"]["button_rune_3"].get_image())
    SYSTEM["buttons"]["button_rune_4"] = Button(SYSTEM["images"]["rune_4"], None,\
                                            lambda: rune(4))
    SYSTEM["images"]["pop_rune_4"] = Hoverable(0, 0, None, trad("runes", "othalan"),\
                            surface=SYSTEM["buttons"]["button_rune_4"].get_image())
    SYSTEM["buttons"]["button_rune_5"] = Button(SYSTEM["images"]["rune_5"], None,\
                                            lambda: rune(5))
    SYSTEM["images"]["pop_rune_5"] = Hoverable(0, 0, None, trad("runes", "uruz"),\
                            surface=SYSTEM["buttons"]["button_rune_5"].get_image())
    SYSTEM["buttons"]["button_rune_6"] = Button(SYSTEM["images"]["rune_6"], None,\
                                            lambda: rune(6))
    SYSTEM["images"]["pop_rune_6"] = Hoverable(0, 0, None, trad("runes", "raido"),\
                            surface=SYSTEM["buttons"]["button_rune_6"].get_image())
    SYSTEM["buttons"]["button_rune_7"] = Button(SYSTEM["images"]["rune_7"], None,\
                                            lambda: rune(7))
    SYSTEM["images"]["pop_rune_7"] = Hoverable(0, 0, None, trad("runes", "tiwaz"),\
                            surface=SYSTEM["buttons"]["button_rune_7"].get_image())
    SYSTEM["buttons"]["button_rune_8"] = Button(SYSTEM["images"]["rune_8"], None,\
                                            lambda: rune(8))
    SYSTEM["images"]["pop_rune_8"] = Hoverable(0, 0, None, trad("runes", "eihwaz"),\
                            surface=SYSTEM["buttons"]["button_rune_8"].get_image())
    SYSTEM["buttons"]["button_rune_9"] = Button(SYSTEM["images"]["rune_9"], None,\
                                            lambda: rune(9))
    SYSTEM["images"]["pop_rune_9"] = Hoverable(0, 0, None, trad("runes", "algiz"),\
                                surface=SYSTEM["buttons"]["button_rune_9"].get_image())
    SYSTEM["items_panel"] = SlotPanel(20, 20, default=SYSTEM["player"].inventory,\
        background=SYSTEM["images"]["tile_panel_inv"])

def unloader():
    """Unloads all inventory-specific data."""
    SYSTEM["ui"]["sell_slot"] = None
    SYSTEM["buttons"]["button_sort_name"] = None
    SYSTEM["buttons"]["button_sort_rarity"] = None
    SYSTEM["buttons"]["button_sort_value"] = None
    SYSTEM["buttons"]["button_sort_date"] = None
    SYSTEM["buttons"]["button_rune_0"] = None
    SYSTEM["images"]["pop_rune_0"] = None
    SYSTEM["buttons"]["button_rune_1"] = None
    SYSTEM["images"]["pop_rune_1"] = None
    SYSTEM["buttons"]["button_rune_2"] = None
    SYSTEM["images"]["pop_rune_2"] = None
    SYSTEM["buttons"]["button_rune_3"] = None
    SYSTEM["images"]["pop_rune_3"] = None
    SYSTEM["buttons"]["button_rune_4"] = None
    SYSTEM["images"]["pop_rune_4"] = None
    SYSTEM["buttons"]["button_rune_5"] = None
    SYSTEM["images"]["pop_rune_5"] = None
    SYSTEM["buttons"]["button_rune_6"] = None
    SYSTEM["images"]["pop_rune_6"] = None
    SYSTEM["buttons"]["button_rune_7"] = None
    SYSTEM["images"]["pop_rune_7"] = None
    SYSTEM["buttons"]["button_rune_8"] = None
    SYSTEM["images"]["pop_rune_8"] = None
    SYSTEM["buttons"]["button_rune_9"] = None
    SYSTEM["images"]["pop_rune_9"] = None
    SYSTEM["items_panel"] = None

def draw_inventory(events):
    """Draws the inventory windows."""
    SYSTEM["windows"].blit(SYSTEM["city_back"].draw(), (0, 0))
    SYSTEM["items_panel"].tick().draw()
    gold = SYSTEM["player"].gold
    text = Text(str(gold), font="font_detail")
    SYSTEM["windows"].blit(SYSTEM["images"]["char_details"].image, (1500, 20))
    SYSTEM["windows"].blit(SYSTEM["images"]["gold_icon"].image, (1520, 40))
    SYSTEM["windows"].blit(text.surface, (1584, 72))
    c = 0
    for i in [0, 7, 9, 8, 6, 1, 2, 3, 5, 4]:
        SYSTEM["buttons"][f"button_rune_{i}"].set(1520, 110 + c * 74).draw(SYSTEM["windows"])
        SYSTEM["images"][f"pop_rune_{i}"].set(1520, 110 + c * 74).tick()
        Text(f"{SYSTEM['player'].runes[i] if SYSTEM['player'].runes[i] < 1000 else '999+'}",\
            font="font_detail").draw(1584, 132 + c * 74)
        c += 1
    SYSTEM["buttons"]["button_sort_name"].set(1300, 20).draw(SYSTEM["windows"])
    SYSTEM["buttons"]["button_sort_rarity"].set(1300, 50).draw(SYSTEM["windows"])
    SYSTEM["buttons"]["button_sort_value"].set(1300, 80).draw(SYSTEM["windows"])
    SYSTEM["buttons"]["button_sort_date"].set(1300, 110).draw(SYSTEM["windows"])
    SYSTEM["ui"]["sell_slot"].tick().draw()
    draw_bottom_bar(events)
    if SYSTEM["rune"] != -1:
        SYSTEM["windows"].blit(SYSTEM["rune_display"].image, SYSTEM["mouse"])
    tick()
    draw_game(False, False, False, False, False)
    for event in events:
        if event.type == pygame.MOUSEBUTTONDOWN:
            SYSTEM["buttons"]["button_rune_0"].press()
            SYSTEM["buttons"]["button_rune_1"].press()
            SYSTEM["buttons"]["button_rune_2"].press()
            SYSTEM["buttons"]["button_rune_3"].press()
            SYSTEM["buttons"]["button_rune_4"].press()
            SYSTEM["buttons"]["button_rune_5"].press()
            SYSTEM["buttons"]["button_rune_6"].press()
            SYSTEM["buttons"]["button_rune_7"].press()
            SYSTEM["buttons"]["button_rune_8"].press()
            SYSTEM["buttons"]["button_rune_9"].press()
            SYSTEM["buttons"]["button_sort_name"].press()
            SYSTEM["buttons"]["button_sort_rarity"].press()
            SYSTEM["buttons"]["button_sort_value"].press()
            SYSTEM["buttons"]["button_sort_date"].press()
