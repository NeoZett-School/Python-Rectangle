from Rectangle import pygame_phys_premade as rtngle_phys_premade
from Rectangle import Rect, Color
import pygame
import sys

pygame.init()

WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

WHITE = Color(255, 255, 255)
ORANGE = Color(255, 125, 0)

box = rtngle_phys_premade.Box(
    surface = screen, 
    rect = Rect(10, 10, 50, 50), 
    color = ORANGE, 
    use_detail = True
)

white_packed = WHITE.pack()
for x in range(50):
    box.surface[x, 25] = white_packed

active = True
while active:
    dt = clock.tick(60.0) / 1000
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            active = False
        box.handle_event(event)
    pressed_keys = pygame.key.get_pressed()
    screen.fill(WHITE)

    box.update(pressed_keys, dt)
    box.render()

    pygame.display.flip()

pygame.quit()
sys.exit()