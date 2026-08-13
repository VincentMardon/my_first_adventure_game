from enum import Enum, auto


class GuideObjectiveState(Enum):
    """Represent the current state of the Guide's collection objective."""

    NOT_STARTED = auto()
    ACTIVE = auto()
    READY_TO_COMPLETE = auto()
    COMPLETED = auto()
