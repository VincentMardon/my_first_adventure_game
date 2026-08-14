from my_first_adventure_game.game.progression.guide_objective_state import (
    GuideObjectiveState,
)

_OBJECTIVE_STATUS_TEXT = {
    GuideObjectiveState.NOT_STARTED: "Objective: Talk to the Guide",
    GuideObjectiveState.ACTIVE: "Objective: Collect every item",
    GuideObjectiveState.READY_TO_COMPLETE: "Objective: Return to the Guide",
    GuideObjectiveState.COMPLETED: "Objective: Complete",
}


class GuideObjective:
    """Track the state of the Guide's collection objective.

    Attributes:
        state: Current objective state.
        status_text: Text describing the current objective state.
    """

    __slots__ = ("_state",)

    def __init__(self) -> None:
        self._state = GuideObjectiveState.NOT_STARTED

    @property
    def state(self) -> GuideObjectiveState:
        """Return the current objective state."""
        return self._state

    @property
    def status_text(self) -> str:
        """Return text describing the current objective state."""
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
