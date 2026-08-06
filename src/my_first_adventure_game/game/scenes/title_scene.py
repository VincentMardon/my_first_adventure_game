from collections.abc import Callable

import pygame

from my_first_adventure_game.engine.assets import FontCache
from my_first_adventure_game.engine.graphics import draw_text
from my_first_adventure_game.engine.input import InputState
from my_first_adventure_game.engine.scenes import Scene
from my_first_adventure_game.game.input import GameAction

BACKGROUND_COLOR = (24, 28, 36)
TITLE_TEXT = "My First Adventure Game"
TITLE_COLOR = (240, 240, 240)
TITLE_CENTER_Y = 160
TITLE_FONT_PATH = pygame.font.get_default_font()
TITLE_FONT_SIZE = 64


class TitleScene(Scene):
    """Display the initial title screen."""

    def __init__(
        self,
        font_cache: FontCache,
        input_state: InputState[GameAction],
        start_game: Callable[[], None],
    ) -> None:
        self._font_cache = font_cache
        self._input_state = input_state
        self._start_game = start_game

    def handle_event(self, event: pygame.event.Event) -> None:
        return None

    def update(self, delta_time: float) -> None:
        if self._input_state.is_pressed(GameAction.CONFIRM):
            self._start_game()

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
