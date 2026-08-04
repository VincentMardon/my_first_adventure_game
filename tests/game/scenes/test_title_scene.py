from unittest.mock import Mock

from my_first_adventure_game.game.scenes.title_scene import (
    BACKGROUND_COLOR,
    TitleScene,
)


def test_title_scene_draws_background() -> None:
    surface = Mock()
    scene = TitleScene()

    scene.draw(surface)

    surface.fill.assert_called_once_with(BACKGROUND_COLOR)
