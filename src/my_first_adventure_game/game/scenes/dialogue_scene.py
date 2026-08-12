from collections.abc import Callable

import pygame

from my_first_adventure_game.engine.assets import FontCache
from my_first_adventure_game.engine.graphics import draw_text
from my_first_adventure_game.engine.input import InputState
from my_first_adventure_game.engine.scenes import Scene
from my_first_adventure_game.game.input import GameAction

BACKGROUND_COLOR = (24, 28, 36)
DIALOGUE_CENTER_Y = 280
DIALOGUE_COLOR = (240, 240, 240)
DIALOGUE_FONT_PATH = pygame.font.get_default_font()
DIALOGUE_FONT_SIZE = 40
INSTRUCTION_CENTER_Y = 380
INSTRUCTION_COLOR = (184, 192, 208)
INSTRUCTION_TEXT = "Press Enter to continue"


class DialogueScene(Scene):
    """Display one dialogue line until the player confirms."""

    def __init__(
        self,
        font_cache: FontCache,
        input_state: InputState[GameAction],
        dialogue_text: str,
        close_dialogue: Callable[[], None],
    ) -> None:
        self._font_cache = font_cache
        self._input_state = input_state
        self._dialogue_text = dialogue_text
        self._close_dialogue = close_dialogue

    def handle_event(self, event: pygame.event.Event) -> None:
        return None

    def update(self, delta_time: float) -> None:
        if self._input_state.is_pressed(GameAction.CONFIRM):
            self._close_dialogue()

    def draw(self, surface: pygame.Surface) -> None:
        surface.fill(BACKGROUND_COLOR)
        font = self._font_cache.load(
            DIALOGUE_FONT_PATH,
            DIALOGUE_FONT_SIZE,
        )
        center_x = surface.get_width() // 2

        draw_text(
            surface,
            self._dialogue_text,
            font,
            DIALOGUE_COLOR,
            center=(center_x, DIALOGUE_CENTER_Y),
        )
        draw_text(
            surface,
            INSTRUCTION_TEXT,
            font,
            INSTRUCTION_COLOR,
            center=(center_x, INSTRUCTION_CENTER_Y),
        )
