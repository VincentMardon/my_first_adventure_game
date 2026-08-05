from abc import ABC, abstractmethod

import pygame


class Scene(ABC):
    """Define a global application state managed by the scene system."""

    @abstractmethod
    def handle_event(self, event: pygame.event.Event) -> None:
        """Handle an event forwarded by the application."""
        pass

    @abstractmethod
    def update(self, delta_time: float) -> None:
        """Update the scene using elapsed time expressed in seconds."""
        pass

    @abstractmethod
    def draw(self, surface: pygame.Surface) -> None:
        """Draw the scene onto the target surface."""
        pass
