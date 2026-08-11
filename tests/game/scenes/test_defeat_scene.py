from unittest.mock import Mock, call

import pygame

from my_first_adventure_game.engine.assets import FontCache
from my_first_adventure_game.game.scenes import defeat_scene
from my_first_adventure_game.game.scenes.defeat_scene import (
    BACKGROUND_COLOR,
    DEFEAT_CENTER_Y,
    DEFEAT_COLOR,
    DEFEAT_FONT_PATH,
    DEFEAT_FONT_SIZE,
    DEFEAT_TEXT,
    SCORE_CENTER_Y,
    SCORE_COLOR,
    DefeatScene,
)
from my_first_adventure_game.game.scoring import SessionScore


def test_defeat_scene_draws_background() -> None:
    surface = Mock()
    surface.get_width.return_value = 1280
    font_cache = Mock(spec=FontCache)
    session_score = Mock(spec=SessionScore)
    scene = DefeatScene(font_cache, session_score)

    scene.draw(surface)

    surface.fill.assert_called_once_with(BACKGROUND_COLOR)


def test_defeat_scene_draws_message_and_final_score(monkeypatch) -> None:
    surface = Mock()
    surface.get_width.return_value = 1280
    font_cache = Mock(spec=FontCache)
    session_score = Mock(spec=SessionScore)
    session_score.value = 300
    font = Mock(spec=pygame.font.Font)
    font_cache.load.return_value = font
    draw_text = Mock()

    monkeypatch.setattr(defeat_scene, "draw_text", draw_text)

    scene = DefeatScene(font_cache, session_score)

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
    ]
