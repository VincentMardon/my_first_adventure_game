class SessionStatistics:
    """Track factual counters for the current game session.

    Attributes:
        items_collected: Number of items collected during the session.
        obstacles_destroyed: Number of obstacles destroyed during the session.
        enemies_defeated: Number of enemies defeated during the session.
    """

    __slots__ = (
        "_enemies_defeated",
        "_items_collected",
        "_obstacles_destroyed",
    )

    def __init__(self) -> None:
        self._items_collected = 0
        self._obstacles_destroyed = 0
        self._enemies_defeated = 0

    @property
    def items_collected(self) -> int:
        """Return the number of collected items."""
        return self._items_collected

    @property
    def obstacles_destroyed(self) -> int:
        """Return the number of destroyed obstacles."""
        return self._obstacles_destroyed

    @property
    def enemies_defeated(self) -> int:
        """Return the number of defeated enemies."""
        return self._enemies_defeated

    def record_item_collected(self) -> None:
        """Record one collected item."""
        self._items_collected += 1

    def record_obstacle_destroyed(self) -> None:
        """Record one destroyed obstacle."""
        self._obstacles_destroyed += 1

    def record_enemy_defeated(self) -> None:
        """Record one defeated enemy."""
        self._enemies_defeated += 1
