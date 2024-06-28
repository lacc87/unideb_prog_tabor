import random

import pygame
import sys

# Initialize pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 800, 600
FPS = 30 # Frames per second for the animation
CHARACTER_STATES = 6
CHARACTER_WIDTH, CHARACTER_HEIGHT = 100, 100  # Assuming each state is 64x64 pixels

# Set up the display
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Super RPG game")


# Load sprite sheet
soldier_idle = pygame.image.load('sprites/Soldier/Soldier/Soldier-Idle.png').convert_alpha()

soldier_walk = pygame.image.load('sprites/Soldier/Soldier/Soldier-Walk.png').convert_alpha()

soldier_hurt = pygame.image.load('sprites/Soldier/Soldier/Soldier-Hurt.png').convert_alpha()

soldier_attack1 = pygame.image.load('sprites/Soldier/Soldier/Soldier-Attack01.png').convert_alpha()

ground = pygame.image.load('sprites/background/TX Tileset Grass.png').convert_alpha()

#Enemy
orc_idle = pygame.image.load('sprites/Orc/Orc/Orc-Idle.png').convert_alpha()

orc_walk = pygame.image.load('sprites/Orc/Orc/Orc-Walk.png').convert_alpha()

orc_hurt = pygame.image.load('sprites/Orc/Orc/Orc-Hurt.png').convert_alpha()

orc_attack1 = pygame.image.load('sprites/Orc/Orc/Orc-Attack01.png').convert_alpha()

heart = pygame.image.load('sprites/heart.png').convert_alpha()

def get_map(sprite, x, y):
    return sprite.subsurface(pygame.Rect(x * 16, y * 16, 16, 16))

# Function to get a single frame from the sprite sheet
def get_frame(sprite, frame):
    return sprite.subsurface(pygame.Rect(frame * CHARACTER_WIDTH, 0, CHARACTER_WIDTH, CHARACTER_HEIGHT))

# Main game loop
def main():
    clock = pygame.time.Clock()
    frame = 0

    # character location
    charx = 400
    chary = 400

    # enemy location
    orcx = 100
    orcy = 100

    # enemy speed
    orcspeedx = 0
    orcspeedy = 0

    # speed
    speedx = 0
    speedy = 0

    health = 3

    score = 0

    #attack
    attack1 = False
    orcattack1 = False

    stamina = 200

    hurt = False
    enemyhurt = False
    hurttime = 0
    attacktime = 0

    newhurtposx = 0
    newhurtposy = 0

    # orientation
    charright = True
    orcright = True

    attackframe = 0

    map_tile_x = []
    rows, cols = 20, 20
    for i in range(rows):
        col = []
        for j in range(cols):
            col.append(0)
        map_tile_x.append(col)

    map_tile_y = []
    rows, cols = 20, 20
    for i in range(rows):
        col = []
        for j in range(cols):
            col.append(0)
        map_tile_y.append(col)

    random.seed(316)
    for x in range(15):
        for y in range(15):
            map_tile_x[x][y] = random.randint(0, 15)
            map_tile_y[x][y] = random.randint(0, 15)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT:
                    speedx = 0
                if event.key == pygame.K_RIGHT:
                    speedx = 0
                if event.key == pygame.K_UP:
                    speedy = 0
                if event.key == pygame.K_DOWN:
                    speedy = 0
                if event.key == pygame.K_SPACE:
                    attack1 = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    speedx = -40.5
                    charright = False

                if event.key == pygame.K_RIGHT:
                    speedx = 40.5
                    charright = True

                if event.key == pygame.K_UP:
                    speedy = -40.5
                if event.key == pygame.K_DOWN:
                    speedy = 40.5
                if event.key == pygame.K_SPACE:
                    attack1 = True

        stamina = stamina + 10
        if attack1:
            stamina = stamina - 20

        if stamina > 200:
            stamina = 200
        if stamina < 0:
            stamina = 0

        if health == 0:
            speedx = 0
            speedy = 0
            orcspeedy = 0
            orcspeedx = 0
        else:
            if not hurt:
                charx = charx + speedx
                chary = chary + speedy
                orcx = orcx + orcspeedx
                orcy = orcy + orcspeedy

            orcspeedx = charx - orcx

            if orcspeedx > 0:
                orcright = True
            else:
                orcright = False

            if abs(orcspeedx) > 20:
                orcspeedx = orcspeedx / abs(orcspeedx) * 5
            else:
                orcspeedx = 0

            orcspeedy = chary - orcy

            if abs(orcspeedy) > 20:
                orcspeedy = orcspeedy / abs(orcspeedy) * 5
            else:
                orcspeedy = 0

            if charx + 150 < 0:
                charx = -150
            if charx + 250 > WIDTH:
                charx = WIDTH - 250

            if chary + 150 < 0:
                chary = -150
            if chary + 250 > HEIGHT:
                chary = HEIGHT - 250
                #charx + 150, chary + 150, 100, 100

            if abs(charx - orcx) < 40 and abs(chary - orcy) < 40:
                orcattack1 = True
            else:
                orcattack1 = False

        # Update frame
        frame = (frame + 1) % CHARACTER_STATES

        if abs(charx - orcx) < 45 and abs(chary - orcy) < 45 and attack1:
            attacktime = attacktime + 1
        else:
            attacktime = 0

        if attacktime == 7:
            enemyhurt = True
            attacktime = 0
            score = score + 1
            if orcx < 300:
                newhurtposx = 150
            else:
                newhurtposx = -150
            if orcy < 300:
                newhurtposy = 150
            else:
                newhurtposy = -150


        # Clear the screen
        screen.fill((0, 0, 0))

        for x in range(15):
            for y in range(15):
                mapxy = get_map(ground, map_tile_x[x][y], map_tile_y[x][y])
                mapxy = pygame.transform.scale(mapxy, (64, 64))
                screen.blit(mapxy, (x * 64, y * 64))

        # Draw the current frame
        if hurt:
            hurttime = hurttime + 1
            if hurttime == (FPS / 2):
                hurt = False
                hurttime = 0
            current_frame = get_frame(soldier_hurt, frame % 4)

            charx = charx + newhurtposx / (FPS / 2)
            chary = chary + newhurtposy / (FPS / 2)
        else:
            if attack1:
                current_frame = get_frame(soldier_attack1, frame)
            else:
                if speedx == 0 and speedy == 0:
                    current_frame = get_frame(soldier_idle, frame)
                else:
                    current_frame = get_frame(soldier_walk, frame)

        current_frame = pygame.transform.scale(current_frame, (400, 400))
        current_frame = pygame.transform.flip(current_frame, not charright, False)

        screen.blit(current_frame, (charx, chary))

        if enemyhurt:
            hurttime = hurttime + 1
            if hurttime == (FPS / 2):
                enemyhurt = False
                hurttime = 0
            current_frame_orc = get_frame(orc_hurt, frame % 4)

            orcx = orcx + newhurtposx / (FPS / 2)
            orcy = orcy + newhurtposy / (FPS / 2)
        else:
            if orcattack1:
                current_frame_orc = get_frame(orc_attack1, frame)
                if abs(charx - orcx) < 40 and abs(chary - orcy) < 40:
                    attackframe = attackframe + 1
                else:
                    attackframe = 0
            else:
                attackframe = 0
                if orcspeedx == 0 and orcspeedy == 0:
                    current_frame_orc = get_frame(orc_idle, frame)
                else:
                    current_frame_orc = get_frame(orc_walk, frame)

        current_frame_orc = pygame.transform.scale(current_frame_orc, (400, 400))
        current_frame_orc = pygame.transform.flip(current_frame_orc,  not orcright, False)

        screen.blit(current_frame_orc, (orcx, orcy))

        if attackframe == 6:
            health = health - 1
            attackframe = 0
            hurt = True
            if health != 0:
                if charx < 300:
                    newhurtposx = 150
                else:
                    newhurtposx = -150
                if chary < 300:
                    newhurtposy = 150
                else:
                    newhurtposy = -150


        green = (255, 255, 255)
        blue = (0, 0, 0)

        # create a font object.
        # 1st parameter is the font file
        # which is present in pygame.
        # 2nd parameter is size of the font
        font = pygame.font.Font('freesansbold.ttf', 32)

        text = font.render('SCORE: ' + str(score), True, green, blue)
        textRect = text.get_rect()

        textRect.center = (400, 20)
        screen.blit(text, textRect)

        # create a text surface object,
        # on which text is drawn on it.
        if health == 0:
            text = font.render('GAME OVER', True, green, blue)
            textRect = text.get_rect()

            textRect.center = (400, 300)
            screen.blit(text, textRect)



        if health > 2:
            screen.blit(heart, (WIDTH - 120, HEIGHT - 40))
        if health > 1:
            screen.blit(heart, (WIDTH - 80, HEIGHT - 40))
        if health > 0:
            screen.blit(heart, (WIDTH - 40, HEIGHT - 40))

        #pygame.draw.rect(screen, (255,0,0), pygame.Rect(charx + 150, chary + 150, 100, 100), 2)

        pygame.draw.rect(screen, (255, 0, 0), pygame.Rect(20, 560, 200, 20), 2)
        pygame.draw.rect(screen, (255, 0, 0), pygame.Rect(20, 560, stamina, 20), 20)

        # Update the display
        pygame.display.flip()

        # Cap the frame rate
        clock.tick(FPS)

if __name__ == "__main__":
    main()
