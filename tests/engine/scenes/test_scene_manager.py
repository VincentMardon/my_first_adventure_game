from unittest.mock import Mock

from my_first_adventure_game.engine.scenes import Scene, SceneManager


def test_scene_manager_starts_with_initial_scene() -> None:
    initial_scene = Mock(spec=Scene)

    manager = SceneManager(initial_scene)

    assert manager.current_scene is initial_scene


def test_change_scene_replaces_current_scene() -> None:
    initial_scene = Mock(spec=Scene)
    next_scene = Mock(spec=Scene)
    manager = SceneManager(initial_scene)

    manager.change_scene(next_scene)

    assert manager.current_scene is next_scene


def test_scene_manager_delegates_to_current_scene() -> None:
    scene = Mock(spec=Scene)
    event = Mock()
    surface = Mock()
    manager = SceneManager(scene)

    manager.handle_event(event)
    manager.update(0.25)
    manager.draw(surface)

    scene.handle_event.assert_called_once_with(event)
    scene.update.assert_called_once_with(0.25)
    scene.draw.assert_called_once_with(surface)
