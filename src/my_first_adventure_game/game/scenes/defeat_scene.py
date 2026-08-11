import pygame

from my_first_adventure_game.engine.assets import FontCache
from my_first_adventure_game.engine.graphics import draw_text
from my_first_adventure_game.engine.scenes import Scene
from my_first_adventure_game.game.scoring import SessionScore

BACKGROUND_COLOR = (24, 28, 36)
DEFEAT_TEXT = "Game Over"
DEFEAT_COLOR = (248, 112, 112)
DEFEAT_CENTER_Y = 240
DEFEAT_FONT_PATH = pygame.font.get_default_font()
DEFEAT_FONT_SIZE = 64
SCORE_COLOR = (240, 240, 240)
SCORE_CENTER_Y = 340


class DefeatScene(Scene):
    """Display the final score after the player is defeated."""

    def __init__(
        self,
        font_cache: FontCache,
        session_score: SessionScore,
    ) -> None:
        self._font_cache = font_cache
        self._session_score = session_score

    def handle_event(self, event: pygame.event.Event) -> None:
        return None

    def update(self, delta_time: float) -> None:
        return None

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
