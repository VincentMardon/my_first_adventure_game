import pygame

from my_first_adventure_game.engine.assets import FontCache
from my_first_adventure_game.engine.graphics import draw_text
from my_first_adventure_game.engine.scenes import Scene

BACKGROUND_COLOR = (24, 28, 36)
TITLE_TEXT = "My First Adventure Game"
TITLE_COLOR = (240, 240, 240)
TITLE_CENTER_Y = 160
TITLE_FONT_PATH = pygame.font.get_default_font()
TITLE_FONT_SIZE = 64


class TitleScene(Scene):
    """Display the initial title screen."""

    def __init__(self, font_cache: FontCache) -> None:
        self._font_cache = font_cache

    def handle_event(self, event: pygame.event.Event) -> None:
        return None

    def update(self, delta_time: float) -> None:
        return None

    def draw(self, surface: pygame.Surface) -> None:
        surface.fill(BACKGROUND_COLOR)
        title_font = self._font_cache.load(
            TITLE_FONT_PATH,
            TITLE_FONT_SIZE,
        )
        draw_text(
            surface,
            TITLE_TEXT,
            title_font,
            TITLE_COLOR,
            center=(surface.get_width() // 2, TITLE_CENTER_Y),
        )
