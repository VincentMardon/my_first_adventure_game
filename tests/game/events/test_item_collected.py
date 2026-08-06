from dataclasses import FrozenInstanceError

import pytest

from my_first_adventure_game.game.events import ItemCollected


def test_item_collected_identifies_collected_item() -> None:
    event = ItemCollected(item_id="collectible-1")

    assert event.item_id == "collectible-1"


def test_item_collected_is_immutable() -> None:
    event = ItemCollected(item_id="collectible-1")

    with pytest.raises(FrozenInstanceError):
        event.item_id = "collectible-2"
