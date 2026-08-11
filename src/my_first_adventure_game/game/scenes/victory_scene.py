from collections.abc import Callable

import pygame

from my_first_adventure_game.engine.assets import FontCache
from my_first_adventure_game.engine.graphics import draw_text
from my_first_adventure_game.engine.input import InputState
from my_first_adventure_game.engine.scenes import Scene
from my_first_adventure_game.game.input import GameAction
from my_first_adventure_game.game.scoring import SessionScore

BACKGROUND_COLOR = (24, 28, 36)
RETURN_CENTER_Y = 440
RETURN_COLOR = (184, 192, 208)
RETURN_TEXT = "Press Enter to return to title"
SCORE_CENTER_Y = 340
SCORE_COLOR = (240, 240, 240)
VICTORY_CENTER_Y = 240
VICTORY_COLOR = (112, 240, 160)
VICTORY_FONT_PATH = pygame.font.get_default_font()
VICTORY_FONT_SIZE = 64
VICTORY_TEXT = "Victory!"


class VictoryScene(Scene):
    """Display the final score after the game is completed."""

    def __init__(
        self,
        font_cache: FontCache,
        session_score: SessionScore,
        input_state: InputState[GameAction],
        return_to_title: Callable[[], None],
    ) -> None:
        self._font_cache = font_cache
        self._session_score = session_score
        self._input_state = input_state
        self._return_to_title = return_to_title

    def handle_event(self, event: pygame.event.Event) -> None:
        return None

    def update(self, delta_time: float) -> None:
        if self._input_state.is_pressed(GameAction.CONFIRM):
            self._return_to_title()

    def draw(self, surface: pygame.Surface) -> None:
        surface.fill(BACKGROUND_COLOR)
        font = self._font_cache.load(
            VICTORY_FONT_PATH,
            VICTORY_FONT_SIZE,
        )
        center_x = surface.get_width() // 2

        draw_text(
            surface,
            VICTORY_TEXT,
            font,
            VICTORY_COLOR,
            center=(center_x, VICTORY_CENTER_Y),
        )
        draw_text(
            surface,
            f"Score: {self._session_score.value}",
            font,
            SCORE_COLOR,
            center=(center_x, SCORE_CENTER_Y),
        )
        draw_text(
            surface,
            RETURN_TEXT,
            font,
            RETURN_COLOR,
            center=(center_x, RETURN_CENTER_Y),
        )
