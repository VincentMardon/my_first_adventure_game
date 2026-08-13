from collections.abc import Callable

import pygame

from my_first_adventure_game.engine.assets import FontCache
from my_first_adventure_game.engine.graphics import draw_text
from my_first_adventure_game.engine.input import InputState
from my_first_adventure_game.engine.scenes import Scene
from my_first_adventure_game.game.input import GameAction

BACKGROUND_COLOR = (24, 28, 36)
DIALOGUE_COLOR = (240, 240, 240)
DIALOGUE_FONT_PATH = pygame.font.get_default_font()
DIALOGUE_FONT_SIZE = 40
DIALOGUE_LINE_SPACING = 48
INSTRUCTION_COLOR = (184, 192, 208)
INSTRUCTION_GAP = 100
INSTRUCTION_TEXT = "Press Enter to continue"
PANEL_BORDER_COLOR = (112, 128, 152)
PANEL_BORDER_RADIUS = 12
PANEL_BORDER_WIDTH = 3
PANEL_COLOR = (36, 44, 56)
PANEL_MARGIN_X = 120
PANEL_PADDING_BOTTOM = 60
PANEL_TEXT_PADDING = 48
PANEL_TOP = 140
SPEAKER_COLOR = (112, 200, 240)
SPEAKER_DIALOGUE_GAP = 80
SPEAKER_TOP_OFFSET = 60


class DialogueScene(Scene):
    """Display ordered dialogue lines until the player confirms the last one."""

    def __init__(
        self,
        font_cache: FontCache,
        input_state: InputState[GameAction],
        speaker_name: str,
        dialogue_lines: tuple[str, ...],
        close_dialogue: Callable[[], None],
    ) -> None:
        self._font_cache = font_cache
        self._input_state = input_state
        self._speaker_name = speaker_name
        self._dialogue_lines = dialogue_lines
        self._close_dialogue = close_dialogue
        self._current_line_index = 0

    def handle_event(self, event: pygame.event.Event) -> None:
        return None

    def update(self, delta_time: float) -> None:
        if not self._input_state.is_pressed(GameAction.CONFIRM):
            return

        if self._current_line_index < len(self._dialogue_lines) - 1:
            self._current_line_index += 1
            return

        self._close_dialogue()

    def draw(self, surface: pygame.Surface) -> None:
        surface.fill(BACKGROUND_COLOR)
        font = self._font_cache.load(
            DIALOGUE_FONT_PATH,
            DIALOGUE_FONT_SIZE,
        )
        wrapped_lines = _wrap_text(
            self._dialogue_lines[self._current_line_index],
            font,
            max_width=(
                surface.get_width() - PANEL_MARGIN_X * 2 - PANEL_TEXT_PADDING * 2
            ),
        )
        speaker_center_y = PANEL_TOP + SPEAKER_TOP_OFFSET
        first_dialogue_center_y = speaker_center_y + SPEAKER_DIALOGUE_GAP
        last_dialogue_center_y = (
            first_dialogue_center_y + (len(wrapped_lines) - 1) * DIALOGUE_LINE_SPACING
        )
        instruction_center_y = last_dialogue_center_y + INSTRUCTION_GAP
        panel_height = instruction_center_y - PANEL_TOP + PANEL_PADDING_BOTTOM
        panel_rect = pygame.Rect(
            PANEL_MARGIN_X,
            PANEL_TOP,
            surface.get_width() - PANEL_MARGIN_X * 2,
            panel_height,
        )
        pygame.draw.rect(
            surface,
            PANEL_COLOR,
            panel_rect,
            border_radius=PANEL_BORDER_RADIUS,
        )
        pygame.draw.rect(
            surface,
            PANEL_BORDER_COLOR,
            panel_rect,
            width=PANEL_BORDER_WIDTH,
            border_radius=PANEL_BORDER_RADIUS,
        )
        center_x = surface.get_width() // 2

        draw_text(
            surface,
            self._speaker_name,
            font,
            SPEAKER_COLOR,
            center=(center_x, speaker_center_y),
        )

        for line_index, line in enumerate(wrapped_lines):
            draw_text(
                surface,
                line,
                font,
                DIALOGUE_COLOR,
                center=(
                    center_x,
                    first_dialogue_center_y + line_index * DIALOGUE_LINE_SPACING,
                ),
            )

        draw_text(
            surface,
            INSTRUCTION_TEXT,
            font,
            INSTRUCTION_COLOR,
            center=(center_x, instruction_center_y),
        )


def _wrap_text(
    text: str,
    font: pygame.font.Font,
    *,
    max_width: int,
) -> tuple[str, ...]:
    words = text.split()
    wrapped_lines: list[str] = []
    current_line = words[0]

    for word in words[1:]:
        candidate_line = f"{current_line} {word}"

        if font.size(candidate_line)[0] <= max_width:
            current_line = candidate_line
            continue

        wrapped_lines.append(current_line)
        current_line = word

    wrapped_lines.append(current_line)
    return tuple(wrapped_lines)
