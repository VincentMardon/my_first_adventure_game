from collections.abc import Callable

import pygame

from my_first_adventure_game.engine.assets import FontCache
from my_first_adventure_game.engine.graphics import draw_text
from my_first_adventure_game.engine.input import InputState
from my_first_adventure_game.engine.scenes import Scene
from my_first_adventure_game.game.input import GameAction
from my_first_adventure_game.game.scoring import SessionScore
from my_first_adventure_game.game.statistics import SessionStatistics

BACKGROUND_COLOR = (24, 28, 36)
DEFEAT_TEXT = "Game Over"
DEFEAT_COLOR = (248, 112, 112)
DEFEAT_CENTER_Y = 160
DEFEAT_FONT_PATH = pygame.font.get_default_font()
DEFEAT_FONT_SIZE = 64
ENEMIES_DEFEATED_CENTER_Y = 450
ITEMS_COLLECTED_CENTER_Y = 330
OBSTACLES_DESTROYED_CENTER_Y = 390
RETURN_CENTER_Y = 550
RETURN_COLOR = (184, 192, 208)
RETURN_TEXT = "Press Enter to return to title"
SCORE_COLOR = (240, 240, 240)
SCORE_CENTER_Y = 250


class DefeatScene(Scene):
    """Display the final score after the player is defeated."""

    def __init__(
        self,
        font_cache: FontCache,
        session_score: SessionScore,
        session_statistics: SessionStatistics,
        input_state: InputState[GameAction],
        return_to_title: Callable[[], None],
    ) -> None:
        self._font_cache = font_cache
        self._session_score = session_score
        self._session_statistics = session_statistics
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
            DEFEAT_FONT_PATH,
            DEFEAT_FONT_SIZE,
        )
        center_x = surface.get_width() // 2

        draw_text(
            surface,
            DEFEAT_TEXT,
            font,
            DEFEAT_COLOR,
            center=(center_x, DEFEAT_CENTER_Y),
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
            f"Items collected: {self._session_statistics.items_collected}",
            font,
            SCORE_COLOR,
            center=(center_x, ITEMS_COLLECTED_CENTER_Y),
        )
        draw_text(
            surface,
            f"Obstacles destroyed: {self._session_statistics.obstacles_destroyed}",
            font,
            SCORE_COLOR,
            center=(center_x, OBSTACLES_DESTROYED_CENTER_Y),
        )
        draw_text(
            surface,
            f"Enemies defeated: {self._session_statistics.enemies_defeated}",
            font,
            SCORE_COLOR,
            center=(center_x, ENEMIES_DEFEATED_CENTER_Y),
        )
        draw_text(
            surface,
            RETURN_TEXT,
            font,
            RETURN_COLOR,
            center=(center_x, RETURN_CENTER_Y),
        )
