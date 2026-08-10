from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class ObstacleDestroyed:
    """Report that the player destroyed an obstacle.

    Attributes:
        obstacle_id: Stable identifier of the destroyed obstacle.
    """

    obstacle_id: str
