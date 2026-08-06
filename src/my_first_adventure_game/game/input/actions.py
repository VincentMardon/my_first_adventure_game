from enum import Enum, auto


class GameAction(Enum):
    """Identify the concrete actions understood by the game.

    Attributes:
        MOVE_LEFT: Request movement along the negative horizontal screen axis.
        MOVE_RIGHT: Request movement along the positive horizontal screen axis.
        MOVE_UP: Request movement along the negative vertical screen axis.
        MOVE_DOWN: Request movement along the positive vertical screen axis.
        CONFIRM: Confirm the current selection or requested transition.
    """

    MOVE_LEFT = auto()
    MOVE_RIGHT = auto()
    MOVE_UP = auto()
    MOVE_DOWN = auto()
    CONFIRM = auto()
