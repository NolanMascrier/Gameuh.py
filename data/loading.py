"""Handles the loading."""

import threading
import re
import os
import random
import pygame
from pygame.constants import K_q, K_e, K_r, K_f, K_t, K_1, K_2, K_LSHIFT
from data.constants import SYSTEM, SCREEN_HEIGHT, SCREEN_WIDTH, MENU_MAIN, GAME_LEVEL,\
    RESSOURCES, ENNEMY_TRACKER, POWER_UP_TRACKER, trad,\
    PROJECTILE_TRACKER, TEXT_TRACKER, WAVE_TIMER, USEREVENT, TICKER_TIMER, load_options,\
    change_language, UPDATE_TIMER
from data.image.animation import Animation, Image
from data.image.button import Button
from data.image.tile import Tile
from data.image.parallaxe import Parallaxe
from data.image.scrollable import Scrollable
from data.image.text_generator import TextGenerator, Text
from data.image.slotpanel import SlotPanel

from data.game.lootgenerator import LootGenerator
from data.interface.general import setup_bottom_bar
from data.interface.gear import open_gear_screen
from data.interface.spellbook import open_spell_screen
from data.interface.skilltree import open_skill_screen
from data.interface.inventory import open_inventory
from data.interface.options import open_option_screen
from data.interface.gameui import generate_foreground, generate_background
from data.game.level import Level

from data.character import Character
from data.tables.spell_table import generate_spell_list
from data.tables.skilltree_table import generate_tree

from data.image.posteffects import PostEffects

def generate_random_level():
    """Creates a random level."""
    area_lvl = max(SYSTEM["player"].creature.level + random.randint(-3, 5), 0)
    zone = random.randint(0, 3)
    match zone:
        case 0:
            area = SYSTEM["sunrise"]
            icon = SYSTEM["images"]["sunrise_icon"]
            name = "Red mountain of Doom"
        case 1:
            area = SYSTEM["cybercity"]
            icon = SYSTEM["images"]["city_icon"]
            name = "City of the Night"
        case 2:
            area = SYSTEM["forest"]
            icon = SYSTEM["images"]["forest_icon"]
            name = "Forest of things"
        case 3:
            area = SYSTEM["mountains"]
            icon = SYSTEM["images"]["mount_icon"]
            name = "Above the sky"
    level = Level(name, area_lvl, icon, 6000, area)
    return level

def reset():
    """Resets the game's status"""
    SYSTEM["selected"] = None
    SYSTEM["player"].reset()
    ENNEMY_TRACKER.clear()
    PROJECTILE_TRACKER.clear()
    POWER_UP_TRACKER.clear()
    PROJECTILE_TRACKER.clear()
    TEXT_TRACKER.clear()
    levels = []
    SYSTEM["buttons_e"] = []
    for _ in range(4):
        levels.append(generate_random_level())
    for i in range(4):
        butt = Button(levels[i].icon, None, lambda i=i:SYSTEM.__setitem__("selected",\
                                             levels[i]))
        SYSTEM["buttons_e"].append(butt)
    init_timers()
    setup_bottom_bar()

def init_timers():
    """Inits Pygame's timers."""
    pygame.time.set_timer(WAVE_TIMER, 1000)
    pygame.time.set_timer(USEREVENT+1, 2000)
    pygame.time.set_timer(USEREVENT+2, 100)
    pygame.time.set_timer(TICKER_TIMER, int(0.016 * 1000))
    pygame.time.set_timer(UPDATE_TIMER, int(SYSTEM["options"]["fps"]))

def start_level():
    """Starts the level stored in the SYSTEM."""
    if SYSTEM["selected"] is None:
        return
    SYSTEM["player"].reset()
    generate_background()
    generate_foreground()
    SYSTEM["level"] = SYSTEM["selected"]
    SYSTEM["level"].init()
    SYSTEM["game_state"] = GAME_LEVEL
    init_timers()

def quit_level():
    """Quits the current level and resets the player."""
    SYSTEM["game_state"] = MENU_MAIN
    SYSTEM["level"] = None
    reset()

def load_fonts():
    """Loads the fonts."""
    SYSTEM["font_detail"] = pygame.freetype.Font('ressources/dmg.ttf', 30)
    SYSTEM["font_detail_small"] = pygame.freetype.Font('ressources/dmg.ttf', 30)
    SYSTEM["font_crit"] = pygame.freetype.Font('ressources/dmg.ttf', 35)
    SYSTEM["font_crit"].strong = True

def load_animations():
    """Load the animations."""
    SYSTEM["images"]["fireball"] = Animation("fireball.png", 32, 19, frame_rate=0.25).scale(38, 64)
    SYSTEM["images"]["energyball"] = Animation("pew.png", 13, 13, frame_rate=0.25).scale(32, 32)
    SYSTEM["images"]["boss_a"] = Animation("boss.png", 128, 150, frame_rate=0.25).scale(300, 256)
    SYSTEM["images"]["bouncer"] = Animation("bounce.png", 8, 8, frame_rate=0.25).scale(64, 64)
    SYSTEM["images"]["generator"] = Animation("generator.png", 8, 8, frame_rate=0.25).scale(32, 32)
    SYSTEM["images"]["lazer"] = Animation("lazor.png", 16, 10, frame_rate=0.25).scale(16, 64)
    SYSTEM["images"]["exp_orb"] = Animation("exporb.png", 8, 8, frame_rate=0.1).scale(8, 8)
    SYSTEM["images"]["mana_orb"] = Animation("manaorb.png", 16, 16, frame_rate=0.1)
    SYSTEM["images"]["life_orb"] = Animation("lifeorb.png", 16, 14, frame_rate=0.1)
    SYSTEM["images"]["life_jauge"] = Animation("life.png", 144, 144, animated=False)
    SYSTEM["images"]["mana_jauge"] = Animation("mana.png", 144, 144, animated=False)
    SYSTEM["images"]["life_potion"] = Animation("lifepot.png", 16, 16, frame_max=7,\
        frame_rate=0.2, lines=3).scale(64, 64)
    SYSTEM["images"]["mana_potion"] = Animation("manapot.png", 16, 16, frame_max=7,\
        frame_rate=0.2, lines=3).scale(64, 64)
    SYSTEM["images"]["badguy"] = Animation("badguy.png", 60, 130, frame_rate=0.25).flip(False, True)
    SYSTEM["images"]["badguy_flipped"] = Animation("badguy.png", 60, 130, frame_rate=0.25)
    SYSTEM["images"]["witch_flipped"] = Animation("witch.png", 64, 64, frame_rate = 0.25)\
        .flip(False, True)
    SYSTEM["images"]["witch"] = Animation("witch.png", 64, 64, frame_rate = 0.25)

def load_tiles():
    """Load the tiles."""
    SYSTEM["images"]["ui_normal"] = Tile("ui/border_normal.png", scale_factor=2)
    SYSTEM["images"]["ui_magic"] = Tile("ui/border_magic.png", scale_factor=2)
    SYSTEM["images"]["ui_rare"] = Tile("ui/border_rare.png", scale_factor=2)
    SYSTEM["images"]["ui_legendary"] = Tile("ui/border_legend.png", scale_factor=2)
    SYSTEM["images"]["ui_unique"] = Tile("ui/border_unique.png", scale_factor=2)
    SYSTEM["images"]["tile_panel_back"] = Tile("ui/inventory_back.png", 7, 14, 3)
    SYSTEM["images"]["tile_panel_inv"] = Tile("ui/inventory_back.png", 17, 13, 3)
    SYSTEM["images"]["hoverable"] = Tile("ui/hoverable.png")
    SYSTEM["images"]["dropdown"] = Tile("ui/inventory_back.png")
    SYSTEM["images"]["dropdown_menu"] = Tile("ui/border_unique.png")
    SYSTEM["images"]["item_desc"] = Tile("ui/hoverable.png", scale_factor=2)

def load_parallaxes():
    """Load the parallaxes."""
    SYSTEM["mountains"] = Parallaxe("parallax_field.png", 320, 180,\
        speeds = [0.2, 0.6, 1.0, 2.0, 2])
    SYSTEM["city_back"] = Parallaxe("city.png", 576, 324, speeds = [0.1, 0.0])
    SYSTEM["mount"] = Parallaxe("icemount.png", 360, 189,\
        speeds = [0.2, 0.6, 1.0, 2.0, 1, 2.5, 3, 3])
    SYSTEM["cybercity"] = Parallaxe("cybercity.png", 576, 324, speeds = [0.2, 0.5, 1, 1.2, 2])
    SYSTEM["forest"] = Parallaxe("forest.png", 680, 429, speeds = [0.0, 0.1, 0.5, 1, 1.2, 2, 2])
    SYSTEM["sunrise"] = Parallaxe("sunrise.png", 320, 240,\
        speeds = [0.0, 0.1, 0.2, 0.9, 1.0, 1.5, 1.5], scroll_left=False)

def load_buttons():
    """Load the buttons"""
    SYSTEM["buttons"]["menu_states"] = [
        lambda : SYSTEM.__setitem__("game_state", MENU_MAIN),
        open_gear_screen,
        open_spell_screen,
        open_skill_screen,
        open_inventory,
        open_option_screen
    ]
    SYSTEM["buttons"]["button_quit"] = Button(SYSTEM["images"]["btn"], SYSTEM["images"]["btn_p"],\
                                             lambda : SYSTEM.__setitem__("playing", False),\
                                             "Quit Game")
    SYSTEM["buttons"]["button_resume"] = Button(SYSTEM["images"]["btn"], SYSTEM["images"]["btn_p"],\
                                             lambda : SYSTEM.__setitem__("game_state", GAME_LEVEL),\
                                             "Resume")
    SYSTEM["buttons"]["button_abandon"] = Button(SYSTEM["images"]["btn"],\
                                            SYSTEM["images"]["btn_p"],\
                                            quit_level, "Abandon mission")
    SYSTEM["buttons"]["button_continue"] = Button(SYSTEM["images"]["btn"],\
                                            SYSTEM["images"]["btn_p"],\
                                            quit_level, "Return to base")
    SYSTEM["buttons"]["button_assault"] = Button(SYSTEM["images"]["btn"],\
                                            SYSTEM["images"]["btn_p"],\
                                             start_level, "Begin the assault !")

def load_images():
    """Loads the basic images."""
    SYSTEM["images"]["exp_bar"] = Image("exp.png")
    SYSTEM["images"]["exp_bar2"] = Image("exp_back.png")
    SYSTEM["images"]["exp_jauge"] = Image("exp_bar.png")
    SYSTEM["images"]["skill_top"] = Image("ui/skill_top.png").scale(64, 64)
    SYSTEM["images"]["skill_bottom"] = Image("ui/skill_bottom.png").scale(64, 64)
    SYSTEM["images"]["item_top"] = Image("ui/item_top.png").scale(64, 64)
    SYSTEM["images"]["slot_empty"] = Image("ui/item_top.png").scale(64, 64)
    SYSTEM["images"]["slot_magic"] = Image("ui/item_top_m.png").scale(64, 64)
    SYSTEM["images"]["slot_rare"] = Image("ui/item_top_r.png").scale(64, 64)
    SYSTEM["images"]["slot_exalted"] = Image("ui/item_top_e.png").scale(64, 64)
    SYSTEM["images"]["slot_green"] = Image("ui/item_top_g.png").scale(64, 64)
    SYSTEM["images"]["item_bottom"] = Image("ui/item_bottom.png").scale(64, 64)
    SYSTEM["images"][K_q] = Image("ui/kb_q.png")
    SYSTEM["images"][K_e] = Image("ui/kb_e.png")
    SYSTEM["images"][K_f] = Image("ui/kb_f.png")
    SYSTEM["images"][K_r] = Image("ui/kb_r.png")
    SYSTEM["images"][K_t] = Image("ui/kb_t.png")
    SYSTEM["images"][K_LSHIFT] = Image("ui/kb_shift.png")
    SYSTEM["images"][K_1] = Image("ui/kb_1.png")
    SYSTEM["images"][K_2] = Image("ui/kb_2.png")
    SYSTEM["images"]["btn"] = Image("ui/button.png").scale(55, 280)
    SYSTEM["images"]["btn_fat"] = Image("ui/button.png").scale(55, 100)
    SYSTEM["images"]["btn_fat_pressed"] = Image("ui/button_press.png").scale(55, 100)
    SYSTEM["images"]["btn_small"] = Image("ui/button.png").scale(35, 200)
    SYSTEM["images"]["btn_small_pressed"] = Image("ui/button_press.png").scale(35, 200)
    SYSTEM["images"]["btn_tab"] = Image("ui/button.png").scale(35, 100)
    SYSTEM["images"]["btn_tab_pressed"] = Image("ui/button_press.png").scale(35, 100)
    SYSTEM["images"]["btn_p"] = Image("ui/button_press.png").scale(55, 280)
    SYSTEM["images"]["menu_bg"] = Image("ui/menu.png")
    SYSTEM["images"]["menu_button"] = Image("ui/button.png").scale(55, 280)
    SYSTEM["images"]["rune_0"] = Image("icons/rune01.png")
    SYSTEM["images"]["rune_1"] = Image("icons/rune02.png")
    SYSTEM["images"]["rune_2"] = Image("icons/rune03.png")
    SYSTEM["images"]["rune_3"] = Image("icons/rune04.png")
    SYSTEM["images"]["rune_4"] = Image("icons/rune05.png")
    SYSTEM["images"]["rune_5"] = Image("icons/rune06.png")
    SYSTEM["images"]["rune_6"] = Image("icons/rune07.png")
    SYSTEM["images"]["rune_7"] = Image("icons/rune08.png")
    SYSTEM["images"]["rune_8"] = Image("icons/rune09.png")
    SYSTEM["images"]["rune_9"] = Image("icons/rune10.png")
    SYSTEM["images"]["rune_0_mini"] = Image("icons/rune01.png").scale(32, 32)
    SYSTEM["images"]["rune_1_mini"] = Image("icons/rune02.png").scale(32, 32)
    SYSTEM["images"]["rune_2_mini"] = Image("icons/rune03.png").scale(32, 32)
    SYSTEM["images"]["rune_3_mini"] = Image("icons/rune04.png").scale(32, 32)
    SYSTEM["images"]["rune_4_mini"] = Image("icons/rune05.png").scale(32, 32)
    SYSTEM["images"]["rune_5_mini"] = Image("icons/rune06.png").scale(32, 32)
    SYSTEM["images"]["rune_6_mini"] = Image("icons/rune07.png").scale(32, 32)
    SYSTEM["images"]["rune_7_mini"] = Image("icons/rune08.png").scale(32, 32)
    SYSTEM["images"]["rune_8_mini"] = Image("icons/rune09.png").scale(32, 32)
    SYSTEM["images"]["rune_9_mini"] = Image("icons/rune10.png").scale(32, 32)
    SYSTEM["images"]["char_details"] = Image("ui/char_back.png").scale(1050, 376)
    SYSTEM["images"]["panel_back"] = Image("ui/char_back.png").scale(1024, 448)
    SYSTEM["images"]["mini_moolah"] = Image("minifric.png")
    SYSTEM["images"]["moolah"] = Image("fric.png")
    SYSTEM["images"]["big_moolah"] = Image("minisuperfric.png")
    SYSTEM["images"]["super_moolah"] = Image("superfric.png")
    SYSTEM["images"]["mega_moolah"] = Image("megaminifric.png").scale(64, 64)
    SYSTEM["images"]["giga_moolah"] = Image("maximinifric.png").scale(64, 64)
    SYSTEM["images"]["terra_moolah"] = Image("megafric.png").scale(64, 64)
    SYSTEM["images"]["zeta_moolah"] = Image("maxifric.png").scale(64, 64)
    SYSTEM["images"]["supra_moolah"] = Image("grail.png").scale(64, 64)
    SYSTEM["images"]["maxi_moolah"] = Image("maxigrail.png").scale(64, 64)
    SYSTEM["images"]["gold_icon"] = Image("thune.png")
    SYSTEM["images"]["line_break"] = Image("exp.png").scale(32, 128)
    SYSTEM["images"]["mission_map"] = Image("mission.png")
    SYSTEM["images"]["boss_jauge"] = Image("life_boss.png")
    SYSTEM["images"]["gear_weapon"] = Image("ui/gear_weapon.png").scale(64, 64)
    SYSTEM["images"]["gear_offhand"] = Image("ui/gear_offhand.png").scale(64, 64)
    SYSTEM["images"]["gear_helm"] = Image("ui/gear_helm.png").scale(64, 64)
    SYSTEM["images"]["gear_boots"] = Image("ui/gear_boots.png").scale(64, 64)
    SYSTEM["images"]["gear_hands"] = Image("ui/gear_hands.png").scale(64, 64)
    SYSTEM["images"]["gear_armor"] = Image("ui/gear_armor.png").scale(64, 64)
    SYSTEM["images"]["gear_belt"] = Image("ui/gear_belt.png").scale(64, 64)
    SYSTEM["images"]["gear_ring"] = Image("ui/gear_ring.png").scale(64, 64)
    SYSTEM["images"]["gear_amulet"] = Image("ui/gear_amulet.png").scale(64, 64)
    SYSTEM["images"]["gear_relic"] = Image("ui/gear_relic.png").scale(64, 64)
    SYSTEM["images"]["test_armor"] = Image("icons/elementalfury.png").scale(64, 64)
    SYSTEM["images"]["sell_slot"] = Image("ui/gear_helm.png").scale(128, 128)
    SYSTEM["images"]["boss_jauge_back"] = Image("life_boss_back.png")
    SYSTEM["images"]["mount_icon"] = Image("icons/mount.png")
    SYSTEM["images"]["city_icon"] = Image("icons/cybercity.png")
    SYSTEM["images"]["sunrise_icon"] = Image("icons/sunrise.png")
    SYSTEM["images"]["forest_icon"] = Image("icons/forest.png")
    SYSTEM["images"]["item_bootsA"] = Image("icons/bootsA.png")
    SYSTEM["images"]["item_ringA"] = Image("icons/ringA.png")
    SYSTEM["images"]["item_armorA"] = Image("icons/armorA.png")
    SYSTEM["images"]["loot_icon"] = Image("loot.png").scale(32, 32)
    SYSTEM["images"]["tree_start"] = Image("tree/start.png").scale(64, 64)
    SYSTEM["images"]["tree_a"] = Image("tree/node2.png").scale(64, 64)
    SYSTEM["images"]["tree_b"] = Image("tree/node3.png").scale(64, 64)
    SYSTEM["images"]["skillpoints"] = Image("icons/skillpoints.png").scale(128, 128)
    SYSTEM["images"]["checkbox"] = Image("ui/checkbox.png").scale(64, 64)
    SYSTEM["images"]["checkbox_ok"] = Image("ui/checkbox_ok.png").scale(64, 64)
    SYSTEM["images"]["arrow_h"] = Image("arrow.png").scale(128, 128)
    SYSTEM["images"]["buff_elemental_fury"] = Image("icons/elemental_fury.png")
    SYSTEM["images"]["buff_fury"] = Image("icons/fury.png")
    SYSTEM["images"]["buff_celerity"] = Image("icons/celerity.png")
    SYSTEM["images"]["buff_bleed"] = Image("icons/bleed.png")

def load_icons():
    """Loads the icons."""
    corr = {
        "he": "helmets",
        "ar": "armors",
        "gl": "gloves",
        "bo": "boots",
        "be": "belts",
        "ri": "rings",
        "rel": "relics",
        "am": "amulets",
        "oh": "offhands",
        "wpn": "weapons",
        "rune": "runes",
    }
    SYSTEM["images"]["helmets"] = []
    SYSTEM["images"]["armors"] = []
    SYSTEM["images"]["gloves"] = []
    SYSTEM["images"]["boots"] = []
    SYSTEM["images"]["belts"] = []
    SYSTEM["images"]["rings"] = []
    SYSTEM["images"]["relics"] = []
    SYSTEM["images"]["amulets"] = []
    SYSTEM["images"]["offhands"] = []
    SYSTEM["images"]["weapons"] = []
    SYSTEM["images"]["runes"] = []
    pattern = re.compile(r"^(.+?)(\d+)\.png$")
    unsorted = []
    for filename in os.listdir(f"{RESSOURCES}/icons"):
        catch = pattern.match(filename)
        if catch:
            name = catch.group(1)
            number = int(catch.group(2))
            unsorted.append((name, number, filename))
    unsorted.sort(key=lambda x: (x[0], x[1]))
    for name, _, filename in unsorted:
        SYSTEM["images"][corr[name]].append(Image(f"icons/{filename}"))

def load_others():
    """Loads everything else"""
    SYSTEM["images"]["mission_scroller"] = Scrollable(100, 10, 1200, 1000,\
        contains=SYSTEM["images"]["mission_map"].image)
    SYSTEM["images"]["tree_surface"] = pygame.Surface((2000, 2000), pygame.SRCALPHA)
    SYSTEM["images"]["tree_scroller"] = Scrollable(10, 10, SCREEN_WIDTH - 110, SCREEN_HEIGHT - 200,\
        contains=SYSTEM["images"]["tree_surface"])
    generate_tree()
    SYSTEM["ui_surface"] = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
    SYSTEM["ui_background"] = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
    SYSTEM["ui_foreground"] = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
    SYSTEM["layers"] = {
        "pickup": pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA),
        "bullets": pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA),
        "characters": pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
    }

def load_start():
    """Loads the starting events."""
    SYSTEM["game_state"] = MENU_MAIN
    SYSTEM["cooldown"] = 0
    SYSTEM["looter"] = LootGenerator()
    SYSTEM["rune"] = -1
    SYSTEM["mouse"] = pygame.mouse.get_pos()
    #TODO: Put that in scene manager
    levels = []
    SYSTEM["buttons_e"] = []
    for _ in range(4):
        levels.append(generate_random_level())
    for i in range(4):
        butt = Button(levels[i].icon, None, lambda i=i:SYSTEM.__setitem__("selected",\
                                             levels[i]))
        SYSTEM["buttons_e"].append(butt)
    SYSTEM["def_panel"] = SlotPanel(SCREEN_WIDTH - 535, 10)
    SYSTEM["mouse_previous"] = SYSTEM["mouse"]

def create_character():
    """Creates the player character."""
    SYSTEM["player"] = Character(imagefile="witch")

def load():
    """Loads everything inside the system.
    Made to be threaded."""
    tasks = [
        (load_fonts, 1, "fonts"),
        (load_images, 5, "images"),
        (load_icons, 3, "icons"),
        (load_animations, 2, "animations"),
        (load_tiles, 2, "tiles"),
        (load_parallaxes, 2, "parallaxes"),
        (generate_spell_list, 4, "spells"),
        (load_others, 1, "others"),
        (load_buttons, 2, "buttons"),
        (create_character, 1, "player"),
        (load_start, 3, "start")
    ]
    total = sum(weight for _, weight, _ in tasks)
    progress = 0
    for t, w, x in tasks:
        SYSTEM["loading_text"] = Text(trad('loading', x), font="item_titles", size=30)
        t()
        progress += w
        SYSTEM["progress"] = progress / total * 100
    SYSTEM["loaded"] = True

def init_game():
    """Loads the basic data for the game."""
    os.environ['PYGAME_BLEND_ALPHA_SDL2'] = "1"
    pygame.init()
    pygame.font.init()
    SYSTEM["keys"] = pygame.key.get_pressed()
    load_options()
    change_language(SYSTEM["options"]["lang_selec"])
    SYSTEM["post_effects"] = PostEffects()
    SYSTEM["windows"] = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
    SYSTEM["gm_background"] = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
    SYSTEM["gm_parallaxe"] = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
    SYSTEM["font"] = pygame.freetype.Font('ressources/dmg.ttf', 40)
    SYSTEM["text_generator"] = TextGenerator()
    SYSTEM["images"]["load_orb"] = Animation("lifeorb.png", 16, 14, frame_rate=0.1).scale(64, 64)
    SYSTEM["images"]["load_back"] = Image("life_boss_back.png").scale(30, 1500)
    SYSTEM["images"]["load_jauge"] = Image("life_boss.png").scale(30, 1500)
    SYSTEM["loading_text"] = None
    SYSTEM["clock"] = pygame.time.Clock()
    SYSTEM["fps_counter"] = None
    loading_thread = threading.Thread(target=load)
    loading_thread.start()
    SYSTEM["unloader"] = None
    SYSTEM["held"] = False
