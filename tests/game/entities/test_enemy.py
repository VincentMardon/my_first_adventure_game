import pygame
import pytest

from my_first_adventure_game.engine.world import Entity
from my_first_adventure_game.game.entities import Enemy


def test_enemy_stores_spatial_entity_and_health() -> None:
    entity = Entity(
        entity_id="enemy-1",
        position=pygame.Vector2(100.0, 80.0),
        size=pygame.Vector2(32.0, 32.0),
    )

    enemy = Enemy(entity=entity, health=2)

    assert enemy.entity is entity
    assert enemy.health == 2


@pytest.mark.parametrize("health", [0, -1])
def test_enemy_requires_positive_initial_health(health: int) -> None:
    entity = Entity(
        entity_id="enemy-1", position=pygame.Vector2(), size=pygame.Vector2(32.0, 32.0)
    )

    with pytest.raises(ValueError, match="health must be positive"):
        Enemy(entity=entity, health=health)


def test_take_damage_reduces_health_without_defeating_enemy() -> None:
    entity = Entity(
        entity_id="enemy-1",
        position=pygame.Vector2(),
        size=pygame.Vector2(32.0, 32.0),
    )
    enemy = Enemy(entity=entity, health=2)

    defeated = enemy.take_damage(1)

    assert enemy.health == 1
    assert entity.active
    assert not defeated


def test_take_damage_defeats_enemy_and_clamps_health_to_zero() -> None:
    entity = Entity(
        entity_id="enemy-1",
        position=pygame.Vector2(),
        size=pygame.Vector2(32.0, 32.0),
    )
    enemy = Enemy(entity=entity, health=2)

    defeated = enemy.take_damage(3)
    defeated_again = enemy.take_damage(1)

    assert not defeated_again
    assert enemy.health == 0
    assert not entity.active
    assert defeated


@pytest.mark.parametrize("damage", [0, -1])
def test_take_damage_requires_positive_damage(damage: int) -> None:
    entity = Entity(
        entity_id="enemy-1",
        position=pygame.Vector2(),
        size=pygame.Vector2(32.0, 32.0),
    )
    enemy = Enemy(entity=entity, health=2)

    with pytest.raises(ValueError, match="damage must be positive"):
        enemy.take_damage(damage)
