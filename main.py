import pygame
import os
from random import randint
import threading
from time import sleep
WIDTH, HEIGHT = 720, 900
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Holy Bologna")
pygame.font.init()
GENERAL_FONT = pygame.font.SysFont('comicsans', 30)
BOLOGNA_WIDTH, BOLOGNA_HEIGHT = 96, 45
COLOR_WHITE = (255, 255, 255)
COLOR_RED = (255, 0, 0)
COLOR_BLUE = (0, 0, 255)
COLOR_PURPLE = (255, 0, 255)
BOLOGNA_SLAP = pygame.USEREVENT + 1
DROP_BOLOGNA = pygame.USEREVENT + 2
LEVEL_UP = pygame.USEREVENT + 3
MISSED_BOLOGNA = pygame.USEREVENT + 4
BOLOGNA_STARTPOS_X = ((WIDTH / 2) - (BOLOGNA_WIDTH / 2))
BOLOGNA_STARTPOS_Y = HEIGHT - BOLOGNA_HEIGHT - 100
BOLOGNA_SPRITE = pygame.image.load(os.path.join('Assets', 'bologna.png')).convert_alpha()
DELI = pygame.transform.scale(pygame.image.load(os.path.join('Assets', 'deli.jpg')), (WIDTH, HEIGHT)).convert_alpha()
LEVEL_TEXT = pygame.transform.scale(pygame.image.load(os.path.join('Assets', 'level.png')), (300, 150)).convert_alpha()
GUI = pygame.image.load(os.path.join('Assets', 'gui.png')).convert_alpha()
BOLOGNA = pygame.transform.scale(BOLOGNA_SPRITE, (BOLOGNA_WIDTH, BOLOGNA_HEIGHT))
FALLING_BOLOGNA_SPEED = 4
BASE_DROP_DELAY = 1.5
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
    if keys_pressed[pygame.K_SPACE]:
        if level_display > 5:
            VELOCITY = BASE_VELOCITY + (level * .2)
        else:
            VELOCITY = BASE_VELOCITY + (2.5)
    else:
        VELOCITY = 3
    if keys_pressed[pygame.K_LEFT] and cursor.x - VELOCITY > 75:
        cursor.x -= VELOCITY
    if keys_pressed[pygame.K_RIGHT] and cursor.x + VELOCITY + BOLOGNA_WIDTH < WIDTH - 75:
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
            pygame.event.post(pygame.event.Event(MISSED_BOLOGNA))

def handle_falling_bologna():
    while run:
        sleep_delay = BASE_DROP_DELAY / (level_display**(1/BASE_DROP_DELAY))
        sleep(sleep_delay)
        try:
            pygame.event.post(pygame.event.Event(DROP_BOLOGNA))
        except:
            pass

def handle_level_msg():
    global level_msg
    while run:
        if level_msg == True:
            sleep(2)
            level_msg = False
        else:
            sleep(.2)

def main():
    global run
    global level
    global level_display
    global FALLING_BOLOGNA_SPEED
    global VELOCITY
    global missed_bologna
    global captured_bolognas
    global level_msg
    cursor = pygame.Rect(BOLOGNA_STARTPOS_X, BOLOGNA_STARTPOS_Y, BOLOGNA_WIDTH, BOLOGNA_HEIGHT)
    level_display = 1
    missed_bologna = 0
    captured_bolognas = []
    falling_bolognas = []
    score = 0
    level = 1
    level_msg = False
    clock = pygame.time.Clock()
    run = True
    
    drop_bologna_thread = threading.Thread(target=handle_falling_bologna)
    drop_bologna_thread.start()
    level_msg_thread = threading.Thread(target=handle_level_msg)
    level_msg_thread.start()

    while run:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == BOLOGNA_SLAP:
                score += 1
            if event.type == DROP_BOLOGNA:
                falling_bologna = pygame.Rect((randint(75, WIDTH - (BOLOGNA_WIDTH) - 75)), 0, BOLOGNA_WIDTH, BOLOGNA_HEIGHT)
                falling_bolognas.append(falling_bologna)
            if event.type == LEVEL_UP:
                captured_bolognas = []
                level_msg = True
                level_display = level
                level += 1
                FALLING_BOLOGNA_SPEED += .3
            if event.type == MISSED_BOLOGNA:
                if len(captured_bolognas) > 0:
                    for bologna in captured_bolognas:
                        if (captured_bolognas.index(bologna) + 1) == len(captured_bolognas):
                            captured_bolognas.remove(bologna)
                            if score > 0:
                                score -= 1
                else:
                    # Here's where you would 'lose' the game 
                    # I'm not that mean tho
                    pass

        if score % 10 == 0 and score != 0:
            pygame.event.post(pygame.event.Event(LEVEL_UP))
            score = 0
        keys_pressed = pygame.key.get_pressed()
        cursor_move(keys_pressed, cursor)
        remove_bologna(falling_bolognas)
        incoming_bologna(falling_bolognas, cursor, captured_bolognas)
        draw_window(cursor, falling_bolognas, captured_bolognas, level_msg)
    pygame.quit()


if __name__ == "__main__":
    main()