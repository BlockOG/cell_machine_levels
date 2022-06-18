"""The cells module contains the BGCell class and its subclasses."""


class Rotations:
    """Rotations for cells."""

    def __new__(cls, rotation: int = 0) -> int:
        return rotation % cls.AOR

    RIGHT = 0
    DOWN = 1
    LEFT = 2
    UP = 3

    AOR = 4 # Amount of rotations

    @classmethod
    def from_int(cls, i: int) -> str:
        """Create a string from a rotation integer."""
        if i == cls.RIGHT:
            return "RIGHT"
        if i == cls.DOWN:
            return "DOWN"
        if i == cls.LEFT:
            return "LEFT"
        if i == cls.UP:
            return "UP"
        raise ValueError("Invalid rotation integer.")


class BGCell:
    """This is the base class for all cells and is the bg cell."""

    def __init__(self) -> None:
        self._rotation = Rotations.RIGHT

    @property
    def rotation(self) -> Rotations:
        """The rotation of the cell."""
        return self._rotation

    @rotation.setter
    def rotation(self, value: Rotations) -> None:
        self._rotation = value % Rotations.AOR
        self._rotation = Rotations.RIGHT

    def rotate_left(self) -> None:
        """Rotate the cell left."""
        self.rotation = (self.rotation - 1) % Rotations.AOR

    def rotate_right(self) -> None:
        """Rotate the cell right."""
        self.rotation = (self.rotation + 1) % Rotations.AOR

    def __eq__(self, other: object) -> bool:
        return isinstance(other, BGCell)

    def __str__(self) -> str:
        return "BGCell"

    def __repr__(self) -> str:
        return f"{self}({Rotations.from_int(self.rotation)})"


class MoverCell(BGCell):
    """This is the mover cell."""

    def __init__(self, rotation: Rotations = Rotations.RIGHT) -> None:
        self._rotation = rotation

    rotation = super().rotation

    @rotation.setter
    def rotation(self, value: Rotations) -> None:
        self._rotation = value % Rotations.AOR

    def __str__(self) -> str:
        return "MoverCell"
