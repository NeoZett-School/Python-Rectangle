from typing import Union, Optional, overload
from .pygame_phys import Grid, PhysicsBox
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
    def adjust_x(self, player: PhysicsBox, delta_time: float) -> None:
        if (player.rect.right >= player.renderer.pygame_surface.get_height() - 200 and player.velocity.x > 0) or (player.rect.left < 200 and player.velocity.x < 0):
            self.move(-player.velocity.x * delta_time, 0)