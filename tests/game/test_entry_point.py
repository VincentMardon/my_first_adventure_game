from unittest.mock import Mock

from my_first_adventure_game.game import main as game_main


def test_main_builds_and_runs_application(monkeypatch) -> None:
    initial_scene = Mock()
    scene_manager = Mock()
    application = Mock()

    create_title_scene = Mock(return_value=initial_scene)
    create_scene_manager = Mock(return_value=scene_manager)
    create_application = Mock(return_value=application)

    monkeypatch.setattr(game_main, "TitleScene", create_title_scene)
    monkeypatch.setattr(game_main, "SceneManager", create_scene_manager)
    monkeypatch.setattr(game_main, "Application", create_application)

    game_main.main()

    create_title_scene.assert_called_once_with()
    create_scene_manager.assert_called_once_with(initial_scene)
    create_application.assert_called_once_with(
        window_config=game_main.WINDOW_CONFIG,
        scene_manager=scene_manager,
        frames_per_second=game_main.FRAMES_PER_SECOND,
    )
    application.run.assert_called_once_with()
