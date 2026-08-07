class SessionScore:
    """Accumulate the score earned during the current game session.

    Attributes:
        value: Current accumulated score.
    """

    __slots__ = ("_value",)

    def __init__(self) -> None:
        self._value = 0

    @property
    def value(self) -> int:
        """Return the current accumulated score."""
        return self._value

    def add(self, points: int) -> None:
        """Add points to the current score."""
        self._value += points
