from typing import Union, Optional, overload
from .pygame_phys import Grid
from .core import Numeric, CoordinateLike, Coordinate

class Camera:
    def __init__(self, grid: Grid) -> None:
        self._position = Coordinate(0, 0)
        self.grid = grid
    @property
    def position(self) -> Coordinate:
        return self._position
    @position.setter
    def position(self, value: Coordinate) -> None:
        self.move(self.position - value)
    @overload
    def move(self, dx: Numeric, dy: Numeric) -> None: ...
    @overload
    def move(self, delta: CoordinateLike, /) -> None: ...
    def move(self, dx: Union[Numeric, CoordinateLike], dy: Optional[Numeric] = None) -> None:
        if dy is None:
            dx, dy = dx
        for obj in self.grid:
            obj.rect.position += (dx, dy)
        self._position += (dx, dy)