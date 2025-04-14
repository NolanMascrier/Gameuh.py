from constants import *
from Character import Character
from Sprite import Sprite

SPEED = 4
PLAYING = True
PLAYER = (50, 50)

dungeon = [
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
]

def draw_ui(char, bg, ui, fenetre):
    cd = (char.cooldown + 0.001) / char.max_cooldown * 176
    mana = char.mana / 100 * 176
    life = char.life / 100 * 176
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
    #fluff
    fenetre.blit(ui[0], posL)
    fenetre.blit(ui[0], posM)
    fenetre.blit(ui[0], posC)
    #icons
    fenetre.blit(ui[1], posL)
    fenetre.blit(ui[2], posM)
    fenetre.blit(ui[3], posC)

if __name__ == "__main__":
    direction = K_DOWN
    john = Character()
    pygame.init()
    fenetre = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    spri = Sprite("ressources/tiles/Island_24x24.png", 24, 24, 9, 8)
    FONT = pygame.font.SysFont('Comic Sans MS', 11)
    john.image = pygame.image.load("ressources/dude.png").convert_alpha()
    john.sprite = {K_UP:[john.image.subsurface(x,0,64,64)for x in range(0,576,64)],
               K_LEFT:[john.image.subsurface(x,64,64,64)for x in range(0,576,64)],
               K_DOWN:[john.image.subsurface(x,128,64,64)for x in range(0,576,64)],
               K_RIGHT:[john.image.subsurface(x,192,64,64)for x in range(0,576,64)]}
    ui = [
        pygame.transform.scale(pygame.image.load(UI_JAUGE).convert_alpha(), (200, 40)),
        pygame.transform.scale(pygame.image.load(UI_JAUGE_L).convert_alpha(), (200, 40)),
        pygame.transform.scale(pygame.image.load(UI_JAUGE_M).convert_alpha(), (200, 40)),
        pygame.transform.scale(pygame.image.load(UI_JAUGE_C).convert_alpha(), (200, 40)),
        pygame.transform.scale(pygame.image.load(JAUGE_L).convert_alpha(), (176, 40)),
        pygame.transform.scale(pygame.image.load(JAUGE_M).convert_alpha(), (176, 40)),
        pygame.transform.scale(pygame.image.load(JAUGE_C).convert_alpha(), (176, 40))
    ]
    john.rect = john.image.get_rect()
    index = 0
    bg = pygame.image.load("ressources/background.jpg").convert()
    while PLAYING:
        y = 0
        yd = 0
        for line in dungeon:
            x = 0
            xd = 0
            for cell in line:
                if cell == 1:
                    fenetre.blit(spri.set[4][1], (x, y))
                elif (xd + 1) < len(dungeon[0]) and cell == 0 and dungeon[yd][xd + 1] == 1:
                    fenetre.blit(spri.set[4][0], (x, y))
                elif (xd - 1) > 0 and cell == 0 and dungeon[yd][xd - 1] == 1:
                    fenetre.blit(spri.set[4][3], (x, y))
                elif (yd + 1) < len(dungeon) and cell == 0 and dungeon[yd + 1][xd] == 1:
                    fenetre.blit(spri.set[3][1], (x, y))
                elif (yd - 1) > 0 and cell == 0 and dungeon[yd - 1][xd] == 1:
                    fenetre.blit(spri.set[6][1], (x, y))
                elif (yd - 2) > 0 and cell == 0 and dungeon[yd - 2][xd] == 1:
                    fenetre.blit(spri.set[7][1], (x, y))
                #corners
                elif (xd + 1) < len(dungeon[0]) and (yd + 1) < len(dungeon) and cell == 0 and dungeon[yd + 1][xd + 1] == 1:
                    fenetre.blit(spri.set[3][0], (x, y))
                elif (xd - 1) > 0 and (yd + 1) < len(dungeon) and cell == 0 and dungeon[yd + 1][xd - 1] == 1:
                    fenetre.blit(spri.set[3][3], (x, y))
                #general
                else:
                    fenetre.blit(spri.set[7][4], (x, y))
                x += 24
                xd += 1
            y += 24
            yd += 1
        fenetre.blit(john.get_sprite(), john.get_pos())
        for proj in PROJECTILE_TRACKER:
            fenetre.blit(proj._rect, proj.get_pos())
        for event in pygame.event.get():
            if event.type == QUIT:
                PLAYING = False
        keys = pygame.key.get_pressed()
        john.action(keys)
        john.tick()
        for proj in PROJECTILE_TRACKER:
            proj.tick()
        draw_ui(john, bg, ui, fenetre)
        pygame.display.update()
        sleep(0.016)
    pygame.quit()