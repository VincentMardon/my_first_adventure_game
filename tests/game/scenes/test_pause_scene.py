from unittest.mock import Mock, call

import pygame

from my_first_adventure_game.engine.assets import FontCache
from my_first_adventure_game.engine.input import InputState
from my_first_adventure_game.game.input import GameAction
from my_first_adventure_game.game.scenes import pause_scene
from my_first_adventure_game.game.scenes.pause_scene import (
    BACKGROUND_COLOR,
    PAUSE_CENTER_Y,
    PAUSE_COLOR,
    PAUSE_FONT_PATH,
    PAUSE_FONT_SIZE,
    PAUSE_TEXT,
    RESUME_CENTER_Y,
    RESUME_COLOR,
    RESUME_TEXT,
    PauseScene,
)


def test_pause_scene_draws_background() -> None:
    surface = Mock()
    surface.get_width.return_value = 1280
    font_cache = Mock(spec=FontCache)
    input_state = Mock(spec=InputState)
    resume_game = Mock()
    scene = PauseScene(font_cache, input_state, resume_game)

    scene.draw(surface)

    surface.fill.assert_called_once_with(BACKGROUND_COLOR)


def test_pause_scene_draws_message_and_resume_instruction(monkeypatch) -> None:
    surface = Mock()
    surface.get_width.return_value = 1280
    font_cache = Mock(spec=FontCache)
    input_state = Mock(spec=InputState)
    resume_game = Mock()
    font = Mock(spec=pygame.font.Font)
    font_cache.load.return_value = font
    draw_text = Mock()

    monkeypatch.setattr(pause_scene, "draw_text", draw_text)

    scene = PauseScene(font_cache, input_state, resume_game)

    scene.draw(surface)

    font_cache.load.assert_called_once_with(
        PAUSE_FONT_PATH,
        PAUSE_FONT_SIZE,
    )
    assert draw_text.call_args_list == [
        call(
            surface,
            PAUSE_TEXT,
            font,
            PAUSE_COLOR,
            center=(640, PAUSE_CENTER_Y),
        ),
        call(
            surface,
            RESUME_TEXT,
            font,
            RESUME_COLOR,
            center=(640, RESUME_CENTER_Y),
        ),
    ]


def test_pause_scene_resumes_when_pause_is_pressed() -> None:
    font_cache = Mock(spec=FontCache)
    input_state = Mock(spec=InputState)
    input_state.is_pressed.return_value = True
    resume_game = Mock()
    scene = PauseScene(font_cache, input_state, resume_game)

    scene.update(0.016)

    input_state.is_pressed.assert_called_once_with(GameAction.PAUSE)
    resume_game.assert_called_once_with()


def test_pause_scene_does_not_resume_without_pause_action() -> None:
    font_cache = Mock(spec=FontCache)
    input_state = Mock(spec=InputState)
    input_state.is_pressed.return_value = False
    resume_game = Mock()
    scene = PauseScene(font_cache, input_state, resume_game)

    scene.update(0.016)

    input_state.is_pressed.assert_called_once_with(GameAction.PAUSE)
    resume_game.assert_not_called()
