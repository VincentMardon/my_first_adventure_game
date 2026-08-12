from collections.abc import Callable

import pygame

from my_first_adventure_game.engine.assets import FontCache
from my_first_adventure_game.engine.graphics import draw_text
from my_first_adventure_game.engine.input import InputState
from my_first_adventure_game.engine.scenes import Scene
from my_first_adventure_game.game.input import GameAction

BACKGROUND_COLOR = (24, 28, 36)
PAUSE_CENTER_Y = 260
PAUSE_COLOR = (240, 240, 240)
PAUSE_TEXT = "Paused"
PAUSE_FONT_PATH = pygame.font.get_default_font()
PAUSE_FONT_SIZE = 64
RESUME_CENTER_Y = 380
RESUME_COLOR = (184, 192, 208)
RESUME_TEXT = "Press Escape to resume"


class PauseScene(Scene):
    """Pause gameplay until the player requests to resume."""

    def __init__(
        self,
        font_cache: FontCache,
        input_state: InputState[GameAction],
        resume_game: Callable[[], None],
    ) -> None:
        self._font_cache = font_cache
        self._input_state = input_state
        self._resume_game = resume_game

    def handle_event(self, event: pygame.event.Event) -> None:
        return None

    def update(self, delta_time: float) -> None:
        if self._input_state.is_pressed(GameAction.PAUSE):
            self._resume_game()

    def draw(self, surface: pygame.Surface) -> None:
        surface.fill(BACKGROUND_COLOR)
        font = self._font_cache.load(
            PAUSE_FONT_PATH,
            PAUSE_FONT_SIZE,
        )
        center_x = surface.get_width() // 2

        draw_text(
            surface,
            PAUSE_TEXT,
            font,
            PAUSE_COLOR,
            center=(center_x, PAUSE_CENTER_Y),
        )
        draw_text(
            surface,
            RESUME_TEXT,
            font,
            RESUME_COLOR,
            center=(center_x, RESUME_CENTER_Y),
        )
