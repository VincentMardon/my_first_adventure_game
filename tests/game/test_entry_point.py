from types import SimpleNamespace
from unittest.mock import Mock

import pygame
import pytest

from my_first_adventure_game.game import main as game_main


def test_main_runs_one_frame_and_shuts_down(monkeypatch) -> None:
    screen = Mock()
    clock = Mock()
    quit_event = SimpleNamespace(type=pygame.QUIT)

    initialize_pygame = Mock()
    quit_pygame = Mock()
    set_mode = Mock(return_value=screen)
    set_caption = Mock()
    get_events = Mock(return_value=[quit_event])
    flip_display = Mock()
    create_clock = Mock(return_value=clock)

    monkeypatch.setattr(pygame, "init", initialize_pygame)
    monkeypatch.setattr(pygame, "quit", quit_pygame)
    monkeypatch.setattr(pygame.display, "set_mode", set_mode)
    monkeypatch.setattr(pygame.display, "set_caption", set_caption)
    monkeypatch.setattr(pygame.event, "get", get_events)
    monkeypatch.setattr(pygame.display, "flip", flip_display)
    monkeypatch.setattr(pygame.time, "Clock", create_clock)

    game_main.main()

    initialize_pygame.assert_called_once_with()
    set_mode.assert_called_once_with(game_main.WINDOW_CONFIG.size)
    set_caption.assert_called_once_with(game_main.WINDOW_CONFIG.title)
    screen.fill.assert_called_once_with(game_main.BACKGROUND_COLOR)
    flip_display.assert_called_once_with()
    clock.tick.assert_called_once_with(game_main.FRAMES_PER_SECOND)
    quit_pygame.assert_called_once_with()


def test_main_shuts_down_pygame_when_startup_fails(monkeypatch) -> None:
    quit_pygame = Mock()

    monkeypatch.setattr(pygame, "init", Mock())
    monkeypatch.setattr(
        pygame.display,
        "set_mode",
        Mock(side_effect=RuntimeError("Unable to create the window")),
    )
    monkeypatch.setattr(pygame, "quit", quit_pygame)

    with pytest.raises(RuntimeError, match="Unable to create the window"):
        game_main.main()

    quit_pygame.assert_called_once_with()
