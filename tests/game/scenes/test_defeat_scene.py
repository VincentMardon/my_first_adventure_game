from unittest.mock import Mock, call

import pygame

from my_first_adventure_game.engine.assets import FontCache
from my_first_adventure_game.engine.input import InputState
from my_first_adventure_game.game.input import GameAction
from my_first_adventure_game.game.scenes import defeat_scene
from my_first_adventure_game.game.scenes.defeat_scene import (
    BACKGROUND_COLOR,
    DEFEAT_CENTER_Y,
    DEFEAT_COLOR,
    DEFEAT_FONT_PATH,
    DEFEAT_FONT_SIZE,
    DEFEAT_TEXT,
    ENEMIES_DEFEATED_CENTER_Y,
    ITEMS_COLLECTED_CENTER_Y,
    OBSTACLES_DESTROYED_CENTER_Y,
    RETURN_CENTER_Y,
    RETURN_COLOR,
    RETURN_TEXT,
    SCORE_CENTER_Y,
    SCORE_COLOR,
    DefeatScene,
)
from my_first_adventure_game.game.scoring import SessionScore
from my_first_adventure_game.game.statistics import SessionStatistics


def test_defeat_scene_draws_background() -> None:
    surface = Mock()
    surface.get_width.return_value = 1280
    font_cache = Mock(spec=FontCache)
    session_score = Mock(spec=SessionScore)
    session_statistics = Mock(spec=SessionStatistics)
    input_state = Mock(spec=InputState)
    return_to_title = Mock()
    scene = DefeatScene(
        font_cache,
        session_score,
        session_statistics,
        input_state,
        return_to_title,
    )

    scene.draw(surface)

    surface.fill.assert_called_once_with(BACKGROUND_COLOR)


def test_defeat_scene_draws_session_summary(monkeypatch) -> None:
    surface = Mock()
    surface.get_width.return_value = 1280
    font_cache = Mock(spec=FontCache)
    session_score = Mock(spec=SessionScore)
    session_statistics = Mock(spec=SessionStatistics)
    session_statistics.items_collected = 2
    session_statistics.obstacles_destroyed = 1
    session_statistics.enemies_defeated = 1
    session_score.value = 300
    input_state = Mock(spec=InputState)
    return_to_title = Mock()
    font = Mock(spec=pygame.font.Font)
    font_cache.load.return_value = font
    draw_text = Mock()

    monkeypatch.setattr(defeat_scene, "draw_text", draw_text)

    scene = DefeatScene(
        font_cache,
        session_score,
        session_statistics,
        input_state,
        return_to_title,
    )

    scene.draw(surface)

    font_cache.load.assert_called_once_with(
        DEFEAT_FONT_PATH,
        DEFEAT_FONT_SIZE,
    )
    assert draw_text.call_args_list == [
        call(
            surface,
            DEFEAT_TEXT,
            font,
            DEFEAT_COLOR,
            center=(640, DEFEAT_CENTER_Y),
        ),
        call(
            surface,
            "Score: 300",
            font,
            SCORE_COLOR,
            center=(640, SCORE_CENTER_Y),
        ),
        call(
            surface,
            "Items collected: 2",
            font,
            SCORE_COLOR,
            center=(640, ITEMS_COLLECTED_CENTER_Y),
        ),
        call(
            surface,
            "Obstacles destroyed: 1",
            font,
            SCORE_COLOR,
            center=(640, OBSTACLES_DESTROYED_CENTER_Y),
        ),
        call(
            surface,
            "Enemies defeated: 1",
            font,
            SCORE_COLOR,
            center=(640, ENEMIES_DEFEATED_CENTER_Y),
        ),
        call(
            surface,
            RETURN_TEXT,
            font,
            RETURN_COLOR,
            center=(640, RETURN_CENTER_Y),
        ),
    ]


def test_defeat_scene_returns_to_title_when_confirm_is_pressed() -> None:
    font_cache = Mock(spec=FontCache)
    session_score = Mock(spec=SessionScore)
    session_statistics = Mock(spec=SessionStatistics)
    input_state = Mock(spec=InputState)
    input_state.is_pressed.return_value = True
    return_to_title = Mock()
    scene = DefeatScene(
        font_cache,
        session_score,
        session_statistics,
        input_state,
        return_to_title,
    )

    scene.update(0.016)

    input_state.is_pressed.assert_called_once_with(GameAction.CONFIRM)
    return_to_title.assert_called_once_with()


def test_defeat_scene_does_not_return_without_confirmation() -> None:
    font_cache = Mock(spec=FontCache)
    session_score = Mock(spec=SessionScore)
    session_statistics = Mock(spec=SessionStatistics)
    input_state = Mock(spec=InputState)
    input_state.is_pressed.return_value = False
    return_to_title = Mock()
    scene = DefeatScene(
        font_cache,
        session_score,
        session_statistics,
        input_state,
        return_to_title,
    )

    scene.update(0.016)

    input_state.is_pressed.assert_called_once_with(GameAction.CONFIRM)
    return_to_title.assert_not_called()
