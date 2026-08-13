from unittest.mock import Mock, call

import pygame

from my_first_adventure_game.engine.assets import FontCache
from my_first_adventure_game.engine.input import InputState
from my_first_adventure_game.game.input import GameAction
from my_first_adventure_game.game.scenes import dialogue_scene
from my_first_adventure_game.game.scenes.dialogue_scene import (
    BACKGROUND_COLOR,
    DIALOGUE_COLOR,
    DIALOGUE_FONT_PATH,
    DIALOGUE_FONT_SIZE,
    DIALOGUE_LINE_SPACING,
    INSTRUCTION_COLOR,
    INSTRUCTION_GAP,
    INSTRUCTION_TEXT,
    PANEL_BORDER_COLOR,
    PANEL_BORDER_RADIUS,
    PANEL_BORDER_WIDTH,
    PANEL_COLOR,
    PANEL_MARGIN_X,
    PANEL_PADDING_BOTTOM,
    PANEL_TEXT_PADDING,
    PANEL_TOP,
    SPEAKER_COLOR,
    SPEAKER_DIALOGUE_GAP,
    SPEAKER_TOP_OFFSET,
    DialogueScene,
)


def test_dialogue_scene_draws_background(monkeypatch) -> None:
    surface = Mock()
    surface.get_width.return_value = 1280
    font_cache = Mock(spec=FontCache)
    input_state = Mock(spec=InputState)
    close_dialogue = Mock()

    monkeypatch.setattr(pygame.draw, "rect", Mock())
    monkeypatch.setattr(
        dialogue_scene,
        "_wrap_text",
        Mock(return_value=("Welcome, traveler!",)),
    )

    scene = DialogueScene(
        font_cache,
        input_state,
        "Guide",
        ("Welcome, traveler!",),
        close_dialogue,
    )

    scene.draw(surface)

    surface.fill.assert_called_once_with(BACKGROUND_COLOR)


def test_dialogue_scene_draws_dialogue_and_instruction(monkeypatch) -> None:
    surface = Mock()
    surface.get_width.return_value = 1280
    font_cache = Mock(spec=FontCache)
    input_state = Mock(spec=InputState)
    close_dialogue = Mock()
    font = Mock(spec=pygame.font.Font)
    font_cache.load.return_value = font
    draw_text = Mock()

    monkeypatch.setattr(dialogue_scene, "draw_text", draw_text)
    monkeypatch.setattr(pygame.draw, "rect", Mock())
    monkeypatch.setattr(
        dialogue_scene,
        "_wrap_text",
        Mock(return_value=("Welcome, traveler!",)),
    )

    scene = DialogueScene(
        font_cache,
        input_state,
        "Guide",
        ("Welcome, traveler!",),
        close_dialogue,
    )

    scene.draw(surface)

    speaker_center_y = PANEL_TOP + SPEAKER_TOP_OFFSET
    dialogue_center_y = speaker_center_y + SPEAKER_DIALOGUE_GAP
    insctruction_center_y = dialogue_center_y + INSTRUCTION_GAP

    font_cache.load.assert_called_once_with(
        DIALOGUE_FONT_PATH,
        DIALOGUE_FONT_SIZE,
    )
    assert draw_text.call_args_list == [
        call(
            surface,
            "Guide",
            font,
            SPEAKER_COLOR,
            center=(640, speaker_center_y),
        ),
        call(
            surface,
            "Welcome, traveler!",
            font,
            DIALOGUE_COLOR,
            center=(640, dialogue_center_y),
        ),
        call(
            surface,
            INSTRUCTION_TEXT,
            font,
            INSTRUCTION_COLOR,
            center=(640, insctruction_center_y),
        ),
    ]


def test_dialogue_scene_closes_when_confirm_is_pressed() -> None:
    font_cache = Mock(spec=FontCache)
    input_state = Mock(spec=InputState)
    input_state.is_pressed.return_value = True
    close_dialogue = Mock()
    scene = DialogueScene(
        font_cache,
        input_state,
        "Guide",
        ("Welcome, traveler!",),
        close_dialogue,
    )

    scene.update(0.016)

    input_state.is_pressed.assert_called_once_with(GameAction.CONFIRM)
    close_dialogue.assert_called_once_with()


def test_dialogue_scene_remains_open_without_confirm_action() -> None:
    font_cache = Mock(spec=FontCache)
    input_state = Mock(spec=InputState)
    input_state.is_pressed.return_value = False
    close_dialogue = Mock()
    scene = DialogueScene(
        font_cache,
        input_state,
        "Guide",
        ("Welcome, traveler!",),
        close_dialogue,
    )

    scene.update(0.016)

    input_state.is_pressed.assert_called_once_with(GameAction.CONFIRM)
    close_dialogue.assert_not_called()


def test_dialogue_scene_advances_to_next_line_before_closing(
    monkeypatch,
) -> None:
    surface = Mock()
    surface.get_width.return_value = 1280
    font_cache = Mock(spec=FontCache)
    input_state = Mock(spec=InputState)
    input_state.is_pressed.return_value = True
    close_dialogue = Mock()
    font = Mock(spec=pygame.font.Font)
    font_cache.load.return_value = font
    draw_text = Mock()

    monkeypatch.setattr(dialogue_scene, "draw_text", draw_text)
    monkeypatch.setattr(pygame.draw, "rect", Mock())
    monkeypatch.setattr(
        dialogue_scene,
        "_wrap_text",
        Mock(return_value=("The road ahead is dangerous.",)),
    )

    scene = DialogueScene(
        font_cache,
        input_state,
        "Guide",
        (
            "Welcome, traveler!",
            "The road ahead is dangerous.",
        ),
        close_dialogue,
    )

    scene.update(0.016)
    scene.draw(surface)

    close_dialogue.assert_not_called()

    speaker_center_y = PANEL_TOP + SPEAKER_TOP_OFFSET
    dialogue_center_y = speaker_center_y + SPEAKER_DIALOGUE_GAP
    instruction_center_y = dialogue_center_y + INSTRUCTION_GAP

    assert draw_text.call_args_list == [
        call(
            surface,
            "Guide",
            font,
            SPEAKER_COLOR,
            center=(640, speaker_center_y),
        ),
        call(
            surface,
            "The road ahead is dangerous.",
            font,
            DIALOGUE_COLOR,
            center=(640, dialogue_center_y),
        ),
        call(
            surface,
            INSTRUCTION_TEXT,
            font,
            INSTRUCTION_COLOR,
            center=(640, instruction_center_y),
        ),
    ]


def test_dialogue_scene_closes_after_last_line() -> None:
    font_cache = Mock(spec=FontCache)
    input_state = Mock(spec=InputState)
    input_state.is_pressed.return_value = True
    close_dialogue = Mock()
    scene = DialogueScene(
        font_cache,
        input_state,
        "Guide",
        (
            "Welcome, traveler!",
            "The road ahead is dangerous.",
        ),
        close_dialogue,
    )

    scene.update(0.016)

    close_dialogue.assert_not_called()

    scene.update(0.016)

    assert input_state.is_pressed.call_count == 2
    close_dialogue.assert_called_once_with()


def test_dialogue_scene_draws_panel(monkeypatch) -> None:
    surface = Mock()
    surface.get_width.return_value = 1280
    font_cache = Mock(spec=FontCache)
    input_state = Mock(spec=InputState)
    close_dialogue = Mock()
    draw_rect = Mock()

    monkeypatch.setattr(pygame.draw, "rect", draw_rect)
    monkeypatch.setattr(
        dialogue_scene,
        "_wrap_text",
        Mock(return_value=("The road ahead", "is dangerous.")),
    )

    scene = DialogueScene(
        font_cache,
        input_state,
        "Guide",
        ("Welcome, traveler!",),
        close_dialogue,
    )

    scene.draw(surface)

    expected_panel_height = (
        SPEAKER_TOP_OFFSET
        + SPEAKER_DIALOGUE_GAP
        + DIALOGUE_LINE_SPACING
        + INSTRUCTION_GAP
        + PANEL_PADDING_BOTTOM
    )

    panel_rect = pygame.Rect(
        PANEL_MARGIN_X,
        PANEL_TOP,
        1280 - PANEL_MARGIN_X * 2,
        expected_panel_height,
    )
    assert draw_rect.call_args_list == [
        call(
            surface,
            PANEL_COLOR,
            panel_rect,
            border_radius=PANEL_BORDER_RADIUS,
        ),
        call(
            surface,
            PANEL_BORDER_COLOR,
            panel_rect,
            width=PANEL_BORDER_WIDTH,
            border_radius=PANEL_BORDER_RADIUS,
        ),
    ]


def test_wrap_text_splits_line_at_word_boundaries() -> None:
    font = Mock(spec=pygame.font.Font)
    font.size.side_effect = lambda text: (len(text) * 10, 40)

    wrapped_lines = dialogue_scene._wrap_text(
        "The road ahead is dangerous.",
        font,
        max_width=100,
    )

    assert wrapped_lines == ("The road", "ahead is", "dangerous.")


def test_wrap_text_keeps_line_that_fits() -> None:
    font = Mock(spec=pygame.font.Font)
    font.size.side_effect = lambda text: (len(text) * 10, 40)

    wrapped_lines = dialogue_scene._wrap_text(
        "Welcome!",
        font,
        max_width=100,
    )

    assert wrapped_lines == ("Welcome!",)


def test_dialogue_scene_wraps_and_centers_visual_lines(
    monkeypatch,
) -> None:
    surface = Mock()
    surface.get_width.return_value = 1280
    font_cache = Mock(spec=FontCache)
    input_state = Mock(spec=InputState)
    close_dialogue = Mock()
    font = Mock(spec=pygame.font.Font)
    font_cache.load.return_value = font
    draw_text = Mock()
    wrap_text = Mock(
        return_value=(
            "The road ahead",
            "is dangerous.",
        )
    )

    monkeypatch.setattr(pygame.draw, "rect", Mock())
    monkeypatch.setattr(dialogue_scene, "draw_text", draw_text)
    monkeypatch.setattr(dialogue_scene, "_wrap_text", wrap_text)

    scene = DialogueScene(
        font_cache,
        input_state,
        "Guide",
        ("The road ahead is dangerous.",),
        close_dialogue,
    )

    scene.draw(surface)

    wrap_text.assert_called_once_with(
        "The road ahead is dangerous.",
        font,
        max_width=(1280 - PANEL_MARGIN_X * 2 - PANEL_TEXT_PADDING * 2),
    )

    speaker_center_y = PANEL_TOP + SPEAKER_TOP_OFFSET
    first_dialogue_center_y = speaker_center_y + SPEAKER_DIALOGUE_GAP
    second_dialogue_center_y = first_dialogue_center_y + DIALOGUE_LINE_SPACING
    instruction_center_y = second_dialogue_center_y + INSTRUCTION_GAP

    assert draw_text.call_args_list == [
        call(
            surface,
            "Guide",
            font,
            SPEAKER_COLOR,
            center=(640, speaker_center_y),
        ),
        call(
            surface,
            "The road ahead",
            font,
            DIALOGUE_COLOR,
            center=(640, first_dialogue_center_y),
        ),
        call(
            surface,
            "is dangerous.",
            font,
            DIALOGUE_COLOR,
            center=(640, second_dialogue_center_y),
        ),
        call(
            surface,
            INSTRUCTION_TEXT,
            font,
            INSTRUCTION_COLOR,
            center=(640, instruction_center_y),
        ),
    ]
