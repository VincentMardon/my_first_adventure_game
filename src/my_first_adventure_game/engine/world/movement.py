from collections.abc import Iterable

import pygame

from my_first_adventure_game.engine.collisions import AABB
from my_first_adventure_game.engine.world.entity import Entity


def move_entity(
    entity: Entity,
    movement: pygame.Vector2,
    solid_bounds: Iterable[AABB],
) -> pygame.Vector2:
    """Move an entity axis by axis and return the applied movement."""
    obstacles = tuple(solid_bounds)

    horizontal = _resolve_horizontal(
        entity.bounds,
        movement.x,
        obstacles,
    )
    entity.position.x += horizontal

    vertical = _resolve_vertical(
        entity.bounds,
        movement.y,
        obstacles,
    )
    entity.position.y += vertical

    return pygame.Vector2(horizontal, vertical)


def _resolve_horizontal(
    bounds: AABB,
    movement: float,
    obstacles: tuple[AABB, ...],
) -> float:
    resolved = movement

    for obstacle in obstacles:
        if not _ranges_overlap(
            bounds.top,
            bounds.bottom,
            obstacle.top,
            obstacle.bottom,
        ):
            continue

        if movement > 0 and bounds.right <= obstacle.left:
            resolved = min(resolved, obstacle.left - bounds.right)
        elif movement < 0 and bounds.left >= obstacle.right:
            resolved = max(resolved, obstacle.right - bounds.left)

    return resolved


def _resolve_vertical(
    bounds: AABB,
    movement: float,
    obstacles: tuple[AABB, ...],
) -> float:
    resolved = movement
    for obstacle in obstacles:
        if not _ranges_overlap(
            bounds.left,
            bounds.right,
            obstacle.left,
            obstacle.right,
        ):
            continue

        if movement > 0 and bounds.bottom <= obstacle.top:
            resolved = min(resolved, obstacle.top - bounds.bottom)
        elif movement < 0 and bounds.top >= obstacle.bottom:
            resolved = max(resolved, obstacle.bottom - bounds.top)

    return resolved


def _ranges_overlap(
    first_start: float,
    first_end: float,
    second_start: float,
    second_end: float,
) -> bool:
    return first_start < second_end and first_end > second_start
