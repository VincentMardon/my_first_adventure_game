from enum import Enum, auto

import pygame
import pytest

from my_first_adventure_game.engine.input import (
    InputState,
    KeyboardBindings,
    movement_axis,
)


class ExampleAction(Enum):
    MOVE_LEFT = auto()
    MOVE_RIGHT = auto()
    MOVE_UP = auto()
    MOVE_DOWN = auto()


KEYS = {
    ExampleAction.MOVE_LEFT: (10,),
    ExampleAction.MOVE_RIGHT: (20,),
    ExampleAction.MOVE_UP: (30,),
    ExampleAction.MOVE_DOWN: (40,),
}


def create_input_state() -> InputState[ExampleAction]:
    return InputState(KeyboardBindings(KEYS))


def get_axis(input_state: InputState[ExampleAction]) -> pygame.Vector2:
    return movement_axis(
        input_state,
        left=ExampleAction.MOVE_LEFT,
        right=ExampleAction.MOVE_RIGHT,
        up=ExampleAction.MOVE_UP,
        down=ExampleAction.MOVE_DOWN,
    )


def hold_key(input_state: InputState[ExampleAction], key: int) -> None:
    input_state.handle_event(
        pygame.event.Event(
            pygame.KEYDOWN,
            key=key,
        )
    )


def test_axis_is_zero_without_directional_input() -> None:
    input_state = create_input_state()

    assert get_axis(input_state) == pygame.Vector2(0, 0)


@pytest.mark.parametrize(
    ("key", "expected"),
    [
        (10, pygame.Vector2(-1, 0)),
        (20, pygame.Vector2(1, 0)),
        (30, pygame.Vector2(0, -1)),
        (40, pygame.Vector2(0, 1)),
    ],
)
def test_axis_uses_screen_coordinate_directions(
    key: int,
    expected: pygame.Vector2,
) -> None:
    input_state = create_input_state()
    hold_key(input_state, key)

    assert get_axis(input_state) == expected


def test_opposite_directions_cancel_each_other() -> None:
    input_state = create_input_state()
    hold_key(input_state, 10)
    hold_key(input_state, 20)
    hold_key(input_state, 30)
    hold_key(input_state, 40)

    assert get_axis(input_state) == pygame.Vector2(0, 0)


def test_diagonal_axis_is_normalized() -> None:
    input_state = create_input_state()
    hold_key(input_state, 20)
    hold_key(input_state, 30)

    axis = get_axis(input_state)

    assert axis.x == pytest.approx(2**-0.5)
    assert axis.y == pytest.approx(-(2**-0.5))
    assert axis.length() == pytest.approx(1)
