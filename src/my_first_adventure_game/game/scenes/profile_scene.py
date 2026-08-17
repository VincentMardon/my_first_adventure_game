from collections.abc import Callable

import pygame

from my_first_adventure_game.engine.assets import FontCache
from my_first_adventure_game.engine.graphics import draw_text
from my_first_adventure_game.engine.input import InputState
from my_first_adventure_game.engine.scenes import Scene
from my_first_adventure_game.game.input import GameAction
from my_first_adventure_game.game.profile import PlayerProfile

BACKGROUND_COLOR = (24, 28, 36)
PROFILE_COLOR = (240, 240, 240)
PROFILE_FONT_PATH = pygame.font.get_default_font()
PROFILE_FONT_SIZE = 40
PROFILE_LINE_GAP = 52
PROFILE_START_Y = 140
PROFILE_TITLE_CENTER_Y = 70
PROFILE_TITLE_TEXT = "Player profile"
RETURN_CENTER_Y = 620
RETURN_COLOR = (184, 192, 208)
RETURN_TEXT = "Press Enter to return to title"


class ProfileScene(Scene):
    """Display statistics accumulated in the player profile."""

    def __init__(
        self,
        font_cache: FontCache,
        player_profile: PlayerProfile,
        input_state: InputState[GameAction],
        return_to_title: Callable[[], None],
    ) -> None:
        self._font_cache = font_cache
        self._player_profile = player_profile
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
            PROFILE_FONT_PATH,
            PROFILE_FONT_SIZE,
        )
        center_x = surface.get_width() // 2
        profile_lines = (
            f"Games started: {self._player_profile.games_started}",
            f"Games finished: {self._player_profile.games_finished}",
            f"Victories: {self._player_profile.victories}",
            f"Best score: {self._player_profile.best_score}",
            f"Total score: {self._player_profile.total_score}",
            f"Items collected: {self._player_profile.items_collected}",
            f"Obstacles destroyed: {self._player_profile.obstacles_destroyed}",
            f"Enemies defeated: {self._player_profile.enemies_defeated}",
        )

        draw_text(
            surface,
            PROFILE_TITLE_TEXT,
            font,
            PROFILE_COLOR,
            center=(center_x, PROFILE_TITLE_CENTER_Y),
        )

        for index, text in enumerate(profile_lines):
            draw_text(
                surface,
                text,
                font,
                PROFILE_COLOR,
                center=(center_x, PROFILE_START_Y + index * PROFILE_LINE_GAP),
            )

        draw_text(
            surface,
            RETURN_TEXT,
            font,
            RETURN_COLOR,
            center=(center_x, RETURN_CENTER_Y),
        )
