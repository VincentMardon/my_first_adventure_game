from importlib.resources import Anchor, files
from io import BytesIO

import pygame


class FontCache:
    """Load and cache fonts stored in a Python package."""

    def __init__(self, package: Anchor) -> None:
        self._package = package
        self._fonts: dict[tuple[str, int], pygame.font.Font] = {}
        self._font_files: dict[tuple[str, int], BytesIO] = {}

    def load(self, path: str, size: int) -> pygame.font.Font:
        """Return the font cached for a resource path and size."""
        key = (path, size)

        if key not in self._fonts:
            resource = files(self._package).joinpath(path)
            font_file = BytesIO(resource.read_bytes())
            font = pygame.font.Font(font_file, size)

            self._font_files[key] = font_file
            self._fonts[key] = font

        return self._fonts[key]
