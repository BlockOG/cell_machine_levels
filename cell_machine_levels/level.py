"""This module contains the level class and the cell class."""

import importlib
from enum import IntEnum
from typing import Tuple, Union
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
    """The class used for cells in the Level class."""

    def __init__(self, type: CellEnum = 0, rotation: Rotations = 0) -> None:
        self.type = type
        self.rotation = rotation

    def rotate_left(self) -> None:
        """Rotate the cell left."""
        self.rotation = (self.rotation - 1) % 4

    def rotate_right(self) -> None:
        """Rotate the cell right."""
        self.rotation = (self.rotation + 1) % 4

    def __str__(self) -> str:
        return f"{self.type}:{self.rotation}"

    __repr__ = __str__

    # Comparisons

    def __eq__(self, other: object) -> bool:
        if isinstance(other, Cell):
            return self.type == other.type and self.rotation == other.rotation
        elif isinstance(other, int):
            return self.type == other
        elif isinstance(other, tuple) or isinstance(other, list):
            return self.type == other[0] and self.rotation == other[1]
        elif isinstance(other, str):
            return str(self) == other
        else:
            raise TypeError(f"Cannot compare Cell to {type(other)}")


class Level:
    """The main class for levels. You can use this class to create levels
    and to parse level codes."""

    def __init__(
        self, width: int, height: int, name: str = "", wall_effect: WallEffect = 0
    ) -> None:
        self._size = (width, height)
        self.cell_grid = [[Cell() for _ in range(width)] for _ in range(height)]
        self.place_grid = [[False for _ in range(width)] for _ in range(height)]
        self.name = name
        self.wall_effect = wall_effect
        self._pos = None  # Cause pylint is complaining

    def optimized(self) -> "Level":
        """Optimize the level.

        Returns:
            Level: The optimized level."""
        result = Level(self.width, self.height, self.name, self.wall_effect)

        for x, y, cell, place in self:
            if cell.type in (
                CellEnum.enemy,
                CellEnum.immobile,
                CellEnum.push,
                CellEnum.trash,
                CellEnum.spinner_left,
                CellEnum.spinner_right,
            ):
                result[x, y] = Cell(cell.type, 0)
            elif cell.type == CellEnum.slide:
                result[x, y] = Cell(cell.type, cell.rotation % 2)
            else:
                result[x, y] = cell

            result[x, y] = place

        return result

    def optimize(self) -> None:
        """Optimize this level without returning anything."""
        self.cell_grid = self.optimized().cell_grid

    # Saving the level

    def save(self, format: str) -> str:
        """Save the level to a level code of the given format.

        Args:
            format (str): The format to save the level in.

        Returns:
            str: The level code."""
        if format in _plugins:
            return importlib.import_module(f".{format}", "cell_machine_levels").save(
                self
            )
        else:
            raise ValueError(f"The format {format} is not supported or doesn't exist.")

    # Iterable methods

    def __iter__(self) -> "Level":
        self._pos = [0, 0]
        return self

    def __next__(self) -> Tuple[int, int, Cell, bool]:
        if self._pos[1] < self.height:
            ret = (
                self._pos[0],
                self._pos[1],
                self.cell_grid[self._pos[1]][self._pos[0]],
                self.place_grid[self._pos[1]][self._pos[0]],
            )
            self._pos[0] += 1
            if self._pos[0] >= self.width:
                self._pos = [0, self._pos[1] + 1]
            return ret
        else:
            raise StopIteration

    # Getters and setters

    def __getitem__(self, pos: Tuple[int, int, bool]) -> Union[Cell, bool]:
        if pos[2]:
            return self.place_grid[pos[1]][pos[0]]
        else:
            return self.cell_grid[pos[1]][pos[0]]

    def __setitem__(self, pos: Tuple[int, int], value: Union[Cell, bool]) -> None:
        if isinstance(value, bool):
            self.place_grid[pos[1]][pos[0]] = value
        else:
            self.cell_grid[pos[1]][pos[0]] = value

    # Getting size

    @property
    def size(self):
        """Tuple[int, int]: The size of the level."""
        return self._size

    @property
    def width(self):
        """int: The width of the level."""
        return self._size[0]

    @property
    def height(self):
        """int: The height of the level."""
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
                return self.save(other.split(";")[0]) == other
            except ValueError as ex:
                form = other.split(";")[0]
                raise ValueError(
                    f"The format {form[:10] + '...' if len(form) > 10 else form} is not supported or doesn't exist."
                ) from ex
        elif isinstance(other, list):
            return self.cell_grid == other
        else:
            raise TypeError(f"Cannot compare Level with {type(other)}")


class LevelParsingError(Exception):
    """Exception raised when parsing a level fails."""


def open(level_code: str) -> Level:
    """Open a level from a level code.

    Args:
        level_code (str): The level code.

    Returns:
        Level: The level."""
    for plugin in _plugins:
        if level_code.startswith(plugin + ";"):
            return importlib.import_module(f".{plugin}", "cell_machine_levels").open(
                level_code
            )
    raise LevelParsingError(
        f"The format {level_code.split(';')[0]} is not supported or doesn't exist."
    )
