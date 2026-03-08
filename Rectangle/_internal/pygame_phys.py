from typing import Union, Optional, Any, overload
from abc import ABC, abstractmethod
from .prefab import RectBox
from .pygame import BoxRenderer
from .core import Numeric, ColorLike, Vector, Rect
import pygame

class Box:
    """The box is a uniform rectangle with a renderer, called a box and boxrenderer when also including an optional surface."""

    __all__ = ("surface", "renderer")
    def __init__(self, surface: pygame.Surface, rect: Rect, color: ColorLike, use_detail: bool = False) -> None:
        self.surface = RectBox(rect, color)
        self.renderer = BoxRenderer(self.surface, surface, use_detail)
    @property
    def rect(self) -> Rect:
        return self.surface.rect
    def render(self) -> None:
        self.renderer.render()

class _PhysicsBox(Box):
    __all__ = ("surface", "renderer", "velocity")
    def __init__(self, surface: pygame.Surface, rect: Rect, color: ColorLike, use_detail: bool = False) -> None:
        Box.__init__(self, surface, rect, color, use_detail)
        self.velocity = Vector(0, 0)
    @overload
    def apply_force(self, x: Numeric, y: Numeric) -> None: ...
    @overload
    def apply_force(self, vector: Vector, /) -> None: ...
    def apply_force(self, x: Union[Numeric, Vector], y: Optional[Numeric] = None) -> None:
        if y is None:
            x, y = x
        self.velocity += (x, y)
    def update(self, delta_time: float = 1.0) -> None:
        self.rect.move(self.velocity * delta_time)

class PhysicsBox(ABC, _PhysicsBox):
    """The physics box works just like the box but provisions physics methods."""

    @abstractmethod
    def handle_event(self, event: pygame.event.Event) -> None:
        ...
    @abstractmethod
    def update(self, pressed_keys: pygame.key.ScancodeWrapper, delta_time: float = 1.0) -> None:
        ...

def update(self: PhysicsBox, delta_time: float) -> None:
    _PhysicsBox.update(self, delta_time)