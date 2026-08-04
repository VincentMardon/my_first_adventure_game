import pygame

from my_first_adventure_game.engine.scenes import Scene

BACKGROUND_COLOR = (24, 28, 36)


class TitleScene(Scene):
    def handle_event(self, event: pygame.event.Event) -> None:
        return None

    def update(self, delta_time: float) -> None:
        return None

    def draw(self, surface: pygame.Surface) -> None:
        surface.fill(BACKGROUND_COLOR)
