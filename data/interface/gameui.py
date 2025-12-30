"""File for drawing in game UI, such as the skill bar,
exp bar, enemy life, boss life ..."""

from functools import lru_cache

from data.api.surface import Surface
from data.api.keycodes import KEY_EVENT, K_1, K_2

from data.image.text import Text
from data.constants import SYSTEM, SCREEN_HEIGHT, SCREEN_WIDTH, trad, ENNEMY_TRACKER, \
    RED_WEAK, YELLOW
from data.image.textgenerator import make_text

UI_SKILLS_OFFSET = 400
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
    'potion_texts': [None, None]
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
    reserved_mana = char["mana"].get_reserved_prop()
    mana_dh = round((current_mana / max_mana) * 198)
    mana_dy = 198 - mana_dh
    mana_r_dh = 198 - round((reserved_mana / max_mana) * 198)
    mana_orb = SYSTEM["images"]["ui_orb_mana"].extracts(0, mana_dy, 198, mana_dh)
    mana_res = SYSTEM["images"]["ui_orb_reserv"].extracts(0, 0, 198, 198 - mana_r_dh)

    max_life = char["life"].get_value()
    current_life = max(min(char["life"].current_value, max_life), 0)
    reserved_life = char["life"].get_reserved_prop()
    life_dh = round((current_life / max_life) * 198)
    life_dy = 198 - life_dh
    life_r_dh = 198 - round((reserved_life / max_life) * 198)
    life_orb = SYSTEM["images"]["ui_orb_life"].extracts(0, life_dy, 198, life_dh)
    life_res = SYSTEM["images"]["ui_orb_reserv"].extracts(0, 0, 198, 198 - life_r_dh)

    data.append((life_orb.image, (90, SCREEN_HEIGHT - 201 + life_dy)))
    data.append((life_res.image, (90, SCREEN_HEIGHT - 201)))
    data.append((mana_orb.image, (SCREEN_WIDTH - 288, SCREEN_HEIGHT - 201 + mana_dy)))
    data.append((mana_res.image, (SCREEN_WIDTH - 288, SCREEN_HEIGHT - 201)))
    return data

def draw_potions():
    """Draw the potions icons and use count."""
    char = SYSTEM["player"]
    if _UI_CACHE['last_potion_counts'] != tuple(char.potions):
        _UI_CACHE['last_potion_counts'] = tuple(char.potions)
        _UI_CACHE['potion_texts'][0] = Text(f"{int(char.potions[0])}", size=30, font="item_desc")
        _UI_CACHE['potion_texts'][1] = Text(f"{int(char.potions[1])}", size=30, font="item_desc")
    data = []
    life_off = _UI_CACHE['potion_texts'][0].width // 2
    mana_off = _UI_CACHE['potion_texts'][1].width // 2
    data.append((_UI_CACHE['potion_texts'][0].surface,
                 (POTION_OFFSET - life_off, SCREEN_HEIGHT - 42)))
    data.append((_UI_CACHE['potion_texts'][1].surface,
                 (POTION_OFFSET_REV + 32 - mana_off, SCREEN_HEIGHT - 42)))
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
    def_x = x = 16
    y = SCREEN_HEIGHT - 96
    for buff, duration in buffs.items():
        if f"buff_{buff}" in SYSTEM["images"]:
            if i >= 3:
                i = 0
                y -= 96
            x = def_x + 32 * i
            data.extend(build_buff_icon(x, y, buff, duration[0], duration[1]))
            i += 1
    return data

def draw_skills():
    """Draws the skill bar."""
    data = []
    char = SYSTEM["player"]
    skill_items = list(char.equipped_spells.items())
    for i, (_, skill) in enumerate(skill_items):
        spell = SYSTEM["spells"][skill]
        if spell is not None:
            cdc = spell.cooldown
            cdm = spell.stats["cooldown"].get_value()
            cdl = cdc / cdm * 60
            oom = bool(char.creature.get_efficient_value(spell.stats["mana_cost"]\
                .get_value()) > char.creature.stats["mana"].current_value)
            x_pos = UI_SKILLS_OFFSET + 104 * i
            y_pos = SCREEN_HEIGHT - 100
            data.append((spell.icon.get_image(), (x_pos, y_pos)))
            if oom:
                s2 = Surface(60, 60)
                s2.set_alpha(128)
                s2.fill(RED_WEAK)
                data.append((s2, (x_pos + UI_SKILLS_PANEL_OFFSET, y_pos + 2)))
            if cdc > 0:
                s = Surface(int(cdl), 60)
                s.set_alpha(128)
                s.fill(YELLOW)
                data.append((s, (x_pos + UI_SKILLS_PANEL_OFFSET, y_pos + 2)))
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
    life = max(enemy.creature.stats["life"].current_value /\
               enemy.creature.stats["life"].c_value * 300, 0)
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
    SYSTEM["layers"]["ui"].extend(draw_potions())
