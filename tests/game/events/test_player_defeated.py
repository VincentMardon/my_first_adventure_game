from dataclasses import FrozenInstanceError

import pytest

from my_first_adventure_game.game.events import PlayerDefeated


def test_player_defeated_stores_player_identifier() -> None:
    event = PlayerDefeated(player_id="player")

    assert event.player_id == "player"


def test_player_deteated_is_immutable() -> None:
    event = PlayerDefeated(player_id="player")

    with pytest.raises(FrozenInstanceError):
        event.player_id = "other-player"  # type: ignore[misc]
