from unittest.mock import Mock, call

import pygame

from my_first_adventure_game.engine.assets import FontCache
from my_first_adventure_game.engine.input import InputState
from my_first_adventure_game.game.input import GameAction
from my_first_adventure_game.game.scenes import title_scene
from my_first_adventure_game.game.scenes.title_scene import (
    BACKGROUND_COLOR,
    INSTRUCTION_COLOR,
    INSTRUCTION_FONT_PATH,
    INSTRUCTION_FONT_SIZE,
    PROFILE_CENTER_Y,
    PROFILE_TEXT,
    START_CENTER_Y,
    START_TEXT,
    TITLE_CENTER_Y,
    TITLE_COLOR,
    TITLE_FONT_PATH,
    TITLE_FONT_SIZE,
    TITLE_TEXT,
    TitleScene,
)


def test_title_scene_draws_background() -> None:
    surface = Mock()
    surface.get_width.return_value = 1280
    font_cache = Mock(spec=FontCache)
    input_state = Mock(spec=InputState)
    start_game = Mock()
    show_profile = Mock()
    scene = TitleScene(
        font_cache,
        input_state,
        start_game,
        show_profile,
    )

    scene.draw(surface)

    surface.fill.assert_called_once_with(BACKGROUND_COLOR)


def test_title_scene_draws_title_and_navigation_instructions(
    monkeypatch,
) -> None:
    surface = Mock()
    surface.get_width.return_value = 1280
    font_cache = Mock(spec=FontCache)
    input_state = Mock(spec=InputState)
    start_game = Mock()
    show_profile = Mock()
    title_font = Mock(spec=pygame.font.Font)
    instruction_font = Mock(spec=pygame.font.Font)
    font_cache.load.side_effect = (
        title_font,
        instruction_font,
    )
    draw_text = Mock()

    monkeypatch.setattr(title_scene, "draw_text", draw_text)

    scene = TitleScene(
        font_cache,
        input_state,
        start_game,
        show_profile,
    )

    scene.draw(surface)

    assert font_cache.load.call_args_list == [
        call(TITLE_FONT_PATH, TITLE_FONT_SIZE),
        call(INSTRUCTION_FONT_PATH, INSTRUCTION_FONT_SIZE),
    ]
    assert draw_text.call_args_list == [
        call(
            surface,
            TITLE_TEXT,
            title_font,
            TITLE_COLOR,
            center=(640, TITLE_CENTER_Y),
        ),
        call(
            surface,
            START_TEXT,
            instruction_font,
            INSTRUCTION_COLOR,
            center=(640, START_CENTER_Y),
        ),
        call(
            surface,
            PROFILE_TEXT,
            instruction_font,
            INSTRUCTION_COLOR,
            center=(640, PROFILE_CENTER_Y),
        ),
    ]


def test_title_scene_starts_game_when_confirm_is_pressed() -> None:
    font_cache = Mock(spec=FontCache)
    input_state = Mock(spec=InputState)
    input_state.is_pressed.return_value = True
    start_game = Mock()
    show_profile = Mock()
    scene = TitleScene(
        font_cache,
        input_state,
        start_game,
        show_profile,
    )

    scene.update(0.016)

    input_state.is_pressed.assert_called_once_with(GameAction.CONFIRM)
    start_game.assert_called_once_with()
    show_profile.assert_not_called()


def test_title_scene_does_not_start_game_without_confirmation() -> None:
    font_cache = Mock(spec=FontCache)
    input_state = Mock(spec=InputState)
    input_state.is_pressed.return_value = False
    start_game = Mock()
    show_profile = Mock()
    scene = TitleScene(
        font_cache,
        input_state,
        start_game,
        show_profile,
    )

    scene.update(0.016)

    assert input_state.is_pressed.call_args_list == [
        call(GameAction.CONFIRM),
        call(GameAction.SHOW_PROFILE),
    ]
    start_game.assert_not_called()
    show_profile.assert_not_called()


def test_title_scene_requests_profile_when_profile_action_is_pressed() -> None:
    font_cache = Mock(spec=FontCache)
    input_state = Mock(spec=InputState)
    input_state.is_pressed.side_effect = lambda action: (
        action is GameAction.SHOW_PROFILE
    )
    start_game = Mock()
    show_profile = Mock()
    scene = TitleScene(
        font_cache,
        input_state,
        start_game,
        show_profile,
    )

    scene.update(0.016)

    assert input_state.is_pressed.call_args_list == [
        call(GameAction.CONFIRM),
        call(GameAction.SHOW_PROFILE),
    ]
    start_game.assert_not_called()
    show_profile.assert_called_once_with()
