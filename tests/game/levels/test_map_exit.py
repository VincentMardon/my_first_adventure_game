import pygame

from my_first_adventure_game.engine.world import Entity
from my_first_adventure_game.game.levels import MapExit


def test_map_exit_describes_destination_and_spawn_position() -> None:
    entity = Entity(
        entity_id="exit-to-clearing",
        position=pygame.Vector2(1200.0, 320.0),
        size=pygame.Vector2(32.0, 80.0),
    )

    map_exit = MapExit(
        entity=entity,
        destination_map_id="clearing",
        destination_position=(64.0, 320.0),
    )

    assert map_exit.entity is entity
    assert map_exit.destination_map_id == "clearing"
    assert map_exit.destination_position == (64.0, 320.0)
