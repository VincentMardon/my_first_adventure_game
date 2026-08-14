from my_first_adventure_game.game.progression.guide_objective_state import (
    GuideObjectiveState,
)

_OBJECTIVE_STATUS_TEXT = {
    GuideObjectiveState.NOT_STARTED: "Objective: Talk to the Guide",
    GuideObjectiveState.READY_TO_COMPLETE: "Objective: Return to the Guide",
    GuideObjectiveState.COMPLETED: "Objective: Complete",
}


class GuideObjective:
    """Track the state of the Guide's collection objective.

    Attributes:
        state: Current objective state.
        status_text: Text describing the current objective state.
        total_items: Number of items required by the objective.
        collected_items: Number of items collected for the objective.
    """

    __slots__ = (
        "_state",
        "_total_items",
        "_collected_items",
    )

    def __init__(self, total_items: int) -> None:
        self._state = GuideObjectiveState.NOT_STARTED
        self._total_items = total_items
        self._collected_items = 0

    @property
    def state(self) -> GuideObjectiveState:
        """Return the current objective state."""
        return self._state

    @property
    def total_items(self) -> int:
        """Return the number of items required by the objective."""
        return self._total_items

    @property
    def collected_items(self) -> int:
        """Return the number of collected objective items."""
        return self._collected_items

    @property
    def status_text(self) -> str:
        """Return text describing the current objective state."""
        if self._state is GuideObjectiveState.ACTIVE:
            return (
                "Objective: Collect items "
                f"({self._collected_items}/{self._total_items})"
            )
        return _OBJECTIVE_STATUS_TEXT[self._state]

    def start(self) -> None:
        """Start the collection objective."""
        self._state = GuideObjectiveState.ACTIVE

    def mark_ready_to_complete(self) -> None:
        """Mark the collection objective as ready for completion."""
        self._state = GuideObjectiveState.READY_TO_COMPLETE

    def complete(self) -> None:
        """Complete the collection objective."""
        self._state = GuideObjectiveState.COMPLETED

    def record_item_collected(self) -> None:
        """Record one collected objective item."""
        self._collected_items += 1

        if self._collected_items == self._total_items:
            self.mark_ready_to_complete()
