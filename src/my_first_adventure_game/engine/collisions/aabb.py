from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class AABB:
    """Represent immutable axis-aligned bounds using floating-point values.

    Attributes:
        x: Horizontal position of the left edge.
        y: Vertical position of the top edge.
        width: Non-negative horizontal extent.
        height: Non-negative vertical extent.
    """

    x: float
    y: float
    width: float
    height: float

    def __post_init__(self) -> None:
        if self.width < 0 or self.height < 0:
            raise ValueError("AABB dimensions must be non-negative.")

    @property
    def left(self) -> float:
        """Return the horizontal position of the left edge."""
        return self.x

    @property
    def right(self) -> float:
        """Return the horizontal position of the right edge."""
        return self.x + self.width

    @property
    def top(self) -> float:
        """Return the vertical position of the top edge."""
        return self.y

    @property
    def bottom(self) -> float:
        """Return the vertical position of the bottom edge."""
        return self.y + self.height

    def overlaps(self, other: "AABB") -> bool:
        """Return whether both bounds share a positive area."""
        if self.width == 0 or self.height == 0 or other.width == 0 or other.height == 0:
            return False

        return (
            self.left < other.right
            and self.right > other.left
            and self.top < other.bottom
            and self.bottom > other.top
        )
