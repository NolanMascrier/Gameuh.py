import random
import os
import re
from time import sleep

import pygame.freetype
from data.image.text import Text
from data.constants import *
from data.character import Character
from data.generator import Generator
from data.image.animation import Animation
from data.image.parallaxe import Parallaxe
from data.image.image import Image
from data.image.tile import Tile
from data.image.button import Button
from data.image.text_generator import TextGenerator
from data.interface.gameui import draw_ui
from data.game.level import Level
from data.tables.spell_table import generate_spell_list
from data.image.slotpanel import SlotPanel
from data.image.slot import Slot
from data.item import Item
from data.game.lootgenerator import LootGenerator
from data.interface.inventory import open_inventory, draw_inventory
from data.interface.spellbook import open_spell_screen, draw_spells
from data.interface.general import tick, draw_game
from data.image.scrollable import Scrollable

PLAYING = True

def equip(item: Item, slot: Slot):
    """Equips an item on the player character."""
    if item is None:
        return
    if slot.flag not in item.flags:
        SYSTEM["gear_panel"].insert(slot.contains)
        slot.remove()
    else:
        SYSTEM["player"].creature.equip(slot.flag, item, slot.left)
        SYSTEM["player"].inventory.remove(item)

def unequip(item: Item, slot: Slot):
    """Removes the equiped item from the slot."""
    if item is None:
        return
    it = SYSTEM["player"].creature.unequip(slot.flag, slot.left)
    SYSTEM["player"].inventory.append(it)

def debug_create_items():
    """Creates a bunch of items."""
    lg = LootGenerator()
    base_loot = lg.roll(300, 5)
    SYSTEM["player"].inventory.extend(base_loot)

def start_level():
    """Starts the level stored in the SYSTEM."""
    SYSTEM["player"].reset()
    SYSTEM["level"] = SYSTEM["selected"]
    SYSTEM["game_state"] = GAME_LEVEL
    init_timers()

def quit_level():
    """Quits the current level and resets the player."""
    SYSTEM["game_state"] = MENU_MAIN
    reset()

def open_gear_screen():
    """Sets up the gear screen."""
    SYSTEM["game_state"] = MENU_GEAR
    x = SCREEN_WIDTH / 2- 32
    y = SCREEN_HEIGHT / 2 - 128
    SYSTEM["ui"]["gear_helm"] = Slot(x, y - 32, "gear_helm", equip, unequip,\
         Flags.HELM, SYSTEM["player"].creature.gear["helms"])
    SYSTEM["ui"]["gear_amulet"] = Slot(x, y + 32, "gear_amulet", equip, unequip,\
         Flags.AMULET, SYSTEM["player"].creature.gear["amulets"])
    SYSTEM["ui"]["gear_armor"] = Slot(x, y + 96, "gear_armor", equip, unequip,\
         Flags.ARMOR, SYSTEM["player"].creature.gear["armors"])
    SYSTEM["ui"]["gear_weapon"] = Slot(x - 128, y + 96, "gear_weapon", equip, unequip,\
         Flags.WEAPON, SYSTEM["player"].creature.gear["weapons"])
    SYSTEM["ui"]["gear_ring"] = Slot(x - 64, y + 64, "gear_ring", equip, unequip,\
         Flags.RING, SYSTEM["player"].creature.gear["rings"]["left"], True)
    SYSTEM["ui"]["gear_ring2"] = Slot(x + 64, y + 64, "gear_ring", equip, unequip,\
         Flags.RING, SYSTEM["player"].creature.gear["rings"]["right"])
    SYSTEM["ui"]["gear_offhand"] = Slot(x + 128, y + 96, "gear_offhand", equip, unequip,\
         Flags.OFFHAND, SYSTEM["player"].creature.gear["offhand"])
    SYSTEM["ui"]["gear_hands"] = Slot(x + 64, y + 128, "gear_hands", equip, unequip,\
         Flags.HANDS, SYSTEM["player"].creature.gear["gloves"])
    SYSTEM["ui"]["gear_relic"] = Slot(x - 64, y + 128, "gear_relic", equip, unequip,\
         Flags.RELIC, SYSTEM["player"].creature.gear["relics"])
    SYSTEM["ui"]["gear_belt"] = Slot(x, y + 174, "gear_belt", equip, unequip,\
         Flags.BELT, SYSTEM["player"].creature.gear["belts"])
    SYSTEM["ui"]["gear_boots"] = Slot(x, y + 238, "gear_boots", equip, unequip,\
         Flags.BOOTS, SYSTEM["player"].creature.gear["boots"])
    data = []
    for item in SYSTEM["player"].inventory:
        if isinstance(item, Item):
            if Flags.GEAR in item.flags:
                data.append(item)
    SYSTEM["gear_panel"] = SlotPanel(SCREEN_WIDTH - 535, 10, default=data)

def init_game():
    """Loads the basic data for the game."""
    pygame.init()
    pygame.font.init()
    #TODO: Load options
    flags = pygame.SCALED|pygame.FULLSCREEN
    SYSTEM["real_windows"] = pygame.display.set_mode((SYSTEM["options"]["screen_width"],\
        SYSTEM["options"]["screen_height"]), flags, vsync=1)
    SYSTEM["windows"] = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)

    SYSTEM["font"] = pygame.freetype.Font('ressources/dmg.ttf', 40)
    SYSTEM["font_detail"] = pygame.freetype.Font('ressources/dmg.ttf', 30)
    SYSTEM["font_detail_small"] = pygame.freetype.Font('ressources/dmg.ttf', 30)
    SYSTEM["font_crit"] = pygame.freetype.Font('ressources/dmg.ttf', 35)
    SYSTEM["font_crit"].strong = True
    SYSTEM["images"]["fireball"] = Animation("fireball.png", 32, 19, frame_rate=0.25).scale(38, 64)
    SYSTEM["images"]["energyball"] = Animation("pew.png", 13, 13, frame_rate=0.25).scale(32, 32)
    SYSTEM["images"]["boss_a"] = Animation("boss.png", 128, 150, frame_rate=0.25).scale(300, 256)
    SYSTEM["images"]["bouncer"] = Animation("bounce.png", 8, 8, frame_rate=0.25).scale(64, 64)
    SYSTEM["images"]["generator"] = Animation("generator.png", 8, 8, frame_rate=0.25).scale(32, 32)
    SYSTEM["images"]["lazer"] = Animation("lazor.png", 16, 10, frame_rate=0.25).scale(16, 64)
    SYSTEM["images"]["exp_orb"] = Animation("exporb.png", 8, 8, frame_rate=0.1).scale(8, 8)
    SYSTEM["images"]["mana_orb"] = Animation("manaorb.png", 16, 16, frame_rate=0.1)
    SYSTEM["images"]["life_orb"] = Animation("lifeorb.png", 16, 14, frame_rate=0.1)
    SYSTEM["images"]["exp_bar"] = Image("exp.png")
    SYSTEM["images"]["exp_bar2"] = Image("exp_back.png")
    SYSTEM["images"]["exp_jauge"] = Image("exp_bar.png")
    SYSTEM["images"]["life_jauge"] = Animation("life.png", 144, 144, animated=False)
    SYSTEM["images"]["mana_jauge"] = Animation("mana.png", 144, 144, animated=False)
    SYSTEM["images"]["life_potion"] = Animation("lifepot.png", 16, 16, frame_max=7,\
        frame_rate=0.2, lines=3).scale(64, 64)
    SYSTEM["images"]["mana_potion"] = Animation("manapot.png", 16, 16, frame_max=7,\
        frame_rate=0.2, lines=3).scale(64, 64)
    SYSTEM["images"]["badguy"] = Animation("badguy.png", 60, 130, frame_rate=0.25).flip(False, True)
    SYSTEM["images"]["skill_top"] = Image("ui/skill_top.png").scale(64, 64)
    SYSTEM["images"]["skill_bottom"] = Image("ui/skill_bottom.png").scale(64, 64)
    SYSTEM["images"]["item_top"] = Image("ui/item_top.png").scale(64, 64)
    SYSTEM["images"]["slot_empty"] = Image("ui/item_top.png").scale(64, 64)
    SYSTEM["images"]["slot_magic"] = Image("ui/item_top_m.png").scale(64, 64)
    SYSTEM["images"]["slot_rare"] = Image("ui/item_top_r.png").scale(64, 64)
    SYSTEM["images"]["slot_exalted"] = Image("ui/item_top_e.png").scale(64, 64)
    SYSTEM["images"]["item_bottom"] = Image("ui/item_bottom.png").scale(64, 64)
    SYSTEM["images"][K_q] = Image("ui/kb_q.png").image
    SYSTEM["images"][K_e] = Image("ui/kb_e.png").image
    SYSTEM["images"][K_f] = Image("ui/kb_f.png").image
    SYSTEM["images"][K_r] = Image("ui/kb_r.png").image
    SYSTEM["images"][K_t] = Image("ui/kb_t.png").image
    SYSTEM["images"][K_1] = Image("ui/kb_1.png").image
    SYSTEM["images"][K_2] = Image("ui/kb_2.png").image
    SYSTEM["images"]["btn"] = Image("ui/button.png").scale(55, 280)
    SYSTEM["images"]["btn_fat"] = Image("ui/button.png").scale(55, 100)
    SYSTEM["images"]["btn_fat_pressed"] = Image("ui/button_press.png").scale(55, 100)
    SYSTEM["images"]["btn_small"] = Image("ui/button.png").scale(35, 200)
    SYSTEM["images"]["btn_p"] = Image("ui/button_press.png").scale(55, 280)
    SYSTEM["images"][K_LSHIFT] = Image("ui/kb_shift.png").image
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
    SYSTEM["images"]["button_quit"] = Button(SYSTEM["images"]["btn"], SYSTEM["images"]["btn_p"],\
                                             lambda : SYSTEM.__setitem__("playing", False),\
                                             "Quit Game")
    SYSTEM["images"]["button_resume"] = Button(SYSTEM["images"]["btn"], SYSTEM["images"]["btn_p"],\
                                             lambda : SYSTEM.__setitem__("game_state", GAME_LEVEL),\
                                             "Resume")
    SYSTEM["images"]["button_abandon"] = Button(SYSTEM["images"]["btn"], SYSTEM["images"]["btn_p"],\
                                             quit_level,\
                                             "Abandon mission")
    SYSTEM["images"]["button_continue"] = Button(SYSTEM["images"]["btn"], SYSTEM["images"]["btn_p"],\
                                             quit_level,\
                                             "Return to base")
    SYSTEM["images"]["button_map"] = Button(SYSTEM["images"]["btn"], SYSTEM["images"]["btn_p"],\
                                             lambda : SYSTEM.__setitem__("game_state", MENU_MAIN),\
                                             "World Map")
    SYSTEM["images"]["button_gear"] = Button(SYSTEM["images"]["btn"], SYSTEM["images"]["btn_p"],\
                                             open_gear_screen,\
                                             "Gear")
    SYSTEM["images"]["button_spells"] = Button(SYSTEM["images"]["btn"], SYSTEM["images"]["btn_p"],\
                                             open_spell_screen,\
                                             "Spellbook")
    SYSTEM["images"]["button_tree"] = Button(SYSTEM["images"]["btn"], SYSTEM["images"]["btn_p"],\
                                             lambda : SYSTEM.__setitem__("game_state", MENU_TREE),\
                                             "Skill Tree")
    SYSTEM["images"]["button_inventory"] = Button(SYSTEM["images"]["btn"], SYSTEM["images"]["btn_p"],\
                                             open_inventory, "Inventory")
    SYSTEM["images"]["button_options"] = Button(SYSTEM["images"]["btn"], SYSTEM["images"]["btn_p"],\
                                             lambda : SYSTEM.__setitem__("game_state",\
                                             MENU_OPTIONS_GAME), "Options")
    SYSTEM["images"]["button_assault"] = Button(SYSTEM["images"]["btn"], SYSTEM["images"]["btn_p"],\
                                             start_level, "Begin the assault !")
    SYSTEM["images"]["char_details"] = Image("ui/char_back.png").scale(1050, 376)
    SYSTEM["images"]["panel_back"] = Image("ui/char_back.png").scale(1024, 448)
    SYSTEM["images"]["tile_panel_back"] = Tile("ui/inventory_back.png", 7, 14, 3)
    SYSTEM["images"]["tile_panel_inv"] = Tile("ui/inventory_back.png", 17, 13, 3)
    SYSTEM["images"]["hoverable"] = Tile("ui/hoverable.png")
    SYSTEM["images"]["item_desc"] = Tile("ui/hoverable.png", scale_factor=2)
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
    SYSTEM["images"]["mission_map"] = Image("mission.png")
    SYSTEM["images"]["mission_scroller"] = Scrollable(100, 10, 1200, 1000, contains=SYSTEM["images"]["mission_map"].image)
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
    SYSTEM["text_generator"] = TextGenerator()
    SYSTEM["images"]["mount_icon"] = Image("icons/mount.png")
    SYSTEM["images"]["city_icon"] = Image("icons/cybercity.png")
    SYSTEM["images"]["sunrise_icon"] = Image("icons/sunrise.png")
    SYSTEM["images"]["forest_icon"] = Image("icons/forest.png")
    SYSTEM["images"]["ui_normal"] = Tile("ui/border_normal.png", scale_factor=2)
    SYSTEM["images"]["ui_magic"] = Tile("ui/border_magic.png", scale_factor=2)
    SYSTEM["images"]["ui_rare"] = Tile("ui/border_rare.png", scale_factor=2)
    SYSTEM["images"]["ui_legendary"] = Tile("ui/border_legend.png", scale_factor=2)
    SYSTEM["images"]["ui_unique"] = Tile("ui/border_unique.png", scale_factor=2)
    SYSTEM["images"]["item_bootsA"] = Image("icons/bootsA.png")
    SYSTEM["images"]["item_ringA"] = Image("icons/ringA.png")
    SYSTEM["images"]["item_armorA"] = Image("icons/armorA.png")
    SYSTEM["images"]["loot_icon"] = Image("loot.png").scale(32, 32)
    #Get all the items image
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
    for name, _, filename in unsorted:
        SYSTEM["images"][corr[name]].append(Image(f"icons/{filename}"))

    #Spells
    generate_spell_list()
    #TODO: Offset this to the scene manager
    SYSTEM["mountains"] = Parallaxe("parallax_field.png", 320, 180, speeds = [0.2, 0.6, 1.0, 2.0, 2])
    SYSTEM["city_back"] = Parallaxe("city.png", 576, 324, speeds = [0.1, 0.0])
    SYSTEM["mount"] = Parallaxe("icemount.png", 360, 189, speeds = [0.2, 0.6, 1.0, 2.0, 1, 2.5, 3, 3])
    SYSTEM["cybercity"] = Parallaxe("cybercity.png", 576, 324, speeds = [0.2, 0.5, 1, 1.2, 2])
    SYSTEM["forest"] = Parallaxe("forest.png", 680, 429, speeds = [0.0, 0.1, 0.5, 1, 1.2, 2, 2])
    SYSTEM["sunrise"] = Parallaxe("sunrise.png", 320, 240, speeds = [0.0, 0.1, 0.2, 0.9, 1.0, 1.5, 1.5], scroll_left=False)
    SYSTEM["player"] = Character(imagefile=Animation("witch.png", 64, 64, frame_rate = 0.25))

def reset():
    """Resets the game's status"""
    SYSTEM["selected"] = None
    SYSTEM["player"].reset()
    ENNEMY_TRACKER.clear()
    PROJECTILE_TRACKER.clear()
    POWER_UP_TRACKER.clear()
    SLASH_TRACKER.clear()
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

def init_timers():
    """Inits Pygame's timers."""
    pygame.time.set_timer(WAVE_TIMER, 1000)
    pygame.time.set_timer(USEREVENT+1, 2000)
    pygame.time.set_timer(USEREVENT+2, 100)
    pygame.time.set_timer(TICKER_TIMER, 20)

def game_loop(keys, events):
    """Main game loop."""
    #Handle Events
    for event in events:
        if event.type == QUIT:
            SYSTEM["playing"] = False
        if event.type == WAVE_TIMER:
            SYSTEM["level"].next_wave()
        if event.type == TICKER_TIMER:
            tick()
    SYSTEM["windows"].blit(SYSTEM["level"].background.draw(), (0, 0))
    #Handle logic
    SYSTEM["player"].action(keys)
    #Handle printing on screen
    draw_game()
    #Draw the UI
    draw_ui()
    if SYSTEM["player"].creature.stats["life"].current_value <= 0:
        SYSTEM["game_state"] = GAME_DEATH
    SYSTEM["latest_frame"] = SYSTEM["windows"].copy()

def draw_victory(events):
    """Draws the victory screen."""
    for event in events:
        if event.type == TICKER_TIMER:
            tick()
    SYSTEM["windows"].blit(SYSTEM["level"].background.draw(), (0, 0))
    draw_game()
    x_offset = SCREEN_WIDTH / 2 - SYSTEM["images"]["menu_bg"].width / 2
    y_offset = SCREEN_HEIGHT / 2 - SYSTEM["images"]["menu_bg"].height / 2
    SYSTEM["windows"].blit(SYSTEM["images"]["menu_bg"].image, (x_offset, y_offset))
    SYSTEM["images"]["button_continue"].set(x_offset + 200, y_offset + 300)
    SYSTEM["images"]["button_continue"].draw(SYSTEM["windows"])
    gold = SYSTEM["level"].gold
    text = Text(f"#c#{(255, 179, 0)}{gold}")
    SYSTEM["windows"].blit(SYSTEM["images"]["gold_icon"].image, (x_offset, y_offset))
    SYSTEM["windows"].blit(text.surface, (x_offset + 80, y_offset + 32))
    for event in events:
        if event.type == pygame.MOUSEBUTTONDOWN:
            SYSTEM["images"]["button_continue"].press()

def draw_game_over(events):
    """Draws the defeat screen."""
    for event in events:
        if event.type == TICKER_TIMER:
            tick()
    SYSTEM["windows"].blit(SYSTEM["level"].background.draw(), (0, 0))
    draw_game(False)
    x_offset = SCREEN_WIDTH / 2 - SYSTEM["images"]["menu_bg"].width / 2
    y_offset = SCREEN_HEIGHT / 2 - SYSTEM["images"]["menu_bg"].height / 2
    SYSTEM["windows"].blit(SYSTEM["images"]["menu_bg"].image, (x_offset, y_offset))
    SYSTEM["images"]["button_continue"].set(x_offset + 200, y_offset + 300)
    SYSTEM["images"]["button_continue"].draw(SYSTEM["windows"])
    gold = SYSTEM["level"].gold
    text = Text(f"#c#{(255, 179, 0)}{gold}")
    SYSTEM["windows"].blit(SYSTEM["images"]["gold_icon"].image, (x_offset, y_offset))
    SYSTEM["windows"].blit(text.surface, (x_offset + 80, y_offset + 32))
    for event in events:
        if event.type == pygame.MOUSEBUTTONDOWN:
            SYSTEM["images"]["button_continue"].press()

def draw_pause(events):
    """Draws the pause menu."""
    x_offset = SCREEN_WIDTH / 2 - SYSTEM["images"]["menu_bg"].width / 2
    y_offset = SCREEN_HEIGHT / 2 - SYSTEM["images"]["menu_bg"].height / 2
    SYSTEM["windows"].blit(SYSTEM["latest_frame"], (0, 0))
    SYSTEM["windows"].blit(SYSTEM["images"]["menu_bg"].image, (x_offset, y_offset))
    SYSTEM["images"]["button_resume"].set(x_offset + 200, y_offset + 100)
    SYSTEM["images"]["button_abandon"].set(x_offset + 200, y_offset + 200)
    SYSTEM["images"]["button_quit"].set(x_offset + 200, y_offset + 300)
    SYSTEM["images"]["button_resume"].draw(SYSTEM["windows"])
    SYSTEM["images"]["button_abandon"].draw(SYSTEM["windows"])
    SYSTEM["images"]["button_quit"].draw(SYSTEM["windows"])
    for event in events:
        if event.type == pygame.MOUSEBUTTONDOWN:
            SYSTEM["images"]["button_resume"].press()
            SYSTEM["images"]["button_abandon"].press()
            SYSTEM["images"]["button_quit"].press()

def draw_small_card():
    """Draws a small character card."""
    x = SCREEN_WIDTH - SYSTEM["images"]["char_details"].width
    y = 0
    SYSTEM["windows"].blit(SYSTEM["images"]["char_details"].image, (x, y))
    li = SYSTEM["player"].creature.generate_stat_simple(x + 10, y + 10)
    for l in li:
        l.draw(SYSTEM["windows"])
        l.tick()

def draw_bottom_bar(events):
    """Draws the bottom bar, quick access to the menus."""
    SYSTEM["images"]["button_map"].set(10, SCREEN_HEIGHT - 64)
    SYSTEM["images"]["button_map"].draw(SYSTEM["windows"])
    SYSTEM["images"]["button_gear"].set(300, SCREEN_HEIGHT - 64)
    SYSTEM["images"]["button_gear"].draw(SYSTEM["windows"])
    SYSTEM["images"]["button_spells"].set(590, SCREEN_HEIGHT - 64)
    SYSTEM["images"]["button_spells"].draw(SYSTEM["windows"])
    SYSTEM["images"]["button_tree"].set(880, SCREEN_HEIGHT - 64)
    SYSTEM["images"]["button_tree"].draw(SYSTEM["windows"])
    SYSTEM["images"]["button_inventory"].set(1170, SCREEN_HEIGHT - 64)
    SYSTEM["images"]["button_inventory"].draw(SYSTEM["windows"])
    SYSTEM["images"]["button_options"].set(1460, SCREEN_HEIGHT - 64)
    SYSTEM["images"]["button_options"].draw(SYSTEM["windows"])
    for event in events:
        if event.type == pygame.MOUSEBUTTONDOWN:
            SYSTEM["images"]["button_map"].press()
            SYSTEM["images"]["button_gear"].press()
            SYSTEM["images"]["button_tree"].press()
            SYSTEM["images"]["button_inventory"].press()
            SYSTEM["images"]["button_options"].press()
            SYSTEM["images"]["button_spells"].press()

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

def draw_menu(events):
    """Draws the main game menu."""
    SYSTEM["windows"].blit(SYSTEM["city_back"].draw(), (0, 0))
    sfc = pygame.Surface((2000, 2000), pygame.SRCALPHA)
    sfc.blit(SYSTEM["images"]["mission_map"].image, (0, 0))
    SYSTEM["buttons_e"][0].set(350, 680, SYSTEM["images"]["mission_scroller"]).draw(sfc)
    SYSTEM["buttons_e"][1].set(860, 250, SYSTEM["images"]["mission_scroller"]).draw(sfc)
    SYSTEM["buttons_e"][2].set(900, 900, SYSTEM["images"]["mission_scroller"]).draw(sfc)
    SYSTEM["buttons_e"][3].set(478, 420, SYSTEM["images"]["mission_scroller"]).draw(sfc)
    SYSTEM["images"]["mission_scroller"].contains = sfc
    SYSTEM["images"]["mission_scroller"].tick().draw()
    draw_small_card()
    if SYSTEM["selected"] is not None and isinstance(SYSTEM["selected"], Level):
        name = Text(f'{SYSTEM["selected"].name}', True)
        lvl = Text(f'Area level: {SYSTEM["selected"].area_level}', True)
        #TODO: modifiers ...
        SYSTEM["windows"].blit(name.surface, (1500, 750))
        SYSTEM["windows"].blit(lvl.surface, (1500, 775))
        SYSTEM["images"]["button_assault"].set(1500, 1000).draw(SYSTEM["windows"])
        SYSTEM["windows"].blit(SYSTEM["selected"].icon.image, (1500, 800))
    draw_bottom_bar(events)
    for event in events:
        if event.type == pygame.MOUSEBUTTONDOWN:
            SYSTEM["buttons_e"][0].press()
            SYSTEM["buttons_e"][1].press()
            SYSTEM["buttons_e"][2].press()
            SYSTEM["buttons_e"][3].press()
            SYSTEM["images"]["button_assault"].press()

def draw_gear(events):
    """Draws the gear menu."""
    SYSTEM["windows"].blit(SYSTEM["city_back"].draw(), (0, 0))
    x_offset = SCREEN_WIDTH / 2 - SYSTEM["images"]["menu_bg"].width / 2
    y_offset = SCREEN_HEIGHT / 2 - SYSTEM["images"]["menu_bg"].height / 2
    SYSTEM["windows"].blit(SYSTEM["images"]["menu_bg"].image, (x_offset, y_offset))
    SYSTEM["ui"]["gear_weapon"].tick().draw()
    SYSTEM["ui"]["gear_offhand"].tick().draw()
    SYSTEM["ui"]["gear_helm"].tick().draw()
    SYSTEM["ui"]["gear_boots"].tick().draw()
    SYSTEM["ui"]["gear_hands"].tick().draw()
    SYSTEM["ui"]["gear_armor"].tick().draw()
    SYSTEM["ui"]["gear_belt"].tick().draw()
    SYSTEM["ui"]["gear_ring"].tick().draw()
    SYSTEM["ui"]["gear_ring2"].tick().draw()
    SYSTEM["ui"]["gear_amulet"].tick().draw()
    SYSTEM["ui"]["gear_relic"].tick().draw()
    SYSTEM["gear_panel"].tick().draw()
    x = 10
    y = 10
    SYSTEM["windows"].blit(SYSTEM["images"]["char_details"].image, (x, y))
    li = SYSTEM["player"].creature.generate_stat_details(x + 10, y + 10)
    for l in li:
        l.draw(SYSTEM["windows"])
        l.tick()
    draw_bottom_bar(events)

if __name__ == "__main__":
    init_game()
    init_timers()
    held = False
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
    debug_create_items()
    ###
    while SYSTEM["playing"]:
        SYSTEM["pop_up"] = None
        get_mouse_pos()
        SYSTEM["mouse_click"] = pygame.mouse.get_pressed()
        if SYSTEM["mouse_click"][0] and not held:
            held = True
            SYSTEM["mouse_previous"] = SYSTEM["mouse"]
        if held and not SYSTEM["mouse_click"][0]:
            held = False
        SYSTEM["mouse_wheel"] = [(0, 0), (0, 0)]
        events = pygame.event.get()
        for event in events:
            if event.type == QUIT:
                PLAYING = False
            if event.type == MOUSEWHEEL:
                SYSTEM["mouse_wheel"][0] = SYSTEM["mouse_wheel"][1]
                SYSTEM["mouse_wheel"][1] = (event.x, event.y)
        keys = pygame.key.get_pressed()
        SYSTEM["keys"] = keys
        if keys[K_ESCAPE]:
            if SYSTEM["cooldown"] <= 0:
                SYSTEM["cooldown"] = 0.5
                if SYSTEM["game_state"] == GAME_LEVEL:
                    SYSTEM["game_state"] = GAME_PAUSE
                elif SYSTEM["game_state"] == GAME_PAUSE:
                    SYSTEM["game_state"] = GAME_LEVEL
        if SYSTEM["game_state"] == GAME_LEVEL:
            game_loop(keys, events)
        if SYSTEM["game_state"] == GAME_PAUSE:
            draw_pause(events)
        if SYSTEM["game_state"] == GAME_VICTORY:
            draw_victory(events)
        if SYSTEM["game_state"] == GAME_DEATH:
            draw_game_over(events)
        if SYSTEM["game_state"] == MENU_MAIN:
            draw_menu(events)
        if SYSTEM["game_state"] == MENU_GEAR:
            draw_gear(events)
        if SYSTEM["game_state"] == MENU_SPELLBOOK:
            draw_spells(events)
        if SYSTEM["game_state"] == MENU_INVENTORY:
            draw_inventory(events)

        if SYSTEM["pop_up"] is not None:
            x = SYSTEM["mouse"][0] - SYSTEM["pop_up"][1]
            if x < 0:
                x += SYSTEM["pop_up"][1]
            y = SYSTEM["mouse"][1]
            if y + SYSTEM["pop_up"][2] > SCREEN_HEIGHT:
                y -= y + SYSTEM["pop_up"][2] - SCREEN_HEIGHT
            SYSTEM["windows"].blit(SYSTEM["pop_up"][0], (x, y))

        SYSTEM["cooldown"] -= 0.032
        SYSTEM["cooldown"] = max(SYSTEM["cooldown"], 0)
        if SYSTEM["dragged"] is not None:
            SYSTEM["dragged"].tick().draw()
        if not SYSTEM["mouse_click"][0]:
            SYSTEM["dragged"] = None
        if SYSTEM["mouse_click"][0] and SYSTEM["cooldown"] <= 0:
            if SYSTEM["rune"] != -1 and not SYSTEM["keys"][K_LSHIFT]:
                SYSTEM["rune"] = -1
                SYSTEM["rune_display"] = None
                SYSTEM["cooldown"] = 0.8
            if SYSTEM["rune"] != -1 and SYSTEM["player"].runes[SYSTEM["rune"]] <= 0:
                SYSTEM["rune"] = -1
                SYSTEM["rune_display"] = None
                SYSTEM["cooldown"] = 0.8
        window = pygame.transform.smoothscale(SYSTEM["windows"],\
            (SYSTEM["options"]["screen_width"], SYSTEM["options"]["screen_height"]))
        SYSTEM["real_windows"].blit(window, (0, 0))
        pygame.display.update()
        sleep(float(SYSTEM["options"]["fps"]))
