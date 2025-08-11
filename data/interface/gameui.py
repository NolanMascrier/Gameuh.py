"""File for drawing in game UI, such as the skill bar,
exp bar, enemy life, boss life ..."""

import pygame
from data.image.text import Text
from data.constants import SYSTEM, SCREEN_HEIGHT, SCREEN_WIDTH, K_1, K_2
from data.interface.render import renders

UI_SKILLS_OFFSET = 650
UI_SKILLS_PANEL_OFFSET = 2
UI_SKILLS_INPUT_OFFSET = 48

DYNAMIC    = []

def generate_background():
    """Generates the background surface of the UI. To be called only once when the
    level loads !"""
    SYSTEM["ui_background"].fill((0,0,0,0))
    char = SYSTEM["player"]
    data = []
    #POTIONS
    data.append((SYSTEM["images"]["item_bottom"].image, (524, SCREEN_HEIGHT - 130)))
    data.append((SYSTEM["images"]["life_potion"].get_image(), (524, SCREEN_HEIGHT - 130)))
    data.append((SYSTEM["images"]["item_bottom"].image,\
                        (SCREEN_WIDTH - 588, SCREEN_HEIGHT - 130)))
    data.append((SYSTEM["images"]["mana_potion"].get_image(),\
                        (SCREEN_WIDTH - 588, SCREEN_HEIGHT - 130)))
    #GOLD
    data.append((SYSTEM["images"]["gold_icon"].image, (10, 10)))
    #EXP
    data.append((SYSTEM["images"]["exp_bar2"].image, (210, SCREEN_HEIGHT - 60)))
    #SKILLS
    i = 0
    for name, _ in char.equipped_spells.items():
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
    data.append((SYSTEM["images"][K_1], (508, SCREEN_HEIGHT - 82)))
    data.append((SYSTEM["images"]["item_top"].image,\
                           (SCREEN_WIDTH - 588, SCREEN_HEIGHT - 130)))
    data.append((SYSTEM["images"][K_2], (SCREEN_WIDTH - 540, SCREEN_HEIGHT - 82)))
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

def draw_gold():
    """Draws the gold and item counter."""
    data = []
    gold = SYSTEM["level"].gold
    text = Text(f"#c#(255, 179, 0){gold}")
    data.append((text.surface, (80, 42)))
    return data

def draw_exp_bar():
    """Draws the EXP bar."""
    data = []
    char = SYSTEM["player"]
    exp_len = char.creature.exp / char.creature.exp_to_next * 1434
    exp_len = min(max(exp_len, 0), SYSTEM["images"]["exp_jauge"].width - 1)
    #c = pygame.transform.scale(SYSTEM["images"]["exp_jauge"].image, (exp_len, 9))
    c = SYSTEM["images"]["exp_jauge"].image.subsurface(0, 0, exp_len, 9)
    data.append((c, (243, SCREEN_HEIGHT - 39)))
    return data

def draw_life_mana():
    """Draws the life and mana orbs."""
    data = []
    char = SYSTEM["player"]
    mana = 8 - int(char.creature.stats["mana"].current_value\
                   / char.creature.stats["mana"].get_value() * 8)
    life = 8 - int(char.creature.stats["life"].current_value\
                   / char.creature.stats["life"].get_value() * 8)

    SYSTEM["images"]["life_jauge"].frame = life
    SYSTEM["images"]["mana_jauge"].frame = mana

    data.append((SYSTEM["images"]["life_jauge"].get_image(), (380, SCREEN_HEIGHT - 200)))
    data.append((SYSTEM["images"]["mana_jauge"].get_image(),\
                           (SCREEN_WIDTH - 524, SCREEN_HEIGHT - 200)))

    life_buff = Text(f"#c#(0, 37, 97){round(char.creature.stats['life'].current_value)}"\
        + f"/{char.creature.stats['life'].get_value()}")
    mana_buff = Text(f"#c#(97, 0, 0){round(char.creature.stats['mana'].current_value)}"\
        + f"/{char.creature.stats['mana'].get_value()}")

    life_size_img = SYSTEM["images"]["life_jauge"].get_image().get_size()
    mana_size_img = SYSTEM["images"]["mana_jauge"].get_image().get_size()
    life_size = life_buff.get_size()
    mana_size = mana_buff.get_size()
    life_center = (380 + life_size_img[0] / 2 - life_size[0] / 2,\
                   SCREEN_HEIGHT - 200 + life_size_img[1] / 2 - life_size[1] / 2)
    mana_center = (SCREEN_WIDTH - 524 + mana_size_img[0] / 2 - mana_size[0] / 2,\
                   SCREEN_HEIGHT - 200 + mana_size_img[1] / 2 - mana_size[1] / 2)

    data.append((life_buff.surface, life_center))
    data.append((mana_buff.surface, mana_center))
    return data

def draw_potions():
    """Draw the potions icons and use count."""
    data = []
    char = SYSTEM["player"]
    #Life potions
    life_amount = Text(f"{char.potions[0]}")
    data.append((life_amount.surface, (572, SCREEN_HEIGHT - 82)))
    #Mana potions
    mana_amount = Text(f"{char.potions[1]}")
    data.append((mana_amount.surface, (SCREEN_WIDTH - 604, SCREEN_HEIGHT - 82)))
    return data

def draw_skills():
    """Draws the skill bar."""
    data = []
    i = 0
    char = SYSTEM["player"]
    for name, skill in char.equipped_spells.items():
        spell = SYSTEM["spells"][skill]
        if spell is not None:
            cdc = spell.cooldown
            cdm = spell.stats["cooldown"].get_value()
            cdl = cdc / cdm * 60
            oom = bool(char.creature.get_efficient_value(spell.stats["mana_cost"]\
                .get_value()) > char.creature.stats["mana"].current_value)
            s = pygame.Surface((cdl, 60))
            s.set_alpha(128)
            s.fill((255, 196, 0))
            s2 = pygame.Surface((60, 60))
            s2.set_alpha(128 if oom else 0)
            s2.fill((255, 0, 0))
            data.append((spell.icon.get_image(),\
                (UI_SKILLS_OFFSET + 104 * i, SCREEN_HEIGHT - 130)))
            data.append((s2, (UI_SKILLS_OFFSET + UI_SKILLS_PANEL_OFFSET + 104 * i,\
                SCREEN_HEIGHT - 128)))
            data.append((s, (UI_SKILLS_OFFSET + UI_SKILLS_PANEL_OFFSET + 104 * i,\
                SCREEN_HEIGHT - 128)))
        i += 1
    return data

def draw_ui(boss_here = False, boss = None):
    """Draws the user interface."""
    SYSTEM["ui_surface"].fill((0,0,0,0))
    to_draw = []
    to_draw.extend(draw_life_mana())
    to_draw.extend(draw_potions())
    to_draw.extend(draw_exp_bar())
    to_draw.extend(draw_skills())
    to_draw.extend(draw_gold())
    SYSTEM["ui_surface"].blit(SYSTEM["ui_background"], (0, 0))
    SYSTEM["ui_surface"].blits(to_draw)
    SYSTEM["ui_surface"].blit(SYSTEM["ui_foreground"], (0, 0))
