"""File for drawing in game UI, such as the skill bar,
exp bar, enemy life, boss life ..."""

from functools import lru_cache

from data.api.surface import Surface

from data.image.text import Text
from data.constants import SYSTEM, SCREEN_HEIGHT, SCREEN_WIDTH, K_1, K_2, trad, ENNEMY_TRACKER
from data.image.textgenerator import make_text

UI_SKILLS_OFFSET = 650
UI_SKILLS_PANEL_OFFSET = 2
UI_SKILLS_INPUT_OFFSET = 48

UPDATE_COUNTER = [5]

RED = (150, 0, 0)
BLACK = (0, 0, 0, 0)

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
    SYSTEM["ui_background"].fill(BLACK)
    char = SYSTEM["player"]
    data = []
    #POTIONS
    data.append((SYSTEM["images"]["item_bottom"].image, (524, SCREEN_HEIGHT - 130)))
    data.append((SYSTEM["images"]["life_potion"].get_image(), (524, SCREEN_HEIGHT - 130)))
    data.append((SYSTEM["images"]["item_bottom"].image,\
                        (SCREEN_WIDTH - 588, SCREEN_HEIGHT - 130)))
    data.append((SYSTEM["images"]["mana_potion"].get_image(),\
                        (SCREEN_WIDTH - 588, SCREEN_HEIGHT - 130)))
    #EXP
    data.append((SYSTEM["images"]["exp_bar2"].image, (210, SCREEN_HEIGHT - 60)))
    #SKILLS
    i = 0
    for _ in char.equipped_spells:
        data.append((SYSTEM["images"]["skill_bottom"].image,\
            (UI_SKILLS_OFFSET + 104 * i, SCREEN_HEIGHT - 130)))
        i += 1
    #
    SYSTEM["ui_background"].blits(data)

def generate_foreground():
    """Generates the foreground of the UI. To be called only once when 
    the level loads !"""
    SYSTEM["ui_foreground"].fill((0,0,0,0))
    char = SYSTEM["player"]
    data = []
    #POTIONS
    data.append((SYSTEM["images"]["item_top"].image, (524, SCREEN_HEIGHT - 130)))
    data.append((SYSTEM["images"][K_1].image, (508, SCREEN_HEIGHT - 82)))
    data.append((SYSTEM["images"]["item_top"].image,\
                           (SCREEN_WIDTH - 588, SCREEN_HEIGHT - 130)))
    data.append((SYSTEM["images"][K_2].image, (SCREEN_WIDTH - 540, SCREEN_HEIGHT - 82)))
    #EXP
    data.append((SYSTEM["images"]["exp_bar"].image, (210, SCREEN_HEIGHT - 60)))
    #SKILLS
    i = 0
    for name, _ in char.equipped_spells.items():
        data.append((SYSTEM["images"]["skill_top"].image, (UI_SKILLS_OFFSET + 104 * i,\
            SCREEN_HEIGHT - 130)))
        data.append((SYSTEM["images"][SYSTEM["key_chart"][name][0]].image,\
            (UI_SKILLS_OFFSET + UI_SKILLS_INPUT_OFFSET + 104 * i,SCREEN_HEIGHT - 82)))
        i += 1
    #
    SYSTEM["ui_foreground"].blits(data)

def draw_exp_bar():
    """Draws the EXP bar."""
    data = []
    char = SYSTEM["player"]
    exp_len = char.creature.exp / char.creature.exp_to_next * 1434
    exp_len = min(max(exp_len, 0), 1433)
    c = SYSTEM["images"]["exp_jauge"].image.subsurface((0, 0, exp_len, 9))
    data.append((c, (243, SCREEN_HEIGHT - 39)))
    return data

def draw_life_mana():
    """Draws the life and mana orbs."""
    char = SYSTEM["player"]
    current_mana = char.creature.stats["mana"].current_value
    max_mana = char.creature.stats["mana"].get_value()
    current_life = char.creature.stats["life"].current_value
    max_life = char.creature.stats["life"].get_value()
    if (_UI_CACHE['last_life'] != current_life or 
        _UI_CACHE['last_life_max'] != max_life):
        _UI_CACHE['last_life'] = current_life
        _UI_CACHE['last_life_max'] = max_life
        _UI_CACHE['life_text'] = Text(
            f"#c#(0, 37, 97){round(current_life)}/{max_life}"
        )
    if (_UI_CACHE['last_mana'] != current_mana or 
        _UI_CACHE['last_mana_max'] != max_mana):
        _UI_CACHE['last_mana'] = current_mana
        _UI_CACHE['last_mana_max'] = max_mana
        _UI_CACHE['mana_text'] = Text(
            f"#c#(97, 0, 0){round(current_mana)}/{max_mana}"
        )
    data = []
    mana_frame = 8 - int(current_mana / max_mana * 8)
    life_frame = 8 - int(current_life / max_life * 8)
    SYSTEM["images"]["life_jauge"].frame = life_frame
    SYSTEM["images"]["mana_jauge"].frame = mana_frame
    data.append((SYSTEM["images"]["life_jauge"].get_image(), (380, SCREEN_HEIGHT - 200)))
    data.append((SYSTEM["images"]["mana_jauge"].get_image(),
                 (SCREEN_WIDTH - 524, SCREEN_HEIGHT - 200)))
    life_buff = _UI_CACHE['life_text']
    mana_buff = _UI_CACHE['mana_text']
    life_size_img = SYSTEM["images"]["life_jauge"].get_image().get_size()
    mana_size_img = SYSTEM["images"]["mana_jauge"].get_image().get_size()
    life_size = life_buff.get_size()
    mana_size = mana_buff.get_size()
    life_center = (380 + life_size_img[0] / 2 - life_size[0] / 2,
                   SCREEN_HEIGHT - 200 + life_size_img[1] / 2 - life_size[1] / 2)
    mana_center = (SCREEN_WIDTH - 524 + mana_size_img[0] / 2 - mana_size[0] / 2,
                   SCREEN_HEIGHT - 200 + mana_size_img[1] / 2 - mana_size[1] / 2)
    data.append((life_buff.surface, life_center))
    data.append((mana_buff.surface, mana_center))
    return data

def draw_potions():
    """Draw the potions icons and use count."""
    char = SYSTEM["player"]
    if _UI_CACHE['last_potion_counts'] != tuple(char.potions):
        _UI_CACHE['last_potion_counts'] = tuple(char.potions)
        _UI_CACHE['potion_texts'][0] = Text(f"{char.potions[0]}")
        _UI_CACHE['potion_texts'][1] = Text(f"{char.potions[1]}")
    data = []
    data.append((_UI_CACHE['potion_texts'][0].surface, (572, SCREEN_HEIGHT - 82)))
    data.append((_UI_CACHE['potion_texts'][1].surface, (SCREEN_WIDTH - 604, SCREEN_HEIGHT - 82)))
    return data

def draw_buffs():
    """Draws the buff list.
    TODO: Multiple line supports, maybe backgrounds ?"""
    data = []
    buffs = SYSTEM["player"].creature.build_debuff_list()
    i = 0
    x = 64
    y = SCREEN_HEIGHT - 96
    for buff, duration in buffs.items():
        if f"buff_{buff}" in SYSTEM["images"]:
            SYSTEM["images"][f"buff_{buff}"].opacity(duration[0])
            data.append((SYSTEM["images"][f"buff_{buff}"].image, (x + i * 64, y)))
            if duration[1] > 1:
                txt = make_text(f"{duration[1]}", size=30)
                data.append((txt.surface,
                            (x + i * 64 - txt.width / 2 + 32, y - txt.height / 2 + 32)))
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
            s = Surface(int(cdl), 60)
            s.set_alpha(128)
            s.fill((255, 196, 0))
            s2 = Surface(60, 60)
            s2.set_alpha(128 if oom else 0)
            s2.fill((255, 0, 0))
            x_pos = UI_SKILLS_OFFSET + 104 * i
            y_pos = SCREEN_HEIGHT - 130
            data.append((spell.icon.get_image(), (x_pos, y_pos)))
            data.append((s2, (x_pos + UI_SKILLS_PANEL_OFFSET, y_pos + 2)))
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
              f'/{round(SYSTEM["level"].boss.creature.stats["life"].c_value)}', size=30, font="item_desc")
    data.append((SYSTEM["images"]["boss_jauge_back"].image, (150, 30)))
    data.append((boss, (150, 30)))
    data.append((txt.image, (170, 20)))
    data.append((hp.image, (170 + 1680 - hp.width, 20)))
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
    txt = Text(trad('enemies', enemy.creature.name), size=23, font="item_desc", default_color=RED)
    hp = Text(f'{round(enemy.creature.stats["life"].current_value)}' + \
              f'/{round(enemy.creature.stats["life"].c_value)}', size=23, font="item_desc",\
                default_color=RED)
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
    to_draw.extend(draw_potions())
    to_draw.extend(draw_exp_bar())
    to_draw.extend(draw_skills())
    to_draw.extend(draw_buffs())
    to_draw.extend(draw_enemy_card())
    to_draw.extend(draw_boss())
    SYSTEM["ui_surface"].fill((0,0,0,0))
    SYSTEM["ui_surface"].blit(SYSTEM["ui_background"], (0, 0), True)
    SYSTEM["ui_surface"].blits(to_draw)
    SYSTEM["ui_surface"].blit(SYSTEM["ui_foreground"], (0, 0), True)
