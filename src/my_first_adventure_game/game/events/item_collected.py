from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class ItemCollected:
    """Report that the player collected an item.

    Attributes:
        item_id: Stable identifier of the collected item.
    """

    item_id: str
