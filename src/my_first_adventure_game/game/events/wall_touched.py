from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class WallTouched:
    """Report that the player touched a wall.

    Attributes:
        wall_id: Stable identifier of the touched wall.
    """

    wall_id: str
