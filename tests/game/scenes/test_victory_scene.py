from unittest.mock import Mock, call

import pygame

from my_first_adventure_game.engine.assets import FontCache
from my_first_adventure_game.engine.input import InputState
from my_first_adventure_game.game.input import GameAction
from my_first_adventure_game.game.scenes import victory_scene
from my_first_adventure_game.game.scenes.victory_scene import (
    BACKGROUND_COLOR,
    RETURN_CENTER_Y,
    RETURN_COLOR,
    RETURN_TEXT,
    SCORE_CENTER_Y,
    SCORE_COLOR,
    VICTORY_CENTER_Y,
    VICTORY_COLOR,
    VICTORY_FONT_PATH,
    VICTORY_FONT_SIZE,
    VICTORY_TEXT,
    VictoryScene,
)
from my_first_adventure_game.game.scoring import SessionScore


def test_victory_scene_draws_background() -> None:
    surface = Mock()
    surface.get_width.return_value = 1280
    font_cache = Mock(spec=FontCache)
    session_score = Mock(spec=SessionScore)
    input_state = Mock(spec=InputState)
    return_to_title = Mock()
    scene = VictoryScene(
        font_cache,
        session_score,
        input_state,
        return_to_title,
    )

    scene.draw(surface)

    surface.fill.assert_called_once_with(BACKGROUND_COLOR)


def test_victory_scene_draws_message_final_score_and_instruction(
    monkeypatch,
) -> None:
    surface = Mock()
    surface.get_width.return_value = 1280
    font_cache = Mock(spec=FontCache)
    session_score = Mock(spec=SessionScore)
    session_score.value = 500
    input_state = Mock(spec=InputState)
    return_to_title = Mock()
    font = Mock(spec=pygame.font.Font)
    font_cache.load.return_value = font
    draw_text = Mock()

    monkeypatch.setattr(victory_scene, "draw_text", draw_text)

    scene = VictoryScene(
        font_cache,
        session_score,
        input_state,
        return_to_title,
    )

    scene.draw(surface)

    font_cache.load.assert_called_once_with(
        VICTORY_FONT_PATH,
        VICTORY_FONT_SIZE,
    )
    assert draw_text.call_args_list == [
        call(
            surface,
            VICTORY_TEXT,
            font,
            VICTORY_COLOR,
            center=(640, VICTORY_CENTER_Y),
        ),
        call(
            surface,
            "Score: 500",
            font,
            SCORE_COLOR,
            center=(640, SCORE_CENTER_Y),
        ),
        call(
            surface,
            RETURN_TEXT,
            font,
            RETURN_COLOR,
            center=(640, RETURN_CENTER_Y),
        ),
    ]


def test_victory_scene_returns_to_title_when_confirm_is_pressed() -> None:
    font_cache = Mock(spec=FontCache)
    session_score = Mock(spec=SessionScore)
    input_state = Mock(spec=InputState)
    input_state.is_pressed.return_value = True
    return_to_title = Mock()
    scene = VictoryScene(
        font_cache,
        session_score,
        input_state,
        return_to_title,
    )

    scene.update(0.016)

    input_state.is_pressed.assert_called_once_with(GameAction.CONFIRM)
    return_to_title.assert_called_once_with()


def test_victory_scene_does_not_return_without_confirmation() -> None:
    font_cache = Mock(spec=FontCache)
    session_score = Mock(spec=SessionScore)
    input_state = Mock(spec=InputState)
    input_state.is_pressed.return_value = False
    return_to_title = Mock()
    scene = VictoryScene(
        font_cache,
        session_score,
        input_state,
        return_to_title,
    )

    scene.update(0.016)

    input_state.is_pressed.assert_called_once_with(GameAction.CONFIRM)
    return_to_title.assert_not_called()
