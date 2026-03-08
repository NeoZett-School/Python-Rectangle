from typing import Union, Optional, overload
from abc import ABC, abstractmethod
from .prefab import RectBox
from .pygame import BoxRenderer
from .core import Numeric, ColorLike, Vector, Rect
from .spatial_grid import UniformGrid
import pygame

class Grid(UniformGrid["Box"]):
    def add_object(self, obj: "Box") -> None:
        UniformGrid.add_object(self, obj, obj.rect)
    def remove_object(self, obj: "Box") -> None:
        UniformGrid.remove_object(obj, obj.rect)
    def update(self, obj: "Box") -> None:
        old_rect = Rect(self._old_rects[id(obj)])
        self.remove_object(obj, old_rect)
        self.add_object(obj, obj.rect)
    def render_all(self) -> None:
        for position in self.cells.values():
            for box in position:
                box.render()

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
    __all__ = ("surface", "renderer", "velocity", "static")
    def __init__(self, surface: pygame.Surface, rect: Rect, color: ColorLike, static: bool = False, use_detail: bool = False) -> None:
        Box.__init__(self, surface, rect, color, use_detail)
        self.velocity = Vector(0, 0)
        self.static = static
    @overload
    def apply_force(self, x: Numeric, y: Numeric) -> None: ...
    @overload
    def apply_force(self, vector: Vector, /) -> None: ...
    def apply_force(self, x: Union[Numeric, Vector], y: Optional[Numeric] = None) -> None:
        if y is None:
            x, y = x
        self.velocity += (x, y)
    def resolve_collision(self, other: Box) -> Optional[str]:
        if self.rect.intersects(other.rect):
            overlap_top = abs(self.rect.top - other.rect.bottom)
            overlap_bottom = abs(self.rect.bottom - other.rect.top)
            overlap_left = abs(self.rect.left - other.rect.right)
            overlap_right = abs(self.rect.right - other.rect.left)
            smallest_overlap = min(overlap_top, overlap_bottom, overlap_left, overlap_right)
            if smallest_overlap == overlap_top:
                self.rect.top = other.rect.bottom
                return "top"
            elif smallest_overlap == overlap_bottom:
                self.rect.bottom = other.rect.top
                return "bottom"
            elif smallest_overlap == overlap_left:
                self.rect.left = other.rect.right
                return "left"
            elif smallest_overlap == overlap_right:
                self.rect.right = other.rect.left
                return "right"
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