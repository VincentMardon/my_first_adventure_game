from collections.abc import Iterable

import pygame

from my_first_adventure_game.engine.collisions import AABB
from my_first_adventure_game.engine.world import move_entity, movement_towards
from my_first_adventure_game.game.entities.npc import NPC


def move_npc_towards(
    npc: NPC,
    target: pygame.Vector2,
    *,
    speed: float,
    delta_time: float,
    solid_bounds: Iterable[AABB],
) -> pygame.Vector2:
    """Move an NPC toward a target and return the applied movement."""
    requested_movement = movement_towards(
        npc.entity.position,
        target,
        max_distance=speed * delta_time,
    )
    return move_entity(
        npc.entity,
        requested_movement,
        solid_bounds,
    )
