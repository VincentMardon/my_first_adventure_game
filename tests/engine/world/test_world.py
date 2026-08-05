import pygame
import pytest

from my_first_adventure_game.engine.world import Entity, World


def make_entity(entity_id: str) -> Entity:
    return Entity(
        entity_id=entity_id,
        position=pygame.Vector2(),
        size=pygame.Vector2(16.0, 16.0),
    )


def test_world_starts_empty() -> None:
    world = World()

    assert world.entities == ()
    assert world.get("missing") is None


def test_add_registers_entity_by_stable_identifier() -> None:
    world = World()
    entity = make_entity("player")

    world.add(entity)

    assert world.get("player") is entity
    assert world.entities == (entity,)


def test_entities_preserve_insertion_order_and_return_a_snapshot() -> None:
    world = World()
    player = make_entity("player")
    wall = make_entity("wall")

    world.add(player)
    snapshot = world.entities
    world.add(wall)

    assert snapshot == (player,)
    assert world.entities == (player, wall)


def test_add_rejects_duplicate_entity_identifier() -> None:
    world = World()
    original = make_entity("player")
    duplicate = make_entity("player")

    world.add(original)

    with pytest.raises(ValueError, match="player"):
        world.add(duplicate)

    assert world.get("player") is original
    assert world.entities == (original,)
