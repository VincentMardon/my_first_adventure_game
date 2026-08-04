from my_first_adventure_game.engine.application import WindowConfig


def test_window_config_stores_window_properties() -> None:
    config = WindowConfig(title="Test Game", size=(1280, 720))

    assert config.title == "Test Game"
    assert config.size == (1280, 720)
