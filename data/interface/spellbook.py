"""Handles the spellbook tabs of the main menu."""

from data.interface.general import draw_bottom_bar, setup_bottom_bar
from data.constants import SYSTEM, Flags, MENU_SPELLBOOK, SCREEN_HEIGHT, SCREEN_WIDTH,\
    MENU_SPELLBOOK_Q, MENU_SPELLBOOK_F, MENU_SPELLBOOK_E, MENU_SPELLBOOK_R,\
    MENU_SPELLBOOK_SHIFT, MENU_SPELLBOOK_T, K_q, K_t, K_e, K_r, K_f, K_LSHIFT, trad
from data.game.spell import Spell
from data.image.slotpanel import SlotPanel
from data.image.slot import Slot
from data.image.tabs import Tabs
from data.image.text import Text
from data.interface.render import render

PAGES = {
    MENU_SPELLBOOK_Q: 0,
    MENU_SPELLBOOK_E: 1,
    MENU_SPELLBOOK_F: 2,
    MENU_SPELLBOOK_T: 3,
    MENU_SPELLBOOK_R: 4,
    MENU_SPELLBOOK_SHIFT: 5
}

INPUT = {
    MENU_SPELLBOOK_Q: "spell_1",
    MENU_SPELLBOOK_E: "spell_2",
    MENU_SPELLBOOK_F: "spell_3",
    MENU_SPELLBOOK_T: "spell_4",
    MENU_SPELLBOOK_R: "spell_5",
    MENU_SPELLBOOK_SHIFT: "dash"
}

STATES = [MENU_SPELLBOOK_Q, MENU_SPELLBOOK_E, MENU_SPELLBOOK_F,\
    MENU_SPELLBOOK_T, MENU_SPELLBOOK_R, MENU_SPELLBOOK_SHIFT]

def slot_in(contain, slot):
    """Slots in a spell."""
    for f in SYSTEM["spells"]:
        if SYSTEM["spells"][f] == contain:
            key = f
            break
    SYSTEM["player"].equipped_spells[slot.flag] = key
    SYSTEM["ui"][slot.flag] = [
        Text(contain.describe()["name"],\
            font="item_titles", size=45, default_color=(0,0,0)),
        Text(f"{trad('meta_words', 'level')} " +\
            f"{contain.describe()['level']}",\
            font="item_desc", size=20, default_color=(0,0,0)),
        Text(contain.describe()["desc"],\
            font="item_desc", size=20, default_color=(0,0,0)),
        Text(contain.describe()["damage"],\
            font="item_desc", size=20, default_color=(0,0,0)),
        contain.describe()["buffs"]
    ]

def slot_out(contain, slot):
    """Slots out a spell."""
    SYSTEM["player"].equipped_spells[slot.flag] = None
    SYSTEM["ui"][slot.flag] = None

def set_page(page):
    """Changes the page of the spellbook."""
    if page in PAGES:
        SYSTEM["spell_page"] = PAGES[page]

def open_spell_screen():
    """Sets up the spell screen menu."""
    SYSTEM["game_state"] = MENU_SPELLBOOK
    setup_bottom_bar()
    SYSTEM["spell_page"] = MENU_SPELLBOOK_Q
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
        SYSTEM["images"]["btn_fat"], SYSTEM["images"]["btn_fat_pressed"])
    SYSTEM["ui"]["slot_q"] = Slot(x_offset_slot, 380, "skill_top", slot_in, slot_out,\
        default=SYSTEM["spells"][SYSTEM["player"].equipped_spells["spell_1"]], flag="spell_1")
    SYSTEM["ui"]["slot_e"] = Slot(x_offset_slot, 380, "skill_top", slot_in, slot_out,\
        default=SYSTEM["spells"][SYSTEM["player"].equipped_spells["spell_2"]], flag="spell_2")
    SYSTEM["ui"]["slot_f"] = Slot(x_offset_slot, 380, "skill_top", slot_in, slot_out,\
        default=SYSTEM["spells"][SYSTEM["player"].equipped_spells["spell_3"]], flag="spell_3")
    SYSTEM["ui"]["slot_r"] = Slot(x_offset_slot, 380, "skill_top", slot_in, slot_out,\
        default=SYSTEM["spells"][SYSTEM["player"].equipped_spells["spell_4"]], flag="spell_4")
    SYSTEM["ui"]["slot_t"] = Slot(x_offset_slot, 380, "skill_top", slot_in, slot_out,\
        default=SYSTEM["spells"][SYSTEM["player"].equipped_spells["spell_5"]], flag="spell_5")
    SYSTEM["ui"]["slot_shift"] = Slot(x_offset_slot, 380, "skill_top", slot_in, slot_out,\
        default=SYSTEM["spells"][SYSTEM["player"].equipped_spells["dash"]], flag="dash")
    for key in ["spell_1", "spell_2", "spell_3", "spell_4", "spell_5", "dash"]:
        spell = SYSTEM["spells"][SYSTEM["player"].equipped_spells[key]]\
            if SYSTEM["player"].equipped_spells[key] is not None else None
        SYSTEM["ui"][key] = [
            Text(spell.describe()["name"],\
                font="item_titles", size=45, default_color=(0,0,0)),
            Text(f"{trad('meta_words', 'level')} " +\
                f"{spell.describe()['level']}",\
                font="item_desc", size=20, default_color=(0,0,0)),
            Text(spell.describe()["desc"],\
                font="item_desc", size=20, default_color=(0,0,0)),
            Text(spell.describe()["damage"],\
                font="item_desc", size=20, default_color=(0,0,0)),
            spell.describe()["buffs"]
        ] if spell is not None else None
    SYSTEM["ui"]["no_spells"] = [
        Text(trad('spells_name', 'none'), font="item_titles", size=45, default_color=(0,0,0)),
        Text(trad('spells_desc', 'none'), font="item_desc", size=20, default_color=(0,0,0))
    ]
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
    SYSTEM["city_back"].draw()
    x_offset = SCREEN_WIDTH / 2 - SYSTEM["images"]["menu_bg"].width / 2
    y_offset = SCREEN_HEIGHT / 2 - SYSTEM["images"]["menu_bg"].height / 2
    render(SYSTEM["images"]["menu_bg"].image, (x_offset, y_offset))
    val = PAGES[SYSTEM["spell_page"]]
    SYSTEM["gear_tabs"].tick()
    match val:
        case 1:
            SYSTEM["ui"]["slot_e"].tick().draw()
            SYSTEM["spell_panel"].tick().draw()
        case 2:
            SYSTEM["ui"]["slot_f"].tick().draw()
            SYSTEM["spell_panel"].tick().draw()
        case 3:
            SYSTEM["ui"]["slot_t"].tick().draw()
            SYSTEM["spell_panel"].tick().draw()
        case 4:
            SYSTEM["ui"]["slot_r"].tick().draw()
            SYSTEM["spell_panel"].tick().draw()
        case 5:
            SYSTEM["ui"]["slot_shift"].tick().draw()
            SYSTEM["dash_panel"].tick().draw()
        case _:
            SYSTEM["ui"]["slot_q"].tick().draw()
            SYSTEM["spell_panel"].tick().draw()
    key = INPUT[SYSTEM["spell_page"]]
    if SYSTEM["ui"][key] is not None:
        SYSTEM["ui"][key][0].draw(680, 450)
        SYSTEM["ui"][key][1].draw(680, 490)
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
    else:
        SYSTEM["ui"]["no_spells"][0].draw(680, 450)
        SYSTEM["ui"]["no_spells"][1].draw(680, 490)
    draw_bottom_bar(events)
