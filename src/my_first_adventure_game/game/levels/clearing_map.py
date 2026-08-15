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
    walls = (
        Entity(
            entity_id="clearing-wall-top",
            position=pygame.Vector2(64.0, 64.0),
            size=pygame.Vector2(1152.0, 32.0),
        ),
        Entity(
            entity_id="clearing-wall-bottom",
            position=pygame.Vector2(64.0, 624.0),
            size=pygame.Vector2(1152.0, 32.0),
        ),
        Entity(
            entity_id="clearing-wall-left-top",
            position=pygame.Vector2(64.0, 96.0),
            size=pygame.Vector2(32.0, 224.0),
        ),
        Entity(
            entity_id="clearing-wall-left-bottom",
            position=pygame.Vector2(64.0, 400.0),
            size=pygame.Vector2(32.0, 224.0),
        ),
        Entity(
            entity_id="clearing-wall-right",
            position=pygame.Vector2(1184.0, 96.0),
            size=pygame.Vector2(32.0, 528.0),
        ),
    )

    for entity in (
        player.entity,
        *walls,
        *(map_exit.entity for map_exit in exits),
    ):
        world.add(entity)

    return GameMap(
        map_id="clearing",
        world=world,
        player=player,
        walls=walls,
        enemies=(),
        npcs=(),
        destructible_obstacles=(),
        collectibles=(),
        exits=exits,
    )
