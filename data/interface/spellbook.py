"""Handles the spellbook tabs of the main menu."""

from data.interface.general import draw_bottom_bar
from data.constants import SYSTEM, Flags, MENU_SPELLBOOK, SCREEN_HEIGHT, SCREEN_WIDTH,\
    MENU_SPELLBOOK_Q, MENU_SPELLBOOK_F, MENU_SPELLBOOK_E, MENU_SPELLBOOK_R,\
    MENU_SPELLBOOK_SHIFT, MENU_SPELLBOOK_T, K_q, K_t, K_e, K_r, K_f, K_LSHIFT
from data.game.spell import Spell
from data.image.button import Button
from data.image.slotpanel import SlotPanel
from data.image.slot import Slot

PAGES = {
    0: MENU_SPELLBOOK_Q,
    1: MENU_SPELLBOOK_E,
    2: MENU_SPELLBOOK_F,
    3: MENU_SPELLBOOK_T,
    4: MENU_SPELLBOOK_R,
    5: MENU_SPELLBOOK_SHIFT
}

def slot_in(self, spell):
    """SLots in a spell."""
    
def slot_out(self, spell):
    """Slots out a spell."""

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
    SYSTEM["buttons"]["tab_q"] = Button(SYSTEM["images"]["btn_fat"], None,\
                    lambda: set_page(0), superimage=SYSTEM["images"][K_q])
    SYSTEM["buttons"]["tab_e"] = Button(SYSTEM["images"]["btn_fat"], None,\
                    lambda: set_page(1), superimage=SYSTEM["images"][K_e])
    SYSTEM["buttons"]["tab_f"] = Button(SYSTEM["images"]["btn_fat"], None,\
                    lambda: set_page(2), superimage=SYSTEM["images"][K_f])
    SYSTEM["buttons"]["tab_t"] = Button(SYSTEM["images"]["btn_fat"], None,\
                    lambda: set_page(3), superimage=SYSTEM["images"][K_t])
    SYSTEM["buttons"]["tab_r"] = Button(SYSTEM["images"]["btn_fat"], None,\
                    lambda: set_page(4), superimage=SYSTEM["images"][K_r])
    SYSTEM["buttons"]["tab_s"] = Button(SYSTEM["images"]["btn_fat"], None,\
                    lambda: set_page(5), superimage=SYSTEM["images"][K_LSHIFT])
    SYSTEM["ui"]["slot_q"] = Slot(0, 0, "skill_top", slot_in, slot_out,\
        [], SYSTEM["player"].equipped_spells[K_q])
    SYSTEM["spell_panel"] = SlotPanel(SCREEN_WIDTH - 535, 10, default=spells)
    SYSTEM["dash_panel"] = SlotPanel(SCREEN_WIDTH - 535, 10, default=dashes)

def draw_spells(events):
    """Draws the gear menu."""
    SYSTEM["windows"].blit(SYSTEM["city_back"].draw(), (0, 0))
    x_offset = SCREEN_WIDTH / 2 - SYSTEM["images"]["menu_bg"].width / 2
    y_offset = SCREEN_HEIGHT / 2 - SYSTEM["images"]["menu_bg"].height / 2
    SYSTEM["windows"].blit(SYSTEM["images"]["menu_bg"].image, (x_offset, y_offset))
    SYSTEM["spell_panel"].tick().draw()
    SYSTEM["buttons"]["tab_q"].set(x_offset - 200, y_offset - 200).tick().draw(SYSTEM["windows"])
    SYSTEM["buttons"]["tab_e"].set(x_offset - 100, y_offset - 200).tick().draw(SYSTEM["windows"])
    SYSTEM["buttons"]["tab_f"].set(x_offset, y_offset - 200).tick().draw(SYSTEM["windows"])
    SYSTEM["buttons"]["tab_t"].set(x_offset + 100, y_offset - 200).tick().draw(SYSTEM["windows"])
    SYSTEM["buttons"]["tab_r"].set(x_offset + 200, y_offset - 200).tick().draw(SYSTEM["windows"])
    SYSTEM["buttons"]["tab_s"].set(x_offset + 300, y_offset - 200).tick().draw(SYSTEM["windows"])
    SYSTEM["ui"]["slot_q"].tick().draw()
    draw_bottom_bar(events)
