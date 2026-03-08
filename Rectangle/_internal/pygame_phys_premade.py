from .pygame_phys import PhysicsBox
from .core import ColorLike, Vector, Rect
import pygame

class Box(PhysicsBox):
    """The premade physics box, called box in premade physics, is adaptive and pursuasive. You can easily create a box and create new games with custom collision."""

    def __init__(self, surface: pygame.Surface, rect: Rect,
                 color: ColorLike, use_detail: bool = False) -> None:
        super().__init__(surface, rect, color, use_detail)
        self.ground_level = surface.get_height()
        self.acceleration = Vector(0, 0)
        self.grounded = False
        self.gravity = 3600
        self.jump_force = 1300
        self.max_speed = 300
        self.ground_accel = 2000
        self.air_accel = 900
        self.friction = 1800
    def handle_event(self, event: pygame.event.Event) -> None:
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and self.grounded:
                self.velocity.y = -self.jump_force
                self.grounded = False
    def update(self, pressed_keys: pygame.key.ScancodeWrapper, delta_time: float = 1.0) -> None:
        self.acceleration.xy = (0, 0)
        self.acceleration.y += self.gravity
        move = pressed_keys[pygame.K_d] - pressed_keys[pygame.K_a]
        accel = self.ground_accel if self.grounded else self.air_accel
        self.acceleration.x += move * accel
        self.velocity += self.acceleration * delta_time
        if self.grounded and move == 0:
            if abs(self.velocity.x) < self.friction * delta_time:
                self.velocity.x = 0
            else:
                self.velocity.x -= self.friction * delta_time * (1 if self.velocity.x > 0 else -1)
        self.velocity.x = max(-self.max_speed, min(self.max_speed, self.velocity.x))
        self.rect.x += self.velocity.x * delta_time
        self.rect.y += self.velocity.y * delta_time
        if self.rect.bottom > self.ground_level:
            self.rect.bottom = self.ground_level
            self.velocity.y = 0
            self.grounded = True
        else:
            self.grounded = False