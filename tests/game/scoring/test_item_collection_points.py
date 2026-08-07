from my_first_adventure_game.game.events import ItemCollected
from my_first_adventure_game.game.scoring import item_collection_points


def test_item_collection_awards_one_hundred_points() -> None:
    event = ItemCollected(item_id="collectible-1")

    assert item_collection_points(event) == 100
