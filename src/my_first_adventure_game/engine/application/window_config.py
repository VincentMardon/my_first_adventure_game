from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class WindowConfig:
    title: str
    size: tuple[int, int]
