import pygame

from my_first_adventure_game.engine.collisions import AABB
from my_first_adventure_game.game.entities.wall_stain import WallStain


def caretaker_sidestep_target(
    stain: WallStain,
    caretaker_bounds: AABB,
    player_bounds: AABB,
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

    caretaker_position = pygame.Vector2(
        caretaker_bounds.x,
        caretaker_bounds.y,
    )

    return min(
        candidates,
        key=lambda candidate: (candidate - caretaker_position).length_squared(),
    )
