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

SCROLL_DIST = 50

grid = rtngle_phys.Grid(cell_size=100, width=WIDTH, height=HEIGHT)

player = rtngle_phys_premade.Box(
    surface = screen, 
    rect = Rect(10, 10, 50, 50), 
    color = ORANGE, 
    grid = grid, 
)
grid.add_object(player)

movable_box = rtngle_phys_premade.Box(
    surface = screen, 
    rect = Rect(70, 10, 50, 50), 
    color = ORANGE, 
    grid = grid, 
)
grid.add_object(movable_box)

box1 = rtngle_phys.Box(
    surface = screen, 
    rect = Rect(0, HEIGHT-45, WIDTH-100, 25), 
    color = ORANGE, 
)
grid.add_object(box1)
box2 = rtngle_phys.Box(
    surface = screen, 
    rect = Rect(100, HEIGHT-145, WIDTH-100, 25), 
    color = ORANGE, 
)
grid.add_object(box2)
box3 = rtngle_phys.Box(
    surface = screen, 
    rect = Rect(0, HEIGHT-245, WIDTH-100, 25), 
    color = ORANGE, 
)
grid.add_object(box3)
box4 = rtngle_phys.Box(
    surface = screen, 
    rect = Rect(100, HEIGHT-345, WIDTH-100, 25), 
    color = ORANGE, 
)
grid.add_object(box4)

objects = [
    box1, box2, box3, box4, movable_box
]

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
    movable_box.update([], dt)

    if pressed_keys[pygame.K_a] and player.rect.left < 50:
        player.rect.left += SCROLL_DIST
        for obj in objects:
            obj.rect.left += SCROLL_DIST
    elif pressed_keys[pygame.K_d] and player.rect.right > WIDTH - 50:
        player.rect.right -= SCROLL_DIST
        for obj in objects:
            obj.rect.right -= SCROLL_DIST

    grid.update(player)
    grid.update(movable_box)
    grid.update(box1)
    grid.update(box2)
    grid.render_all()

    pygame.display.flip()

pygame.quit()
sys.exit()