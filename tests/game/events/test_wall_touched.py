from dataclasses import FrozenInstanceError

import pytest

from my_first_adventure_game.game.events import WallTouched


def test_wall_touched_describes_contact() -> None:
    event = WallTouched(
        wall_id="clearing-wall-right",
        contact_position=(1184.0, 332.0),
        surface_normal=(-1.0, 0.0),
    )

    assert event.wall_id == "clearing-wall-right"
    assert event.contact_position == (1184.0, 332.0)
    assert event.surface_normal == (-1.0, 0.0)


def test_wall_touched_is_immutable() -> None:
    event = WallTouched(
        wall_id="clearing-wall-right",
        contact_position=(1184.0, 332.0),
        surface_normal=(-1.0, 0.0),
    )

    with pytest.raises(FrozenInstanceError):
        event.contact_position = (1184.0, 400.0)
