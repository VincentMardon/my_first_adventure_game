from collections.abc import Hashable
from typing import Generic, TypeVar

import pygame

from my_first_adventure_game.engine.input.keyboard_bindings import KeyboardBindings

ActionT = TypeVar("ActionT", bound=Hashable)


class InputState(Generic[ActionT]):
    def __init__(self, bindings: KeyboardBindings[ActionT]) -> None:
        self._bindings = bindings
        self._held_keys: set[int] = set()
        self._pressed_actions: set[ActionT] = set()
        self._released_actions: set[ActionT] = set()

    def start_frame(self) -> None:
        self._pressed_actions.clear()
        self._released_actions.clear()

    def handle_event(self, event: pygame.event.Event) -> None:
        if event.type == pygame.KEYDOWN:
            self._handle_key_down(event.key)
        elif event.type == pygame.KEYUP:
            self._handle_key_up(event.key)

    def is_pressed(self, action: ActionT) -> bool:
        return action in self._pressed_actions

    def is_held(self, action: ActionT) -> bool:
        keys = self._bindings.keys_for(action)
        return not keys.isdisjoint(self._held_keys)

    def is_released(self, action: ActionT) -> bool:
        return action in self._released_actions

    def _handle_key_down(self, key: int) -> None:
        actions = self._bindings.actions_for(key)
        previously_held = {action for action in actions if self.is_held(action)}

        self._held_keys.add(key)
        self._pressed_actions.update(actions - previously_held)

    def _handle_key_up(self, key: int) -> None:
        actions = self._bindings.actions_for(key)
        previously_held = {action for action in actions if self.is_held(action)}

        self._held_keys.discard(key)

        self._released_actions.update(
            action for action in previously_held if not self.is_held(action)
        )
