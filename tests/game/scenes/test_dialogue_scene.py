from unittest.mock import Mock, call

import pygame

from my_first_adventure_game.engine.assets import FontCache
from my_first_adventure_game.engine.input import InputState
from my_first_adventure_game.game.input import GameAction
from my_first_adventure_game.game.scenes import dialogue_scene
from my_first_adventure_game.game.scenes.dialogue_scene import (
    BACKGROUND_COLOR,
    DIALOGUE_CENTER_Y,
    DIALOGUE_COLOR,
    DIALOGUE_FONT_PATH,
    DIALOGUE_FONT_SIZE,
    INSTRUCTION_CENTER_Y,
    INSTRUCTION_COLOR,
    INSTRUCTION_TEXT,
    SPEAKER_CENTER_Y,
    SPEAKER_COLOR,
    DialogueScene,
)


def test_dialogue_scene_draws_background() -> None:
    surface = Mock()
    surface.get_width.return_value = 1280
    font_cache = Mock(spec=FontCache)
    input_state = Mock(spec=InputState)
    close_dialogue = Mock()
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

    scene = DialogueScene(
        font_cache,
        input_state,
        "Guide",
        ("Welcome, traveler!",),
        close_dialogue,
    )

    scene.draw(surface)

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
            center=(640, SPEAKER_CENTER_Y),
        ),
        call(
            surface,
            "Welcome, traveler!",
            font,
            DIALOGUE_COLOR,
            center=(640, DIALOGUE_CENTER_Y),
        ),
        call(
            surface,
            INSTRUCTION_TEXT,
            font,
            INSTRUCTION_COLOR,
            center=(640, INSTRUCTION_CENTER_Y),
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
    assert draw_text.call_args_list == [
        call(
            surface,
            "Guide",
            font,
            SPEAKER_COLOR,
            center=(640, SPEAKER_CENTER_Y),
        ),
        call(
            surface,
            "The road ahead is dangerous.",
            font,
            DIALOGUE_COLOR,
            center=(640, DIALOGUE_CENTER_Y),
        ),
        call(
            surface,
            INSTRUCTION_TEXT,
            font,
            INSTRUCTION_COLOR,
            center=(640, INSTRUCTION_CENTER_Y),
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
