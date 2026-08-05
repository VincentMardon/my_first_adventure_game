import pygame
import pytest

from my_first_adventure_game.engine.collisions import AABB
from my_first_adventure_game.engine.world import Entity


def test_entity_stores_independent_initial_state() -> None:
    position = pygame.Vector2(10.5, 20.25)
    size = pygame.Vector2(16.0, 24.0)

    entity = Entity(entity_id="player", position=position, size=size)

    assert entity.entity_id == "player"
    assert entity.position == position
    assert entity.size == size
    assert entity.active
    assert entity.position is not position
    assert entity.size is not size


def test_entity_id_is_read_only() -> None:
    entity = Entity(
        entity_id="player",
        position=pygame.Vector2(),
        size=pygame.Vector2(16.0, 24.0),
    )

    with pytest.raises(AttributeError):
        entity.entity_id = "changed"


def test_bounds_follow_current_entity_geometry() -> None:
    entity = Entity(
        entity_id="player",
        position=pygame.Vector2(10.5, 20.25),
        size=pygame.Vector2(16.0, 24.0),
    )

    entity.position.update(30.5, 40.25)
    entity.size.update(20.0, 28.0)

    assert entity.bounds == AABB(
        x=30.5,
        y=40.25,
        width=20.0,
        height=28.0,
    )


def test_entity_can_start_inactive() -> None:
    entity = Entity(
        entity_id="hidden-door",
        position=pygame.Vector2(),
        size=pygame.Vector2(32.0, 32.0),
        active=False,
    )

    assert not entity.active
