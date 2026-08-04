from types import SimpleNamespace
from unittest.mock import Mock

import pygame
import pytest

from my_first_adventure_game.engine.application import Application, WindowConfig
from my_first_adventure_game.engine.scenes import SceneManager


def test_run_processes_one_frame_and_delegates_to_scene_manager(
    monkeypatch,
) -> None:
    surface = Mock()
    clock = Mock()
    clock.tick.return_value = 250

    gameplay_event = SimpleNamespace(type=pygame.KEYDOWN)
    quit_event = SimpleNamespace(type=pygame.QUIT)
    scene_manager = Mock(spec=SceneManager)

    set_mode = Mock(return_value=surface)
    set_caption = Mock()
    flip_display = Mock()

    monkeypatch.setattr(pygame, "init", Mock())
    monkeypatch.setattr(pygame, "quit", Mock())
    monkeypatch.setattr(pygame.display, "set_mode", set_mode)
    monkeypatch.setattr(pygame.display, "set_caption", set_caption)
    monkeypatch.setattr(pygame.display, "flip", flip_display)
    monkeypatch.setattr(pygame.time, "Clock", Mock(return_value=clock))
    monkeypatch.setattr(
        pygame.event,
        "get",
        Mock(return_value=[gameplay_event, quit_event]),
    )

    config = WindowConfig(
        title="Test Game",
        size=(800, 600),
    )
    application = Application(
        window_config=config,
        scene_manager=scene_manager,
        frames_per_second=60,
    )

    application.run()

    set_mode.assert_called_once_with((800, 600))
    set_caption.assert_called_once_with("Test Game")
    clock.tick.assert_called_once_with(60)
    scene_manager.handle_event.assert_called_once_with(gameplay_event)
    scene_manager.update.assert_called_once_with(0.25)
    scene_manager.draw.assert_called_once_with(surface)
    flip_display.assert_called_once_with()
    pygame.quit.assert_called_once_with()


def test_run_shuts_down_pygame_when_startup_fails(monkeypatch) -> None:
    quit_pygame = Mock()

    monkeypatch.setattr(pygame, "init", Mock())
    monkeypatch.setattr(
        pygame.display,
        "set_mode",
        Mock(side_effect=RuntimeError("Unable to create the window")),
    )
    monkeypatch.setattr(pygame, "quit", quit_pygame)

    application = Application(
        window_config=WindowConfig(
            title="Test Game",
            size=(800, 600),
        ),
        scene_manager=Mock(spec=SceneManager),
        frames_per_second=60,
    )

    with pytest.raises(RuntimeError, match="Unable to create the window"):
        application.run()

    quit_pygame.assert_called_once_with()
