from typing import Set, Tuple, Dict, Generic, TypeVar, Any
from .core import Numeric, Rect

T = TypeVar("T")

class SpatialGrid:
    __all__ = ("cell_size", "grid_width", "grid_height", "cells", "_old_rects")

    def __init__(self, cell_size: int, width: int, height: int) -> None:
        self.cell_size = cell_size
        self.grid_width = (width // cell_size) + 1
        self.grid_height = (height // cell_size) + 1
        self.cells = {}

        self._old_rects = {}

    def _get_cell_coords(self, rect: Rect) -> None:
        """Get the grid cell coordinates for a given rectangle."""
        x1, y1 = rect.x // self.cell_size, rect.y // self.cell_size
        x2, y2 = (rect.x + rect.width) // self.cell_size, (rect.y + rect.height) // self.cell_size
        return int(x1), int(y1), int(x2), int(y2)

    def add_object(self, obj: Any, rect: Rect) -> None:
        """Add an object to the grid based on its rectangle."""
        x1, y1, x2, y2 = self._get_cell_coords(rect)
        for x in range(x1, x2 + 1):
            for y in range(y1, y2 + 1):
                self.cells.setdefault((x, y), []).append(obj)
        self._old_rects[id(obj)] = tuple(rect)  # Store the rectangle for future updates

    def remove_object(self, obj: Any, rect: Rect) -> None:
        """Remove an object from the grid."""
        x1, y1, x2, y2 = self._get_cell_coords(rect)
        for x in range(x1, x2 + 1):
            for y in range(y1, y2 + 1):
                if (x, y) in self.cells:
                    self.cells[(x, y)].remove(obj)

    def get_nearby_objects(self, rect: Rect) -> Set[Any]:
        """Get all objects in the same or neighboring cells."""
        x1, y1, x2, y2 = self._get_cell_coords(rect)
        nearby_objects = set()
        for x in range(x1 - 1, x2 + 2):
            for y in range(y1 - 1, y2 + 2):
                if (x, y) in self.cells:
                    nearby_objects.update(self.cells[(x, y)])
        return nearby_objects

    def update(self, obj: Any, new_rect: Rect) -> None:
        """Update an object's position in the grid."""
        old_rect = Rect(self._old_rects[id(obj)])
        self.remove_object(obj, old_rect)
        self.add_object(obj, new_rect)

class UniformGrid(Generic[T], SpatialGrid):
    cells: Dict[Tuple[Numeric, Numeric], T]
    def add_object(self, obj: T, rect: Rect) -> None: ...
    def remove_object(self, obj: T, rect: Rect) -> None: ...
    def get_nearby_objects(self, rect: Rect) -> Set[T]: ...
    def update(self, obj: T, new_rect: Rect) -> None: ...