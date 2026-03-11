# General test is variable to new tests. We customize for general tasks and try for new features with a new perspective over already tested and new features.

from Rectangle import Rect, Color
import Rectangle.prefab
import Rectangle.pygame
import Rectangle
import pygame, sys

pygame.init()

WIDTH, HEIGHT = 800, 600
TARGET_FPS = 60.0
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

grid = Rectangle.pygame.physics.Grid(100, WIDTH, HEIGHT)
camera = Rectangle.pygame.camera.Camera(grid)

WHITE = Color(255, 255, 255)
ORANGE = Color(255, 125, 0)

# What it does internally + physics ------------------------------------------
other = Rectangle.prefab.RectBox(10, 10, 100, 100, ORANGE, setup=False)
other_renderer = Rectangle.pygame.BoxRenderer(other, screen)
# You can now modify other.rect directly to move the object.
# ----------------------------------------------------------------------------

player = Rectangle.pygame.premade.Box(
    surface = screen, 
    rect = Rect(WIDTH//2 - 25 - 200, 50, 50, 50), 
    color = ORANGE, 
    grid = grid
)
grid.add_object(player)

wall = Rectangle.pygame.physics.Box(
    surface = screen, 
    rect = Rect(WIDTH//2 - 25, 0, 50, HEIGHT), 
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

    other_renderer.render()
    
    grid.update(player, pressed_keys, delta_time)
    camera.adjust_x(player, delta_time, 200)
    camera.adjust_y(player, delta_time, 200)

    grid.render_all()
    pygame.display.flip()

pygame.quit()
sys.exit()