from my_first_adventure_game.game.events import ItemCollected


def item_collection_points(event: ItemCollected) -> int:
    """Return the points awarded for an item collection.

    Args:
        event: Item collection fact being scored.
    """

    return 100
