from importlib.resources import Anchor, files

import pygame


class FontCache:
    """Load and cache fonts stored in a Python package."""

    def __init__(self, package: Anchor) -> None:
        self._package = package
        self._fonts: dict[tuple[str, int], pygame.font.Font] = {}

    def load(self, path: str, size: int) -> pygame.font.Font:
        """Return the font cached for a resource path and size."""
        key = (path, size)

        if key not in self._fonts:
            resource = files(self._package).joinpath(path)

            with resource.open("rb") as font_file:
                self._fonts[key] = pygame.font.Font(font_file, size)

        return self._fonts[key]
