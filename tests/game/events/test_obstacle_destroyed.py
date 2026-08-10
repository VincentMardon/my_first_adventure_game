from dataclasses import FrozenInstanceError

import pytest

from my_first_adventure_game.game.events import ObstacleDestroyed


def test_obstacle_destroyed_identifies_destroyed_obstacle() -> None:
    event = ObstacleDestroyed(obstacle_id="destructible-1")

    assert event.obstacle_id == "destructible-1"


def test_obstacle_destroyed_is_immutable() -> None:
    event = ObstacleDestroyed(obstacle_id="destructible-1")

    with pytest.raises(FrozenInstanceError):
        event.obstacle_id = "destructible-2"
