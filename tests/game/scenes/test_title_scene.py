from unittest.mock import Mock

import pygame

from my_first_adventure_game.engine.assets import FontCache
from my_first_adventure_game.engine.input import InputState
from my_first_adventure_game.game.input import GameAction
from my_first_adventure_game.game.scenes import title_scene
from my_first_adventure_game.game.scenes.title_scene import (
    BACKGROUND_COLOR,
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
    scene = TitleScene(font_cache, input_state, start_game)

    scene.draw(surface)

    surface.fill.assert_called_once_with(BACKGROUND_COLOR)


def test_title_scene_draws_centered_title(monkeypatch) -> None:
    surface = Mock()
    surface.get_width.return_value = 1280
    font_cache = Mock(spec=FontCache)
    input_state = Mock(spec=InputState)
    start_game = Mock()
    title_font = Mock(spec=pygame.font.Font)
    font_cache.load.return_value = title_font
    draw_text = Mock()

    monkeypatch.setattr(title_scene, "draw_text", draw_text)

    scene = TitleScene(font_cache, input_state, start_game)

    scene.draw(surface)

    font_cache.load.assert_called_once_with(
        TITLE_FONT_PATH,
        TITLE_FONT_SIZE,
    )
    draw_text.assert_called_once_with(
        surface,
        TITLE_TEXT,
        title_font,
        TITLE_COLOR,
        center=(640, TITLE_CENTER_Y),
    )


def test_title_scene_starts_game_when_confirm_is_pressed() -> None:
    font_cache = Mock(spec=FontCache)
    input_state = Mock(spec=InputState)
    input_state.is_pressed.return_value = True
    start_game = Mock()
    scene = TitleScene(font_cache, input_state, start_game)

    scene.update(0.016)

    input_state.is_pressed.assert_called_once_with(GameAction.CONFIRM)
    start_game.assert_called_once_with()


def test_title_scene_does_not_start_game_without_confirmation() -> None:
    font_cache = Mock(spec=FontCache)
    input_state = Mock(spec=InputState)
    input_state.is_pressed.return_value = False
    start_game = Mock()
    scene = TitleScene(font_cache, input_state, start_game)

    scene.update(0.016)

    input_state.is_pressed.assert_called_once_with(GameAction.CONFIRM)
    start_game.assert_not_called()
