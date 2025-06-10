"""File for drawing in game UI, such as the skill bar,
exp bar, enemy life, boss life ..."""

import pygame
from pygame.constants import K_1, K_2
from data.constants import SYSTEM, SCREEN_HEIGHT, SCREEN_WIDTH

UI_SKILLS_OFFSET = 650
UI_SKILLS_PANEL_OFFSET = 2
UI_SKILLS_INPUT_OFFSET = 48

def draw_exp_bar():
    """Draws the EXP bar."""
    char = SYSTEM["player"]
    SYSTEM["windows"].blit(SYSTEM["images"]["exp_bar2"].image, (210, SCREEN_HEIGHT - 60))
    exp_len = char.creature.exp / char.creature.exp_to_next * 1434
    exp_len = max(exp_len, 0)
    c = pygame.transform.scale(SYSTEM["images"]["exp_jauge"].image, (exp_len, 9))
    SYSTEM["windows"].blit(c, (243, SCREEN_HEIGHT - 39))
    SYSTEM["windows"].blit(SYSTEM["images"]["exp_bar"].image, (210, SCREEN_HEIGHT - 60))

def draw_life_mana():
    """Draws the life and mana orbs."""
    char = SYSTEM["player"]
    mana = 8 - int(char.creature.stats["mana"].current_value\
                   / char.creature.stats["mana"].get_value() * 8)
    life = 8 - int(char.creature.stats["life"].current_value\
                   / char.creature.stats["life"].get_value() * 8)

    SYSTEM["images"]["life_jauge"].frame = life
    SYSTEM["images"]["mana_jauge"].frame = mana

    SYSTEM["windows"].blit(SYSTEM["images"]["life_jauge"].get_image(), (380, SCREEN_HEIGHT - 200))
    SYSTEM["windows"].blit(SYSTEM["images"]["mana_jauge"].get_image(),\
                           (SCREEN_WIDTH - 524, SCREEN_HEIGHT - 200))

    life_buff = f"{round(char.creature.stats['life'].current_value)}"\
        + f"/{char.creature.stats['life'].get_value()}"
    mana_buff = f"{round(char.creature.stats['mana'].current_value)}"\
        + f"/{char.creature.stats['mana'].get_value()}"

    text_life = SYSTEM["font_crit"].render(life_buff, False, (0, 37, 97))
    text_mana = SYSTEM["font_crit"].render(mana_buff, False, (97, 0, 0))

    SYSTEM["windows"].blit(text_life, (400, SCREEN_HEIGHT - 165))
    SYSTEM["windows"].blit(text_mana, (SCREEN_WIDTH - 510, SCREEN_HEIGHT - 165))

def draw_potions():
    """Draw the potions icons and use count."""
    char = SYSTEM["player"]
    #Life potions
    SYSTEM["windows"].blit(SYSTEM["images"]["item_bottom"].image, (524, SCREEN_HEIGHT - 130))
    SYSTEM["windows"].blit(SYSTEM["images"]["life_potion"].get_image(), (524, SCREEN_HEIGHT - 130))
    life_amount = SYSTEM["font_crit"].render(f'x{char.potions[0]}', False, (255, 255, 255))
    SYSTEM["windows"].blit(SYSTEM["images"]["item_top"].image, (524, SCREEN_HEIGHT - 130))
    SYSTEM["windows"].blit(SYSTEM["images"][K_1], (508, SCREEN_HEIGHT - 82))
    SYSTEM["windows"].blit(life_amount, (572, SCREEN_HEIGHT - 82))
    #Mana potions
    SYSTEM["windows"].blit(SYSTEM["images"]["item_bottom"].image,\
                        (SCREEN_WIDTH - 588, SCREEN_HEIGHT - 130))
    SYSTEM["windows"].blit(SYSTEM["images"]["mana_potion"].get_image(),\
                        (SCREEN_WIDTH - 588, SCREEN_HEIGHT - 130))
    mana_amount = SYSTEM["font_crit"].render(f'x{char.potions[1]}', False, (255, 255, 255))
    SYSTEM["windows"].blit(SYSTEM["images"]["item_top"].image,\
                           (SCREEN_WIDTH - 588, SCREEN_HEIGHT - 130))
    SYSTEM["windows"].blit(SYSTEM["images"][K_2], (SCREEN_WIDTH - 540, SCREEN_HEIGHT - 82))
    SYSTEM["windows"].blit(mana_amount, (SCREEN_WIDTH - 604, SCREEN_HEIGHT - 82))

def draw_skills():
    """Draws the skill bar."""
    i = 0
    char = SYSTEM["player"]
    for name, skill in char.equipped_spells.items():
        SYSTEM["windows"].blit(SYSTEM["images"]["skill_bottom"].image,\
            (UI_SKILLS_OFFSET + 104 * i, SCREEN_HEIGHT - 130))
        if skill is not None:
            cdc = skill.cooldown
            cdm = skill.stats["cooldown"].get_value()
            cdl = cdc / cdm * 60
            oom = bool(char.creature.get_efficient_value(skill.stats["mana_cost"]\
                .get_value()) > char.creature.stats["mana"].current_value)
            s = pygame.Surface((cdl, 60))
            s.set_alpha(128)
            s.fill((255, 196, 0))
            s2 = pygame.Surface((60, 60))
            s2.set_alpha(128 if oom else 0)
            s2.fill((255, 0, 0))
            SYSTEM["windows"].blit(skill.icon.get_image(),\
                (UI_SKILLS_OFFSET + 104 * i, SCREEN_HEIGHT - 130))
            SYSTEM["windows"].blit(s2, (UI_SKILLS_OFFSET + UI_SKILLS_PANEL_OFFSET + 104 * i,\
                SCREEN_HEIGHT - 128))
            SYSTEM["windows"].blit(s, (UI_SKILLS_OFFSET + UI_SKILLS_PANEL_OFFSET + 104 * i,\
                SCREEN_HEIGHT - 128))
        SYSTEM["windows"].blit(SYSTEM["images"]["skill_top"].image, (UI_SKILLS_OFFSET + 104 * i,\
            SCREEN_HEIGHT - 130))
        SYSTEM["windows"].blit(SYSTEM["images"][name], (UI_SKILLS_OFFSET + UI_SKILLS_INPUT_OFFSET\
            + 104 * i,SCREEN_HEIGHT - 82))
        i += 1

def draw_ui(boss_here = False, boss = None):
    """Draws the user interface."""
    draw_life_mana()
    draw_potions()
    draw_exp_bar()
    draw_skills()
    #Boss life bar
    if boss_here:
        boss_name = SYSTEM["font_crit"].render(f'{boss.creature.name}',\
                                      False, (255, 255, 255))
        bossl = (boss.creature.stats["life"].current_value/boss.creature.stats["life"].c_value) * 1500
        b = pygame.transform.scale(SYSTEM["images"]["boss_jauge"].image, (bossl, 80))
        bb = pygame.transform.scale(SYSTEM["images"]["boss_jauge_back"].image, (1500, 80))
        SYSTEM["windows"].blit(bb, (200, 20))
        SYSTEM["windows"].blit(b, (200, 20))
        SYSTEM["windows"].blit(boss_name, (200, 20))