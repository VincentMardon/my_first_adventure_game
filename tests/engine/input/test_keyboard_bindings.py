from enum import Enum, auto

from my_first_adventure_game.engine.input import KeyboardBindings


class ExampleAction(Enum):
    MOVE_LEFT = auto()
    INTERACT = auto()


def test_keys_for_returns_keys_bound_to_action() -> None:
    bindings = KeyboardBindings(
        {
            ExampleAction.MOVE_LEFT: (10, 20),
            ExampleAction.INTERACT: (30,),
        }
    )

    assert bindings.keys_for(ExampleAction.MOVE_LEFT) == frozenset({10, 20})
    assert bindings.keys_for(ExampleAction.INTERACT) == frozenset({30})


def test_actions_for_returns_actions_bound_to_key() -> None:
    bindings = KeyboardBindings(
        {
            ExampleAction.MOVE_LEFT: (10,),
            ExampleAction.INTERACT: (10, 30),
        }
    )

    assert bindings.actions_for(10) == frozenset(
        {
            ExampleAction.MOVE_LEFT,
            ExampleAction.INTERACT,
        }
    )


def test_unknown_action_and_key_have_no_bindings() -> None:
    bindings = KeyboardBindings(
        {
            ExampleAction.MOVE_LEFT: (10,),
        }
    )

    assert bindings.keys_for(ExampleAction.INTERACT) == frozenset()
    assert bindings.actions_for(99) == frozenset()
