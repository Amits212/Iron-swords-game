import pygame
import random
import keyboard
import time
from pygame.locals import (
    K_ESCAPE,
    KEYDOWN,
)

pygame.init()

screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
clock = pygame.time.Clock()

background_image = pygame.image.load('gaza1.jpg')

RED = (255, 0, 0)
BLUE = (0, 0, 255)
screen_width = screen.get_width()
screen_height = screen.get_height()

rcircles = []
bcircles = []
for _ in range(20):
    rcircle = {
        'x': random.randint(0, screen_width),
        'y': random.randint(0, screen_height),
        'x_vel': random.uniform(-2, 2),
        'y_vel': random.uniform(-2, 2),
        'radius': 4
    }
    rcircles.append(rcircle)
for _ in range(10):
    bcircle = {
        'x': random.randint(0, screen_width),
        'y': random.randint(0, screen_height),
        'x_vel': random.uniform(-2, 2),
        'y_vel': random.uniform(-2, 2),
        'radius': 4
    }
    bcircles.append(bcircle)

font = pygame.font.Font('freesansbold.ttf', 32)

text = font.render('Game over', True, (0, 0, 255), (255, 255, 0))
textRect = text.get_rect()
textRect.center = (screen_width // 2, screen_height // 2)

text2 = font.render('You won all terrorist are dead!', True, (0, 0, 255), (255, 255, 0))
text2Rect = text2.get_rect()
text2Rect.center = (screen_width // 2, screen_height // 2)


rect_width = 60
rect_height = 60
rect_x = (screen_width - rect_width) // 2
rect_y = (screen_height - rect_height) // 2
rect = pygame.Rect(rect_x, rect_y, rect_width, rect_height)

ex_list = ['ex1.png', 'ex2.png', 'ex3.png', 'ex4.png', 'ex5.png', 'ex6.png', 'ex7.png', 'ex8.png', 'ex9.png']
explosions = [pygame.transform.scale(pygame.image.load(ex), (60, 60)) for ex in ex_list]
current_explosion_index = 0  # Initialize the current explosion index
last_animation_time = time.time()  # Initialize the timer
positions = []

running = True
while running:

    clock.tick(100)
    for event in pygame.event.get():
        if event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                running = False
            elif event.key == pygame.K_SPACE:
                last_animation_time = time.time()
                current_explosion_index = 0
                positions.append((rect.x, rect.y))

    for rcircle in rcircles:
        rcircle['x'] += rcircle['x_vel']
        rcircle['y'] += rcircle['y_vel']

        if rcircle['x'] < 0 or rcircle['x'] > screen_width:
            rcircle['x_vel'] *= -1
        elif rcircle['y'] < 0 or rcircle['y'] > screen_height:
            rcircle['y_vel'] *= -1

    for bcircle in bcircles:
        bcircle['x'] += bcircle['x_vel']
        bcircle['y'] += bcircle['y_vel']

        if bcircle['x'] < 0 or bcircle['x'] > screen_width:
            bcircle['x_vel'] *= -1
        if bcircle['y'] < 0 or bcircle['y'] > screen_height:
            bcircle['y_vel'] *= -1

    for rcircle in rcircles:
        for bcircle in bcircles:
            distance = ((rcircle['x'] - bcircle['x']) ** 2 + (rcircle['y'] - bcircle['y']) ** 2) ** 0.5
            if distance < rcircle['radius'] + bcircle['radius']:
                bcircles.remove(bcircle)
            if keyboard.is_pressed('space') and (
                    rect.x < bcircle['x'] < rect.x + 60 and rect.y < bcircle['y'] < rect.y + 60):
                bcircles.remove(bcircle)
        if keyboard.is_pressed('space') and (rect.x<rcircle['x']<rect.x+60 and rect.y<rcircle['y']<rect.y+60):
            rcircles.remove(rcircle)

    screen.blit(background_image, (0, 0))
    if len(bcircles) == 0:
        screen.blit(text, textRect)
    elif len(rcircles) == 0:
        screen.blit(text2, text2Rect)

    for rcircle in rcircles:
        pygame.draw.circle(screen, RED, (int(rcircle['x']), int(rcircle['y'])), rcircle['radius'])

    for bcircle in bcircles:
        pygame.draw.circle(screen, BLUE, (int(bcircle['x']), int(bcircle['y'])), bcircle['radius'])

    if keyboard.is_pressed('left'):
        rect_x -= 5
    elif keyboard.is_pressed('right'):
        rect_x += 5
    elif keyboard.is_pressed('up'):
        rect_y -= 5
    elif keyboard.is_pressed('down'):
        rect_y += 5

    rect.x = rect_x
    rect.y = rect_y
    pygame.draw.rect(screen, (0, 255, 0), rect, 2)

    for position in positions:
        if time.time() - last_animation_time < 0.5:
            screen.blit(explosions[current_explosion_index], position)
            current_explosion_index = (current_explosion_index + 1) % len(explosions)
        else:
            positions.clear()

    pygame.display.update()

pygame.quit()