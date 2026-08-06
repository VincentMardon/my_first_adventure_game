from importlib import import_module

import pytest

PACKAGES = (
    "my_first_adventure_game.engine",
    "my_first_adventure_game.engine.application",
    "my_first_adventure_game.engine.assets",
    "my_first_adventure_game.engine.collisions",
    "my_first_adventure_game.engine.graphics",
    "my_first_adventure_game.engine.input",
    "my_first_adventure_game.engine.persistence",
    "my_first_adventure_game.engine.scenes",
    "my_first_adventure_game.engine.world",
    "my_first_adventure_game.game",
    "my_first_adventure_game.game.assets",
    "my_first_adventure_game.game.entities",
    "my_first_adventure_game.game.events",
    "my_first_adventure_game.game.input",
    "my_first_adventure_game.game.levels",
    "my_first_adventure_game.game.localization",
    "my_first_adventure_game.game.profile",
    "my_first_adventure_game.game.scenes",
    "my_first_adventure_game.game.scoring",
)


@pytest.mark.parametrize("package_name", PACKAGES)
def test_package_is_importable(package_name: str) -> None:
    imported_package = import_module(package_name)

    assert imported_package.__name__ == package_name
