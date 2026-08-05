from typing import Protocol

import pygame


class InputProcessor(Protocol):
    """Define the input lifecycle required by the application."""

    def start_frame(self) -> None:
        """Begin a new frame and clear transient input states."""
        ...

    def handle_event(self, event: pygame.event.Event) -> None:
        """Process an event forwarded by the application."""
        ...
