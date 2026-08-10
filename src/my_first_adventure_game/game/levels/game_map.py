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
        destructible_obstacles: Wall entities that the game allows attacks to destroy.
    """

    world: World
    player: Entity
    walls: tuple[Entity, ...]
    destructible_obstacles: tuple[Entity, ...]
    collectibles: tuple[Entity, ...]
