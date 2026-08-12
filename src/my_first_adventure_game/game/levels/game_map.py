from dataclasses import dataclass

from my_first_adventure_game.engine.world import Entity, World
from my_first_adventure_game.game.entities import NPC, Enemy, Player


@dataclass(frozen=True, slots=True)
class GameMap:
    """Group a world with the entities used by the gameplay scene.

    Attributes:
        world: World containing every entity registered for the map.
        player: Concrete player and its spatial entity.
        walls: Entities selected as solid obstacles by the gameplay scene.
        collectibles: Entities assigned the collectible role by the game.
        destructible_obstacles: Wall entities that the game allows attacks to destroy.
        enemies: Entities assigned the enemy role by the game.
        npcs: Non-player characters assigned an interaction role by the game.
    """

    world: World
    player: Player
    walls: tuple[Entity, ...]
    enemies: tuple[Enemy, ...]
    npcs: tuple[NPC, ...]
    destructible_obstacles: tuple[Entity, ...]
    collectibles: tuple[Entity, ...]
