from dataclasses import dataclass

from my_first_adventure_game.engine.world import Entity, World


@dataclass(frozen=True, slots=True)
class GameMap:
    """Group a world with the entities used by the gameplay scene.

    Attributes:
        world: World containing every entity registered for the map.
        player: Entity controlled by the player.
        walls: Entities selected as solid obstacles by the gameplay scene.
        collectibles: Entities assigned the collectible role by the game.
    """

    world: World
    player: Entity
    walls: tuple[Entity, ...]
    collectibles: tuple[Entity, ...]
