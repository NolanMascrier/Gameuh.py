import random
from time import sleep
from data.constants import *
from data.character import Character
from data.projectile import Projectile
from data.generator import Generator
from data.image.animation import Animation
from data.image.hoverable import Hoverable
from data.image.parallaxe import Parallaxe
from data.image.image import Image
from data.image.button import Button
from data.image.text_generator import TextGenerator
from data.interface.gameui import draw_ui
from data.game.level import Level
from data.spell_list import generate_spell_list

SPEED = 4
PLAYING = True
PLAYER = (50, SCREEN_HEIGHT/2)

SPEED_FACTOR = 5

def init_game():
    """Loads the basic data for the game."""
    pygame.init()
    pygame.font.init()
    #TODO: Load options
    flags = pygame.SCALED|pygame.FULLSCREEN
    SYSTEM["windows"] = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), flags, vsync=1)

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
    SYSTEM["images"]["item_bottom"] = Image("ui/item_bottom.png").scale(64, 64)
    SYSTEM["images"][K_q] = Image("ui/kb_q.png").image
    SYSTEM["images"][K_e] = Image("ui/kb_e.png").image
    SYSTEM["images"][K_f] = Image("ui/kb_f.png").image
    SYSTEM["images"][K_r] = Image("ui/kb_r.png").image
    SYSTEM["images"][K_t] = Image("ui/kb_t.png").image
    SYSTEM["images"][K_1] = Image("ui/kb_1.png").image
    SYSTEM["images"][K_2] = Image("ui/kb_2.png").image
    SYSTEM["images"][K_LSHIFT] = Image("ui/kb_shift.png").image
    SYSTEM["images"]["menu_bg"] = Image("ui/menu.png")
    SYSTEM["images"]["menu_button"] = Image("ui/button.png").scale(55, 280)
    SYSTEM["images"]["button_quit"] = Button("ui/button.png",\
                                             lambda : SYSTEM.__setitem__("playing", False),\
                                             "Quit Game").scale(55, 280)
    SYSTEM["images"]["button_resume"] = Button("ui/button.png",\
                                             lambda : SYSTEM.__setitem__("game_state", GAME_LEVEL),\
                                             "Resume").scale(55, 280)
    SYSTEM["images"]["button_abandon"] = Button("ui/button.png",\
                                             lambda : SYSTEM.__setitem__("game_state", MENU_MAIN),\
                                             "Abandon mission").scale(55, 280)
    SYSTEM["images"]["button_continue"] = Button("ui/button.png",\
                                             lambda : SYSTEM.__setitem__("game_state", MENU_MAIN),\
                                             "Return to base").scale(55, 280)
    SYSTEM["images"]["button_map"] = Button("ui/button.png",\
                                             lambda : SYSTEM.__setitem__("game_state", MENU_MAIN),\
                                             "World Map").scale(55, 280)
    SYSTEM["images"]["button_gear"] = Button("ui/button.png",\
                                             lambda : SYSTEM.__setitem__("game_state", MENU_GEAR),\
                                             "Gear").scale(55, 280)
    SYSTEM["images"]["button_tree"] = Button("ui/button.png",\
                                             lambda : SYSTEM.__setitem__("game_state", MENU_TREE),\
                                             "Skill Tree").scale(55, 280)
    SYSTEM["images"]["button_inventory"] = Button("ui/button.png",\
                                             lambda : SYSTEM.__setitem__("game_state",\
                                             MENU_INVENTORY), "Inventory").scale(55, 280)
    SYSTEM["images"]["button_options"] = Button("ui/button.png",\
                                             lambda : SYSTEM.__setitem__("game_state",\
                                             MENU_OPTIONS_GAME), "Options").scale(55, 280)
    SYSTEM["images"]["char_details"] = Image("ui/char_back.png").scale(1050, 376)
    SYSTEM["images"]["hoverable"] = Image("ui/hoverable.png")
    SYSTEM["images"]["mini_moolah"] = Image("minifric.png")
    SYSTEM["images"]["moolah"] = Image("fric.png")
    SYSTEM["images"]["big_moolah"] = Image("superminifric.png")
    SYSTEM["images"]["super_moolah"] = Image("superfric.png")
    SYSTEM["images"]["mega_moolah"] = Image("megaminifric.png").scale(64, 64)
    SYSTEM["images"]["giga_moolah"] = Image("maximinifric.png").scale(64, 64)
    SYSTEM["images"]["terra_moolah"] = Image("megafric.png").scale(64, 64)
    SYSTEM["images"]["zeta_moolah"] = Image("maxifric.png").scale(64, 64)
    SYSTEM["images"]["supra_moolah"] = Image("grail.png").scale(64, 64)
    SYSTEM["images"]["maxi_moolah"] = Image("maxigrail.png").scale(64, 64)
    SYSTEM["images"]["gold_icon"] = Image("thune.png")
    SYSTEM["images"]["boss_jauge"] = Image("life_boss.png")
    SYSTEM["images"]["boss_jauge_back"] = Image("life_boss_back.png")
    SYSTEM["font"] = pygame.font.SysFont('ressources/dmg.ttf', 30)
    SYSTEM["font_detail"] = pygame.font.SysFont('ressources/dogica.ttf', 25)
    SYSTEM["font_detail_small"] = pygame.font.SysFont('ressources/dogica.ttf', 20)
    SYSTEM["font_crit"] = pygame.font.SysFont('ressources/dmg.ttf', 35, True)
    SYSTEM["text_generator"] = TextGenerator()
    generate_spell_list()
    #TODO: Offset this to the scene manager
    SYSTEM["mountains"] = Parallaxe("parallax_field.png", 320, 180, speeds = [0.2, 0.6, 1.0, 2.0])
    SYSTEM["city_back"] = Parallaxe("city.png", 576, 324, speeds = [0.1, 0.0])
    SYSTEM["mount"] = Parallaxe("icemount.png", 360, 189, speeds = [0.2, 0.6, 1.0, 2.0, 1, 2.5, 3])
    SYSTEM["cybercity"] = Parallaxe("cybercity.png", 576, 324, speeds = [0.2, 0.5, 1, 1.2, 2])
    SYSTEM["forest"] = Parallaxe("forest.png", 680, 429, speeds = [0.0, 0.1, 0.5, 1, 1.2, 2])
    SYSTEM["sunrise"] = Parallaxe("sunrise.png", 320, 240, speeds = [0.0, 0.1, 0.2, 0.9, 1.0, 1.5], scroll_left=False)
    SYSTEM["player"] = Character(imagefile=Animation("witch.png", 64, 64, frame_rate = 0.25))

def init_timers():
    """Inits Pygame's timers."""
    pygame.time.set_timer(WAVE_TIMER, 2000)
    pygame.time.set_timer(USEREVENT+1, 2000)
    pygame.time.set_timer(USEREVENT+2, 100)
    pygame.time.set_timer(TICKER_TIMER, 20)

def game_loop(keys):
    """Main game loop."""
    #Handle Events
    for events in pygame.event.get():
        if events.type == QUIT:
            SYSTEM["playing"] = False
        if events.type == WAVE_TIMER:
            SYSTEM["level"].next_wave()
        if events.type == TICKER_TIMER:
            generate_grids()
            SYSTEM["player"].tick()
            for bubble in POWER_UP_TRACKER.copy():
                bubble.tick(SYSTEM["player"])
                if bubble.flagged_for_deletion:
                    POWER_UP_TRACKER.remove(bubble)
            for baddie in ENNEMY_TRACKER.copy():
                baddie.tick(SYSTEM["player"])
                if baddie.destroyed:
                    ENNEMY_TRACKER.remove(baddie)
            for p in PROJECTILE_TRACKER.copy():
                if isinstance(p, Generator):
                    p.tick(SYSTEM["player"])
                    continue
                p.tick()
                if p.can_be_destroyed():
                    PROJECTILE_TRACKER.remove(p)
            for s in SLASH_TRACKER.copy():
                s.tick()
                if s.finished:
                    SLASH_TRACKER.remove(s)
            for txt in TEXT_TRACKER.copy():
                sfc = txt[0]
                sfc.set_alpha(txt[3])
                txt[3] -= 5
                txt[2] -= 3
                if txt[3] < 10:
                    TEXT_TRACKER.remove(txt)
            clean_grids()
    SYSTEM["windows"].blit(SYSTEM["level"].background.draw(), (0, 0))
    #Handle logic
    SYSTEM["player"].action(keys)
    #Handle printing on screen
    SYSTEM["windows"].blit(SYSTEM["player"].get_image(), SYSTEM["player"].get_pos())
    for bubble in POWER_UP_TRACKER:
        SYSTEM["windows"].blit(bubble.get_image(), (bubble.x, bubble.y))
    for baddie in ENNEMY_TRACKER:
        SYSTEM["windows"].blit(baddie.get_image(), (baddie.x, baddie.y))
    for p in PROJECTILE_TRACKER:
        if isinstance(p, Generator):
            SYSTEM["windows"].blit(p.get_image(), p.get_pos())
        elif isinstance(p, Projectile):
            SYSTEM["windows"].blit(p.get_image(), p.get_pos())
    for s in SLASH_TRACKER:
        SYSTEM["windows"].blit(s.get_image(), s.get_pos())
    for txt in TEXT_TRACKER:
        SYSTEM["windows"].blit(txt[0], (txt[1], txt[2]))
    #Draw the UI
    draw_ui()
    SYSTEM["latest_frame"] = SYSTEM["windows"].copy()

def draw_victory():
    """Draws the victory screen."""
    for events in pygame.event.get():
        if events.type == TICKER_TIMER:
            generate_grids()
            SYSTEM["player"].tick()
            for bubble in POWER_UP_TRACKER.copy():
                bubble.tick(SYSTEM["player"])
                if bubble.flagged_for_deletion:
                    POWER_UP_TRACKER.remove(bubble)
            for baddie in ENNEMY_TRACKER.copy():
                baddie.tick(SYSTEM["player"])
                if baddie.destroyed:
                    ENNEMY_TRACKER.remove(baddie)
            for p in PROJECTILE_TRACKER.copy():
                if isinstance(p, Generator):
                    p.tick(SYSTEM["player"])
                    continue
                p.tick()
                if p.can_be_destroyed():
                    PROJECTILE_TRACKER.remove(p)
            for s in SLASH_TRACKER.copy():
                s.tick()
                if s.finished:
                    SLASH_TRACKER.remove(s)
            for txt in TEXT_TRACKER.copy():
                sfc = txt[0]
                sfc.set_alpha(txt[3])
                txt[3] -= 5
                txt[2] -= 3
                if txt[3] < 10:
                    TEXT_TRACKER.remove(txt)
            clean_grids()
    SYSTEM["windows"].blit(SYSTEM["level"].background.draw(), (0, 0))
    for bubble in POWER_UP_TRACKER:
        SYSTEM["windows"].blit(bubble.get_image(), (bubble.x, bubble.y))
    x_offset = SCREEN_WIDTH / 2 - SYSTEM["images"]["menu_bg"].width / 2
    y_offset = SCREEN_HEIGHT / 2 - SYSTEM["images"]["menu_bg"].height / 2
    SYSTEM["windows"].blit(SYSTEM["images"]["menu_bg"].image, (x_offset, y_offset))
    SYSTEM["images"]["button_continue"].set(x_offset + 200, y_offset + 300)
    SYSTEM["images"]["button_continue"].draw(SYSTEM["windows"])
    gold = SYSTEM["level"].gold
    text = SYSTEM["font_crit"].render(f"{gold}", False, (255, 179, 0))
    SYSTEM["windows"].blit(SYSTEM["images"]["gold_icon"].image, (x_offset, y_offset))
    SYSTEM["windows"].blit(text, (x_offset + 80, y_offset + 32))
    for events in pygame.event.get():
        if events.type == pygame.MOUSEBUTTONDOWN:
            SYSTEM["images"]["button_continue"].press(events.pos)

def draw_pause():
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
    for events in pygame.event.get():
        if events.type == pygame.MOUSEBUTTONDOWN:
            SYSTEM["images"]["button_resume"].press(events.pos)
            SYSTEM["images"]["button_abandon"].press(events.pos)
            SYSTEM["images"]["button_quit"].press(events.pos)

def draw_small_card():
    """Draws a small character card."""
    x = SCREEN_WIDTH - SYSTEM["images"]["char_details"].width
    y = 0
    SYSTEM["windows"].blit(SYSTEM["images"]["char_details"].image, (x, y))
    li = SYSTEM["player"].creature.generate_stat_simple(x + 10, y + 10)
    for l in li:
        l.draw(SYSTEM["windows"])
        l.tick()

def draw_bottom_bar():
    """Draws the bottom bar, quick access to the menus."""
    SYSTEM["images"]["button_map"].set(10, SCREEN_HEIGHT - 64)
    SYSTEM["images"]["button_map"].draw(SYSTEM["windows"])
    SYSTEM["images"]["button_gear"].set(300, SCREEN_HEIGHT - 64)
    SYSTEM["images"]["button_gear"].draw(SYSTEM["windows"])
    SYSTEM["images"]["button_tree"].set(590, SCREEN_HEIGHT - 64)
    SYSTEM["images"]["button_tree"].draw(SYSTEM["windows"])
    SYSTEM["images"]["button_inventory"].set(880, SCREEN_HEIGHT - 64)
    SYSTEM["images"]["button_inventory"].draw(SYSTEM["windows"])
    SYSTEM["images"]["button_options"].set(1170, SCREEN_HEIGHT - 64)
    SYSTEM["images"]["button_options"].draw(SYSTEM["windows"])

def draw_menu():
    """Draws the main game menu."""
    SYSTEM["windows"].blit(SYSTEM["city_back"].draw(), (0, 0))
    draw_small_card()
    draw_bottom_bar()
    for events in pygame.event.get():
        if events.type == pygame.MOUSEBUTTONDOWN:
            SYSTEM["images"]["button_map"].press(events.pos)
            SYSTEM["images"]["button_gear"].press(events.pos)
            SYSTEM["images"]["button_tree"].press(events.pos)
            SYSTEM["images"]["button_inventory"].press(events.pos)
            SYSTEM["images"]["button_options"].press(events.pos)

if __name__ == "__main__":
    init_game()
    init_timers()
    SYSTEM["game_state"] = GAME_LEVEL
    SYSTEM["level"] = Level("Test level", 0, None, 3000, SYSTEM["sunrise"])
    INTERNAL_COOLDOWN = 0
    while SYSTEM["playing"]:
        SYSTEM["mouse"] = pygame.mouse.get_pos()
        keys = pygame.key.get_pressed()
        if keys[K_ESCAPE]:
            if INTERNAL_COOLDOWN <= 0:
                INTERNAL_COOLDOWN = 0.5
                if SYSTEM["game_state"] == GAME_LEVEL:
                    SYSTEM["game_state"] = GAME_PAUSE
                elif SYSTEM["game_state"] == GAME_PAUSE:
                    SYSTEM["game_state"] = GAME_LEVEL
        if SYSTEM["game_state"] == GAME_LEVEL:
            game_loop(keys)
        if SYSTEM["game_state"] == GAME_PAUSE:
            draw_pause()
        if SYSTEM["game_state"] == GAME_VICTORY:
            draw_victory()
        if SYSTEM["game_state"] == MENU_MAIN:
            draw_menu()

        for events in pygame.event.get():
            if events.type == QUIT:
                PLAYING = False

        pygame.display.update()
        INTERNAL_COOLDOWN -= 0.032
        INTERNAL_COOLDOWN = max(INTERNAL_COOLDOWN, 0)
        sleep(float(SYSTEM["options"]["fps"]))
