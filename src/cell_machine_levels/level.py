import re, glob
from enum import IntEnum, auto
from . import _plugins

class CellEnum(IntEnum):
    """The enum used for cell types in the Cell class."""
    bg = 0
    mover = 1
    generator = 2
    immobile = 3
    immovable = immobile
    push = 4
    slide = 5
    trash = 6
    enemy = 7
    spinner_left = 8
    spinner_right = 9

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
    
    def __init__(self, width: int, height: int, name: str = "", wall_effect: WallEffect = 0) -> None:
        self._size = (width, height)
        self.cell_grid = [[Cell() for _ in range(width)] for _ in range(height)]
        self.place_grid = [[False for _ in range(width)] for _ in range(height)]
        self.name = name
        self.wall_effect = wall_effect
    
    # Saving the level
    
    def save(self, format: str, v4: bool = True) -> str:
        if format in _plugins:
            return __import__(f"cell_machine_levels.{format}").save(self, v4 = v4)
    
    # Iterable methods
    
    def __iter__(self) -> None:
        self._pos = (0, 0)
    
    def __next__(self) -> tuple[int, int, Cell, bool]:
        if self._pos[1] < self.height:
            ret = self._pos[0], self._pos[1], self.cell_grid[self._pos[1]][self._pos[0]], self.place_grid[self._pos[1]][self._pos[0]]
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

class LevelParsingError(Exception):
    pass

def open(level_code: str, v4: bool = True) -> Level:
        for plugin in _plugins:
            if level_code.startswith(plugin + ";"):
                return __import__(f"cell_machine_levels.{plugin}").open(level_code, v4 = v4)
