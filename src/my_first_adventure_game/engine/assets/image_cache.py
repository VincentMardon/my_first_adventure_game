from importlib.resources import Anchor, files

import pygame


class ImageCache:
    """Load and cache images stored in a Python package."""

    def __init__(self, package: Anchor) -> None:
        self._package = package
        self._images: dict[str, pygame.Surface] = {}

    def load(self, path: str) -> pygame.Surface:
        """Return the cached image or load it from the resource package."""
        if path not in self._images:
            resource = files(self._package).joinpath(path)

            with resource.open("rb") as image_file:
                self._images[path] = pygame.image.load(image_file, path)

        return self._images[path]
