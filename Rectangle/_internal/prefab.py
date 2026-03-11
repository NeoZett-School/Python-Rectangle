from typing import (
    Union, Sequence, Optional, TypeAlias, Any, overload
)
from .core import (
    RectLike, Coordinate, CoordinateLike, 
    Rect, Square, Surface, ColorLike
)

class RectBox(Surface):
    @overload
    def __init__(self, x: int, y: int, width: int, height: int, color: Optional[ColorLike] = None, *, setup: bool = True) -> None: ...
    @overload
    def __init__(self, rect: RectLike, color: Optional[ColorLike], *, setup: bool = True) -> None: ...
    def __init__(self, x: Union[int, RectLike], y: Optional[Union[int, ColorLike]] = None, width: Optional[int] = None, height: Optional[int] = None, color: Optional[ColorLike] = None, *, setup: bool = True) -> None:
        if isinstance(y, Sequence):
            color = y
        if y is None or width is None or height is None:
            x, y, width, height = x
        self.rect = Rect(x, y, width, height)
        if setup:
            self.setup(int(width), int(height))
        self._elements = []
        if color is not None:
            self.fill((color[0] << 16) | (color[1] << 8) | color[2])
            self._elements.append((self.rect, color))
        self._use_detail = False
        self._color = color
    def set_detail(self, active: bool = False) -> None:
        self._use_detail = active
    def fill(self, value: Any) -> None:
        self._elements.clear()
        self._elements.append((self.rect, value))
        self._color = value
        Surface.fill(self, value)
    def clear(self) -> None:
        self._elements.clear()
        if self._color:
            self._elements.append((self.rect, self._color))
        Surface.clear(self)
    def blit(self, surface: Surface, pos: Optional[Union[Rect, RectLike, Coordinate, CoordinateLike]] = None) -> None:
        if hasattr(surface, "rect") and pos is None:
            dx, dy = surface.rect.topleft
            self._elements.append((surface.rect, surface._color))
        elif self._use_detail:
            if isinstance(pos, Rect):
                dx, dy = pos.topleft
            elif isinstance(pos, Sequence):
                if len(pos) == 4:  # RectLike
                    r = Rect(pos)
                    dx, dy = r.topleft
                else:  # CoordinateLike
                    dx, dy = pos
        if self._use_detail:
            Surface.blit(self, surface, (dx, dy))

Box: TypeAlias = RectBox

class SquareBox(RectBox):
    @overload
    def __init__(self, x: int, y: int, width: int, height: int, color: Optional[ColorLike] = None) -> None: ...
    @overload
    def __init__(self, x: int, y: int, size: int, color: Optional[ColorLike] = None) -> None: ...
    @overload
    def __init__(self, rect: RectLike, color: Optional[ColorLike]) -> None: ...
    def __init__(self, x: Union[int, RectLike], y: Optional[Union[int, ColorLike]] = None, width: Optional[int] = None, height: Optional[Union[int, ColorLike]] = None, color: Optional[ColorLike] = None, *, size: Optional[int] = None) -> None:
        if isinstance(x, Sequence):
            color = y if isinstance(y, Sequence) else color
            x, y, width, height = x
        elif size is not None:
            width = height = size
        elif width is not None and not isinstance(height, int):
            color = height if isinstance(height, Sequence) else color
            width = height = width
        self.rect = Square(x, y, width, height)
        self.setup(int(width), int(height))
        self._elements = []
        if color is not None:
            self.fill((color[0] << 16) | (color[1] << 8) | color[2])
            self._elements.append((self.rect, color))
        self._use_detail = False
        self._color = color

AnyBox: TypeAlias = Union[RectBox, SquareBox]