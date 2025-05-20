from time import sleep
import random
from data.constants import *
from data.Character import Character
from data.Sprite import Sprite
from data.Fireball import Fireball
from data.physics.hitbox import HitBox
from data.physics.entity import Entity
from data.creature import Creature
from data.game.enemy import Enemy
from data.game.pickup import PickUp
from data.generator import Generator

SPEED = 4
PLAYING = True
PLAYER = (50, 50)

SPEED_FACTOR = 5

shoot_da_bouncy = False
bouncies = 0

def draw_ui(char, bg, ui, fenetre, boss_here = False, boss = 1, boss_max = 1):
    cd = (char.cooldown + 0.001) / char.max_cooldown * 176
    mana = char.mana / 100 * 176
    life = char.life / 100 * 176
    boss = (boss/boss_max) * 1000
    #Positions
    posL = (0, 10)
    posM = (0, 50)
    posC = (0, 90)
    #sizes up
    l = pygame.transform.scale(ui[4], (life, 40))
    m = pygame.transform.scale(ui[5], (mana, 40))
    c = pygame.transform.scale(ui[6], (cd, 40))
    #jauges
    fenetre.blit(l, (posL[0] + 24, posL[1]))
    fenetre.blit(m, (posM[0] + 24, posM[1]))
    fenetre.blit(c, (posC[0] + 24, posC[1]))
    if boss_here:
        b = pygame.transform.scale(ui[7], (boss, 80))
        bb = pygame.transform.scale(ui[8], (1000, 80))
        fenetre.blit(bb, (100, SCREEN_HEIGHT - 100))
        fenetre.blit(b, (100, SCREEN_HEIGHT - 100))
    #fluff
    fenetre.blit(ui[0], posL)
    fenetre.blit(ui[0], posM)
    fenetre.blit(ui[0], posC)
    #icons
    fenetre.blit(ui[1], posL)
    fenetre.blit(ui[2], posM)
    fenetre.blit(ui[3], posC)

def move_boss(boss_cord, img, gen, laz):
    global shoot_da_bouncy, bouncies
    pattern = random.randint(0, 12)
    #pattern = 11
    x = random.randint(900, 1100)
    y = random.randint(0, SCREEN_HEIGHT - 300)
    if pattern >= 0 and pattern <= 7:
        for i in range(9):
            sh = Fireball(boss_cord[0], boss_cord[1], 200 - 5*i, animated=True, image=img, speed=10, max_frame=5, evil=True, len=32, height=32, frame_delay=0.25)
            PROJECTILE_TRACKER.append(sh)
    if pattern > 7 and pattern <= 10:
        pygame.time.set_timer(USEREVENT+1, 3500)
        shoot_da_bouncy = True
        bouncies = random.randint(2, 4)
    if pattern > 10 and pattern <= 12:
        for i in range(3):
            sh = Generator(boss_cord[0], boss_cord[1], (boss_cord[0] + random.randint(-100,100), boss_cord[1]+ random.randint(100,250) * (random.randint(0, 1) - 1)), 0.025, 1, 3,\
                        gen, laz)
            PROJECTILE_TRACKER.append(sh)
    return (x, y)

def explode(target, img1, img2):
    amount = random.randint(0,5)
    for _ in range(amount + 1):
        power_type = True if random.randint(0, 1) == 0 else False
        x = target.x + 30
        y = target.y + 60
        img = img1 if power_type else img2
        pu = PickUp(x, y, img, value = 1)
        if power_type:
            pu.flags.append(Flags.MANA)
        else:
            pu.flags.append(Flags.LIFE)
        POWER_UP_TRACKER.append(pu)

def draw_hitbox(box, fenetre, color):
    s = pygame.Surface((box.width, box.height))
    s.set_alpha(128)
    s.fill(color)
    fenetre.blit(s, (box.x, box.y))
    s = pygame.Surface((4, 4))
    s.set_alpha(255)
    s.fill(color)
    fenetre.blit(s, box.center)

def spawn_enemies(image, attack_anim):
    to_spawn = random.randint(3, 10)
    for i in range(to_spawn + 1):
        y_pos = random.randint(0, SCREEN_HEIGHT)
        enemy_type = Flags.SHOOTER if random.randint(0, 1) == 1 else Flags.CHASER
        hb = HitBox(SCREEN_WIDTH - 100, y_pos, 64, 128)
        ent = Entity(SCREEN_WIDTH - 100, y_pos, image, hb)
        crea = Creature("bob")
        if enemy_type == Flags.CHASER:
            crea.stats["life"].value = 20
        else:
            crea.stats["life"].value = 10
        enemy = Enemy(ent, crea, attack_anim, behaviours=[enemy_type], timer=1)
        ENNEMY_TRACKER.append(enemy)

if __name__ == "__main__":
    boss_cord = [1000, 500]
    boss_hitbox = HitBox(boss_cord[0], boss_cord[1], 100, 200)
    boss_life = 500
    boss_max = 500
    destination = (1000, 500)
    boss_here = False
    waves = 5

    direction = K_DOWN
    john = Character()
    pygame.init()
    pygame.font.init()
    pygame.time.set_timer(WAVE_TIMER, 2000)
    pygame.time.set_timer(USEREVENT+1, 2000)
    pygame.time.set_timer(USEREVENT+2, 100)
    fenetre = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    spri = Sprite("ressources/tiles/Island_24x24.png", 24, 24, 9, 8)
    fnt_txt = pygame.font.SysFont('ressources/dmg.ttf', 30)
    SYSTEM["font"] = pygame.font.SysFont('ressources/dmg.ttf', 30)
    char = pygame.image.load("ressources/witch.png").convert_alpha()
    char_anim = [pygame.transform.scale(char.subsurface(x, 0, 64, 64), (128, 128))
                 for x in range(0, 576, 64)]
    john.image = char_anim[0]
    ui = [
        pygame.transform.scale(pygame.image.load(UI_JAUGE).convert_alpha(), (200, 40)),
        pygame.transform.scale(pygame.image.load(UI_JAUGE_L).convert_alpha(), (200, 40)),
        pygame.transform.scale(pygame.image.load(UI_JAUGE_M).convert_alpha(), (200, 40)),
        pygame.transform.scale(pygame.image.load(UI_JAUGE_C).convert_alpha(), (200, 40)),
        pygame.transform.scale(pygame.image.load(JAUGE_L).convert_alpha(), (176, 40)),
        pygame.transform.scale(pygame.image.load(JAUGE_M).convert_alpha(), (176, 40)),
        pygame.transform.scale(pygame.image.load(JAUGE_C).convert_alpha(), (176, 40)),
        pygame.transform.scale(pygame.image.load(JAUGE_BOSS).convert_alpha(), (176, 40)),
        pygame.transform.scale(pygame.image.load(JAUGE_BOSS_BACK).convert_alpha(), (176, 40))
    ]
    john.rect = john.image.get_rect()
    index = 0
    bg = pygame.image.load("ressources/parallax_field.png").convert_alpha()
    parallaxes = [
        pygame.transform.scale(bg.subsurface((0, 0, 320, 180)), (SCREEN_WIDTH, SCREEN_HEIGHT)),
        pygame.transform.scale(bg.subsurface((320, 0, 320, 180)), (SCREEN_WIDTH, SCREEN_HEIGHT)),
        pygame.transform.scale(bg.subsurface((640, 0, 320, 180)), (SCREEN_WIDTH, SCREEN_HEIGHT)),
        pygame.transform.scale(bg.subsurface((960, 0, 320, 180)), (SCREEN_WIDTH, SCREEN_HEIGHT)),
        pygame.transform.scale(bg.subsurface((1280, 0, 320, 180)), (SCREEN_WIDTH, SCREEN_HEIGHT))
    ]

    boss = pygame.image.load("ressources/boss.png").convert_alpha()
    boss_anim = [pygame.transform.scale(boss.subsurface(x, 0, 128, 150), (256, 300))
                 for x in range(0, 768, 128)]

    attack = pygame.image.load("ressources/pew.png").convert_alpha()
    attack_anim = [pygame.transform.scale(attack.subsurface(x, 0, 13, 13), (32, 32))
                 for x in range(0, 65, 13)]

    ball = pygame.image.load("ressources/bounce.png").convert_alpha()
    ball_anim = [pygame.transform.scale(ball.subsurface(x, 0, 8, 8), (64, 64))
                 for x in range(0, 32, 8)]

    generator = pygame.image.load("ressources/generator.png").convert_alpha()
    generator_anim = [pygame.transform.scale(generator.subsurface(x, 0, 8, 8), (32, 32))
                 for x in range(0, 32, 8)]

    lazor = pygame.image.load("ressources/lazor.png").convert_alpha()
    lazor_anim = [pygame.transform.scale(lazor.subsurface(x, 0, 16, 10), (64, 16))
                 for x in range(0, 64, 16)]

    manaorb = pygame.image.load("ressources/manaorb.png").convert_alpha()
    manaorb_anim = [pygame.transform.scale(manaorb.subsurface(x, 0, 16, 14), (16, 16))
                 for x in range(0, 64, 16)]

    lifeorb = pygame.image.load("ressources/lifeorb.png").convert_alpha()
    lifeorb_anim = [pygame.transform.scale(lifeorb.subsurface(x, 0, 16, 14), (16, 16))
                 for x in range(0, 64, 16)]

    badguy = pygame.transform.flip(pygame.image.load("ressources/badguy.png").convert_alpha(),\
                                   True, False)
    badguy_anim = [pygame.transform.scale(badguy.subsurface(x, 0, 60, 130), (64, 128))
                 for x in range(0, 540, 60)]

    diff_x = [0.0, 0.0, 0.0, 0.0]
    speeds = [0.2, 0.6, 1.0, 2.0]
    frame = 0

    while PLAYING:
        frame += 0.2
        fenetre.blit(parallaxes[0], (0, 0))
        for i in range(4):
            diff_x[i] = (diff_x[i] + speeds[i] * SPEED_FACTOR) % SCREEN_WIDTH
        for layer in range(4):
            for y in range(0, 2):
                x = int((y * SCREEN_WIDTH) - diff_x[layer])
                fenetre.blit(parallaxes[layer + 1], (x, 0))

        if boss_cord[0] < destination[0]:
            boss_cord[0] += 10
        if boss_cord[0] > destination[0]:
            boss_cord[0] -= 10
        if boss_cord[1] < destination[1]:
            boss_cord[1] += 10
        if boss_cord[1] > destination[1]:
            boss_cord[1] -= 10

        fenetre.blit(john.image, john.get_pos())
        if boss_here:
            boss_hitbox.move((boss_cord[0] + 20, boss_cord[1] + 80))
            fenetre.blit(boss_anim[int(frame) % 6], (boss_cord[0], boss_cord[1]))

        for event in pygame.event.get():
            if event.type == QUIT:
                PLAYING = False
            if event.type == WAVE_TIMER:
                if waves > 0:
                    pygame.time.set_timer(WAVE_TIMER, 12000)
                    spawn_enemies(badguy_anim, attack_anim)
                    waves -= 1
                else:
                    boss_here = True
            if boss_here:
                if event.type == USEREVENT+1:
                    destination = move_boss(boss_cord, attack_anim, generator_anim, lazor_anim)
                if event.type == USEREVENT+2:
                    if shoot_da_bouncy:
                        if bouncies <= 0:
                            shoot_da_bouncy = False
                            pygame.time.set_timer(USEREVENT+1, 2000)
                        sh = Fireball(boss_cord[0], boss_cord[1], 145 if random.randint(0, 1) == 1 else -145, power=15, animated=True, image=ball_anim, speed=5, max_frame=4, evil=True, len=64, height=64, bounces=5, behaviours=[Flags.BOUNCE], frame_delay=0.25)
                        PROJECTILE_TRACKER.append(sh)
                        bouncies -= 1

        if boss_here:
            draw_hitbox(boss_hitbox, fenetre, 0xFF0000)
        #draw_hitbox(john._box, fenetre, 0x00FF00)

        keys = pygame.key.get_pressed()
        john.action(keys)
        john.tick()
        for bubble in POWER_UP_TRACKER.copy():
            bubble.tick(john)
            fenetre.blit(bubble.get_image(), (bubble.x, bubble.y))
            if bubble.flagged_for_deletion:
                POWER_UP_TRACKER.remove(bubble)
        for baddie in ENNEMY_TRACKER.copy():
            fenetre.blit(baddie.get_image(), (baddie.x, baddie.y))
            baddie.tick(john)
            if baddie._creature.stats["life"].current_value <= 0:
                explode(baddie, manaorb_anim, lifeorb_anim)
                ENNEMY_TRACKER.remove(baddie)
            #draw_hitbox(baddie.hitbox, fenetre, 0xFF00A2)
        for proj in PROJECTILE_TRACKER.copy():
            proj.tick(john)
            #draw_hitbox(proj.box, fenetre, 0x0000FF)
            fenetre.blit(proj.get_image(), proj.get_pos())
            if boss_here:
                if not proj.evil and proj.box.is_colliding(boss_hitbox):
                    boss_life -= proj.power
                    text = fnt_txt.render(f'{proj.power}', False, (255, 30, 30))
                    TEXT_TRACKER.append([text, proj.x, proj.y, 255])
                    PROJECTILE_TRACKER.remove(proj)
            if proj.evil and proj.box.is_colliding(john._box):
                john.life -= proj.power
                text = fnt_txt.render(f'{proj.power}', False, (0, 0, 0))
                TEXT_TRACKER.append([text, proj.x, proj.y, 255])
                PROJECTILE_TRACKER.remove(proj)

        for txt in TEXT_TRACKER.copy():
            sfc = txt[0]
            sfc.set_alpha(txt[3])
            txt[3] -= 5
            txt[2] -= 3
            fenetre.blit(sfc, (txt[1], txt[2]))
            if txt[3] < 10:
                TEXT_TRACKER.remove(txt)
        draw_ui(john, bg, ui, fenetre, False, boss_life, boss_max)
        pygame.display.update()
        sleep(0.016)
        john.image = char_anim[int(frame) % 9]
        if frame >= 60:
            frame -= 60
    pygame.quit()
