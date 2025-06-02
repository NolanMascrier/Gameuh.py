from time import sleep
import random
from data.constants import *
from data.character import Character
from data.Sprite import Sprite
from data.projectile import Projectile
from data.physics.hitbox import HitBox
from data.physics.entity import Entity
from data.creature import Creature
from data.game.enemy import Enemy
from data.game.pickup import PickUp
from data.generator import Generator
from data.image.animation import Animation
from data.image.image import Image
from data.image.text_generator import TextGenerator
from data.spell_list import *

SPEED = 4
PLAYING = True
PLAYER = (50, SCREEN_HEIGHT/2)

SPEED_FACTOR = 5

UI_SKILLS_OFFSET = 600
UI_SKILLS_PANEL_OFFSET = 2
UI_SKILLS_INPUT_OFFSET = 48

shoot_da_bouncy = False
bouncies = 0

def draw_ui(char, bg, ui, boss_here = False, boss = None):
    cd = (char.cooldown + 0.001) / char.max_cooldown * 176
    if cd < 0:
        cd = 0
    mana = char.creature.stats["mana"].current_value / char.creature.stats["mana"].get_value() * 176
    life = char.creature.stats["life"].current_value / char.creature.stats["life"].get_value() * 176
    bossl = (boss.creature.stats["life"].current_value/boss.creature.stats["life"].c_value) * 1000
    #Positions
    posL = (0, 10)
    posM = (0, 50)
    posC = (0, 90)
    #sizes up
    l = pygame.transform.scale(ui[4], (life, 40))
    m = pygame.transform.scale(ui[5], (mana, 40))
    c = pygame.transform.scale(ui[6], (cd, 40))
    #jauges
    SYSTEM["windows"].blit(l, (posL[0] + 24, posL[1]))
    SYSTEM["windows"].blit(m, (posM[0] + 24, posM[1]))
    SYSTEM["windows"].blit(c, (posC[0] + 24, posC[1]))
    if boss_here:
        b = pygame.transform.scale(ui[7], (bossl, 80))
        bb = pygame.transform.scale(ui[8], (1000, 80))
        SYSTEM["windows"].blit(bb, (200, 20))
        SYSTEM["windows"].blit(b, (200, 20))
    #fluff
    SYSTEM["windows"].blit(ui[0], posL)
    SYSTEM["windows"].blit(ui[0], posM)
    SYSTEM["windows"].blit(ui[0], posC)
    #icons
    SYSTEM["windows"].blit(ui[1], posL)
    SYSTEM["windows"].blit(ui[2], posM)
    SYSTEM["windows"].blit(ui[3], posC)
    #Skills
    i = 0
    for name, skill in char._equipped_spells.items():
        SYSTEM["windows"].blit(SYSTEM["images"]["skill_bottom"].image, (UI_SKILLS_OFFSET + 104 * i, SCREEN_HEIGHT - 130))
        if skill is not None:
            cdc = skill.cooldown
            cdm = skill.stats["cooldown"].get_value()
            cdl = cdc / cdm * 60
            oom = bool(char.creature.get_efficient_value(skill.stats["mana_cost"].get_value()) > char.creature.stats["mana"].current_value)
            s = pygame.Surface((cdl, 60))
            s.set_alpha(128)
            s.fill((255, 196, 0))
            s2 = pygame.Surface((60, 60))
            s2.set_alpha(128 if oom else 0)
            s2.fill((255, 0, 0))
            SYSTEM["windows"].blit(skill.icon.get_image(), (UI_SKILLS_OFFSET + 104 * i, SCREEN_HEIGHT - 130))
            SYSTEM["windows"].blit(s2, (UI_SKILLS_OFFSET + UI_SKILLS_PANEL_OFFSET + 104 * i, SCREEN_HEIGHT - 128))
            SYSTEM["windows"].blit(s, (UI_SKILLS_OFFSET + UI_SKILLS_PANEL_OFFSET + 104 * i, SCREEN_HEIGHT - 128))
        SYSTEM["windows"].blit(SYSTEM["images"]["skill_top"].image, (UI_SKILLS_OFFSET + 104 * i, SCREEN_HEIGHT - 130))
        SYSTEM["windows"].blit(SYSTEM["images"][name], (UI_SKILLS_OFFSET + UI_SKILLS_INPUT_OFFSET + 104 * i, SCREEN_HEIGHT - 82))
        i += 1

def move_boss(boss, img, gen, laz):
    global shoot_da_bouncy, bouncies
    pattern = random.randint(0, 12)
    #pattern = 11
    x = random.randint(900, 1100)
    y = random.randint(0, SCREEN_HEIGHT - 300)
    if pattern >= 0 and pattern <= 7:
        for i in range(9):
            sh = Projectile(boss.x, boss.y, 200 - 5*i, SYSTEM["images"]["energyball"], FIREBOLT, boss.creature, True)
            PROJECTILE_TRACKER.append(sh)
            pass
    if pattern > 7 and pattern <= 10:
        pygame.time.set_timer(USEREVENT+1, 3500)
        shoot_da_bouncy = True
        bouncies = random.randint(2, 4)
    if pattern > 10 and pattern <= 12:
        for i in range(3):
            sh = Generator(boss.x, boss.y, (boss.x + random.randint(-100,100), boss.y+ random.randint(100,250) * (random.randint(0, 1) - 1)), 0.025, 1, 3,\
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

def draw_hitbox(box, color):
    s = pygame.Surface((box.width, box.height))
    s.set_alpha(128)
    s.fill(color)
    SYSTEM["windows"].blit(s, (box.x, box.y))
    s = pygame.Surface((4, 4))
    s.set_alpha(255)
    s.fill(color)
    SYSTEM["windows"].blit(s, box.center)

def spawn_boss():
    boss_cord = [1000, 500]
    boss_hitbox = HitBox(boss_cord[0], boss_cord[1], 100, 200)
    ent = Entity(boss_cord[0], boss_cord[1], SYSTEM["images"]["boss_a"], boss_hitbox, 5)
    crea = Creature("Orcus")
    crea.stats["life"].value = 500
    crea.stats["life"].refill()
    crea.stats["speed"].value = 12
    boss = Enemy(ent, crea, None)
    return boss

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
    
    boss = None
    destination = (1000, 500)
    boss_here = False
    waves = 1

    direction = K_DOWN
    pygame.init()
    pygame.font.init()
    pygame.time.set_timer(WAVE_TIMER, 2000)
    pygame.time.set_timer(USEREVENT+1, 2000)
    pygame.time.set_timer(USEREVENT+2, 100)
    flags = pygame.SCALED|pygame.FULLSCREEN
    SYSTEM["windows"] = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), flags, vsync=1)
    spri = Sprite("ressources/tiles/Island_24x24.png", 24, 24, 9, 8)
    fnt_txt = pygame.font.SysFont('ressources/dmg.ttf', 30)
    SYSTEM["font"] = pygame.font.SysFont('ressources/dmg.ttf', 30)
    SYSTEM["font_crit"] = pygame.font.SysFont('ressources/dmg.ttf', 35, True)
    SYSTEM["text_generator"] = TextGenerator()
    generate_spell_list()
    img = Animation("witch.png", 64, 64, frame_rate = 0.25)
    john = Character(imagefile=img)
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
    #john.rect = john.image.get_rect()
    index = 0
    bg = pygame.image.load("ressources/parallax_field.png").convert_alpha()
    parallaxes = [
        pygame.transform.scale(bg.subsurface((0, 0, 320, 180)), (SCREEN_WIDTH, SCREEN_HEIGHT)),
        pygame.transform.scale(bg.subsurface((320, 0, 320, 180)), (SCREEN_WIDTH, SCREEN_HEIGHT)),
        pygame.transform.scale(bg.subsurface((640, 0, 320, 180)), (SCREEN_WIDTH, SCREEN_HEIGHT)),
        pygame.transform.scale(bg.subsurface((960, 0, 320, 180)), (SCREEN_WIDTH, SCREEN_HEIGHT)),
        pygame.transform.scale(bg.subsurface((1280, 0, 320, 180)), (SCREEN_WIDTH, SCREEN_HEIGHT))
    ]

    SYSTEM["images"]["fireball"] = Animation("fireball.png", 32, 19, frame_rate=0.25).scale(38, 64)
    SYSTEM["images"]["energyball"] = Animation("pew.png", 13, 13, frame_rate=0.25).scale(32, 32)
    SYSTEM["images"]["boss_a"] = Animation("boss.png", 128, 150, frame_rate=0.25).scale(300, 256)
    SYSTEM["images"]["bouncer"] = Animation("bounce.png", 8, 8, frame_rate=0.25).scale(64, 64)
    SYSTEM["images"]["generator"] = Animation("generator.png", 8, 8, frame_rate=0.25).scale(32, 32)
    SYSTEM["images"]["lazer"] = Animation("lazor.png", 16, 10, frame_rate=0.25).scale(16, 64)

    manaorb = pygame.image.load("ressources/manaorb.png").convert_alpha()
    manaorb_anim = [pygame.transform.scale(manaorb.subsurface(x, 0, 16, 14), (16, 16))
                 for x in range(0, 64, 16)]

    lifeorb = pygame.image.load("ressources/lifeorb.png").convert_alpha()
    lifeorb_anim = [pygame.transform.scale(lifeorb.subsurface(x, 0, 16, 14), (16, 16))
                 for x in range(0, 64, 16)]

    badguy = Animation("badguy.png", 60, 130, frame_rate=0.25).flip(False, True)
    SYSTEM["images"]["skill_top"] = Image("ui/skill_top.png").scale(64, 64)
    SYSTEM["images"]["skill_bottom"] = Image("ui/skill_bottom.png").scale(64, 64)
    SYSTEM["images"][K_q] = Image("ui/kb_q.png").image
    SYSTEM["images"][K_e] = Image("ui/kb_e.png").image
    SYSTEM["images"][K_f] = Image("ui/kb_f.png").image
    SYSTEM["images"][K_r] = Image("ui/kb_r.png").image
    SYSTEM["images"][K_t] = Image("ui/kb_t.png").image
    SYSTEM["images"][K_LSHIFT] = Image("ui/kb_shift.png").image

    diff_x = [0.0, 0.0, 0.0, 0.0]
    speeds = [0.2, 0.6, 1.0, 2.0]
    frame = 0
    
    boss = spawn_boss()


    while PLAYING:
        frame += 0.2
        SYSTEM["windows"].blit(parallaxes[0], (0, 0))
        for i in range(4):
            diff_x[i] = (diff_x[i] + speeds[i] * SPEED_FACTOR) % SCREEN_WIDTH
        for layer in range(4):
            for y in range(0, 2):
                x = int((y * SCREEN_WIDTH) - diff_x[layer])
                SYSTEM["windows"].blit(parallaxes[layer + 1], (x, 0))

        SYSTEM["windows"].blit(john.get_image(), john.get_pos())
        if boss_here:
            boss.entity.move(destination)
            SYSTEM["windows"].blit(boss.entity.get_image(), (boss.x, boss.y))

        for event in pygame.event.get():
            if event.type == QUIT:
                PLAYING = False
            if event.type == WAVE_TIMER:
                if waves > 0:
                    pygame.time.set_timer(WAVE_TIMER, 12000)
                    spawn_enemies(badguy, SYSTEM["images"]["energyball"])
                    waves -= 1
                else:
                    boss_here = True
            if boss_here:
                if event.type == USEREVENT+1:
                    destination = move_boss(boss, SYSTEM["images"]["energyball"], SYSTEM["images"]["generator"], SYSTEM["images"]["lazer"])
                if event.type == USEREVENT+2:
                    if shoot_da_bouncy:
                        if bouncies <= 0:
                            shoot_da_bouncy = False
                            pygame.time.set_timer(USEREVENT+1, 2000)
                        sh = Projectile(boss.x, boss.y, 145 if random.randint(0, 1) == 1 else -145, SYSTEM["images"]["bouncer"], ICEBOLT, boss.creature, speed=5, evil=True, bounces=5, behaviours=[Flags.BOUNCE])
                        PROJECTILE_TRACKER.append(sh)
                        bouncies -= 1

        #if boss_here:
        #    draw_hitbox(boss_hitbox, 0xFF0000)
        #draw_hitbox(john.hitbox, 0x00FF00)

        keys = pygame.key.get_pressed()
        john.action(keys)
        john.tick()
        boss.tick(john)
        for bubble in POWER_UP_TRACKER.copy():
            bubble.tick(john)
            SYSTEM["windows"].blit(bubble.get_image(), (bubble.x, bubble.y))
            if bubble.flagged_for_deletion:
                POWER_UP_TRACKER.remove(bubble)
        for baddie in ENNEMY_TRACKER.copy():
            SYSTEM["windows"].blit(baddie.get_image(), (baddie.x, baddie.y))
            baddie.tick(john)
            if baddie._creature.stats["life"].current_value <= 0:
                explode(baddie, manaorb_anim, lifeorb_anim)
                ENNEMY_TRACKER.remove(baddie)
        for proj in PROJECTILE_TRACKER.copy():
            if not isinstance(proj, Projectile):
                continue
            proj.tick()
            SYSTEM["windows"].blit(proj.get_image(), proj.get_pos())
            if proj.evil and proj.hitbox.is_colliding(john.hitbox):
                dmg, crit = john.creature.damage(proj.damage)
                SYSTEM["text_generator"].generate_damage_text(proj.x, proj.y, (255, 30, 30), crit, dmg)
                PROJECTILE_TRACKER.remove(proj)

        for txt in TEXT_TRACKER.copy():
            sfc = txt[0]
            sfc.set_alpha(txt[3])
            txt[3] -= 5
            txt[2] -= 3
            SYSTEM["windows"].blit(sfc, (txt[1], txt[2]))
            if txt[3] < 10:
                TEXT_TRACKER.remove(txt)
        draw_ui(john, bg, ui, boss_here, boss)
        pygame.display.update()
        sleep(0.016)
        john.tick()
        if frame >= 60:
            frame -= 60
    pygame.quit()
