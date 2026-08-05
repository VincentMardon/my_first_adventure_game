import pygame

from my_first_adventure_game.engine.scenes.scene import Scene


class SceneManager:
    """Own the active scene and delegate runtime operations to it."""

    def __init__(self, initial_scene: Scene) -> None:
        self._current_scene = initial_scene

    @property
    def current_scene(self) -> Scene:
        """Return the active scene."""
        return self._current_scene

    def change_scene(self, scene: Scene) -> None:
        """Replace the active scene immediately."""
        self._current_scene = scene

    def handle_event(self, event: pygame.event.Event) -> None:
        """Forward an event to the active scene."""
        self._current_scene.handle_event(event)

    def update(self, delta_time: float) -> None:
        """Update the active scene using elapsed time in seconds."""
        self._current_scene.update(delta_time)

    def draw(self, surface: pygame.Surface) -> None:
        """Draw the active scene onto the target surface."""
        self._current_scene.draw(surface)
