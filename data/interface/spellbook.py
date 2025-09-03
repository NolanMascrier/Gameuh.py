"""Handles the spellbook tabs of the main menu."""

from data.interface.general import draw_bottom_bar, setup_bottom_bar
from data.constants import SYSTEM, Flags, MENU_SPELLBOOK, SCREEN_HEIGHT, SCREEN_WIDTH,\
    MENU_SPELLBOOK_1, MENU_SPELLBOOK_3, MENU_SPELLBOOK_2, MENU_SPELLBOOK_5,\
    MENU_SPELLBOOK_DASH, MENU_SPELLBOOK_4, K_q, K_t, K_e, K_r, K_f, K_LSHIFT, trad
from data.game.spell import Spell
from data.item import Item
from data.image.slotpanel import SlotPanel
from data.image.slot import Slot
from data.image.tabs import Tabs
from data.image.text import Text
from data.interface.render import render, renders

BLACK = (0,0,0)

PAGES = {
    MENU_SPELLBOOK_1: 0,
    MENU_SPELLBOOK_2: 1,
    MENU_SPELLBOOK_3: 2,
    MENU_SPELLBOOK_4: 3,
    MENU_SPELLBOOK_5: 4,
    MENU_SPELLBOOK_DASH: 5
}

INPUT = {
    MENU_SPELLBOOK_1: "spell_1",
    MENU_SPELLBOOK_2: "spell_2",
    MENU_SPELLBOOK_3: "spell_3",
    MENU_SPELLBOOK_4: "spell_4",
    MENU_SPELLBOOK_5: "spell_5",
    MENU_SPELLBOOK_DASH: "dash"
}

STATES = [MENU_SPELLBOOK_1, MENU_SPELLBOOK_2, MENU_SPELLBOOK_3,\
    MENU_SPELLBOOK_4, MENU_SPELLBOOK_5, MENU_SPELLBOOK_DASH]

def refresh():
    """Refreshs the current spell window."""
    SYSTEM["spells"]\
        [SYSTEM["player"].equipped_spells[INPUT[SYSTEM["spell_page"]]]].recalculate_damage()
    make_slot(SYSTEM["spells"]\
        [SYSTEM["player"].equipped_spells[INPUT[SYSTEM["spell_page"]]]],
        INPUT[SYSTEM["spell_page"]])

def slot_jewel(jewel, slot):
    """Slots the jewel."""
    if jewel is None or not isinstance(jewel, Item):
        return
    SYSTEM["spells"]\
        [SYSTEM["player"].equipped_spells[INPUT[SYSTEM["spell_page"]]]].equip(slot.flag, jewel)
    SYSTEM["player"].inventory.remove(jewel)
    refresh()

def unslot_jewel(jewel, slot):
    """Unslots the jewel."""
    it = SYSTEM["spells"]\
        [SYSTEM["player"].equipped_spells[INPUT[SYSTEM["spell_page"]]]].unequip(slot.flag)
    if it is not None:
        SYSTEM["player"].inventory.append(it)
    refresh()

def overwrite_jewel(jewel, slot):
    """Overwrites the jewel."""
    if jewel is None or not isinstance(jewel, Item):
        return
    it = SYSTEM["spells"]\
        [SYSTEM["player"].equipped_spells[INPUT[SYSTEM["spell_page"]]]].unequip(slot.flag)
    if it is not None:
        SYSTEM["player"].inventory.append(it)
        SYSTEM["gear_panel"].insert(None, None, it)
    refresh()

def make_slot(spell: Spell, key):
    """Creates the description data of the spell."""
    SYSTEM["ui"][key] = [
        Text(spell.describe()["name"],\
            font="item_titles", size=45, default_color=BLACK),
        Text(f"{trad('meta_words', 'level')} " +\
            f"{spell.describe()['level']}",\
            font="item_desc", size=20, default_color=BLACK),
        Text(spell.describe()["desc"],\
            font="item_desc", size=20, default_color=BLACK),
        Text(spell.describe()["damage"],\
            font="item_desc", size=20, default_color=BLACK),
        spell.describe()["buffs"],
        Text(f"{spell.exp}/{spell.exp_to_next}",font="item_desc", size=20, default_color=BLACK),
        [Slot(0, 0, "gear_relic", slot_jewel, unslot_jewel, overwrite_jewel,\
         slot, jewel, accept_only=Item) for slot, jewel in spell.jewels.items()]
    ] if spell is not None else None

def slot_in(contain, slot):
    """Slots in a spell."""
    if not isinstance(contain, Spell):
        return
    for f in SYSTEM["spells"]:
        if SYSTEM["spells"][f] == contain:
            key = f
            break
    SYSTEM["player"].equipped_spells[slot.flag] = key
    make_slot(contain, slot.flag)

def slot_out(contain, slot):
    """Slots out a spell."""
    SYSTEM["player"].equipped_spells[slot.flag] = None
    SYSTEM["ui"][slot.flag] = None

def open_spell_screen():
    """Sets up the spell screen menu."""
    SYSTEM["game_state"] = MENU_SPELLBOOK
    setup_bottom_bar()
    SYSTEM["spell_page"] = MENU_SPELLBOOK_1
    spells = []
    dashes = []
    for spell_ref in SYSTEM["player"].spellbook:
        spell = SYSTEM["spells"][spell_ref]
        if isinstance(spell, Spell):
            if Flags.DASH in spell.flags:
                dashes.append(spell)
            else:
                spells.append(spell)
    images = [
        SYSTEM["images"][K_q],
        SYSTEM["images"][K_e],
        SYSTEM["images"][K_f],
        SYSTEM["images"][K_t],
        SYSTEM["images"][K_r],
        SYSTEM["images"][K_LSHIFT]
    ]
    x_offset = SCREEN_WIDTH / 2 - 300
    x_offset_slot = SCREEN_WIDTH / 2 - 32
    SYSTEM["gear_tabs"] = Tabs(x_offset, 300, images, STATES, "spell_page",\
        SYSTEM["images"]["btn_fat"], SYSTEM["images"]["btn_fat_pressed"], additional_action=refresh)
    SYSTEM["ui"]["slot_1"] = Slot(x_offset_slot, 380, "skill_top", slot_in, slot_out,\
        default=SYSTEM["spells"][SYSTEM["player"].equipped_spells["spell_1"]], flag="spell_1",\
        accept_only=Spell)
    SYSTEM["ui"]["slot_2"] = Slot(x_offset_slot, 380, "skill_top", slot_in, slot_out,\
        default=SYSTEM["spells"][SYSTEM["player"].equipped_spells["spell_2"]], flag="spell_2",\
        accept_only=Spell)
    SYSTEM["ui"]["slot_3"] = Slot(x_offset_slot, 380, "skill_top", slot_in, slot_out,\
        default=SYSTEM["spells"][SYSTEM["player"].equipped_spells["spell_3"]], flag="spell_3",\
        accept_only=Spell)
    SYSTEM["ui"]["slot_4"] = Slot(x_offset_slot, 380, "skill_top", slot_in, slot_out,\
        default=SYSTEM["spells"][SYSTEM["player"].equipped_spells["spell_4"]], flag="spell_4",\
        accept_only=Spell)
    SYSTEM["ui"]["slot_5"] = Slot(x_offset_slot, 380, "skill_top", slot_in, slot_out,\
        default=SYSTEM["spells"][SYSTEM["player"].equipped_spells["spell_5"]], flag="spell_5",\
        accept_only=Spell)
    SYSTEM["ui"]["slot_dash"] = Slot(x_offset_slot, 380, "skill_top", slot_in, slot_out,\
        default=SYSTEM["spells"][SYSTEM["player"].equipped_spells["dash"]], flag="dash")
    for key in ["spell_1", "spell_2", "spell_3", "spell_4", "spell_5", "dash"]:
        spell = SYSTEM["spells"][SYSTEM["player"].equipped_spells[key]]\
            if SYSTEM["player"].equipped_spells[key] is not None else None
        make_slot(spell, key)
    SYSTEM["ui"]["no_spells"] = [
        Text(trad('spells_name', 'none'), font="item_titles", size=45, default_color=BLACK),
        Text(trad('spells_desc', 'none'), font="item_desc", size=20, default_color=BLACK)
    ]
    SYSTEM["gear_panel"] = SlotPanel(10, 10,\
        default=SYSTEM["player"].inventory, filter=Flags.JEWEL)
    SYSTEM["spell_panel"] = SlotPanel(SCREEN_WIDTH - 535, 10, default=spells, immutable=True)
    SYSTEM["dash_panel"] = SlotPanel(SCREEN_WIDTH - 535, 10, default=dashes, immutable=True)

def unloader():
    """Unloads all spellbook-specific data."""
    SYSTEM["gear_tabs"] = None
    SYSTEM["spell_panel"] = None
    SYSTEM["dash_panel"] = None
    SYSTEM["ui"]["slot_q"] = None
    SYSTEM["ui"]["slot_e"] = None
    SYSTEM["ui"]["slot_f"] = None
    SYSTEM["ui"]["slot_r"] = None
    SYSTEM["ui"]["slot_t"] = None
    SYSTEM["ui"]["slot_shift"] = None

def draw_spells(events):
    """Draws the gear menu."""
    renders(SYSTEM["city_back"].as_background)
    x_offset = SCREEN_WIDTH / 2 - SYSTEM["images"]["menu_bg"].width / 2
    y_offset = SCREEN_HEIGHT / 2 - SYSTEM["images"]["menu_bg"].height / 2
    render(SYSTEM["images"]["menu_bg"].image, (x_offset, y_offset))
    val = PAGES[SYSTEM["spell_page"]]
    SYSTEM["gear_tabs"].tick()
    SYSTEM["gear_panel"].tick().draw()
    match val:
        case 1:
            SYSTEM["ui"]["slot_2"].tick().draw()
            SYSTEM["spell_panel"].tick().draw()
        case 2:
            SYSTEM["ui"]["slot_3"].tick().draw()
            SYSTEM["spell_panel"].tick().draw()
        case 3:
            SYSTEM["ui"]["slot_4"].tick().draw()
            SYSTEM["spell_panel"].tick().draw()
        case 4:
            SYSTEM["ui"]["slot_5"].tick().draw()
            SYSTEM["spell_panel"].tick().draw()
        case 5:
            SYSTEM["ui"]["slot_dash"].tick().draw()
            SYSTEM["dash_panel"].tick().draw()
        case _:
            SYSTEM["ui"]["slot_1"].tick().draw()
            SYSTEM["spell_panel"].tick().draw()
    key = INPUT[SYSTEM["spell_page"]]
    if SYSTEM["ui"][key] is not None:
        SYSTEM["ui"][key][0].draw(680, 450)
        SYSTEM["ui"][key][1].draw(680, 490)
        SYSTEM["ui"][key][5].draw(710 + SYSTEM["ui"][key][1].width , 490)
        SYSTEM["ui"][key][2].draw(680, 510)
        y = 530 + SYSTEM["ui"][key][2].height
        SYSTEM["ui"][key][3].draw(680, y)
        y += SYSTEM["ui"][key][3].height
        try:
            for afflic in SYSTEM["ui"][key][4]:
                afflic.set(680, y).tick().draw()
                y += afflic.height
        except IndexError:
            pass
        y = SCREEN_HEIGHT - 64 * 5
        x = SCREEN_WIDTH / 2 - int((64 * 5) / 2)
        for slot in SYSTEM["ui"][key][6]:
            slot.set(x, y).tick().draw()
            x += 64
    else:
        SYSTEM["ui"]["no_spells"][0].draw(680, 450)
        SYSTEM["ui"]["no_spells"][1].draw(680, 490)
    draw_bottom_bar(events)
