from unittest.mock import Mock, call

import pygame

from my_first_adventure_game.engine.assets import FontCache
from my_first_adventure_game.engine.input import InputState
from my_first_adventure_game.game.input import GameAction
from my_first_adventure_game.game.scenes import victory_scene
from my_first_adventure_game.game.scenes.victory_scene import (
    BACKGROUND_COLOR,
    ENEMIES_DEFEATED_CENTER_Y,
    ITEMS_COLLECTED_CENTER_Y,
    OBSTACLES_DESTROYED_CENTER_Y,
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
    WALL_STAINS_CLEANED_CENTER_Y,
    VictoryScene,
)
from my_first_adventure_game.game.scoring import SessionScore
from my_first_adventure_game.game.statistics import SessionStatistics


def test_victory_scene_draws_background() -> None:
    surface = Mock()
    surface.get_width.return_value = 1280
    font_cache = Mock(spec=FontCache)
    session_score = Mock(spec=SessionScore)
    session_statistics = Mock(spec=SessionStatistics)
    input_state = Mock(spec=InputState)
    return_to_title = Mock()
    scene = VictoryScene(
        font_cache,
        session_score,
        session_statistics,
        input_state,
        return_to_title,
    )

    scene.draw(surface)

    surface.fill.assert_called_once_with(BACKGROUND_COLOR)


def test_victory_scene_draws_session_summary(monkeypatch) -> None:
    surface = Mock()
    surface.get_width.return_value = 1280
    font_cache = Mock(spec=FontCache)
    session_score = Mock(spec=SessionScore)
    session_statistics = Mock(spec=SessionStatistics)
    session_statistics.items_collected = 3
    session_statistics.obstacles_destroyed = 1
    session_statistics.enemies_defeated = 2
    session_statistics.wall_stains_cleaned = 4
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
        session_statistics,
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
            "Items collected: 3",
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
            "Enemies defeated: 2",
            font,
            SCORE_COLOR,
            center=(640, ENEMIES_DEFEATED_CENTER_Y),
        ),
        call(
            surface,
            "Wall stains cleaned: 4",
            font,
            SCORE_COLOR,
            center=(640, WALL_STAINS_CLEANED_CENTER_Y),
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
    session_statistics = Mock(spec=SessionStatistics)
    input_state = Mock(spec=InputState)
    input_state.is_pressed.return_value = True
    return_to_title = Mock()
    scene = VictoryScene(
        font_cache,
        session_score,
        session_statistics,
        input_state,
        return_to_title,
    )

    scene.update(0.016)

    input_state.is_pressed.assert_called_once_with(GameAction.CONFIRM)
    return_to_title.assert_called_once_with()


def test_victory_scene_does_not_return_without_confirmation() -> None:
    font_cache = Mock(spec=FontCache)
    session_score = Mock(spec=SessionScore)
    session_statistics = Mock(spec=SessionStatistics)
    input_state = Mock(spec=InputState)
    input_state.is_pressed.return_value = False
    return_to_title = Mock()
    scene = VictoryScene(
        font_cache,
        session_score,
        session_statistics,
        input_state,
        return_to_title,
    )

    scene.update(0.016)

    input_state.is_pressed.assert_called_once_with(GameAction.CONFIRM)
    return_to_title.assert_not_called()
