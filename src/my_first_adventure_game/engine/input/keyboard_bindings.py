from collections.abc import Hashable, Iterable, Mapping
from typing import Generic, TypeVar

ActionT = TypeVar("ActionT", bound=Hashable)


class KeyboardBindings(Generic[ActionT]):
    """Provide immutable many-to-many mappings between actions and keys."""

    def __init__(self, bindings: Mapping[ActionT, Iterable[int]]) -> None:
        self._keys_by_action = {
            action: frozenset(keys) for action, keys in bindings.items()
        }

        actions_by_key: dict[int, set[ActionT]] = {}

        for action, keys in self._keys_by_action.items():
            for key in keys:
                actions_by_key.setdefault(key, set()).add(action)

        self._actions_by_key = {
            key: frozenset(actions) for key, actions in actions_by_key.items()
        }

    def keys_for(self, action: ActionT) -> frozenset[int]:
        """Return the keys bound to an action."""
        return self._keys_by_action.get(action, frozenset())

    def actions_for(self, key: int) -> frozenset[ActionT]:
        """Return the actions bound to a key."""
        return self._actions_by_key.get(key, frozenset())
