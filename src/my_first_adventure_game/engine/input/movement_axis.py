from collections.abc import Hashable
from typing import TypeVar

import pygame

from my_first_adventure_game.engine.input.input_state import InputState

ActionT = TypeVar("ActionT", bound=Hashable)


def movement_axis(
    input_state: InputState[ActionT],
    *,
    left: ActionT,
    right: ActionT,
    up: ActionT,
    down: ActionT,
) -> pygame.Vector2:
    """Return a normalized directional axis from held movement actions."""
    horizontal = int(input_state.is_held(right)) - int(input_state.is_held(left))
    vertical = int(input_state.is_held(down)) - int(input_state.is_held(up))

    axis = pygame.Vector2(horizontal, vertical)

    if axis.length_squared() > 1:
        return axis.normalize()

    return axis
