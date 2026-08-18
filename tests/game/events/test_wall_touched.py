from dataclasses import FrozenInstanceError

import pytest

from my_first_adventure_game.game.events import WallTouched


def test_wall_touched_identifies_touched_wall() -> None:
    event = WallTouched(wall_id="clearing-wall-top")

    assert event.wall_id == "clearing-wall-top"


def test_wall_touched_is_immutable() -> None:
    event = WallTouched(wall_id="clearing-wall-top")

    with pytest.raises(FrozenInstanceError):
        event.wall_id = "clearing-wall-bottom"
