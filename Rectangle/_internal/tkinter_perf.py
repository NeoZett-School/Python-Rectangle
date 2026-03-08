from typing import Union, Sequence, List, Tuple, Optional
import tkinter as tk

from .core import (
    CoordinateLike, RectLike, ColorLike, Coordinate, Rect, Surface, Color
)
from .prefab import RectBox, SquareBox

class InterfaceSurface(Surface):
    pass

class InterfaceTool:
    __all__ = ("surface",)

    def __init__(self, surface: Surface) -> None:
        self.surface = surface
    def translate_to_photoimage(self) -> tk.PhotoImage:
        return translate_surface(self.surface)
    def rectangles(self) -> List[Tuple[Rect, ColorLike]]:
        return self.surface._elements

class AutomaticRenderer:
    __all__ = ("box_surface_tool", "canvas", "use_detail")

    def __init__(self, box_surface: Surface, canvas: tk.Canvas, use_detail: bool = False) -> None:
        self.box_surface_tool = InterfaceTool(box_surface)
        self.canvas = canvas
        self.use_detail = use_detail
        self._img = None
        box_surface._use_detail = use_detail
    def render(self, dest: Optional[Union[Rect, RectLike, Coordinate, CoordinateLike]] = None) -> None:
        if self.use_detail:
            img = self.box_surface_tool.translate_to_photoimage()
            self._img = img  # prevent GC
            x = 0
            y = 0
            if dest:
                x, y = dest
            self.canvas.create_image(x, y, anchor="nw", image=img)
        else:
            for rect, color in self.box_surface_tool.rectangles():
                coords = []
                for vx, vy in rect.vertices:
                    coords.extend((vx, vy))
                self.canvas.create_polygon(coords, fill=color, outline=color)

class BoxRenderer:
    __all__ = ("box_surface_tool", "box_surface_rect", "canvas", "use_detail")

    def __init__(self, box_surface: Union[RectBox, SquareBox], canvas: tk.Canvas, use_detail: bool = False) -> None:
        self.box_surface_tool = InterfaceTool(box_surface)
        self.box_surface_rect = box_surface.rect
        self.canvas = canvas
        self.use_detail = use_detail
        self._img = None
        box_surface._use_detail = use_detail
    def render(self) -> None:
        if self.use_detail:
            img = self.box_surface_tool.translate_to_photoimage()
            self._img = img
            x, y = self.box_surface_rect.topleft
            self.canvas.create_image(x, y, anchor="nw", image=img)
        else:
            for rect, color in self.box_surface_tool.rectangles():
                coords = []
                for vx, vy in rect.vertices:
                    coords.extend((vx, vy))
                self.canvas.create_polygon(coords, fill=color, outline=color)

def accustom_screen(canvas: tk.Canvas,
                    background_color: ColorLike = "#000000",
                    use_detail: bool = False) -> Tuple[RectBox, AutomaticRenderer]:
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


def translate_surface(surface: Surface) -> tk.PhotoImage:
    width = len(surface)
    height = len(surface[0])

    img = tk.PhotoImage(width=width, height=height)

    for y in range(height):
        row = []
        for x in range(width):
            color = surface[x][y]
            if color is None:
                row.append("")
            else:
                row.append(color_to_hex(Color.unpack(color)))
        img.put("{" + " ".join(row) + "}", to=(0, y))

    return img

def color_to_hex(color: ColorLike) -> str:
    if isinstance(color, str):
        return color

    r, g, b = color
    return f"#{r:02x}{g:02x}{b:02x}"