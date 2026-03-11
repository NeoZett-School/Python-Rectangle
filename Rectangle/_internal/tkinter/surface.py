from typing import Union, Sequence, List, Tuple, Optional
import tkinter as tk

from ..core import (
    CoordinateLike, RectLike, ColorLike, Coordinate, Rect, Surface
)
from ..prefab import RectBox, SquareBox

class InterfaceSurface(Surface):
    pass

class InterfaceTool:
    __all__ = ("surface",)

    def __init__(self, surface: Surface) -> None:
        self.surface = surface
    def rectangles(self) -> List[Tuple[Rect, ColorLike]]:
        return self.surface._elements

class AutomaticRenderer:
    __all__ = ("box_surface_tool", "canvas", "use_detail")

    def __init__(self, box_surface: Surface, canvas: tk.Canvas, use_detail: bool = False) -> None:
        self.box_surface_tool = InterfaceTool(box_surface)
        self.canvas = canvas
        self.use_detail = use_detail
        box_surface._use_detail = use_detail

    def render(self, dest: Optional[Union[Rect, RectLike, Coordinate, CoordinateLike]] = None) -> None:
        if self.use_detail:
            # Pixel rendering (slow in Tkinter)
            draw_surface_pixels(self.canvas, self.box_surface_tool.surface, dest)
        else:
            for rect, color in self.box_surface_tool.rectangles():
                draw_polygon(self.canvas, rect, color)


class BoxRenderer:
    __all__ = ("box_surface_tool", "box_surface_rect", "canvas", "use_detail")

    def __init__(self, box_surface: Union[RectBox, SquareBox], canvas: tk.Canvas, use_detail: bool = False) -> None:
        self.box_surface_tool = InterfaceTool(box_surface)
        self.box_surface_rect = box_surface.rect
        self.canvas = canvas
        self.use_detail = use_detail
        box_surface._use_detail = use_detail
    def render(self) -> None:
        if self.use_detail:
            draw_surface_pixels(self.canvas, self.box_surface_tool.surface)
        else:
            for rect, color in self.box_surface_tool.rectangles():
                draw_polygon(self.canvas, rect, color)


def accustom_screen(canvas: tk.Canvas,
                    background_color: ColorLike = "#000000",
                    use_detail: bool = False
                    ) -> Tuple[RectBox, AutomaticRenderer]:
    width = int(canvas["width"])
    height = int(canvas["height"])

    surf = RectBox((0, 0, width, height), background_color)

    return surf, AutomaticRenderer(surf, canvas, use_detail)


def create_screen(size: Sequence[int],
                  background_color: ColorLike = "#000000",
                  use_detail: bool = False):
    root = tk.Tk()

    canvas = tk.Canvas(root, width=size[0], height=size[1])
    canvas.pack()

    surf, tool = accustom_screen(canvas, background_color, use_detail)

    return root, canvas, surf, tool


def draw_polygon(canvas: tk.Canvas, rect: Rect, color: ColorLike):
    coords = []
    for x, y in rect.vertices:
        coords.extend((x, y))

    canvas.create_polygon(coords, fill=color, outline=color)


def draw_surface_pixels(canvas: tk.Canvas, surface: Surface, dest=None):
    offset_x = 0
    offset_y = 0

    if dest:
        offset_x, offset_y = dest

    for x, column in enumerate(surface):
        for y, color in enumerate(column):
            if color is None:
                continue

            canvas.create_rectangle(
                x + offset_x,
                y + offset_y,
                x + offset_x + 1,
                y + offset_y + 1,
                outline=color,
                fill=color
            )