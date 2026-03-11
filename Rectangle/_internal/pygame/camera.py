from typing import Union, Optional, overload
from .physics import Grid, PhysicsBox
from ..core import Numeric, CoordinateLike, Coordinate

class Camera:
    """The camera automatically handles moving around the world, instead of moving an object in the world."""

    __all__ = ("_position", "_scale", "grid")

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
    def adjust_x(self, player: PhysicsBox, delta_time: float, scroll_at: float = 200.0) -> None:
        """Adjust the camera to frame the player on the x-axis."""
        if (player.rect.right >= player.renderer.pygame_surface.get_width() - scroll_at and player.velocity.x > 0) or (player.rect.left < scroll_at and player.velocity.x < 0):
            self.move(-player.velocity.x * delta_time, 0)
    def adjust_y(self, player: PhysicsBox, delta_time: float, scroll_at: float = 300.0) -> None:
        """Adjust the camera to frame the player on the y-axis."""
        if (player.rect.bottom >= player.renderer.pygame_surface.get_height() - scroll_at and player.velocity.y > 0 and self._position.y < 0) or (player.rect.top < scroll_at and player.velocity.y < 0):
            self.move(0, -player.velocity.y * delta_time)