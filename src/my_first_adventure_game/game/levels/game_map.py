from dataclasses import dataclass

from my_first_adventure_game.engine.world import Entity, World


@dataclass(frozen=True, slots=True)
class GameMap:
    """Group a world with the entities used by the gameplay scene."""

    world: World
    player: Entity
    walls: tuple[Entity, ...]
