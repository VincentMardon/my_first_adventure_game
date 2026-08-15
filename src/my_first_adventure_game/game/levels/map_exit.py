from dataclasses import dataclass

from my_first_adventure_game.engine.world import Entity


@dataclass(frozen=True, slots=True)
class MapExit:
    """Describe a spatial exit and its destination.

    Attributes:
        entity: Spatial trigger used to detect the exit.
        destination_map_id: Stable identifier of the destination map.
        destination_position: Player position after entering the destination.
    """

    entity: Entity
    destination_map_id: str
    destination_position: tuple[float, float]
