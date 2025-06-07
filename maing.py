import random
from time import sleep
from data.constants import *
from data.character import Character
from data.Sprite import Sprite
from data.projectile import Projectile
from data.physics.hitbox import HitBox
from data.physics.entity import Entity
from data.creature import Creature
from data.game.enemy import Enemy
from data.slash import Slash
from data.generator import Generator
from data.image.animation import Animation
from data.image.parallaxe import Parallaxe
from data.image.image import Image
from data.image.text_generator import TextGenerator
from data.spell_list import *

SPEED = 4
PLAYING = True
PLAYER = (50, SCREEN_HEIGHT/2)

SPEED_FACTOR = 5

UI_SKILLS_OFFSET = 650
UI_SKILLS_PANEL_OFFSET = 2
UI_SKILLS_INPUT_OFFSET = 48

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
    SYSTEM["images"]["boss_jauge"] = Image("life_boss.png")
    SYSTEM["images"]["boss_jauge_back"] = Image("life_boss_back.png")
    SYSTEM["font"] = pygame.font.SysFont('ressources/dmg.ttf', 30)
    SYSTEM["font_crit"] = pygame.font.SysFont('ressources/dmg.ttf', 35, True)
    SYSTEM["text_generator"] = TextGenerator()
    generate_spell_list()
    #TODO: Offset this to the scene manager
    SYSTEM["background"] = Parallaxe("parallax_field.png", 320, 180, speeds = [0.2, 0.6, 1.0, 2.0])
    SYSTEM["player"] = Character(imagefile=Animation("witch.png", 64, 64, frame_rate = 0.25))

def init_timers():
    """Inits Pygame's timers."""
    pygame.time.set_timer(WAVE_TIMER, 2000)
    pygame.time.set_timer(USEREVENT+1, 2000)
    pygame.time.set_timer(USEREVENT+2, 100)
    pygame.time.set_timer(TICKER_TIMER, 16)

def game_loop():
    """Main game loop."""
    global PLAYING
    #Handle Events
    for events in pygame.event.get():
        if events.type == QUIT:
            PLAYING = False
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
    #Handle logic
    keys = pygame.key.get_pressed()
    SYSTEM["player"].action(keys)
    #Handle printing on screen
    SYSTEM["windows"].blit(SYSTEM["background"].draw(), (0, 0))
    SYSTEM["windows"].blit(SYSTEM["player"].get_image(), SYSTEM["player"].get_pos())
    for bubble in POWER_UP_TRACKER:
        SYSTEM["windows"].blit(bubble.get_image(), (bubble.x, bubble.y))
    for baddie in ENNEMY_TRACKER:
        SYSTEM["windows"].blit(baddie.get_image(), (baddie.x, baddie.y))
    for p in PROJECTILE_TRACKER:
        if isinstance(p, Generator):
            SYSTEM["windows"].blit(p.get_image(), p.get_pos())
        elif (isinstance(p, Projectile)):
            SYSTEM["windows"].blit(p.get_image(), p.get_pos())
    for s in SLASH_TRACKER:
        SYSTEM["windows"].blit(s.get_image(), s.get_pos())
    for txt in TEXT_TRACKER:
        SYSTEM["windows"].blit(sfc, (txt[1], txt[2]))

if __name__ == "__main__":
    init_game()
    init_timers()
    SYSTEM["game_state"] = GAME_LEVEL

    while PLAYING:
        if SYSTEM["game_state"] == GAME_LEVEL:
            game_loop()
        if SYSTEM["game_state"] == GAME_PAUSE:
            pass

        for events in pygame.event.get():
            if events.type == QUIT:
                PLAYING = False

        pygame.display.update()
        sleep(0.016)
