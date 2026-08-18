from dataclasses import FrozenInstanceError

import pytest

from my_first_adventure_game.game.events import NPCTargetReached


def test_npc_target_reached_identifies_npc_and_target() -> None:
    event = NPCTargetReached(
        npc_id="npc-clearing-caretaker",
        target_id="player",
    )

    assert event.npc_id == "npc-clearing-caretaker"
    assert event.target_id == "player"


def test_npc_target_reached_is_immutable() -> None:
    event = NPCTargetReached(npc_id="npc-clearing-caretaker", target_id="player")

    with pytest.raises(FrozenInstanceError):
        event.target_id = "another-target"
