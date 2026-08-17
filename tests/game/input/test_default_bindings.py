import pygame
import pytest

from my_first_adventure_game.game.input import (
    DEFAULT_KEYBOARD_BINDINGS,
    GameAction,
)


@pytest.mark.parametrize(
    ("action", "key"),
    [
        (GameAction.MOVE_LEFT, pygame.K_LEFT),
        (GameAction.MOVE_RIGHT, pygame.K_RIGHT),
        (GameAction.MOVE_UP, pygame.K_UP),
        (GameAction.MOVE_DOWN, pygame.K_DOWN),
        (GameAction.CONFIRM, pygame.K_RETURN),
        (GameAction.ATTACK, pygame.K_SPACE),
        (GameAction.PAUSE, pygame.K_ESCAPE),
        (GameAction.INTERACT, pygame.K_e),
        (GameAction.SHOW_PROFILE, pygame.K_p),
    ],
)
def test_action_has_default_key(
    action: GameAction,
    key: int,
) -> None:
    assert DEFAULT_KEYBOARD_BINDINGS.keys_for(action) == frozenset({key})
