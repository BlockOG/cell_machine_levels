"""The level parser for V2 levels."""

import re
from .level import Level, LevelParsingError, Cell
from .base74 import b74_decode, b74_encode, b74_key


def open(level_code: str) -> Level:
    if re.match(r"^V2;;[0-3]?$", level_code):
        level_list = level_code.split(";")
        level = Level(
            b74_decode(level_list[1]),
            b74_decode(level_list[2]),
            level_list[4],
            int(level_list[5]) if level_list[5] != "" else 0,
        )

        level_list[
            3
        ] += "0"  # This only gets compared against in the context of being ) or (

        count = 0
        while count < len(level_list[3]) - 1:
            if level_list[3][count + 1] is ")":
                repeat = b74_decode(level_list[3][count + 2])
            elif level_list[3][count + 1] is "(":
                repeat = b74_decode(level_list[3][count + 2 :].split(")")[0])
            else:
                repeat = 0

            for i in range(repeat):
                cell_num = b74_decode(level_list[3][count + i])
                level[(count + i) % level.width, (count + i) // level.height] = (
                    cell_num % 2 == 1
                )
                level[(count + i) % level.width, (count + i) // level.height] = Cell(
                    (cell_num // 2) % 9, [0, 3, 2, 1][cell_num // 18]
                )

            count += repeat

        return level
    else:
        raise LevelParsingError("Invalid V2 level code.")


def save(level: Level) -> str:
    placeable = []
    cells = []
    for x, y, cell, place in level:
        if place:
            placeable.append(f"{x}.{y}")

        if cell.type != 0:
            cells.append(f"{int(cell.type)}.{int(cell.rotation)}.{x}.{y}")

    return f"V2;{level.width};{level.height};{';'.join(placeable)};{';'.join(cells)};{level.name};{int(level.wall_effect)}"
