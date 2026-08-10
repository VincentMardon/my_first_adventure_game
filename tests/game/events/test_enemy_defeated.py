from dataclasses import FrozenInstanceError

import pytest

from my_first_adventure_game.game.events import EnemyDefeated


def test_enemy_defeated_stores_enemy_identifier() -> None:
    event = EnemyDefeated(enemy_id="enemy-1")

    assert event.enemy_id == "enemy-1"


def test_enemy_defeated_is_immutable() -> None:
    event = EnemyDefeated(enemy_id="enemy-1")

    with pytest.raises(FrozenInstanceError):
        event.enemy_id = "enemy-2"  # type: ignore[misc]
