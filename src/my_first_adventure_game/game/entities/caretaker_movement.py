from enum import Enum, auto

import pygame

from my_first_adventure_game.engine.collisions import AABB
from my_first_adventure_game.game.entities.wall_stain import WallStain


class CaretakerSide(Enum):
    """Identify one of the two directions parallel to a stained wall."""

    NEGATIVE = auto()
    POSITIVE = auto()


def caretaker_nearest_side(
    stain: WallStain,
    caretaker_bounds: AABB,
    player_bounds: AABB,
) -> CaretakerSide:
    """Return the side of the player nearest to the Caretaker."""
    if stain.surface_normal[0] == 0.0:
        caretaker_center = caretaker_bounds.x + caretaker_bounds.width / 2.0
        player_center = player_bounds.x + player_bounds.width / 2.0
    else:
        caretaker_center = caretaker_bounds.y + caretaker_bounds.height / 2.0
        player_center = player_bounds.y + player_bounds.height / 2.0

    if caretaker_center <= player_center:
        return CaretakerSide.NEGATIVE

    return CaretakerSide.POSITIVE


def caretaker_push_movement(
    stain: WallStain,
    caretaker_bounds: AABB,
    player_bounds: AABB,
) -> pygame.Vector2:
    """Return one player-sized push along the wall away from the Caretaker."""
    if stain.surface_normal[0] == 0.0:
        caretaker_center = caretaker_bounds.x + caretaker_bounds.width / 2.0
        player_center = player_bounds.x + player_bounds.width / 2.0
        direction = 1.0 if caretaker_center < player_center else -1.0

        return pygame.Vector2(
            player_bounds.width * direction,
            0.0,
        )

    caretaker_center = caretaker_bounds.y + caretaker_bounds.height / 2.0
    player_center = player_bounds.y + player_bounds.height / 2.0
    direction = 1.0 if caretaker_center < player_center else -1.0

    return pygame.Vector2(
        0.0,
        player_bounds.height * direction,
    )


def caretaker_rounding_target(
    stain: WallStain,
    caretaker_bounds: AABB,
    player_bounds: AABB,
    *,
    side: CaretakerSide | None = None,
) -> pygame.Vector2:
    """Return the nearest outer corner used to move around the player."""
    target = caretaker_sidestep_target(
        stain,
        caretaker_bounds,
        player_bounds,
        side=side,
    )

    if stain.surface_normal[0] == 0.0:
        target.y = (
            player_bounds.bottom
            if stain.surface_normal[1] > 0.0
            else player_bounds.top - caretaker_bounds.height
        )
    else:
        target.x = (
            player_bounds.right
            if stain.surface_normal[0] > 0.0
            else player_bounds.left - caretaker_bounds.width
        )

    return target


def caretaker_sidestep_target(
    stain: WallStain,
    caretaker_bounds: AABB,
    player_bounds: AABB,
    *,
    side: CaretakerSide | None = None,
) -> pygame.Vector2:
    """Return the closest position beside the player along the stained wall."""
    approach_position = stain.approach_position(
        pygame.Vector2(
            caretaker_bounds.width,
            caretaker_bounds.height,
        )
    )

    if stain.surface_normal[0] == 0.0:
        candidates = (
            pygame.Vector2(
                player_bounds.left - caretaker_bounds.width,
                approach_position.y,
            ),
            pygame.Vector2(
                player_bounds.right,
                approach_position.y,
            ),
        )
    else:
        candidates = (
            pygame.Vector2(
                approach_position.x,
                player_bounds.top - caretaker_bounds.height,
            ),
            pygame.Vector2(
                approach_position.x,
                player_bounds.bottom,
            ),
        )

    if side is CaretakerSide.NEGATIVE:
        return candidates[0]

    if side is CaretakerSide.POSITIVE:
        return candidates[1]

    caretaker_position = pygame.Vector2(
        caretaker_bounds.x,
        caretaker_bounds.y,
    )

    return min(
        candidates,
        key=lambda candidate: (candidate - caretaker_position).length_squared(),
    )
