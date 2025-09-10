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
RED = (255, 25, 25)
BLUE = (25, 25, 255)

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

LEFT_COLUMN = ["crit_r", "cooldown", "aoe", "projs"]
RIGHT_COLUMN = ["crit_d", "life_cost", "mana_cost"]

STATES = [MENU_SPELLBOOK_1, MENU_SPELLBOOK_2, MENU_SPELLBOOK_3,\
    MENU_SPELLBOOK_4, MENU_SPELLBOOK_5, MENU_SPELLBOOK_DASH]

STEPS = [0,1,2,3,4,5]

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

def unslot_jewel(_, slot):
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

def single_slot(spell, superspell = None):
    """Creates the description data of a single spell."""
    data = spell.describe()
    data_super = superspell.describe() if superspell is not None else spell.describe()
    cost_l = f"{trad('descripts', 'life_cost')}: {data['costs'][0]}" if\
        data["costs"][0] > 0 else None
    cost_m = f"{trad('descripts', 'mana_cost')}: {data['costs'][1]}" if\
        data["costs"][1] > 0 else None
    crit_c = data["crit_rate"] * SYSTEM["player"].creature.stats["crit_rate"].c_value\
        if data["crit_rate"] is not None else None
    crit_d = data["crit_dmg"] * SYSTEM["player"].creature.stats["crit_dmg"].c_value\
        if data["crit_dmg"] is not None else None
    area = data["area"] + SYSTEM["player"].creature.stats["area"].c_value\
        if data["area"] is not None else None
    slot = {
        "type": "single",
        "name": Text(data_super["name"],\
            font="item_titles", size=45, default_color=BLACK),
        "level": Text(f"{trad('meta_words', 'level')} " +\
            f"{data_super['level']}",\
            font="item_desc", size=20, default_color=BLACK),
        "desc": Text(data_super["desc"],\
            font="item_desc", size=20, default_color=BLACK),
        "damage": Text(data["damage"],\
            font="item_desc", size=20, default_color=BLACK),
        "buffs": data["buffs"],
        "exp": Text(f"{spell.exp}/{spell.exp_to_next}",\
            font="item_desc", size=20, default_color=BLACK),
        "slots": [Slot(0, 0, "gear_relic", slot_jewel, unslot_jewel, overwrite_jewel,\
            slot, jewel, accept_only=Item) for slot, jewel in spell.jewels.items()],
        "crit_r": Text(f"{trad('descripts', 'crit_rate')}: {int(crit_c * 100)}%",\
            font="item_desc", size=20, default_color=BLACK)\
            if crit_c is not None else None,
        "crit_d": Text(f"{trad('descripts', 'crit_dmg')}: {int(crit_d * 100)}%",\
            font="item_desc", size=20, default_color=BLACK)\
            if crit_d is not None else None,
        "cooldown": Text(f"{trad('descripts', 'cooldown')}: {data['cooldown']}s",\
            font="item_desc", size=20, default_color=BLACK),
        "projs": Text(f"{trad('descripts', 'projectiles')}: {round(data['projectiles'])}",\
            font="item_desc", size=20, default_color=BLACK) if data["projectiles"] is not None\
            else None,
        "life_cost": Text(cost_l, font="item_desc", size=20, default_color=RED)\
                if cost_l is not None else None,
        "mana_cost": Text(cost_m, font="item_desc", size=20, default_color=BLUE)\
                if cost_m is not None else None,
        "dmg_eff": data["dmg_effic"],
        "aoe": Text(f"{trad('descripts', 'area')}: {int(area * 100)}%",\
            font="item_desc", size=20, default_color=BLACK)\
            if area is not None else None,
    } if spell is not None else None
    return slot

def make_slot(spell: Spell, key):
    """Creates the description data of the spell."""
    if spell is None:
        SYSTEM["ui"][key] = None
        return
    data = spell.describe()
    if data["sequence"] is None:
        SYSTEM["ui"][key] = single_slot(spell)
    else:
        values = [f"{trad('descripts', 'step')} {(f + 1)}" for f in STEPS]
        SYSTEM["ui"][key] = {
            "type": "sequence",
            "data": [single_slot(s, spell) for s in data["sequence"]],
            "slots": [Slot(0, 0, "gear_relic", slot_jewel, unslot_jewel, overwrite_jewel,\
                slot, jewel, accept_only=Item) for slot, jewel in spell.jewels.items()],
            "tabs": Tabs(0, 0, values[:len(spell.sequence)],\
                STEPS[:len(spell.sequence)], "step_page",\
                SYSTEM["images"]["btn_fat"], SYSTEM["images"]["btn_fat_pressed"],\
                additional_action=refresh)
        }

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

def slot_out(_, slot):
    """Slots out a spell."""
    SYSTEM["player"].equipped_spells[slot.flag] = None
    SYSTEM["ui"][slot.flag] = None

def open_spell_screen():
    """Sets up the spell screen menu."""
    SYSTEM["game_state"] = MENU_SPELLBOOK
    setup_bottom_bar()
    SYSTEM["spell_page"] = MENU_SPELLBOOK_1
    SYSTEM["step_page"] = 0
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
    SYSTEM["gear_tabs"] = Tabs(x_offset, 100, images, STATES, "spell_page",\
        SYSTEM["images"]["btn_fat"], SYSTEM["images"]["btn_fat_pressed"], additional_action=refresh)
    SYSTEM["ui"]["slot_1"] = Slot(x_offset_slot, 164, "skill_top", slot_in, slot_out,\
        default=SYSTEM["spells"][SYSTEM["player"].equipped_spells["spell_1"]], flag="spell_1",\
        accept_only=Spell)
    SYSTEM["ui"]["slot_2"] = Slot(x_offset_slot, 164, "skill_top", slot_in, slot_out,\
        default=SYSTEM["spells"][SYSTEM["player"].equipped_spells["spell_2"]], flag="spell_2",\
        accept_only=Spell)
    SYSTEM["ui"]["slot_3"] = Slot(x_offset_slot, 164, "skill_top", slot_in, slot_out,\
        default=SYSTEM["spells"][SYSTEM["player"].equipped_spells["spell_3"]], flag="spell_3",\
        accept_only=Spell)
    SYSTEM["ui"]["slot_4"] = Slot(x_offset_slot, 164, "skill_top", slot_in, slot_out,\
        default=SYSTEM["spells"][SYSTEM["player"].equipped_spells["spell_4"]], flag="spell_4",\
        accept_only=Spell)
    SYSTEM["ui"]["slot_5"] = Slot(x_offset_slot, 164, "skill_top", slot_in, slot_out,\
        default=SYSTEM["spells"][SYSTEM["player"].equipped_spells["spell_5"]], flag="spell_5",\
        accept_only=Spell)
    SYSTEM["ui"]["slot_dash"] = Slot(x_offset_slot, 164, "skill_top", slot_in, slot_out,\
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

def draw_single(spell, y_offset = 0):
    """Draws the details of a single spell."""
    spell["name"].draw(680, 250 + y_offset)
    spell["level"].draw(680, 290 + y_offset)
    spell["exp"].draw(710 + spell["level"].width , 290 + y_offset)
    spell["desc"].draw(680, 310 + y_offset)
    y = 330 + spell["desc"].height  + y_offset
    spell["damage"].draw(680, y)
    y += spell["damage"].height
    try:
        for afflic in spell["buffs"]:
            afflic.set(680, y).tick().draw()
            y += afflic.height
    except IndexError:
        pass
    if spell["dmg_eff"] is not None:
        spell["dmg_eff"].set(680, y + 30).draw()
    y_ = y + 60
    for f in LEFT_COLUMN:
        if spell[f] is not None:
            spell[f].draw(680, y_)
            y_ += 30
    y_ = y + 60
    for f in RIGHT_COLUMN:
        if spell[f] is not None:
            spell[f].draw(960, y_)
            y_ += 30

def draw_sequence(key):
    """Draw the detail of a sequence of spells."""
    x = SCREEN_WIDTH / 2 - SYSTEM["ui"][key]["tabs"].width / 2
    SYSTEM["ui"][key]["tabs"].set(x, 250).tick()
    draw_single(SYSTEM["ui"][key]["data"][SYSTEM["step_page"]], 100)

def draw_spells(events):
    """Draws the gear menu."""
    renders(SYSTEM["city_back"].as_background)
    x_offset = SCREEN_WIDTH / 2 - SYSTEM["images"]["menu_bg_alt"].width / 2
    render(SYSTEM["images"]["menu_bg_alt"].image, (x_offset, 10))
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
        if SYSTEM["ui"][key]["type"] == "single":
            draw_single(SYSTEM["ui"][key])
        elif SYSTEM["ui"][key]["type"] == "sequence":
            draw_sequence(key)
        y = SCREEN_HEIGHT - 64 * 4
        x = SCREEN_WIDTH / 2 - int((64 * 5) / 2)
        for slot in SYSTEM["ui"][key]["slots"]:
            slot.set(x, y).tick().draw()
            x += 64
    else:
        SYSTEM["ui"]["no_spells"][0].draw(680, 250)
        SYSTEM["ui"]["no_spells"][1].draw(680, 290)
    draw_bottom_bar(events)
