"""The level parser for V2 levels."""

from .level import Level, LevelParsingError, Cell
from .base74 import b74_decode,b74_encode
import re


def open(level_code: str) -> Level:
    if "insert some regex here":
        level_list = level_code.split(";")
        level_list[1] = b74_decode(level_list[1])
        level_list[2] = b74_decode(level_list[2])
        level = Level(
            level_list[1],
            level_list[2],
            level_list[4],
            int(level_list[5]) if level_list[5] != "" else 0,
        )
        
        level_list[3] += "0" # This only gets compared against in the context of being ) or (
        
        count = 0
        position = 0
        while count < len(level_list[3])-1:
            if level_list[3][count+1] is ")":
                repeat == b74_decode(level_list[3][count+2])
            elif level_list[3][count+1] is "("
                repeat == b74_decode(level_list[3][count+2:].split(")")[0])
            else:
                repeat = 0
            
            for i in range(repeat):
                cell_num = b74_decode(level_list[3][count+i])
                level[(count+i)%level_list[1], (count+i)//level_list[2]] = c % 2 == 1
                level[(count+i)%level_list[1], (count+i)//level_list[2]] = Cell((cell_num//2) % 9,  [0, 3, 2, 1][c // 18])
                
            count += repeat

        return level
    else:
        raise LevelParsingError("Invalid V1 level code.")


def save(level: Level) -> str:
    # Loop through the level and save it to 2 lists which are used in the V1 level code
    placeable = []
    cells = []
    for x, y, cell, place in level:
        if place:
            placeable.append(f"{x}.{y}")

        if cell.type != 0:
            cells.append(f"{int(cell.type)}.{int(cell.rotation)}.{x}.{y}")

    return f"V1;{level.width};{level.height};{';'.join(placeable)};{';'.join(cells)};{level.name};{int(level.wall_effect)}"
