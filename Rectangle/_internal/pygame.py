from typing import Union, Sequence, List, Tuple, Optional
from .core import (
    CoordinateLike, RectLike, ColorLike, Coordinate, Rect, Surface
)
from .prefab import RectBox, SquareBox, AnyBox
import pygame

class InterfaceSurface(Surface):
    def translate_to_pygame(self) -> pygame.Surface:
        return translate_surface(self)

class InterfaceTool:
    __all__ = ("surface",)

    def __init__(self, surface: Surface) -> None:
        self.surface = surface
    def translate_to_pygame(self) -> pygame.Surface:
        return translate_surface(self.surface)
    def rectangles(self) -> List[Tuple[Rect, ColorLike]]:
        return self.surface._elements

class AutomaticRenderer:
    __all__ = ("box_surface_tool", "pygame_surface", "use_detail")

    def __init__(self, box_surface: Surface, pygame_surface: pygame.Surface, use_detail: bool = False) -> None:
        self.box_surface_tool = InterfaceTool(box_surface)
        self.pygame_surface = pygame_surface
        self.use_detail = use_detail
        if isinstance(box_surface, (AnyBox)):
            box_surface.set_detail(use_detail)
    def render(self, dest: Optional[Union[Rect, RectLike, Coordinate, CoordinateLike, pygame.Rect]] = None) -> None:
        if self.use_detail:
            self.pygame_surface.blit(self.box_surface_tool.translate_to_pygame(), dest if dest else (0, 0))
        else:
            for rect, color in self.box_surface_tool.rectangles():
                pygame.draw.polygon(self.pygame_surface, color, rect.vertices)

class BoxRenderer:
    __all__ = ("box_surface_tool", "box_surface_rect", "pygame_surface", "use_detail")

    def __init__(self, box_surface: Union[RectBox, SquareBox], pygame_surface: pygame.Surface, use_detail: bool = False) -> None:
        self.box_surface_tool = InterfaceTool(box_surface)
        self.box_surface_rect = box_surface.rect
        self.pygame_surface = pygame_surface
        self.use_detail = use_detail
        box_surface.set_detail(use_detail)
    def render(self) -> None:
        if self.use_detail:
            self.pygame_surface.blit(self.box_surface_tool.translate_to_pygame(), translate_rect(self.box_surface_rect))
        else:
            for rect, color in self.box_surface_tool.rectangles():
                pygame.draw.polygon(self.pygame_surface, color, rect.vertices)

def accustom_screen(screen: pygame.Surface, background_color: ColorLike = (0, 0, 0), use_detail: bool = False) -> Tuple[RectBox, AutomaticRenderer]:
    surf = RectBox((0, 0, *screen.get_size()), background_color)
    return surf, AutomaticRenderer(surf, screen, use_detail)

def create_screen(size: Sequence[int], background_color: ColorLike = (0, 0, 0), use_detail: bool = False) -> Tuple[RectBox, AutomaticRenderer]:
    """This is unconventional and unperformant, but an easy and powerful integration. For greater performance, you should use the pygame screen directly and a box renderer."""
    screen = pygame.display.set_mode(size)
    surf, tool = accustom_screen(screen, background_color, use_detail)
    return surf, tool

def translate_surface(surface: Surface) -> pygame.Surface:
    pg_surface = pygame.Surface((len(surface), len(surface[0])))
    px = pygame.PixelArray(pg_surface)

    for x, column in enumerate(surface):
        for y, color in enumerate(column):
            if color is None:
                continue
            px[x, y] = color

    return pg_surface

def translate_rect(rect: Rect) -> pygame.Rect:
    return pygame.Rect(*rect.topleft, *rect.size)