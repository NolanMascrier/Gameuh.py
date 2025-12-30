"""File for drawing in game UI, such as the skill bar,
exp bar, enemy life, boss life ..."""

from functools import lru_cache

from data.api.surface import Surface
from data.api.keycodes import KEY_EVENT, K_1, K_2

from data.image.text import Text
from data.constants import SYSTEM, SCREEN_HEIGHT, SCREEN_WIDTH, trad, ENNEMY_TRACKER, \
    RED_WEAK, YELLOW, ORANGE
from data.image.textgenerator import make_text

UI_SKILLS_OFFSET = 408
UI_SKILLS_PANEL_OFFSET = 0
UI_SKILLS_INPUT_OFFSET = 16

POTION_OFFSET = UI_SKILLS_OFFSET - 64 - 32
POTION_OFFSET_REV = SCREEN_WIDTH - POTION_OFFSET - 64

UPDATE_COUNTER = [5]

_UI_CACHE = {
    'last_life': None,
    'last_mana': None,
    'last_life_max': None,
    'last_mana_max': None,
    'last_potion_counts': (None, None),
    'life_text': None,
    'mana_text': None,
    'potion_texts': [None, None],
    'exp_text': None,
    'exp': None,
    'skills': {
        "spell_L": [None, None, None, None],
        "spell_R": [None, None, None, None],
        "spell_M": [None, None, None, None],
        "spell_1": [None, None, None, None],
        "spell_2": [None, None, None, None],
        "spell_3": [None, None, None, None],
        "spell_4": [None, None, None, None],
        "spell_5": [None, None, None, None],
        "spell_6": [None, None, None, None],
        "spell_7": [None, None, None, None],
        "dash": [None, None, None, None]
    },
    "red_square": None,
    "yel_square": None,
    "orb_hp": None,
    "orb_mp": None,
    "orb_hp_img": None,
    "orb_mp_img": None,
    "hp_res": None,
    "hp_res_orb": None,
    "mp_res": None,
    "mp_res_orb": None,
}

def generate_background():
    """Generates the background surface of the UI. To be called only once when the
    level loads !"""
    SYSTEM["ui_background"].clear()
    char = SYSTEM["player"]
    data = []
    #BACKGROUND
    data.append((SYSTEM["images"]["ui_background"].image,
                 (0, SCREEN_HEIGHT - SYSTEM["images"]["ui_background"].height)))
    #POTIONS
    data.append((SYSTEM["images"]["skill_bottom"].image, (POTION_OFFSET, SCREEN_HEIGHT - 100)))
    data.append((SYSTEM["images"]["skill_bottom"].image,\
                        (POTION_OFFSET_REV, SCREEN_HEIGHT - 100)))
    #SKILLS
    i = 0
    for _ in char.equipped_spells:
        data.append((SYSTEM["images"]["skill_bottom"].image,\
            (UI_SKILLS_OFFSET + 104 * i, SCREEN_HEIGHT - 100)))
        i += 1
    #LIFE AND MANA
    data.append((SYSTEM["images"]["ui_orb_life_e"].image, (90, SCREEN_HEIGHT - 201)))
    data.append((SYSTEM["images"]["ui_orb_mana_e"].image,
                 (SCREEN_WIDTH - 288, SCREEN_HEIGHT - 201)))
    #
    SYSTEM["ui_background"] = data

def generate_foreground():
    """Generates the foreground of the UI. To be called only once when 
    the level loads !"""
    SYSTEM["ui_foreground"].clear()
    char = SYSTEM["player"]
    data = []
    #POTIONS
    data.append((SYSTEM["images"]["skill_top"].image, (POTION_OFFSET, SCREEN_HEIGHT - 100)))
    if SYSTEM["player"].creature.gear["life_pot"] is not None:
        data.append((SYSTEM["player"].creature.gear["life_pot"].get_image().image,
                     (POTION_OFFSET, SCREEN_HEIGHT - 100)))
    data.append((SYSTEM["images"][K_1].image, (POTION_OFFSET + 48, SCREEN_HEIGHT - 42)))

    data.append((SYSTEM["images"]["skill_top"].image,\
                           (POTION_OFFSET_REV, SCREEN_HEIGHT - 100)))
    if SYSTEM["player"].creature.gear["mana_pot"] is not None:
        data.append((SYSTEM["player"].creature.gear["mana_pot"].get_image().image,
                     (POTION_OFFSET_REV, SCREEN_HEIGHT - 100)))
    data.append((SYSTEM["images"][K_2].image, (POTION_OFFSET_REV - 16, SCREEN_HEIGHT - 42)))
    #SKILLS
    i = 0
    for name, _ in char.equipped_spells.items():
        data.append((SYSTEM["images"]["skill_top"].image, (UI_SKILLS_OFFSET + 104 * i,\
            SCREEN_HEIGHT - 100)))
        data.append((SYSTEM["images"][KEY_EVENT[name][0]].image,\
            (UI_SKILLS_OFFSET + UI_SKILLS_INPUT_OFFSET + 104 * i,SCREEN_HEIGHT - 52)))
        i += 1
    #LIFE AND MANA
    data.append((SYSTEM["images"]["ui_orb_top_a"].image, (90, SCREEN_HEIGHT - 201)))
    data.append((SYSTEM["images"]["ui_orb_top"].image, (SCREEN_WIDTH - 288, SCREEN_HEIGHT - 201)))
    #EXP
    data.append((SYSTEM["images"]["exp_bar"].image, (264, SCREEN_HEIGHT - 180)))
    #
    SYSTEM["ui_foreground"] = data

def draw_exp_bar():
    """Draws the EXP bar."""
    data = []
    char = SYSTEM["player"]
    exp_len = char.creature.exp / char.creature.exp_to_next * 1326
    exp_len = min(max(exp_len, 0), 1326)
    c = SYSTEM["images"]["exp_jauge"].image.subsurface((0, 0, exp_len, 9))
    data.append((c, (298, SCREEN_HEIGHT - 129)))
    return data

def draw_life_mana():
    """Draws the life and mana orbs."""
    data = []
    char = SYSTEM["player"].creature.stats

    max_mana = char["mana"].get_value()
    current_mana = max(min(char["mana"].current_value, max_mana), 0)
    reserved_mana = char["mana"].get_reserved_ressource()
    mana_dh = round((current_mana / max_mana) * 198)
    mana_dy = 198 - mana_dh
    mana_r_dh = 198 - round((reserved_mana / max_mana) * 198)
    if _UI_CACHE["orb_mp"] != mana_dh:
        _UI_CACHE["orb_mp"] = mana_dh
        _UI_CACHE["orb_mp_img"] = SYSTEM["images"]["ui_orb_mana"].extracts(0, mana_dy, 198, mana_dh)
    if _UI_CACHE["mp_res"] != mana_r_dh:
        _UI_CACHE["mp_res"] = mana_r_dh
        _UI_CACHE["mp_res_orb"] = SYSTEM["images"]["ui_orb_reserv"].extracts(0, 0, 198,
                                                                             198 - mana_r_dh)

    max_life = char["life"].get_value()
    current_life = max(min(char["life"].current_value, max_life), 0)
    reserved_life = char["life"].get_reserved_ressource()
    life_dh = round((current_life / max_life) * 198)
    life_dy = 198 - life_dh
    life_r_dh = 198 - round((reserved_life / max_life) * 198)
    if _UI_CACHE["orb_hp"] != life_dh:
        _UI_CACHE["orb_hp"] = life_dh
        _UI_CACHE["orb_hp_img"] = SYSTEM["images"]["ui_orb_life"].extracts(0, life_dy, 198, life_dh)
    if _UI_CACHE["hp_res"] != life_r_dh:
        _UI_CACHE["hp_res"] = life_r_dh
        _UI_CACHE["hp_res_orb"] = SYSTEM["images"]["ui_orb_reserv"].extracts(0, 0, 198,
                                                                             198 - life_r_dh)

    data.append((_UI_CACHE["orb_hp_img"].image, (90, SCREEN_HEIGHT - 201 + life_dy)))
    data.append((_UI_CACHE["hp_res_orb"].image, (90, SCREEN_HEIGHT - 201)))
    data.append((_UI_CACHE["orb_mp_img"].image, (SCREEN_WIDTH - 288,
                                                 SCREEN_HEIGHT - 201 + mana_dy)))
    data.append((_UI_CACHE["mp_res_orb"].image, (SCREEN_WIDTH - 288, SCREEN_HEIGHT - 201)))
    return data

def draw_text():
    """Draw the texts of the UI (life, mana, potion counts, exp).
    Cooldowns are handled by the skills."""
    char = SYSTEM["player"]
    if _UI_CACHE['last_potion_counts'] != tuple(char.potions):
        _UI_CACHE['last_potion_counts'] = tuple(char.potions)
        _UI_CACHE['potion_texts'][0] = Text(f"{int(char.potions[0])}", size=30, font="item_desc")
        _UI_CACHE['potion_texts'][1] = Text(f"{int(char.potions[1])}", size=30, font="item_desc")
    data = []
    life_off = _UI_CACHE['potion_texts'][0].width // 2 + 16
    mana_off = _UI_CACHE['potion_texts'][1].width // 2
    data.append((_UI_CACHE['potion_texts'][0].surface,
                 (POTION_OFFSET + life_off, SCREEN_HEIGHT - 42)))
    data.append((_UI_CACHE['potion_texts'][1].surface,
                 (POTION_OFFSET_REV + 32 - mana_off, SCREEN_HEIGHT - 42)))
    if SYSTEM["options"]["display_hp"]:
        rsc = char.creature.stats
        if _UI_CACHE["last_life"] != rsc["life"].current_value:
            _UI_CACHE["last_life"] = rsc["life"]
            if rsc["life"].get_reserved_ressource() > 0:
                _UI_CACHE["life_text"] = Text(f"{int(rsc['life'].current_value)}/" +
                                          f"#s#(15){int(rsc['life'].get_value())}\n" +
                                          f"{trad('meta_words', 'reserved')}:" +
                                          f" {int(rsc['life'].get_reserved_ressource())}",
                                          size=20, font="item_desc", centered=True)
            else:
                _UI_CACHE["life_text"] = Text(f"{int(rsc['life'].current_value)}/" +
                                          f"{int(rsc['life'].get_value())}",
                                          size=20, font="item_desc")
        if _UI_CACHE["last_mana"] != rsc["mana"].current_value:
            _UI_CACHE["last_mana"] = rsc["mana"]
            if rsc["mana"].get_reserved_ressource() > 0:
                _UI_CACHE["mana_text"] = Text(f"{int(rsc['mana'].current_value)}/" +
                                          f"{int(rsc['mana'].get_value())}\n" +
                                          f"#s#(15){trad('meta_words', 'reserved')}:" +
                                          f" {int(rsc['mana'].get_reserved_ressource())}",
                                          size=20, font="item_desc", centered=True)
            else:
                _UI_CACHE["mana_text"] = Text(f"{int(rsc['mana'].current_value)}/" +
                                          f"{int(rsc['mana'].get_value())}",
                                          size=20, font="item_desc")
        life_offset_x = 90 + SYSTEM["images"]["ui_orb_life"].width // 2 - \
            _UI_CACHE["life_text"].width // 2
        mana_offset_x = SCREEN_WIDTH - 288 + SYSTEM["images"]["ui_orb_mana"].width // 2 - \
            _UI_CACHE["mana_text"].width // 2
        offset_y = SCREEN_HEIGHT - 198 + SYSTEM["images"]["ui_orb_life"].height // 2 - \
            _UI_CACHE["life_text"].height // 2
        data.append((_UI_CACHE["life_text"].surface, (life_offset_x, offset_y)))
        data.append((_UI_CACHE["mana_text"].surface, (mana_offset_x, offset_y)))
    if SYSTEM["options"]["display_exp"]:
        exp = f"{char.creature.exp}/{char.creature.exp_to_next}"
        if exp != _UI_CACHE["exp"]:
            _UI_CACHE["exp"] = exp
            _UI_CACHE["exp_text"] = Text(exp, font="item_desc", size=20)
        dx = 264 + SYSTEM["images"]["exp_bar"].width // 2 - _UI_CACHE["exp_text"].width // 2
        dy = SCREEN_HEIGHT - 180 + SYSTEM["images"]["exp_bar"].height // 2 + \
            _UI_CACHE["exp_text"].height // 2
        data.append((_UI_CACHE["exp_text"].surface, (dx, dy)))
    return data

@lru_cache(maxsize=128)
def build_buff_icon(x, y, buff, duration, stack, big = True):
    """Builds the icon for the given buff."""
    data = []
    data.append((SYSTEM["images"][f"buff_{buff}"].image, (x, y)))
    w = 32 if big else 16
    h = 64 if big else 32
    if duration > 1:
        dr = round(duration)
        txt = make_text(f"{dr}s", size=20 if big else 15)
        data.append((txt.surface,
                    (x - txt.width / 2 + w, y - txt.height / 2 + h)))
    else:
        dr = round(duration, 2)
        txt = make_text(f"{dr}s", size=20 if big else 15)
        data.append((txt.surface,
                    (x - txt.width / 2 + w, y - txt.height / 2 + h)))
    if stack > 1:
        txt = make_text(f"x{stack}", size=25 if big else 18)
        data.append((txt.surface,
                    (x - txt.width / 2 + w, y - txt.height / 2 + w)))
    return data

def draw_buffs():
    """Draws the buff list."""
    data = []
    buffs = SYSTEM["player"].creature.build_debuff_list()
    i = 0
    def_x = x = 320
    y = SCREEN_HEIGHT - 224
    for buff, duration in buffs.items():
        if f"buff_{buff}" in SYSTEM["images"]:
            if i >= 15:
                i = 0
                y -= 96
            x = def_x + 64 * i
            data.extend(build_buff_icon(x, y, buff, duration[2], duration[1]))
            i += 1
    return data

def draw_skills():
    """Draws the skill bar."""
    if _UI_CACHE["red_square"] is None:
        _UI_CACHE["red_square"] = Surface(60, 60)
        _UI_CACHE["red_square"].set_alpha(128)
        _UI_CACHE["red_square"].fill(RED_WEAK)
    if _UI_CACHE["yel_square"] is None:
        _UI_CACHE["yel_square"] = Surface(60, 60)
        _UI_CACHE["yel_square"].set_alpha(128)
        _UI_CACHE["yel_square"].fill(YELLOW)
    data = []
    char = SYSTEM["player"]
    skill_items = list(char.equipped_spells.items())
    for i, (slot, skill) in enumerate(skill_items):
        spell = SYSTEM["spells"][skill]
        if spell is not None:
            cdc = spell.cooldown
            cdm = spell.stats["cooldown"].get_value()
            cdl = int(cdc / cdm * 60)
            oom = bool(char.creature.get_efficient_value(spell.stats["mana_cost"]\
                .get_value()) > char.creature.stats["mana"].current_value)
            x_pos = UI_SKILLS_OFFSET + 104 * i
            y_pos = SCREEN_HEIGHT - 100
            data.append((spell.icon.get_image(), (x_pos, y_pos)))
            if oom:
                data.append((_UI_CACHE["red_square"], (x_pos + UI_SKILLS_PANEL_OFFSET, y_pos + 2)))
            if cdc > 0:
                if _UI_CACHE["skills"][slot][0] != cdl:
                    _UI_CACHE["skills"][slot][0] = cdl
                    _UI_CACHE["skills"][slot][1] = _UI_CACHE["yel_square"].subsurface((0, 0,
                                                                                       cdl, 60))
                data.append((_UI_CACHE["skills"][slot][1],
                             (x_pos + UI_SKILLS_PANEL_OFFSET, y_pos + 2)))
                if SYSTEM["options"]["display_cd"]:
                    if _UI_CACHE["skills"][slot][2] != cdc:
                        _UI_CACHE["skills"][slot][2] = cdc
                        _UI_CACHE["skills"][slot][3] = Text(str(round(cdc, 1)) if cdc < 1
                                                            else str(int(round(cdc))),
                                                            font="item_desc", size=20,
                                                            default_color=ORANGE)
                dx = x_pos + 35 - _UI_CACHE["skills"][slot][3].width // 2
                dy = y_pos + 30 - _UI_CACHE["skills"][slot][3].height // 2
                data.append((_UI_CACHE["skills"][slot][3].surface, (dx, dy)))
    return data

def draw_boss():
    """Draws the boss life bar."""
    if SYSTEM["level"] is None or SYSTEM["level"].boss is None or \
        SYSTEM["level"].current_wave != SYSTEM["level"].waves or \
        SYSTEM["level"].boss not in ENNEMY_TRACKER:
        return []
    data = []
    life = SYSTEM["level"].boss.creature.stats["life"].current_value /\
        SYSTEM["level"].boss.creature.stats["life"].c_value
    w = life * 1680
    boss = SYSTEM["images"]["boss_jauge"].image.subsurface((0, 0, w, 100))
    txt = Text(trad('enemies', SYSTEM["level"].boss.creature.name), size=30, font="item_titles_alt")
    hp = Text(f'{round(SYSTEM["level"].boss.creature.stats["life"].current_value)}' + \
              f'/{round(SYSTEM["level"].boss.creature.stats["life"].c_value)}',
              size=30, font="item_desc")
    data.append((SYSTEM["images"]["boss_jauge_back"].image, (150, 30)))
    data.append((boss, (150, 30)))
    data.append((txt.image, (170, 20)))
    data.append((hp.image, (170 + 1680 - hp.width, 20)))
    buffs = SYSTEM["level"].boss.creature.build_debuff_list()
    i = 0
    def_x = x = 150
    y = 100
    for buff, duration in buffs.items():
        if f"buff_{buff}" in SYSTEM["images"]:
            if i >= 10:
                i = 0
                y += 96
            x = def_x + 32 * i
            data.extend(build_buff_icon(x, y, buff, duration[0], duration[1]))
            i += 1
    return data

@lru_cache(maxsize=64)
def enemy_life(life):
    """Returns the enemy life bar (cached)"""
    return SYSTEM["images"]["enemy_jauge"].image.subsurface((0, 0, life, 50))

def draw_enemy_card():
    """Draws the enemy's details."""
    if SYSTEM["mouse_target"] is None or SYSTEM["mouse_target"] == SYSTEM["level"].boss\
        or SYSTEM["options"]["show_cards"] is False:
        return []
    data = []
    enemy = SYSTEM["mouse_target"]
    life = min(max(enemy.creature.stats["life"].current_value /\
               enemy.creature.stats["life"].c_value * 300, 0), 300)
    img = enemy_life(round(life))
    txt = Text(trad('enemies', enemy.creature.name), size=23,
               font="item_desc", default_color=RED_WEAK)
    hp = Text(f'{round(enemy.creature.stats["life"].current_value)}' + \
              f'/{round(enemy.creature.stats["life"].c_value)}', size=23, font="item_desc",\
                default_color=RED_WEAK)
    if SYSTEM["level"] is None or SYSTEM["level"].boss is None or\
        SYSTEM["level"].current_wave != SYSTEM["level"].waves:
        pos = (SCREEN_WIDTH / 2 - SYSTEM["images"]["enemy_jauge_back"].width / 2, 80)
        c_pos = (SCREEN_WIDTH / 2 - SYSTEM["images"]["enemy_jauge_back"].width / 2, 0)
        name_pos = (SCREEN_WIDTH / 2 - txt.width / 2, 70)
        hp_pos = (SCREEN_WIDTH / 2 - hp.width / 2, 140)
    else:
        pos = (SCREEN_WIDTH / 2 - SYSTEM["images"]["enemy_jauge_back"].width / 2, 190)
        c_pos = (SCREEN_WIDTH / 2 - SYSTEM["images"]["enemy_jauge_back"].width / 2, 110)
        name_pos = (SCREEN_WIDTH / 2 - txt.width / 2, 180)
        hp_pos = (SCREEN_WIDTH / 2 - hp.width / 2, 250)
    data.append((SYSTEM["images"]["enemy_card"].image, c_pos))
    data.append((SYSTEM["images"]["enemy_jauge_back"].image, pos))
    data.append((img, pos))
    data.append((txt.image, name_pos))
    data.append((hp.image, hp_pos))
    buffs = enemy.creature.build_debuff_list()
    i = 0
    def_x = x = pos[0]
    y = pos[1] + 40
    for buff, duration in buffs.items():
        if f"buff_mini_{buff}" in SYSTEM["images"]:
            if i >= 5:
                i = 0
                y += 96
            x = def_x + 32 * i
            data.extend(build_buff_icon(x, y, f"mini_{buff}", duration[0], duration[1], False))
            i += 1
    return data

def draw_ui():
    """Draws the user interface."""
    SYSTEM["images"]["enemy_card"].tick()
    UPDATE_COUNTER[0] += 1
    if UPDATE_COUNTER[0] < 5:
        return
    UPDATE_COUNTER[0] = 0
    to_draw = []
    to_draw.extend(draw_life_mana())
    to_draw.extend(draw_exp_bar())
    to_draw.extend(draw_skills())
    to_draw.extend(draw_buffs())
    to_draw.extend(draw_enemy_card())
    to_draw.extend(draw_boss())
    SYSTEM["layers"]["ui"].clear()
    SYSTEM["layers"]["ui"].extend(SYSTEM["ui_background"])
    SYSTEM["layers"]["ui"].extend(to_draw)
    SYSTEM["layers"]["ui"].extend(SYSTEM["ui_foreground"])
    SYSTEM["layers"]["ui"].extend(draw_text())
