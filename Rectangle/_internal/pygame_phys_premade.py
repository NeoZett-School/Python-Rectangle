from typing import Optional
from .pygame_phys import Box, PhysicsBox
from .core import ColorLike, Vector, Rect
from .spatial_grid import SpatialGrid
from .keybinds import Keybinds
import pygame

default_keybinds = Keybinds({
    "jump": pygame.K_SPACE,
    "left": pygame.K_a,
    "right": pygame.K_d
})

class Box(PhysicsBox):
    """The premade physics box, called box in premade physics, is adaptive and pursuasive. You can easily create a box and create new games with custom collision."""

    def __init__(self, surface: pygame.Surface, rect: Rect,
                 color: ColorLike, static: bool = False, 
                 grid: Optional[SpatialGrid] = None, 
                 keybinds: Optional[Keybinds] = None, 
                 use_detail: bool = False, 
                 cover_surface: Optional[pygame.Surface] = None) -> None:
        super().__init__(surface, rect, color, static, use_detail, cover_surface)
        self.ground_level = surface.get_height()
        self.acceleration = Vector(0, 0)
        self.grounded = False
        self.gravity = 3600
        self.jump_force = 1300
        self.max_speed = 300
        self.ground_accel = 2000
        self.air_accel = 900
        self.friction = 1800
        self.keybinds = keybinds or default_keybinds
        self.grid = grid
    def handle_event(self, event: pygame.event.Event) -> None:
        if event.type == pygame.KEYDOWN:
            if event.key == self.keybinds.mapping["jump"] and self.grounded:
                self.velocity.y = -self.jump_force
                self.grounded = False
    def resolve_collision(self, other: Box) -> None:
        side = PhysicsBox.resolve_collision(self, other)
        if side is None:
            return
        if hasattr(other, "static") and not other.static:
            if side in ("top", "bottom"):
                self.velocity.y, other.velocity.y = other.velocity.y, self.velocity.y
                if side == "bottom":
                    self.grounded = True
            elif side in ("left", "right"):
                self.velocity.x, other.velocity.x = other.velocity.x, self.velocity.x
        else:
            if side == "top":
                self.velocity.y = max(self.velocity.y, 0)
            elif side == "bottom":
                self.velocity.y = min(self.velocity.y, 0)
                self.grounded = True
            elif side == "left":
                self.velocity.x = min(self.velocity.x, 0)
            elif side == "right":
                self.velocity.x = max(self.velocity.x, 0)
    def update(self, pressed_keys: pygame.key.ScancodeWrapper, delta_time: float = 1.0) -> None:
        self.acceleration.xy = (0, 0)
        if not self.static:
            self.acceleration.y += self.gravity
        if len(pressed_keys) > 0:
            mapped_keys = self.keybinds.sort_pressed(pressed_keys)
            move = mapped_keys["right"] - mapped_keys["left"]
        else:
            move = 0
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
        if self.grid is not None:
            for obj in self.grid.get_nearby_objects(self.rect):
                if obj is self:
                    continue
                self.resolve_collision(obj)