import pygame

from my_first_adventure_game.engine.world import Entity, World
from my_first_adventure_game.game.entities import Player
from my_first_adventure_game.game.levels.game_map import GameMap
from my_first_adventure_game.game.levels.map_exit import MapExit


def create_clearing_map(player: Player) -> GameMap:
    """Create the clearing map with the current session player."""
    world = World()
    exits = (
        MapExit(
            entity=Entity(
                entity_id="exit-to-demo",
                position=pygame.Vector2(64.0, 320.0),
                size=pygame.Vector2(32.0, 80.0),
            ),
            destination_map_id="demo",
            destination_position=(1120.0, 320.0),
        ),
    )

    for entity in (
        player.entity,
        *(map_exit.entity for map_exit in exits),
    ):
        world.add(entity)

    return GameMap(
        map_id="clearing",
        world=world,
        player=player,
        walls=(),
        enemies=(),
        npcs=(),
        destructible_obstacles=(),
        collectibles=(),
        exits=exits,
    )
