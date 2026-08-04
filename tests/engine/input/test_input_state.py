from enum import Enum, auto

import pygame

from my_first_adventure_game.engine.input import InputState, KeyboardBindings


class ExampleAction(Enum):
    MOVE_LEFT = auto()
    INTERACT = auto()


def test_action_state_follows_key_transitions() -> None:
    state = InputState(
        KeyboardBindings(
            {
                ExampleAction.INTERACT: (10,),
            }
        )
    )

    state.start_frame()
    state.handle_event(pygame.event.Event(pygame.KEYDOWN, key=10))

    assert state.is_pressed(ExampleAction.INTERACT)
    assert state.is_held(ExampleAction.INTERACT)
    assert not state.is_released(ExampleAction.INTERACT)

    state.start_frame()

    assert not state.is_pressed(ExampleAction.INTERACT)
    assert state.is_held(ExampleAction.INTERACT)
    assert not state.is_released(ExampleAction.INTERACT)

    state.handle_event(pygame.event.Event(pygame.KEYUP, key=10))

    assert not state.is_pressed(ExampleAction.INTERACT)
    assert not state.is_held(ExampleAction.INTERACT)
    assert state.is_released(ExampleAction.INTERACT)

    state.start_frame()

    assert not state.is_pressed(ExampleAction.INTERACT)
    assert not state.is_held(ExampleAction.INTERACT)
    assert not state.is_released(ExampleAction.INTERACT)


def test_action_remains_held_until_every_bound_key_is_released() -> None:
    state = InputState(
        KeyboardBindings(
            {
                ExampleAction.MOVE_LEFT: (10, 20),
            }
        )
    )

    state.start_frame()
    state.handle_event(pygame.event.Event(pygame.KEYDOWN, key=10))
    state.start_frame()
    state.handle_event(pygame.event.Event(pygame.KEYDOWN, key=20))

    assert state.is_held(ExampleAction.MOVE_LEFT)
    assert not state.is_pressed(ExampleAction.MOVE_LEFT)

    state.handle_event(pygame.event.Event(pygame.KEYUP, key=10))

    assert state.is_held(ExampleAction.MOVE_LEFT)
    assert not state.is_released(ExampleAction.MOVE_LEFT)

    state.handle_event(pygame.event.Event(pygame.KEYUP, key=20))

    assert not state.is_held(ExampleAction.MOVE_LEFT)
    assert state.is_released(ExampleAction.MOVE_LEFT)


def test_repeated_key_down_does_not_press_action_again() -> None:
    state = InputState(
        KeyboardBindings(
            {
                ExampleAction.INTERACT: (10,),
            }
        )
    )

    state.start_frame()
    state.handle_event(pygame.event.Event(pygame.KEYDOWN, key=10))
    state.start_frame()
    state.handle_event(pygame.event.Event(pygame.KEYDOWN, key=10))

    assert not state.is_pressed(ExampleAction.INTERACT)
    assert state.is_held(ExampleAction.INTERACT)
