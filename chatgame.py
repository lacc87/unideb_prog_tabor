import random

import pygame
import sys

import time


import socket
import threading

import re

def use_regex(input_text):
    pattern = re.compile(r"[A-Za-z]+\|\d+|[A-Za-z]+\|-?[0-9],-?[0-9]+,-?[0-9]+,-?[0-9]+", re.IGNORECASE)
    return pattern.match(input_text)

SERVER_IP = "172.22.230.10"
SERVER_PORT = 12000
BUFFER_SIZE = 1024

players = {}  # "ID": "x,y"
playertime = {}


def receive_message(client_socket, stop):
    while True:
        try:
            if stop():
                break
            message, _ = client_socket.recvfrom(BUFFER_SIZE)
            message = message.decode('utf-8').split("#")
            players[message[0]] = message[1]
            playertime[message[0]] = time.time()

        except:
            pass


# Initialize pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 640, 640
FPS = 12  # Frames per second for the animation
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


def get_map(sprite, x, y):
    return sprite.subsurface(pygame.Rect(x * 16, y * 16, 16, 16))


# Function to get a single frame from the sprite sheet
def get_frame(sprite, frame):
    return sprite.subsurface(pygame.Rect(frame * CHARACTER_WIDTH, 0, CHARACTER_WIDTH, CHARACTER_HEIGHT))


# Main game loop
def main():
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    stop_threads = False

    receive_thread = threading.Thread(target=receive_message, args=(client_socket, lambda: stop_threads))
    receive_thread.start()

    clock = pygame.time.Clock()
    frame = 0

    current_frame_x = 0
    current_frame_y = 0

    # character location
    charx = 300
    chary = 300

    # speed
    speedx = 0
    speedy = 0
    anim = 0

    # orientation
    charright = True
    attack1 = False

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

    while True:

        random.seed(current_frame_x * 1000 + current_frame_y)
        for x in range(15):
            for y in range(15):
                map_tile_x[x][y] = random.randint(0, 15)
                map_tile_y[x][y] = random.randint(0, 15)

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
                if event.key == pygame.K_ESCAPE:
                    stop_threads = True
                    pygame.quit()
                    sys.exit()
                if event.key == pygame.K_LEFT:
                    speedx = -40.5
                    charright = False
                if event.key == pygame.K_SPACE:
                    attack1 = True
                if event.key == pygame.K_RIGHT:
                    speedx = 40.5
                    charright = True

                if event.key == pygame.K_UP:
                    speedy = -40.5
                if event.key == pygame.K_DOWN:
                    speedy = 40.5
        # Update frame
        frame = (frame + 1) % CHARACTER_STATES

        charx = charx + speedx
        chary = chary + speedy

        if charx < -150:
            charx = -150
            if current_frame_x > 0:
                current_frame_x = current_frame_x - 1
                charx = 640 - 160
        if chary < -150:
            chary = -150
            if current_frame_y > 0:
                current_frame_y = current_frame_y - 1
                chary = 640 - 160

        if charx > 640 - 150:
            charx = -150
            current_frame_x = current_frame_x + 1
        if chary > 640 - 150:
            chary = -150
            current_frame_y = current_frame_y + 1

        # Clear the screen
        screen.fill((0, 0, 0))

        for x in range(15):
            for y in range(15):
                mapxy = get_map(ground, map_tile_x[x][y], map_tile_y[x][y])
                mapxy = pygame.transform.scale(mapxy, (64, 64))
                screen.blit(mapxy, (x * 64, y * 64))

        if attack1:
            current_frame = get_frame(soldier_attack1, frame)
            anim = 0
        else:
            if speedx == 0 and speedy == 0:
                current_frame = get_frame(soldier_idle, frame)
                anim = 1
            else:
                current_frame = get_frame(soldier_walk, frame)
                anim = 2

        current_frame = pygame.transform.scale(current_frame, (400, 400))
        current_frame_2 = pygame.transform.scale(current_frame, (400, 400))
        current_frame = pygame.transform.flip(current_frame, not charright, False)

        client_socket.sendto(("Laci|" + str(anim) + "|" + str(charright) + "|" + str(round(charx)) + "," + str(round(chary)) + "," + str(current_frame_x) + "," + str(current_frame_y)).encode('utf-8'),(SERVER_IP, SERVER_PORT))

        screen.blit(current_frame, (charx, chary))

        green = (255, 255, 255)
        blue = (0, 0, 0)

        font = pygame.font.Font('freesansbold.ttf', 24)

        for key, value in players.copy().items():
            now = time.time()
            if now - playertime[key] < 5 and use_regex(value) is not None:
                NAMEOXY = value.split("|")
                NAME = NAMEOXY[0]
                anim = int(NAMEOXY[1])
                cr = NAMEOXY[2].lower() == "true"
                XY = NAMEOXY[3].split(",")
                if len(XY) != 4:
                    continue

                if int(XY[2]) != current_frame_x or int(XY[3]) != current_frame_y:
                    continue

                current_frame = get_frame(soldier_idle, frame)
                if anim == 0:
                    current_frame = get_frame(soldier_attack1, frame)
                if anim == 1:
                    current_frame = get_frame(soldier_idle, frame)
                if anim == 2:
                    current_frame = get_frame(soldier_walk, frame)

                current_frame = pygame.transform.scale(current_frame, (400, 400))
                current_frame = pygame.transform.flip(current_frame, not cr, False)

                screen.blit(current_frame, (float(XY[0]), float(XY[1])))

                text = font.render(NAME, True, green, blue)
                textRect = text.get_rect()

                textRect.center = (float(XY[0]) + 200, float(XY[1]) + 150)
                screen.blit(text, textRect)

        text = font.render('MY CHAR', True, green, blue)
        textRect = text.get_rect()

        textRect.center = (charx + 200, chary + 150)
        screen.blit(text, textRect)

        # Update the display
        pygame.display.flip()

        # Cap the frame rate
        clock.tick(FPS)


if __name__ == "__main__":
    main()
