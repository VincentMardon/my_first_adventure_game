from unittest.mock import Mock, call

import pygame

from my_first_adventure_game.engine.assets import FontCache
from my_first_adventure_game.engine.input import InputState
from my_first_adventure_game.game.input import GameAction
from my_first_adventure_game.game.profile import PlayerProfile
from my_first_adventure_game.game.scenes import ProfileScene, profile_scene
from my_first_adventure_game.game.scenes.profile_scene import (
    BACKGROUND_COLOR,
    PROFILE_COLOR,
    PROFILE_FONT_PATH,
    PROFILE_FONT_SIZE,
    PROFILE_LINE_GAP,
    PROFILE_START_Y,
    PROFILE_TITLE_CENTER_Y,
    PROFILE_TITLE_TEXT,
    RETURN_CENTER_Y,
    RETURN_COLOR,
    RETURN_TEXT,
)


def test_profile_scene_returns_to_title_when_confirm_is_pressed() -> None:
    font_cache = Mock(spec=FontCache)
    player_profile = Mock(spec=PlayerProfile)
    input_state = Mock(spec=InputState)
    input_state.is_pressed.return_value = True
    return_to_title = Mock()
    scene = ProfileScene(
        font_cache,
        player_profile,
        input_state,
        return_to_title,
    )

    scene.update(0.016)

    input_state.is_pressed.assert_called_once_with(GameAction.CONFIRM)
    return_to_title.assert_called_once_with()


def test_profile_scene_does_not_return_without_confirmation() -> None:
    font_cache = Mock(spec=FontCache)
    player_profile = Mock(spec=PlayerProfile)
    input_state = Mock(spec=InputState)
    input_state.is_pressed.return_value = False
    return_to_title = Mock()
    scene = ProfileScene(
        font_cache,
        player_profile,
        input_state,
        return_to_title,
    )

    scene.update(0.016)

    input_state.is_pressed.assert_called_once_with(GameAction.CONFIRM)
    return_to_title.assert_not_called()


def test_profile_scene_draws_background() -> None:
    surface = Mock()
    surface.get_width.return_value = 1280
    font_cache = Mock(spec=FontCache)
    player_profile = PlayerProfile()
    input_state = Mock(spec=InputState)
    return_to_title = Mock()
    scene = ProfileScene(
        font_cache,
        player_profile,
        input_state,
        return_to_title,
    )

    scene.draw(surface)

    surface.fill.assert_called_once_with(BACKGROUND_COLOR)


def test_profile_scene_draws_persisted_statistics(monkeypatch) -> None:
    surface = Mock()
    surface.get_width.return_value = 1280
    font_cache = Mock(spec=FontCache)
    player_profile = PlayerProfile(
        games_started=7,
        games_finished=6,
        victories=2,
        best_score=900,
        total_score=2400,
        items_collected=12,
        obstacles_destroyed=4,
        enemies_defeated=5,
    )
    input_state = Mock(spec=InputState)
    return_to_title = Mock()
    font = Mock(spec=pygame.font.Font)
    font_cache.load.return_value = font
    draw_text = Mock()

    monkeypatch.setattr(profile_scene, "draw_text", draw_text)

    scene = ProfileScene(
        font_cache,
        player_profile,
        input_state,
        return_to_title,
    )

    scene.draw(surface)

    font_cache.load.assert_called_once_with(
        PROFILE_FONT_PATH,
        PROFILE_FONT_SIZE,
    )

    expected_lines = (
        "Games started: 7",
        "Games finished: 6",
        "Victories: 2",
        "Best score: 900",
        "Total score: 2400",
        "Items collected: 12",
        "Obstacles destroyed: 4",
        "Enemies defeated: 5",
    )

    assert draw_text.call_args_list == [
        call(
            surface,
            PROFILE_TITLE_TEXT,
            font,
            PROFILE_COLOR,
            center=(640, PROFILE_TITLE_CENTER_Y),
        ),
        *[
            call(
                surface,
                text,
                font,
                PROFILE_COLOR,
                center=(640, PROFILE_START_Y + index * PROFILE_LINE_GAP),
            )
            for index, text in enumerate(expected_lines)
        ],
        call(
            surface,
            RETURN_TEXT,
            font,
            RETURN_COLOR,
            center=(640, RETURN_CENTER_Y),
        ),
    ]
