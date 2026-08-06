from enum import Enum, auto


class GameAction(Enum):
    """Identify the concrete actions understood by the game."""

    MOVE_LEFT = auto()
    MOVE_RIGHT = auto()
    MOVE_UP = auto()
    MOVE_DOWN = auto()
    CONFIRM = auto()
