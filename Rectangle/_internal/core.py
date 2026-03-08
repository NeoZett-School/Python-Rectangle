from typing import (
    Union, Iterable, Sequence, List, Tuple, 
    Optional, TypeAlias, Self, Any, overload
)
import math

Numeric: TypeAlias = Union[int, float]

CoordinateLike: TypeAlias = Sequence[Numeric]
RectLike: TypeAlias = Sequence[Numeric]

ColorLike: TypeAlias = Sequence[Numeric]

class Coordinate(list):
    @overload
    def __init__(self, x: Numeric, y: Numeric) -> None: ...
    @overload
    def __init__(self, pos: CoordinateLike, /) -> None: ...
    def __init__(self, x: Union[Numeric, CoordinateLike], y: Optional[Numeric] = None) -> None:
        if y is None:
            if not isinstance(x, Sequence) or len(x) != 2:
                raise ValueError("Coordinate must have exactly 2 values (x, y)")
            list.__init__(self, x)
        else:
            list.__init__(self, (x, y))
    @property
    def xy(self) -> Tuple[Numeric, Numeric]: 
        return (self[0], self[1])
    @xy.setter
    def xy(self, value: CoordinateLike) -> None: 
        self[0] = value[0]
        self[1] = value[1]
    @property
    def x(self) -> Numeric:
        return self[0]
    @x.setter
    def x(self, value: Numeric) -> None:
        self[0] = value
    @property
    def y(self) -> Numeric:
        return self[1]
    @y.setter
    def y(self, value: Numeric) -> None:
        self[1] = value
    def magnitude(self) -> float:
        return (self[0] ** 2 + self[1] ** 2) ** 0.5
    def normalize(self) -> Self:
        mag = self.magnitude()
        if mag == 0:
            return Coordinate(0, 0)
        return Coordinate(self[0] / mag, self[1] / mag)
    def length(self) -> float:
        return math.hypot(self.x, self.y)
    def distance(self, other: CoordinateLike) -> float:
        return math.dist(self, other)
    def dot(self, other: CoordinateLike) -> float:
        return self[0] * other[0] + self[1] * other[1]
    def cross(self, other: CoordinateLike) -> float:
        return self[0] * other[1] - self[1] * other[0]
    def cross_scalar(self, scalar: float) -> Self:
        return Coordinate(-scalar * self[1], scalar * self[0])
    def __add__(self, other: CoordinateLike) -> Self:
        return Coordinate(self[0] + other[0], self[1] + other[1])
    def __radd__(self, other: CoordinateLike) -> Self:
        return Coordinate(other[0] + self[0], other[1] + self[1])
    def __iadd__(self, other: CoordinateLike) -> Self:
        return Coordinate(self[0] + other[0], self[1] + other[1])
    def __sub__(self, other: CoordinateLike) -> Self:
        return Coordinate(self[0] - other[0], self[1] - other[1])
    def __rsub__(self, other: CoordinateLike) -> Self:
        return Coordinate(other[0] - self[0], other[1] - self[1])
    def __isub__(self, other: CoordinateLike) -> Self:
        return Coordinate(self[0] - other[0], self[1] - other[1])
    def __mul__(self, other: Numeric) -> Self:
        return Coordinate(self[0] * other, self[1] * other)
    def __rmul__(self, other: Numeric) -> Self:
        return Coordinate(other * self[0], other * self[1])
    def __imul__(self, other: Numeric) -> Self:
        return Coordinate(self[0] * other, self[1] * other)
    def __truediv__(self, other: Numeric) -> Self:
        return Coordinate(self[0] / other, self[1] / other)
    def __rtruediv__(self, other: Numeric) -> Self:
        return Coordinate(other / self[0], other / self[1])
    def __itruediv__(self, other: Numeric) -> Self:
        return Coordinate(self[0] / other, self[1] / other)
    def __floordiv__(self, other: Numeric) -> Self:
        return Coordinate(self[0] // other, self[1] // other)
    def __rfloordiv__(self, other: Numeric) -> Self:
        return Coordinate(other // self[0], other // self[1])
    def __ifloordiv__(self, other: Numeric) -> Self:
        return Coordinate(self[0] // other, self[1] // other)
    def __mod__(self, other: Numeric) -> Self:
        return Coordinate(self[0] % other, self[1] % other)
    def __rmod__(self, other: Numeric) -> Self:
        return Coordinate(other % self[0], other % self[1])
    def __imod__(self, other: Numeric) -> Self:
        return Coordinate(self[0] % other, self[1] % other)
    def __pow__(self, other: Numeric) -> Self:
        return Coordinate((self[0] ** other).real, (self[1] ** other).real)
    def __rpow__(self, other: Numeric) -> Self:
        return Coordinate((other ** self[0]).real, (other ** self[1]).real)
    def __ipow__(self, other: Numeric) -> Self:
        return Coordinate((self[0] ** other).real, (self[1] ** other).real)
    def __neg__(self) -> Self:
        return Coordinate(-self[0], -self[1])
    def __pos__(self) -> Self:
        return self
    def __abs__(self) -> Self:
        return Coordinate(abs(self[0]), abs(self[1]))
    def __round__(self, n: Optional[int] = None) -> Self:
        return Coordinate(round(self[0], n), round(self[1], n))
    def __getnewargs__(self) -> Tuple[float, float]:
        return (self[0], self[1])
    def __repr__(self) -> str:
        return f"Coordinate({self[0]}, {self[1]})"

Vec2D: TypeAlias = Coordinate
Point: TypeAlias = Coordinate
Position: TypeAlias = Coordinate
Pos: TypeAlias = Coordinate
Vector: TypeAlias = Coordinate

class CoordinateList(list):
    @overload
    def __init__(self, *args: CoordinateLike) -> None: ...
    @overload
    def __init__(self, *, coordinates: Iterable[CoordinateLike]) -> None: ...
    def __init__(self, *args: CoordinateLike, coordinates: Optional[Iterable[CoordinateLike]] = None) -> None:
        list.__init__(self, (Coordinate(arg) for arg in (coordinates if coordinates is not None else args)))
    def __contains__(self, item: CoordinateLike) -> bool:
        return list.__contains__(self, Coordinate(item))
    def append(self, item: CoordinateLike) -> None:
        list.append(self, Coordinate(item))
    def remove(self, item: CoordinateLike) -> None:
        list.remove(self, Coordinate(item))
    def index(self, item: CoordinateLike) -> int:
        return list.index(self, Coordinate(item))
    def count(self, item: CoordinateLike) -> int:
        return list.count(self, Coordinate(item))
    def insert(self, index: int, item: CoordinateLike) -> None:
        list.insert(self, index, Coordinate(item))
    def extend(self, iterable: Iterable[CoordinateLike]) -> None:
        list.extend(self, (Coordinate(item) for item in iterable))
    def copy(self) -> Self:
        return CoordinateList(coordinates=self)

Vec2DList: TypeAlias = CoordinateList
PointList: TypeAlias = CoordinateList
PositionList: TypeAlias = CoordinateList
PosList: TypeAlias = CoordinateList
Vertices: TypeAlias = CoordinateList

class Lines(CoordinateList):
    @property
    def start(self) -> Coordinate:
        return self[0]
    @property
    def end(self) -> Coordinate:
        return self[-1]

class Rect(RectLike):
    __all__ = ("_coordinates",)

    @overload
    def __init__(self, x: Numeric, y: Numeric, width: Numeric, height: Numeric) -> None: ...
    @overload
    def __init__(self, rectangle: RectLike, /) -> None: ...
    def __init__(self, x: Union[Numeric, RectLike], y: Optional[Numeric] = None, width: Optional[Numeric] = None, height: Optional[Numeric] = None) -> None:
        if y is None or width is None or height is None:
            x, y, width, height = x
        self._coordinates = CoordinateList(
            (x, y),
            (x + width, y),
            (x + width, y + height),
            (x, y + height)
        )
    def _translate(self, dx: float, dy: float) -> None:
        for i, c in enumerate(self._coordinates):
            self._coordinates[i] = Coordinate(c[0] + dx, c[1] + dy)
    @property
    def xy(self) -> Coordinate:
        return self.position
    @xy.setter
    def xy(self, value: Coordinate) -> None:
        self.position = value
    @property
    def x(self) -> float:
        return self.left
    @x.setter
    def x(self, value: float) -> None:
        self.left = value
    @property
    def y(self) -> float:
        return self.top
    @y.setter
    def y(self, value: float) -> None:
        self.top = value
    @property
    def vertices(self) -> CoordinateList:
        return self._coordinates
    @property
    def edges(self) -> CoordinateList:
        return self._coordinates
    @property
    def width(self) -> float:
        return float(self._coordinates[1][0] - self._coordinates[0][0])
    @width.setter
    def width(self, value: float) -> None:
        left = self.left
        self._coordinates[1] = Coordinate(left + value, self._coordinates[1][1])
        self._coordinates[2] = Coordinate(left + value, self._coordinates[2][1])
    @property
    def height(self) -> float:
        return float(self._coordinates[3][1] - self._coordinates[0][1])
    @height.setter
    def height(self, value: float) -> None:
        top = self.top
        self._coordinates[2] = Coordinate(self._coordinates[2][0], top + value)
        self._coordinates[3] = Coordinate(self._coordinates[3][0], top + value)
    @property
    def size(self) -> Coordinate:
        return Coordinate(self.width, self.height)
    @size.setter
    def size(self, value: CoordinateLike) -> None:
        self.width, self.height = value
    @property
    def top(self) -> float:
        return float(self._coordinates[0][1])
    @top.setter
    def top(self, value: float) -> None:
        self._translate(0, value - self.top)
    @property
    def bottom(self) -> float:
        return float(self._coordinates[2][1])
    @bottom.setter
    def bottom(self, value: float) -> None:
        self._translate(0, value - self.bottom)
    @property
    def left(self) -> float:
        return float(self._coordinates[0][0])
    @left.setter
    def left(self, value: float) -> None:
        self._translate(value - self.left, 0)
    @property
    def right(self) -> float:
        return float(self._coordinates[1][0])
    @right.setter
    def right(self, value: float) -> None:
        self._translate(value - self.right, 0)
    @property
    def topleft(self) -> Coordinate:
        return self._coordinates[0]
    @topleft.setter
    def topleft(self, value: CoordinateLike) -> None:
        v = Coordinate(value)
        self._translate(v[0] - self.left, v[1] - self.top)
    @property
    def bottomleft(self) -> Coordinate:
        return self._coordinates[3]
    @bottomleft.setter
    def bottomleft(self, value: CoordinateLike) -> None:
        v = Coordinate(value)
        self._translate(v[0] - self.left, v[1] - self.bottom)
    @property
    def topright(self) -> Coordinate:
        return self._coordinates[1]
    @topright.setter
    def topright(self, value: CoordinateLike) -> None:
        v = Coordinate(value)
        self._translate(v[0] - self.right, v[1] - self.top)
    @property
    def bottomright(self) -> Coordinate:
        return self._coordinates[2]
    @bottomright.setter
    def bottomright(self, value: CoordinateLike) -> None:
        v = Coordinate(value)
        self._translate(v[0] - self.right, v[1] - self.bottom)
    @property
    def center(self) -> Coordinate:
        return Coordinate(
            (self.left + self.right) / 2,
            (self.top + self.bottom) / 2
        )
    @center.setter
    def center(self, value: CoordinateLike) -> None:
        v = Coordinate(value)
        c = self.center
        self._translate(v[0] - c[0], v[1] - c[1])
    @property
    def centerleft(self) -> Coordinate:
        return Coordinate(self.left, (self.top + self.bottom) / 2)
    @centerleft.setter
    def centerleft(self, value: CoordinateLike) -> None:
        v = Coordinate(value)
        c = self.centerleft
        self._translate(v[0] - c[0], v[1] - c[1])
    @property
    def centerright(self) -> Coordinate:
        return Coordinate(self.right, (self.top + self.bottom) / 2)
    @centerright.setter
    def centerright(self, value: CoordinateLike) -> None:
        v = Coordinate(value)
        c = self.centerright
        self._translate(v[0] - c[0], v[1] - c[1])
    @property
    def centertop(self) -> Coordinate:
        return Coordinate((self.left + self.right) / 2, self.top)
    @centertop.setter
    def centertop(self, value: CoordinateLike) -> None:
        v = Coordinate(value)
        c = self.centertop
        self._translate(v[0] - c[0], v[1] - c[1])
    @property
    def centerbottom(self) -> Coordinate:
        return Coordinate((self.left + self.right) / 2, self.bottom)
    @centerbottom.setter
    def centerbottom(self, value: CoordinateLike) -> None:
        v = Coordinate(value)
        c = self.centerbottom
        self._translate(v[0] - c[0], v[1] - c[1])
    @property
    def area(self) -> float:
        return float(self.width * self.height)
    @property
    def circumference(self) -> float:
        return float(2 * (self.width + self.height))
    @property
    def position(self) -> Coordinate:
        return self.topleft
    @position.setter
    def position(self, value: CoordinateLike) -> None:
        self.topleft = value
    @overload
    def move(self, dx: Numeric, dy: Numeric) -> None: ...
    @overload
    def move(self, delta: CoordinateLike, /) -> None: ...
    def move(self, dx: Union[Numeric, CoordinateLike], dy: Optional[Numeric] = None) -> None:
        if dy is None:
            self._translate(*dx)
        else:
            self._translate(dx, dy)
    @overload
    def translate(self, dx: Numeric, dy: Numeric) -> None: ...
    @overload
    def translate(self, delta: CoordinateLike, /) -> None: ...
    def translate(self, dx: Union[Numeric, CoordinateLike], dy: Optional[Numeric] = None) -> None:
        if dy is None:
            self._translate(*dx)
        else:
            self._translate(dx, dy)
    @overload
    def scale(self, dw: Numeric, dh: Numeric) -> None: ...
    @overload
    def scale(self, delta: CoordinateLike, /) -> None: ...
    def scale(self, dw: Union[Numeric, CoordinateLike], dh: Optional[Numeric] = None) -> None:
        if dh is None:
            self.width += dw[0]
            self.height += dw[1]
        else:
            self.width += dw
            self.height += dh
    def contains(self, other: Union[Self, RectLike, Coordinate, CoordinateLike]) -> bool:
        if isinstance(other, Rect):
            return (
                other.left >= self.left and
                other.right <= self.right and
                other.top >= self.top and
                other.bottom <= self.bottom
            )
        if isinstance(other, Sequence):
            if len(other) == 4:  # RectLike
                r = Rect(other)
                return (
                    r.left >= self.left and
                    r.right <= self.right and
                    r.top >= self.top and
                    r.bottom <= self.bottom
                )
            elif len(other) == 2:  # CoordinateLike
                x, y = other
                return (
                    self.left <= x <= self.right and
                    self.top <= y <= self.bottom
                )
        return False
    def intersects(self, other: Union[Self, RectLike, Coordinate, CoordinateLike]) -> bool:
        if isinstance(other, Rect):
            return not (
                other.left > self.right or
                other.right < self.left or
                other.top > self.bottom or
                other.bottom < self.top
            )
        if isinstance(other, Sequence):
            if len(other) == 4:  # RectLike
                r = Rect(other)
                return not (
                    r.left > self.right or
                    r.right < self.left or
                    r.top > self.bottom or
                    r.bottom < self.top
                )
            elif len(other) == 2:  # CoordinateLike
                x, y = other
                return (
                    self.left <= x <= self.right and
                    self.top <= y <= self.bottom
                )
        return False
    def distance(self, other: Union[Self, RectLike, Coordinate, CoordinateLike]) -> float:
        if isinstance(other, Rect):
            return self.center.distance(other.position)
        if isinstance(other, Sequence):
            if len(other) == 4:  # RectLike
                r = Rect(other)
                return self.center.distance(r.position)
            else:  # CoordinateLike
                return self.center.distance(other)
        return False
    def __getitem__(self, index: int) -> None:
        return self.__iter__()[index]
    def __len__(self) -> int:
        return 4
    def __iter__(self) -> Iterable[Numeric]:
        return iter((*self.topleft, *self.size))
    def __repr__(self) -> str:
        return f"Rect({', '.join((*(str(c) for c in self.topleft), *(str(c) for c in self.size)))})"

Rectangle: TypeAlias = Rect

class Square(Rect):
    @overload
    def __init__(self, x: Numeric, y: Numeric, width: Numeric, height: Optional[Numeric] = None) -> None: ...
    @overload
    def __init__(self, x: Numeric, y: Numeric, size: Numeric) -> None: ...
    @overload
    def __init__(self, rectangle: RectLike, /) -> None: ...
    def __init__(self, x: Union[Numeric, RectLike], y: Optional[Numeric] = None, width: Optional[Numeric] = None, height: Optional[Numeric] = None, *, size: Optional[Numeric] = None) -> None:
        if width is not None and height is None:
            x, y, width, height = x, y, width, width
        elif size is not None:
            x, y, width, height = x, y, size, size
        elif y is None or width is None or height is None:
            x, y, width, height = x
        if not width == height:
            raise RuntimeError("width must be equal to height in a square")
        Rect.__init__(self, x, y, width, height)

class Surface(list):
    def __init__(self) -> None: ...
    def __getitem__(self, index: Union[int, Tuple[int, int]]) -> Union[List, Any]:
        if type(index) is tuple:
            x, y = index
            return list.__getitem__(self, x)[y]
        return list.__getitem__(self, index)
    def __setitem__(self, index: Union[int, Tuple[int, int]], value: Any) -> None:
        if type(index) is tuple:
            x, y = index
            list.__getitem__(self, x)[y] = value
        else:
            list.__setitem__(self, index, value)
    @overload
    def setup(self, x: int, y: int) -> None: ...
    @overload
    def setup(self, size: Sequence[int], /) -> None: ...
    def setup(self, x: Union[int, Sequence[int]], y: Optional[int] = None) -> None:
        if y is None:
            x, y = x
        self[:] = [[0x0] * y for _ in range(x)]
    def blit(self, surface: Self, pos: Union[Rect, RectLike, Coordinate, CoordinateLike]) -> None:
        if isinstance(pos, Rect):
            dx, dy = pos.topleft
        elif isinstance(pos, Sequence):
            if len(pos) == 4:  # RectLike
                r = Rect(pos)
                dx, dy = r.topleft
            else:  # CoordinateLike
                dx, dy = pos
        for x, row in enumerate(surface):
            dst_row = self[int(x + dx)]
            for y, val in enumerate(row):
                dst_row[int(y + dy)] = val
    def fill(self, value: Any) -> None:
        self[:] = [[value] * len(self[0]) for _ in range(len(self))]
    def clear(self) -> None:
        self[:] = [[0x0] * len(self[0]) for _ in range(len(self))]
    def reset(self) -> None:
        list.clear(self)
    def get_rect(self, **kwargs: Numeric) -> Rect:
        size = (len(self), len(self[0]))
        return create_rect(0, 0, *size, **kwargs)

Map: TypeAlias = Surface # The map is a type alias of surface, since it can technically be filled with any python object

def clamp(value: Numeric, maxi: Numeric, mini: Numeric) -> Numeric:
    return max(min(value, maxi), mini)

class Color(tuple):
    @overload
    def __new__(cls, r: Numeric, g: Numeric, b: Numeric) -> Self: ...
    @overload
    def __new__(cls, color: ColorLike, /) -> Self: ...
    def __new__(cls, r: Union[Numeric, ColorLike], g: Optional[Numeric] = None, b: Optional[Numeric] = None) -> Self:
        if g is None or b is None:
            return tuple.__new__(cls, r)
        return tuple.__new__(cls, (r, g, b))
    @staticmethod
    def unpack(packed: int) -> Self:
        r = (packed >> 16) & 255
        g = (packed >> 8) & 255
        b = packed & 255
        return Color(r, g, b)
    @property
    def r(self) -> Numeric:
        return self[0]
    @property
    def g(self) -> Numeric:
        return self[1]
    @property
    def b(self) -> Numeric:
        return self[2]
    def clamp(self) -> Self:
        return Color(clamp(self[0], 255, 0), clamp(self[1], 255, 0), clamp(self[2], 255, 0))
    def pack(self) -> int:
        return (self[0] << 16) | (self[1] << 8) | self[2]
    def __eq__(self, other: Union[ColorLike, int]) -> bool:
        if isinstance(other, int):
            return self.pack() == other
        else:
            return tuple.__eq__(self, other)
    def __ne__(self, other: Union[ColorLike, int]) -> bool:
        if isinstance(other, int):
            return self.pack() != other
        else:
            return tuple.__ne__(self, other)
    def __add__(self, other: ColorLike) -> Self:
        return Color(self[0] + other[0], self[1] + other[1], self[2] + other[2])
    def __radd__(self, other: ColorLike) -> Self:
        return Color(other[0] + self[0], other[1] + self[1], other[2] + self[2])
    def __iadd__(self, other: ColorLike) -> Self:
        return Color(self[0] + other[0], self[1] + other[1], self[2] + other[2])
    def __sub__(self, other: ColorLike) -> Self:
        return Color(self[0] - other[0], self[1] - other[1], self[2] - other[2])
    def __rsub__(self, other: ColorLike) -> Self:
        return Color(other[0] - self[0], other[1] - self[1], other[2] - self[2])
    def __isub__(self, other: ColorLike) -> Self:
        return Color(self[0] - other[0], self[1] - other[1], self[2] - other[2])
    def __mul__(self, other: Numeric) -> Self:
        return Color(self[0] * other, self[1] * other, self[2] * other)
    def __rmul__(self, other: Numeric) -> Self:
        return Color(other * self[0], other * self[1], other * self[2])
    def __imul__(self, other: Numeric) -> Self:
        return Color(self[0] * other, self[1] * other, self[2] * other)
    def __truediv__(self, other: Numeric) -> Self:
        return Color(self[0] / other, self[1] / other, self[2] / other)
    def __rtruediv__(self, other: Numeric) -> Self:
        return Color(other / self[0], other / self[1], other / self[2])
    def __itruediv__(self, other: Numeric) -> Self:
        return Color(self[0] / other, self[1] / other, self[2] / other)
    def __floordiv__(self, other: Numeric) -> Self:
        return Color(self[0] // other, self[1] // other, self[2] // other)
    def __rfloordiv__(self, other: Numeric) -> Self:
        return Color(other // self[0], other // self[1], other // self[2])
    def __ifloordiv__(self, other: Numeric) -> Self:
        return Color(self[0] // other, self[1] // other, self[2] // other)
    def __mod__(self, other: Numeric) -> Self:
        return Color(self[0] % other, self[1] % other, self[2] % other)
    def __rmod__(self, other: Numeric) -> Self:
        return Color(other % self[0], other % self[1], other % self[2])
    def __imod__(self, other: Numeric) -> Self:
        return Color(self[0] % other, self[1] % other, self[2] % other)
    def __neg__(self) -> Self:
        return Color(-self[0], -self[1], -self[2])
    def __pos__(self) -> Self:
        return self
    def __abs__(self) -> Self:
        return Color(abs(self[0]), abs(self[1]), abs(self[2]))
    def __round__(self, n: Optional[int] = None) -> Self:
        return Color(round(self[0], n), round(self[1], n), round(self[2], n))
    def __getnewargs__(self) -> Tuple[Numeric, Numeric, Numeric]:
        return (self[0], self[1], self[2])
    def __repr__(self) -> str:
        return f"Color({self[0]}, {self[1]}, {self[2]})"

@overload
def create_rect(x: Numeric, y: Numeric, width: Numeric, height: Numeric, **kwargs: Numeric) -> Rect: ...
@overload
def create_rect(initial_matrix: RectLike, **kwargs: Numeric) -> Rect: ...
def create_rect(x: Union[Numeric, RectLike], y: Optional[Numeric] = None, width: Optional[Numeric] = None, height: Optional[Numeric] = None, **kwargs: Union[Numeric, RectLike]) -> Rect:
    if "initial_matrix" in kwargs:
        initial_matrix = kwargs["initial_matrix"]
        x, y, width, height = initial_matrix
    elif y is None or width is None or height is None:
        x, y, width, height = x
    rect = Rect(x, y, width, height)
    for name, value in kwargs.items():
        if hasattr(rect, name):
            setattr(rect, name, value)
    return rect