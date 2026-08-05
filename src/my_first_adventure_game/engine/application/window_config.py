from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class WindowConfig:
    """Store the immutable properties used to create the game window."""

    title: str
    size: tuple[int, int]
