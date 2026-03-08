from Rectangle import pygame_phys_premade as rtngle_phys_premade
from Rectangle import pygame_phys as rtngle_phys
from Rectangle import Rect, Color
import pygame
import sys

pygame.init()

WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

WHITE = Color(255, 255, 255)
ORANGE = Color(255, 125, 0)

grid = rtngle_phys.Grid(cell_size=100, width=WIDTH, height=HEIGHT)

player = rtngle_phys_premade.Box(
    surface = screen, 
    rect = Rect(10, 10, 50, 50), 
    color = ORANGE, 
    grid = grid, 
)

grid.add_object(player)

box1 = rtngle_phys.Box(
    surface = screen, 
    rect = Rect(0, HEIGHT-45, WIDTH-100, 25), 
    color = ORANGE, 
)
grid.add_object(box1)
box2 = rtngle_phys.Box(
    surface = screen, 
    rect = Rect(60, HEIGHT-145, WIDTH-60, 25), 
    color = ORANGE, 
)
grid.add_object(box2)

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

    grid.update(player)
    grid.update(box1)
    grid.update(box2)
    grid.render_all()

    pygame.display.flip()

pygame.quit()
sys.exit()