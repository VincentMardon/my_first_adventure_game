from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class WindowConfig:
    """Store the immutable properties used to create the game window.

    Attributes:
        title: Caption displayed in the window title bar.
        size: Window width and height in pixels.
    """

    title: str
    size: tuple[int, int]
