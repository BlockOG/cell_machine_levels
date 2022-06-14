from enum import IntEnum
from . import _plugins


class CellEnum(IntEnum):
    """The enum used for cell types in the Cell class."""

    generator = 0
    spinner_right = 1
    spinner_left = 2
    mover = 3
    slide = 4
    push = 5
    immobile = 6
    immovable = immobile
    enemy = 7
    trash = 8
    bg = 9


class Rotations(IntEnum):
    """The enum used for rotations in the Cell class."""

    right = 0
    down = 1
    left = 2
    up = 3


class WallEffect(IntEnum):
    """The Mystic Mod V4 wall effect enum."""

    stop = 0
    wrap = 1
    delete = 2
    flip = 3


class Cell:
    def __init__(self, type: CellEnum = 0, rotation: Rotations = 0) -> None:
        self.type = type
        self.rotation = rotation

    def rotate_left(self) -> None:
        self.rotation = (self.rotation - 1) % 4

    def rotate_right(self) -> None:
        self.rotation = (self.rotation + 1) % 4


class Level:
    """The main class for levels. You can use this class to create levels and to parse level codes."""

    def __init__(
        self, width: int, height: int, name: str = "", wall_effect: WallEffect = 0
    ) -> None:
        self._size = (width, height)
        self.cell_grid = [[Cell() for _ in range(width)] for _ in range(height)]
        self.place_grid = [[False for _ in range(width)] for _ in range(height)]
        self.name = name
        self.wall_effect = wall_effect

    # Saving the level

    def save(self, format: str, v4: bool = True) -> str:
        if format in _plugins:
            try:
                return __import__(f"cell_machine_levels.{format}").save(self, v4=v4)
            except ImportError:
                raise ValueError(
                    f"The format {format} is not supported or doesn't exist."
                )

    # Iterable methods

    def __iter__(self) -> None:
        self._pos = (0, 0)

    def __next__(self) -> tuple[int, int, Cell, bool]:
        if self._pos[1] < self.height:
            ret = (
                self._pos[0],
                self._pos[1],
                self.cell_grid[self._pos[1]][self._pos[0]],
                self.place_grid[self._pos[1]][self._pos[0]],
            )
            self._pos[0] += 1
            if self._pos[0] >= self.width:
                self._pos = 0, self._pos[1] + 1
            return ret
        else:
            raise StopIteration

    # Getters and setters

    def __getitem__(self, pos: tuple[int, int, bool]) -> Cell:
        if tuple[2]:
            return self.place_grid[pos[1]][pos[0]]
        else:
            return self.cell_grid[pos[1]][pos[0]]

    def __setitem__(self, pos: tuple[int, int, bool], value: Cell) -> None:
        if tuple[2]:
            self.place_grid[pos[1]][pos[0]] = value
        else:
            self.cell_grid[pos[1]][pos[0]] = value

    # Getting size

    @property
    def size(self):
        return self._size

    @property
    def width(self):
        return self._size[0]

    @property
    def height(self):
        return self._size[1]

    # Comparisons

    def __eq__(self, other: object) -> bool:
        if isinstance(other, Level):
            return (
                self.cell_grid == other.cell_grid
                and self.place_grid == other.place_grid
                and self.name == other.name
                and self.wall_effect == other.wall_effect
            )
        elif isinstance(other, str):
            try:
                return (
                    self.save(other.split(";")[0], bool(other.split(";")[-1])) == other
                )
            except ValueError:
                raise ValueError(
                    f"The format {(f := other.split(';')[0])[:10] + '...' if len(f) > 10 else f} is not supported or doesn't exist."
                )
        elif isinstance(other, list):
            return self.cell_grid == other
        else:
            raise TypeError(f"Cannot compare Level with {type(other)}")


class LevelParsingError(Exception):
    pass


def open(level_code: str, v4: bool = True) -> Level:
    for plugin in _plugins:
        if level_code.startswith(plugin + ";"):
            return __import__(f"cell_machine_levels.{plugin}").open(level_code, v4=v4)
