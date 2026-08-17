import pygame
import pytest

from my_first_adventure_game.engine.collisions import AABB
from my_first_adventure_game.engine.world import (
    Entity,
    move_entity,
    movement_towards,
)


def make_entity(
    *,
    position: tuple[float, float] = (0.0, 0.0),
) -> Entity:
    return Entity(
        entity_id="moving",
        position=pygame.Vector2(position),
        size=pygame.Vector2(10.0, 10.0),
    )


def test_move_entity_applies_full_movement_without_obstacles() -> None:
    entity = make_entity()
    requested = pygame.Vector2(3.5, -2.25)

    actual = move_entity(entity, requested, ())

    assert entity.position == pygame.Vector2(3.5, -2.25)
    assert actual == requested
    assert actual is not requested


def test_move_entity_stops_at_horizontal_obstacle() -> None:
    entity = make_entity()
    wall = AABB(x=15.0, y=0.0, width=10.0, height=10.0)

    actual = move_entity(
        entity,
        pygame.Vector2(10.0, 0.0),
        (wall,),
    )

    assert entity.position == pygame.Vector2(5.0, 0.0)
    assert actual == pygame.Vector2(5.0, 0.0)


def test_move_entity_stops_at_obstacle_to_left() -> None:
    entity = make_entity(position=(20.0, 0.0))
    wall = AABB(x=5.0, y=0.0, width=10.0, height=10.0)

    actual = move_entity(
        entity,
        pygame.Vector2(-10.0, 0.0),
        (wall,),
    )

    assert entity.position == pygame.Vector2(15.0, 0.0)
    assert actual == pygame.Vector2(-5.0, 0.0)


def test_move_entity_stops_at_vertical_obstacle() -> None:
    entity = make_entity()
    wall = AABB(x=0.0, y=15.0, width=10.0, height=10.0)

    actual = move_entity(
        entity,
        pygame.Vector2(0.0, 10.0),
        (wall,),
    )

    assert entity.position == pygame.Vector2(0.0, 5.0)
    assert actual == pygame.Vector2(0.0, 5.0)


def test_move_entity_stops_at_obstacle_above() -> None:
    entity = make_entity(position=(0.0, 20.0))
    wall = AABB(x=0.0, y=5.0, width=10.0, height=10.0)

    actual = move_entity(
        entity,
        pygame.Vector2(0.0, -10.0),
        (wall,),
    )

    assert entity.position == pygame.Vector2(0.0, 15.0)
    assert actual == pygame.Vector2(0.0, -5.0)


def test_move_entity_prevents_tunneling_through_obstacle() -> None:
    entity = make_entity()
    wall = AABB(x=30.0, y=0.0, width=5.0, height=10.0)

    actual = move_entity(
        entity,
        pygame.Vector2(100.0, 0.0),
        (wall,),
    )

    assert entity.position == pygame.Vector2(20.0, 0.0)
    assert actual == pygame.Vector2(20.0, 0.0)


def test_move_entity_slides_along_obstacle() -> None:
    entity = make_entity()
    wall = AABB(x=15.0, y=-20.0, width=10.0, height=50.0)

    actual = move_entity(
        entity,
        pygame.Vector2(10.0, 6.0),
        (wall,),
    )

    assert entity.position == pygame.Vector2(5.0, 6.0)
    assert actual == pygame.Vector2(5.0, 6.0)


def test_move_entity_ignores_obstacle_outside_movement_axis() -> None:
    entity = make_entity()
    wall = AABB(x=15.0, y=20.0, width=10.0, height=10.0)

    actual = move_entity(
        entity,
        pygame.Vector2(10.0, 0.0),
        (wall,),
    )

    assert entity.position == pygame.Vector2(10.0, 0.0)
    assert actual == pygame.Vector2(10.0, 0.0)


def test_move_entity_resolves_both_axes_with_one_pass_iterable() -> None:
    entity = make_entity()
    walls = (
        AABB(x=15.0, y=0.0, width=10.0, height=20.0),
        AABB(x=0.0, y=15.0, width=20.0, height=10.0),
    )

    actual = move_entity(
        entity,
        pygame.Vector2(10.0, 10.0),
        (wall for wall in walls),
    )

    assert entity.position == pygame.Vector2(5.0, 5.0)
    assert actual == pygame.Vector2(5.0, 5.0)


def test_movement_towards_moves_along_one_axis() -> None:
    movement = movement_towards(
        pygame.Vector2(2.0, 4.0),
        pygame.Vector2(12.0, 4.0),
        max_distance=3.0,
    )

    assert movement == pygame.Vector2(3.0, 0.0)


def test_movement_towards_normalizes_diagonal_movement() -> None:
    movement = movement_towards(
        pygame.Vector2(0.0, 0.0),
        pygame.Vector2(3.0, 4.0),
        max_distance=2.0,
    )

    assert movement.x == pytest.approx(1.2)
    assert movement.y == pytest.approx(1.6)
    assert movement.length() == pytest.approx(2.0)


def test_movement_towards_stops_at_target() -> None:
    movement = movement_towards(
        pygame.Vector2(0.0, 0.0),
        pygame.Vector2(3.0, 4.0),
        max_distance=10.0,
    )

    assert movement == pygame.Vector2(3.0, 4.0)


def test_movement_towards_returns_zero_at_target() -> None:
    movement = movement_towards(
        pygame.Vector2(3.0, 4.0),
        pygame.Vector2(3.0, 4.0),
        max_distance=2.0,
    )

    assert movement == pygame.Vector2()


def test_movement_towards_rejects_negative_max_distance() -> None:
    with pytest.raises(ValueError, match="max_distance must not be negative"):
        movement_towards(
            pygame.Vector2(),
            pygame.Vector2(10.0, 0.0),
            max_distance=-1.0,
        )


def test_movement_towards_does_not_mutate_inputs() -> None:
    position = pygame.Vector2(1.0, 2.0)
    target = pygame.Vector2(5.0, 8.0)

    movement_towards(position, target, max_distance=2.0)

    assert position == pygame.Vector2(1.0, 2.0)
    assert target == pygame.Vector2(5.0, 8.0)
