import pygame
import pytest

from my_first_adventure_game.engine.world import Entity
from my_first_adventure_game.game.entities import Player


def test_player_stores_spatial_entity_and_health() -> None:
    entity = Entity(
        entity_id="player",
        position=pygame.Vector2(100.0, 80.0),
        size=pygame.Vector2(32.0, 32.0),
    )

    player = Player(entity=entity, health=3)

    assert player.entity is entity
    assert player.health == 3


@pytest.mark.parametrize("health", [0, -1])
def test_player_requires_positive_initial_health(health: int) -> None:
    entity = Entity(
        entity_id="player",
        position=pygame.Vector2(),
        size=pygame.Vector2(32.0, 32.0),
    )

    with pytest.raises(ValueError, match="health must be positive."):
        Player(entity=entity, health=health)


def test_take_damage_reduces_health_without_defeating_player() -> None:
    entity = Entity(
        entity_id="player",
        position=pygame.Vector2(),
        size=pygame.Vector2(32.0, 32.0),
    )
    player = Player(entity=entity, health=3)

    defeated = player.take_damage(1)

    assert player.health == 2
    assert entity.active
    assert not defeated


def test_take_damage_defeats_player_and_clamps_health_to_zero() -> None:
    entity = Entity(
        entity_id="player",
        position=pygame.Vector2(),
        size=pygame.Vector2(32.0, 32.0),
    )
    player = Player(entity=entity, health=1)

    defeated = player.take_damage(2)
    defeated_again = player.take_damage(1)

    assert player.health == 0
    assert not entity.active
    assert defeated
    assert not defeated_again


@pytest.mark.parametrize("damage", [0, -1])
def test_take_damage_requires_positive_damage(damage: int) -> None:
    entity = Entity(
        entity_id="player",
        position=pygame.Vector2(),
        size=pygame.Vector2(32.0, 32.0),
    )
    player = Player(entity=entity, health=3)

    with pytest.raises(ValueError, match="damage must be positive"):
        player.take_damage(damage)
