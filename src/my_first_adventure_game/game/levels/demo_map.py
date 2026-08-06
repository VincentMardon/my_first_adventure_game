import pygame

from my_first_adventure_game.engine.world import Entity, World
from my_first_adventure_game.game.levels.game_map import GameMap


def create_demo_map() -> GameMap:
    """Create the first Python-authored gameplay map."""
    player = Entity(
        entity_id="player",
        position=pygame.Vector2(128.0, 128.0),
        size=pygame.Vector2(32.0, 32.0),
    )
    walls = (
        Entity(
            entity_id="wall-top",
            position=pygame.Vector2(64.0, 64.0),
            size=pygame.Vector2(1152.0, 32.0),
        ),
        Entity(
            entity_id="wall-bottom",
            position=pygame.Vector2(64.0, 624.0),
            size=pygame.Vector2(1152.0, 32.0),
        ),
        Entity(
            entity_id="wall-left",
            position=pygame.Vector2(64.0, 96.0),
            size=pygame.Vector2(32.0, 528.0),
        ),
        Entity(
            entity_id="wall-right",
            position=pygame.Vector2(1184.0, 96.0),
            size=pygame.Vector2(32.0, 528.0),
        ),
        Entity(
            entity_id="wall-center",
            position=pygame.Vector2(400.0, 224.0),
            size=pygame.Vector2(32.0, 256.0),
        ),
    )

    world = World()

    for entity in (player, *walls):
        world.add(entity)

    return GameMap(
        world=world,
        player=player,
        walls=walls,
    )
