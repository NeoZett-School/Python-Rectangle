from Rectangle import pygame_phys_premade as rtngle_phys_premade
from Rectangle.spatial_grid import SpatialGrid
from Rectangle import Rect, Color
import pygame
import sys

pygame.init()

WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

WHITE = Color(255, 255, 255)
ORANGE = Color(255, 125, 0)

grid = SpatialGrid(cell_size=100, width=WIDTH, height=HEIGHT)

player = rtngle_phys_premade.Box(
    surface = screen, 
    rect = Rect(10, 10, 50, 50), 
    color = ORANGE, 
    grid = grid, 
)

grid.add_object(player, player.rect)

box = rtngle_phys_premade.Box(
    surface = screen, 
    rect = Rect(70, 70, 50, 50), 
    color = ORANGE, 
)

grid.add_object(box, box.rect)

active = True
while active:
    dt = clock.tick(60.0) / 1000
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            active = False
        player.handle_event(event)
    pressed_keys = pygame.key.get_pressed()
    screen.fill(WHITE)

    player.update(pressed_keys, dt)
    player.render()

    box.update([], dt)
    box.render()

    grid.update(player, player.rect)
    grid.update(box, box.rect)

    pygame.display.flip()

pygame.quit()
sys.exit()