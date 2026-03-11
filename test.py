# General test is variable to new tests. We customize for general tasks and try for new features with a new perspectiv over already tested and new features.

from Rectangle import Rect, Color
import Rectangle.pygame as rctngle_pg
import Rectangle.pygame_phys as rctngle_phys
import Rectangle.pygame_phys_premade as rctngle_premade
import Rectangle.keybinds as rctngle_kbnds
import Rectangle as rctngle
import pygame
import sys

pygame.init()

WIDTH, HEIGHT = 800, 600
TARGET_FPS = 60.0
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

WHITE = Color(255, 255, 255)
ORANGE = Color(255, 125, 0)

grid = rctngle_phys.Grid(100, WIDTH, HEIGHT)

player = rctngle_premade.Box(
    surface = screen, 
    rect = Rect(WIDTH//2 - 50//2 - 200, 50, 50, 50), 
    color = ORANGE, 
    grid = grid
)
grid.add_object(player)

wall = rctngle_phys.Box(
    surface = screen, 
    rect = Rect(WIDTH//2 - 50//2, 0, 50, HEIGHT), 
    color = ORANGE
)
grid.add_object(wall)

active = True
while active:
    delta_time = clock.tick(TARGET_FPS) / 1000.0
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            active = False
        player.handle_event(event)
    pressed_keys = pygame.key.get_pressed()
    screen.fill(WHITE)

    grid.update(player, pressed_keys, delta_time)
    
    grid.render_all()
    pygame.display.flip()

pygame.quit()
sys.exit()