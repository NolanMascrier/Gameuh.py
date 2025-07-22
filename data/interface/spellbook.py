"""Handles the spellbook tabs of the main menu."""

from data.interface.general import draw_bottom_bar
from data.constants import SYSTEM, Flags, MENU_SPELLBOOK, SCREEN_HEIGHT, SCREEN_WIDTH,\
    MENU_SPELLBOOK_Q, MENU_SPELLBOOK_F, MENU_SPELLBOOK_E, MENU_SPELLBOOK_R,\
    MENU_SPELLBOOK_SHIFT, MENU_SPELLBOOK_T, K_q, K_t, K_e, K_r, K_f, K_LSHIFT
from data.game.spell import Spell
from data.image.slotpanel import SlotPanel
from data.image.slot import Slot
from data.image.tabs import Tabs

PAGES = {
    MENU_SPELLBOOK_Q: 0,
    MENU_SPELLBOOK_E: 1,
    MENU_SPELLBOOK_F: 2,
    MENU_SPELLBOOK_T: 3,
    MENU_SPELLBOOK_R: 4,
    MENU_SPELLBOOK_SHIFT: 5
}

STATES = [MENU_SPELLBOOK_Q, MENU_SPELLBOOK_E, MENU_SPELLBOOK_F,\
    MENU_SPELLBOOK_T, MENU_SPELLBOOK_R, MENU_SPELLBOOK_SHIFT]

def slot_in(contain, slot):
    """SLots in a spell."""
    SYSTEM["player"].equipped_spells[slot.flag] = contain
    
def slot_out(contain, slot):
    """Slots out a spell."""
    SYSTEM["player"].equipped_spells[slot.flag] = None

def set_page(page):
    """Changes the page of the spellbook."""
    if page in PAGES:
        SYSTEM["spell_page"] = PAGES[page]
    print("caca")

def open_spell_screen():
    """Sets up the spell screen menu."""
    SYSTEM["game_state"] = MENU_SPELLBOOK
    SYSTEM["spell_page"] = MENU_SPELLBOOK_Q
    spells = []
    dashes = []
    for spell in SYSTEM["player"].spellbook:
        if isinstance(spell, Spell):
            if Flags.DASH in spell.flags:
                dashes.append(spell)
            else:
                spells.append(spell)
    images = [
        SYSTEM["images"][K_q],
        SYSTEM["images"][K_e],
        SYSTEM["images"][K_f],
        SYSTEM["images"][K_r],
        SYSTEM["images"][K_t],
        SYSTEM["images"][K_LSHIFT]
    ]
    x_offset = SCREEN_WIDTH / 2 - 300
    x_offset_slot = SCREEN_WIDTH / 2 - 32
    SYSTEM["gear_tabs"] = Tabs(x_offset, 300, images, STATES, "spell_page",\
        SYSTEM["images"]["btn_fat"], SYSTEM["images"]["btn_fat_pressed"])
    SYSTEM["ui"]["slot_q"] = Slot(x_offset_slot, 450, "skill_top", lambda a,b: slot_in(a, b), lambda a,b: slot_out(a, b),\
        default=SYSTEM["player"].equipped_spells[K_q], flag=K_q)
    SYSTEM["ui"]["slot_e"] = Slot(x_offset_slot, 450, "skill_top", lambda a,b: slot_in(a, b), lambda a,b: slot_out(a, b),\
        default=SYSTEM["player"].equipped_spells[K_e], flag=K_e)
    SYSTEM["ui"]["slot_f"] = Slot(x_offset_slot, 450, "skill_top", lambda a,b: slot_in(a, b), lambda a,b: slot_out(a, b),\
        default=SYSTEM["player"].equipped_spells[K_f], flag=K_f)
    SYSTEM["ui"]["slot_r"] = Slot(x_offset_slot, 450, "skill_top", lambda a,b: slot_in(a, b), lambda a,b: slot_out(a, b),\
        default=SYSTEM["player"].equipped_spells[K_r], flag=K_r)
    SYSTEM["ui"]["slot_t"] = Slot(x_offset_slot, 450, "skill_top", lambda a,b: slot_in(a, b), lambda a,b: slot_out(a, b),\
        default=SYSTEM["player"].equipped_spells[K_t], flag=K_t)
    SYSTEM["ui"]["slot_shift"] = Slot(x_offset_slot, 450, "skill_top", lambda a,b: slot_in(a, b), lambda a,b: slot_out(a, b),\
        default=SYSTEM["player"].equipped_spells[K_LSHIFT], flag=K_LSHIFT)
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
    SYSTEM["windows"].blit(SYSTEM["city_back"].draw(), (0, 0))
    x_offset = SCREEN_WIDTH / 2 - SYSTEM["images"]["menu_bg"].width / 2
    y_offset = SCREEN_HEIGHT / 2 - SYSTEM["images"]["menu_bg"].height / 2
    SYSTEM["windows"].blit(SYSTEM["images"]["menu_bg"].image, (x_offset, y_offset))
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
            SYSTEM["ui"]["slot_r"].tick().draw()
            SYSTEM["spell_panel"].tick().draw()
        case 4:
            SYSTEM["ui"]["slot_t"].tick().draw()
            SYSTEM["spell_panel"].tick().draw()
        case 5:
            SYSTEM["ui"]["slot_shift"].tick().draw()
            SYSTEM["dash_panel"].tick().draw()
        case _:
            SYSTEM["ui"]["slot_q"].tick().draw()
            SYSTEM["spell_panel"].tick().draw()
    draw_bottom_bar(events)
