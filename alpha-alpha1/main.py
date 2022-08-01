import pygame
import os
from random import randint
import threading
WIDTH, HEIGHT = 720, 900
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Holy Bologna")
pygame.font.init()
GENERAL_FONT = pygame.font.SysFont('comicsans', 30)
BOLOGNA_WIDTH, BOLOGNA_HEIGHT = 96, 45
BOLOGNA_SPRITE = pygame.image.load(
    os.path.join('Assets', 'bologna.png'))
BOLOGNA = pygame.transform.scale(BOLOGNA_SPRITE, (BOLOGNA_WIDTH, BOLOGNA_HEIGHT))
COLOR_WHITE = (255, 255, 255)
COLOR_RED = (255, 0, 0)
COLOR_BLUE = (0, 0, 255)
COLOR_PURPLE = (255, 0, 255)
BOLOGNA_SLAP = pygame.USEREVENT + 1
BOLOGNA_STARTPOS_X = ((WIDTH / 2) - (BOLOGNA_WIDTH / 2))
BOLOGNA_STARTPOS_Y = HEIGHT - BOLOGNA_HEIGHT - 100
DELI = pygame.transform.scale(pygame.image.load(os.path.join('Assets', 'deli.jpg')), (WIDTH, HEIGHT))
LEVEL_TEXT = pygame.transform.scale(pygame.image.load(os.path.join('Assets', 'level.png')), (300, 150))
GUI = pygame.image.load(os.path.join('Assets', 'gui.png'))
FALLING_BOLOGNA_SPEED = 5
BASE_VELOCITY = 3
VELOCITY = 3
FPS = 144


def draw_window(cursor, falling_bolognas, captured_bolognas, level_msg):
    level_text = GENERAL_FONT.render(str(level_display), 1, COLOR_BLUE)
    stack_text = GENERAL_FONT.render(f'{len(captured_bolognas)}', 1, COLOR_PURPLE)
    missed_text = GENERAL_FONT.render(f'{missed_bologna}', 1, COLOR_RED)
    WIN.blit(DELI, (0, 0))
    WIN.blit(BOLOGNA, (cursor.x, cursor.y))
    if level_msg == True:
        WIN.blit(LEVEL_TEXT, ((WIDTH/2) - 250, 30))
    for bologna in falling_bolognas:
        WIN.blit(BOLOGNA, (bologna.x, bologna.y))
    for bologna in captured_bolognas:
        WIN.blit(BOLOGNA, (cursor.x, cursor.y - (8 * captured_bolognas.index(bologna))))
    WIN.blit(GUI, (0, 0))
    WIN.blit(level_text, (630, 30))
    WIN.blit(stack_text, (170, 835))
    WIN.blit(missed_text, (630, 835))
    pygame.display.update()

def cursor_move(keys_pressed, cursor):
    if keys_pressed[pygame.K_LEFT] and cursor.x - VELOCITY > 50:
        cursor.x -= VELOCITY
    if keys_pressed[pygame.K_RIGHT] and cursor.x + VELOCITY + BOLOGNA_WIDTH < WIDTH - 50:
        cursor.x += VELOCITY

def incoming_bologna(falling_bolognas, cursor, captured_bolognas):
    for bologna in falling_bolognas:
        bologna.y += FALLING_BOLOGNA_SPEED
        if cursor.colliderect(bologna):
            pygame.event.post(pygame.event.Event(BOLOGNA_SLAP))
            captured_bolognas.append(bologna)
            falling_bolognas.remove(bologna)

def remove_bologna(falling_bolognas):
    global missed_bologna
    for bologna in falling_bolognas:
        if bologna.y > HEIGHT:
            falling_bolognas.remove(bologna)
            missed_bologna += 1
            print(missed_bologna)

def main():
    global level
    global level_display
    global FALLING_BOLOGNA_SPEED
    global VELOCITY
    global missed_bologna
    global captured_bolognas
    cursor = pygame.Rect(BOLOGNA_STARTPOS_X, BOLOGNA_STARTPOS_Y, BOLOGNA_WIDTH, BOLOGNA_HEIGHT)
    tick1 = 0
    tick2 = 0
    tick3 = 0
    level_display = 1
    missed_bologna = 0
    bologna_count = 0
    captured_bolognas = []
    falling_bolognas = []
    score = 0
    falling_bologna_refresh = 250
    level = 1
    level_msg = False
    clock = pygame.time.Clock()
    run = True
    while run:
        clock.tick(FPS)
        tick1 += 1
        tick2 += 1
        tick3 += 1

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == BOLOGNA_SLAP:
                score += 1
        if score % 10 == 0 and score != 0:
            tick2 = 0
            tick3 = 0
            level_msg = True
            captured_bolognas = []
            print(level)
            level_display = level
        if tick3 == 1:
            level += 1
            falling_bologna_refresh -= 50
            FALLING_BOLOGNA_SPEED += .5

            
        if tick2 == 360:
            tick2 = 0
            level_msg = False
        keys_pressed = pygame.key.get_pressed()
        if keys_pressed[pygame.K_SPACE]:
            VELOCITY = BASE_VELOCITY + (level * .5)
        else:
            VELOCITY = 3
        cursor_move(keys_pressed, cursor)
        if tick1 == (256 - (level * 16)):
            print((level**(-1)*2)*256)
            tick1 = 0
            falling_bologna = pygame.Rect((randint(50, WIDTH - (BOLOGNA_WIDTH) - 50)), 0, BOLOGNA_WIDTH, BOLOGNA_HEIGHT)
            falling_bolognas.append(falling_bologna)
        remove_bologna(falling_bolognas)
        incoming_bologna(falling_bolognas, cursor, captured_bolognas)
        draw_window(cursor, falling_bolognas, captured_bolognas, level_msg)
    pygame.quit()


if __name__ == "__main__":
    main()