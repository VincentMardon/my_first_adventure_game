from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class WallTouched:
    """Report that the player touched a wall.

    Attributes:
        wall_id: Stable identifier of the touched wall.
        contact_position: Contact point on the wall surface.
        surface_normal: Axis-aligned unit vector pointing away from the wall.
    """

    wall_id: str
    contact_position: tuple[float, float]
    surface_normal: tuple[float, float]
